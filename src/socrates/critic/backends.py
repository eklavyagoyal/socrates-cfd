"""LLM backends for the critic.

The critic LLM has no tools: it receives a JSON evidence package and returns
a JSON decision constrained by a schema.  It cannot run commands, read files
or edit cases.  Calls are bounded (timeout) and retried a bounded number of
times with exponential backoff + jitter; every attempt is recorded.
"""

from __future__ import annotations

import json
import os
import random
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field


class LLMUnavailable(RuntimeError):
    pass


@dataclass
class LLMCall:
    ok: bool
    output: dict | None
    raw: str
    latency_s: float
    cost_usd: float | None
    attempts: int
    errors: list[str] = field(default_factory=list)


class ClaudeCLIBackend:
    """Headless Claude Code CLI (`claude -p`) with all tools disabled.

    ``model`` None uses the CLI's configured default model.  Isolation:
    no tools, no MCP servers, no settings files, no session persistence,
    an empty working directory and a replacement system prompt.
    """

    name = "claude-cli"

    def __init__(self, model: str | None = None, timeout_s: float = 300.0, max_attempts: int = 3):
        if shutil.which("claude") is None:
            raise LLMUnavailable("claude CLI not found on PATH")
        self.model = model
        self.timeout_s = timeout_s
        self.max_attempts = max_attempts
        self._cwd = tempfile.mkdtemp(prefix="socrates_critic_")

    def describe(self) -> dict:
        # model identifiers are deliberately not recorded in repository artifacts
        return {"backend": self.name, "model": "cli-default" if self.model is None else "configured",
                "timeout_s": self.timeout_s, "max_attempts": self.max_attempts}

    def complete(self, system_prompt: str, user_prompt: str, schema: dict) -> LLMCall:
        cmd = [
            "claude", "-p", "--output-format", "json", "--tools", "", "--no-session-persistence",
            "--strict-mcp-config", "--setting-sources", "", "--system-prompt", system_prompt,
            "--json-schema", json.dumps(schema),
        ]
        if self.model:
            cmd += ["--model", self.model]
        env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_SESSION_ID",)}
        errors: list[str] = []
        t0 = time.monotonic()
        raw = ""
        for attempt in range(1, self.max_attempts + 1):
            try:
                proc = subprocess.run(cmd, input=user_prompt, capture_output=True, text=True,
                                      timeout=self.timeout_s, cwd=self._cwd, env=env)
                raw = proc.stdout
                if proc.returncode != 0:
                    raise RuntimeError(f"rc={proc.returncode}: {proc.stderr[-500:]}")
                env_json = json.loads(raw)
                if env_json.get("is_error"):
                    raise RuntimeError(f"CLI error result: {str(env_json.get('result'))[:500]}")
                out = env_json.get("structured_output")
                if out is None:
                    out = json.loads(env_json.get("result", ""))
                return LLMCall(True, out, raw, time.monotonic() - t0, env_json.get("total_cost_usd"), attempt, errors)
            except (subprocess.TimeoutExpired, RuntimeError, json.JSONDecodeError) as exc:
                errors.append(f"attempt {attempt}: {type(exc).__name__}: {str(exc)[:300]}")
                if attempt < self.max_attempts:
                    time.sleep(min(30.0, 2.0 ** attempt) * (0.5 + random.random()))
        return LLMCall(False, None, raw, time.monotonic() - t0, None, self.max_attempts, errors)
