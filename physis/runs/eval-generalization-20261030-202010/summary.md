# Generalization evaluation — 20261030-202010

Dataset: `/var/tmp/socrates-cfd/physis/runs/weekend-20261030-sharded800`; 798 ok samples; 5 seeds per trainable model ([0, 1000, 2000, 3000, 4000]). CNN 150 epochs; MLP 3000 epochs; device cuda.

Target = log10(K). R², MAE and maximum absolute error are min–max over seeds; KC is deterministic. Errors are in log10(K).

| split | train / test | model | R² | MAE | max error |
|---|---|---|---|---|---|
| random | 639 / 159 | kozeny_carman | 0.880 | 0.153 | 1.926 |
| random | 639 / 159 | mlp_ensemble | 0.973–0.977 | 0.040–0.041 | 1.191–1.281 |
| random | 639 / 159 | cnn | 0.980–0.987 | 0.035–0.050 | 0.830–1.040 |
| porosity_band_held_out | 564 / 165 | kozeny_carman | 0.944 | 0.090 | 0.209 |
| porosity_band_held_out | 564 / 165 | mlp_ensemble | 0.912–0.984 | 0.040–0.103 | 0.232–0.311 |
| porosity_band_held_out | 564 / 165 | cnn | 0.716–0.848 | 0.117–0.172 | 0.569–0.820 |
| low_porosity | 490 / 221 | kozeny_carman | 0.618 | 0.238 | 2.070 |
| low_porosity | 490 / 221 | mlp_ensemble | 0.683–0.932 | 0.104–0.267 | 1.178–1.856 |
| low_porosity | 490 / 221 | cnn | 0.805–0.879 | 0.129–0.199 | 1.442–1.589 |
| unseen_spheres | 531 / 267 | kozeny_carman | 0.868 | 0.205 | 0.421 |
| unseen_spheres | 531 / 267 | mlp_ensemble | 0.599–0.939 | 0.118–0.295 | 0.461–1.333 |
| unseen_spheres | 531 / 267 | mlp_noflag | 0.069–0.158 | 0.411–0.441 | 1.394–2.391 |
| unseen_spheres | 531 / 267 | cnn | 0.636–0.801 | 0.222–0.296 | 0.796–1.032 |
| unseen_voids | 533 / 265 | kozeny_carman | 0.434 | 0.329 | 2.138 |
| unseen_voids | 533 / 265 | mlp_ensemble | 0.104–0.330 | 0.374–0.458 | 2.129–2.307 |
| unseen_voids | 533 / 265 | mlp_noflag | 0.366–0.382 | 0.362–0.367 | 2.105–2.153 |
| unseen_voids | 533 / 265 | cnn | 0.166–0.309 | 0.460–0.513 | 1.991–2.139 |
| unseen_gyroid | 532 / 266 | kozeny_carman | 0.944 | 0.123 | 0.173 |
| unseen_gyroid | 532 / 266 | mlp_ensemble | -35.237–-6.306 | 1.165–2.184 | 2.648–9.438 |
| unseen_gyroid | 532 / 266 | mlp_noflag | -360.687–-3.134 | 0.844–6.335 | 2.627–28.713 |
| unseen_gyroid | 532 / 266 | cnn | 0.688–0.933 | 0.115–0.263 | 0.373–0.837 |
