# Voids percolation resolution study — 2026-10-30

Eight stored `geometry` specs from `runs/weekend-20261030-sharded800/dataset.jsonl`.
Triton, float32, 400k steps at 128³; 800k at 192³ and above.
Each completed run was appended and fsynced before the next. No volumes were saved.

| index | K(128) | K(192) | K(256) | K(192) / K(128) | K(256) / K(128) | status at 128 / 192 / 256 |
|---|---|---|---|---|---|---|
| 583 | 9.6218909e-07 | 3.5142911e-07 | 1.7199165e-07 | 0.3652 | 0.1788 | ok / ok / ok |
| 325 | 1.3048045e-06 | 5.6029432e-07 | 2.4713027e-07 | 0.4294 | 0.1894 | ok / ok / ok |
| 682 | 2.3925598e-06 | 1.9125104e-06 | 1.8262436e-06 | 0.7994 | 0.7633 | ok / ok / ok |
| 148 | 4.2095606e-06 | 3.2790047e-06 | 2.9104971e-06 | 0.7789 | 0.6914 | ok / ok / ok |
| 220 | 8.1837438e-06 | 6.3757068e-06 | 6.0491062e-06 | 0.7791 | 0.7392 | ok / ok / ok |
| 436 | 3.5141117e-06 | 2.3649687e-06 | 1.8499938e-06 | 0.6730 | 0.5264 | ok / ok / ok |
| 667 | 5.2228650e-08 | 1.1163886e-09 | 8.7217743e-10 | 0.0214 | 0.0167 | not_converged / not_converged / not_converged |
| 790 | -1.6877483e-10 | -3.7967840e-11 | -2.2012214e-10 | 0.2250 | 1.3042 | not_percolating / not_percolating / not_percolating |

Six samples converge at all three resolutions. Their K(256) / K(128) ratios range
from 0.1788 to 0.7633; this selected set has substantial resolution dependence.
Sample 667 reaches every step limit without convergence. Its reported K decreases
but does not establish a steady permeability or a percolation classification.
Sample 790 remains solver-classified `not_percolating` at all three resolutions;
its tiny negative K values are signed numerical residuals, not physical negative
permeabilities. Their ratios are retained for audit only.

Optional 384³: sample 220 converged in 37,632 steps, K = 5.3863135e-6,
K(384) / K(128) = 0.6582. No 384³ runs were completed for the other seven samples;
the step-limit cases and required 128–256³ coverage took priority.

## Run records

| index | n | porosity | K | steps | status | wall s | K / K(128) | host |
|---|---|---|---|---|---|---|---|---|
| 583 | 128 | 0.35725451 | 9.6218909e-07 | 38407 | ok | 16.0 | 1.0000 | nc-10-2-3 |
| 583 | 192 | 0.35727211 | 3.5142911e-07 | 81536 | ok | 112.0 | 0.3652 | nc-10-2-3 |
| 583 | 256 | 0.35724443 | 1.7199165e-07 | 159200 | ok | 516.6 | 0.1788 | nc-10-2-3 |
| 325 | 128 | 0.38582516 | 1.3048045e-06 | 65272 | ok | 27.0 | 1.0000 | nc-10-2-3 |
| 325 | 192 | 0.38589068 | 5.6029432e-07 | 174720 | ok | 239.6 | 0.4294 | nc-10-2-3 |
| 325 | 256 | 0.38586110 | 2.4713027e-07 | 66068 | ok | 214.8 | 0.1894 | nc-10-2-3 |
| 682 | 128 | 0.36016226 | 2.3925598e-06 | 42984 | ok | 18.3 | 1.0000 | nc-10-3-4 |
| 682 | 192 | 0.36008595 | 1.9125104e-06 | 63168 | ok | 88.6 | 0.7994 | nc-10-3-4 |
| 682 | 256 | 0.36007434 | 1.8262436e-06 | 93132 | ok | 308.0 | 0.7633 | nc-10-3-4 |
| 148 | 128 | 0.36131763 | 4.2095606e-06 | 51342 | ok | 21.8 | 1.0000 | nc-10-3-4 |
| 148 | 192 | 0.36135822 | 3.2790047e-06 | 44352 | ok | 62.5 | 0.7789 | nc-10-3-4 |
| 148 | 256 | 0.36137182 | 2.9104971e-06 | 50944 | ok | 169.4 | 0.6914 | nc-10-3-4 |
| 220 | 128 | 0.40021849 | 8.1837438e-06 | 19900 | ok | 8.8 | 1.0000 | nc-11-3-2 |
| 220 | 192 | 0.40021275 | 6.3757068e-06 | 23296 | ok | 33.5 | 0.7791 | nc-11-3-2 |
| 220 | 256 | 0.40019959 | 6.0491062e-06 | 27064 | ok | 91.9 | 0.7392 | nc-11-3-2 |
| 220 | 384 | 0.40019219 | 5.3863135e-06 | 37632 | ok | 222.9 | 0.6582 | nc-9-2-3 |
| 436 | 128 | 0.36570740 | 3.5141117e-06 | 45173 | ok | 19.8 | 1.0000 | nc-11-3-2 |
| 436 | 192 | 0.36563902 | 2.3649687e-06 | 58240 | ok | 84.4 | 0.6730 | nc-11-3-2 |
| 436 | 256 | 0.36561668 | 1.8499938e-06 | 60496 | ok | 205.9 | 0.5264 | nc-11-3-2 |
| 667 | 128 | 0.37363529 | 5.2228650e-08 | 400000 | not_converged | 170.9 | 1.0000 | nc-12-2-5 |
| 667 | 192 | 0.37357613 | 1.1163886e-09 | 800000 | not_converged | 1140.1 | 0.0214 | nc-12-2-5 |
| 667 | 256 | 0.37357658 | 8.7217743e-10 | 800000 | not_converged | 2673.9 | 0.0167 | nc-12-2-5 |
| 790 | 128 | 0.39844608 | -1.6877483e-10 | 400000 | not_percolating | 170.6 | 1.0000 | nc-12-2-5 |
| 790 | 192 | 0.39837053 | -3.7967840e-11 | 800000 | not_percolating | 592.8 | 0.2250 | nc-9-2-3 |
| 790 | 256 | 0.39837819 | -2.2012214e-10 | 800000 | not_percolating | 1393.6 | 1.3042 | nc-9-2-3 |

## Failures, restarts and replicas

No saved run reports a solver exception or a memory skip. Sample 667 did not converge
at 400k / 800k / 800k steps; sample 790 also exhausted those limits and was classified
`not_percolating` by the solver threshold. These statuses are retained.

Several in-flight attempts were interrupted to prioritize required resolutions and to
relaunch under `nohup setsid`; completed rows were preserved. Copied baseline rows in
the raw checkpoint files support resumption and are not additional experiments.

The 325/256 run was repeated on nc-11-3-2 and matches the canonical K and step count.
The 790/192 repeat on nc-12-2-5 differs from the canonical 5090 result by about 1.15e-16
in absolute K; both are negative residuals classified `not_percolating`. A redundant
790/256 run remains active on nc-12-2-5 at collection time. It is not required to fill
the table, whose 790/256 row is the completed 5090 run. It was left running at the
user’s request to let all jobs run.

`results.jsonl` contains the selected complete 25-row study. The `nc-*.jsonl` files
retain the raw checkpoint rows and replicas available at collection time.
