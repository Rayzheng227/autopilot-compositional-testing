# FI-CTRL-005 validation

FI-CTRL-005 drops braking inside `filterControlCommand()` and stores the faulty
result as filter state. The control-command publisher is unchanged.

| ve | xa | xf | clean | fault |
|---:|---:|---:|:---:|:---:|
| 0 | 200 | 10 | CS | Ae |
| 10 | 85 | 10 | CS | Aa |

Both retained cases are deterministic ego-side differentials and have rosbags
with function- and code-level Ground Truth.
