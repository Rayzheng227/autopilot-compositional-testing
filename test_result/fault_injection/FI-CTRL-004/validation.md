# FI-CTRL-004 validation

FI-CTRL-004 drops negative acceleration at the final Control gate and holds the
target speed at least at the current ego speed.

| ve | xa | xf | clean | fault | strict differential |
|---:|---:|---:|:---:|:---:|:---:|
| 0 | 200 | 10 | CS | Ae | yes |
| 10 | 85 | 10 | CS | Aa | yes |
| 15 | 85 | 20 | CS | Aa | yes |

All three retained cases are deterministic safe-to-collision differentials.
Only ego Control differs, and every rosbag contains `scene.yaml` with the
function- and code-level Ground Truth.
