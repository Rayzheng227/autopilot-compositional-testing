# FI-PLAN-005 validation

FI-PLAN-005 mutates the final Planning trajectory after the motion velocity
smoother has applied speed, acceleration, jerk, and stop constraints. Every
published point is overwritten with 40 m/s and +3 m/s2.

## Deterministic differential results

| ve | xa | xf | clean | fault | strict differential |
|---:|---:|---:|:---:|:---:|:---:|
| 5 | 130 | 10 | PS | PS | no |
| 5 | 130 | 20 | PS | PS | no |
| 5 | 130 | 40 | PS | PS | no |
| 5 | 132 | 7.9 | PS | Aa | yes |
| 5 | 132 | 15 | PS | Aa | yes |
| 5 | 133 | 7.9 | PS | Aa | yes |
| 5 | 134 | 7.9 | PS | Aa | yes |
| 5 | 134 | 15 | PS | Aa | yes |
| 5 | 136 | 7.9 | PS | Aa | yes |
| 5 | 136 | 15 | PS | Aa | yes |
| 5 | 138 | 5 | PS | Aa | yes |
| 5 | 138 | 15 | PS | Aa | yes |
| 10 | 118 | 15 | PS | Aa | yes |
| 10 | 118 | 25 | PS | Aa | yes |
| 10 | 120 | 20 | PS | Aa | yes |
| 10 | 122 | 15 | PS | Aa | yes |
| 10 | 122 | 25 | PS | Aa | yes |

The activation marker was emitted from
`MotionVelocitySmootherNode::publishTrajectory()` and recorded non-empty final
trajectories being overwritten. Both successful cases have deterministic clean
`PS` counterfactuals and faulty collision verdicts.

CCTest labels the collision geometry as `Aa` / `arriving_fault`. The causal
software responsibility remains ego: only the ego Planning image differs, and
the clean counterfactual with the identical scenario parameters is safe. The
expanded set contains 14 strict `PS -> Aa` cases and three stable `PS -> PS`
negative controls. All 17 rosbags include `scene.yaml` with function- and
code-level Ground Truth.
