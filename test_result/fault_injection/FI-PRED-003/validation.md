# FI-PRED-003 validation

FI-PRED-003 translates every predicted object and path pose by +1000 m in map
X and Y immediately before publication.

| ve | xa | xf | clean | fault |
|---:|---:|---:|:---:|:---:|
| 10 | 85 | 10 | CS | Aa |
| 10 | 85 | 20 | CS | Aa |
| 15 | 85 | 20 | CS | Aa |

All retained cases are strict deterministic ego-side differentials and have
rosbags with function- and code-level Ground Truth.
