# FI-PRED-001 validation

FI-PRED-001 clears the computed predicted-object list immediately before
publication while preserving the message header and normal node lifecycle.

| vista | ve | xa | xf | clean | fault | strict differential |
|---|---:|---:|---:|:---:|:---:|:---:|
| merging | 10 | 85 | 10 | CS | Aa | yes |

Only the strict collision-producing case is retained. The external traffic is
unchanged; only ego Prediction omits the conflict vehicle. The rosbag contains
`scene.yaml` with function- and code-level Ground Truth.
