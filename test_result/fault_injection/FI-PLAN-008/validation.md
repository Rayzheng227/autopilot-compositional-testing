# FI-PLAN-008 validation

FI-PLAN-008 deletes stop and near-stop velocity constraints from the internal
trajectory before velocity optimization. The final publisher is unchanged.

| ve | xa | xf | clean | fault |
|---:|---:|---:|:---:|:---:|
| 5 | 133 | 7.9 | PS | Aa |
| 10 | 120 | 20 | PS | Aa |

Both retained cases are deterministic ego-side differentials and have rosbags
with function- and code-level Ground Truth.
