# FI-PLAN-006 validation

FI-PLAN-006 suppresses only stop and near-stop points after the final Planning
trajectory has passed velocity, acceleration, jerk, and stop constraints.

| ve | xa | xf | clean | fault | strict differential |
|---:|---:|---:|:---:|:---:|:---:|
| 5 | 133 | 7.9 | PS | Ae | yes |
| 5 | 138 | 5 | PS | Ae | yes |
| 10 | 120 | 20 | PS | Ae | yes |

All three retained cases are deterministic safe-to-ego-fault differentials.
Only ego Planning differs, and every rosbag contains `scene.yaml` with the
function- and code-level Ground Truth.
