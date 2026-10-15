# FI-PRED-002 validation

FI-PRED-002 freezes every dynamic predicted path at the object's current pose
and sets its predicted initial velocity to zero.

| ve | xa | xf | clean | fault |
|---:|---:|---:|:---:|:---:|
| 10 | 85 | 20 | CS | Aa |
| 15 | 85 | 20 | CS | Aa |

Only collision-producing cases are retained. Both have rosbags with function-
and code-level Ground Truth.
