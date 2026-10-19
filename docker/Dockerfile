# syntax=docker/dockerfile:1
# Reproducible environment: Ubuntu 24.04 + OpenFOAM v2412 (ESI, pinned package) + pinned Python deps.
#   docker build -t socrates-cfd -f docker/Dockerfile .
#   docker run --rm -it -v "$PWD/results:/work/results" socrates-cfd pytest -q
#   docker run --rm -it -v "$PWD/results:/work/results" socrates-cfd python3 scripts/run_root_cases.py cases/adversarial/A1_coarse_mesh.yaml
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    SOCRATES_OPENFOAM_BASHRC=/usr/lib/openfoam/openfoam2412/etc/bashrc \
    PIP_BREAK_SYSTEM_PACKAGES=1

# Optional for networks behind a TLS-intercepting proxy (not baked into the image):
#   docker build --secret id=extra_ca,src=/path/to/proxy-ca.crt --build-arg https_proxy=... ...
RUN --mount=type=secret,id=extra_ca,required=false \
    set -eux; \
    if [ -f /run/secrets/extra_ca ]; then mkdir -p /usr/local/share/ca-certificates; \
        cp /run/secrets/extra_ca /usr/local/share/ca-certificates/build-proxy.crt; fi; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl gnupg python3 python3-pip python3-venv; \
    update-ca-certificates; \
    curl -fsSL https://dl.openfoam.com/add-debian-repo.sh -o /tmp/add-openfoam-repo.sh; \
    bash /tmp/add-openfoam-repo.sh; \
    apt-get install -y --no-install-recommends openfoam2412=2412.260127-1; \
    rm -f /usr/local/share/ca-certificates/build-proxy.crt /tmp/add-openfoam-repo.sh; \
    update-ca-certificates --fresh; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY requirements.lock pyproject.toml README.md ./
RUN --mount=type=secret,id=extra_ca,required=false \
    set -eux; if [ -f /run/secrets/extra_ca ]; then export PIP_CERT=/run/secrets/extra_ca; fi; \
    pip3 install --no-cache-dir -r requirements.lock
COPY src ./src
COPY configs ./configs
COPY cases ./cases
COPY benchmark ./benchmark
COPY scripts ./scripts
COPY tests ./tests
RUN --mount=type=secret,id=extra_ca,required=false \
    set -eux; if [ -f /run/secrets/extra_ca ]; then export PIP_CERT=/run/secrets/extra_ca; fi; \
    pip3 install --no-cache-dir --no-deps -e .

# the LLM critic needs the `claude` CLI and credentials; it is optional:
# deterministic systems (A, B, C-rule, B+exh) run without it.
CMD ["bash"]
