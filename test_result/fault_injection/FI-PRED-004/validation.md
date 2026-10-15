# FI-PRED-004 validation

FI-PRED-004 drops the internal tracked-object velocity before map association,
maneuver inference, and path generation. The prediction publisher is unchanged.

| ve | xa | xf | clean | fault |
|---:|---:|---:|:---:|:---:|
| 10 | 85 | 20 | CS | Aa |
| 15 | 85 | 20 | CS | Aa |

Both retained cases are deterministic ego-side differentials and have rosbags
with function- and code-level Ground Truth.
