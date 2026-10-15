# FI-PLAN-007 validation

FI-PLAN-007 adds a constant +20 m/s bias to the final constrained trajectory
while preserving its geometry and relative velocity differences.

| ve | xa | xf | clean | fault |
|---:|---:|---:|:---:|:---:|
| 5 | 133 | 7.9 | PS | Aa |
| 10 | 120 | 20 | PS | Aa |

Both retained cases are strict deterministic ego-side differentials and have
rosbags with function- and code-level Ground Truth.
