# FI-CTRL-002 validation report

## Result

FI-CTRL-002 is a successful ego-side causal fault. Twelve deterministic safe
cases (ten `CS` and two `PS`) changed to collision verdict `Aa` after the
post-filter command mutation.

The current CCTest oracle attaches `arriving_fault` to `Aa`. This is a
collision-geometry classification: it compares ego-front-to-arriving-center
and arriving-front-to-ego-center distances at the last sample. It is distinct
from fault-injection causality. In these experiments only ego Autoware is
modified, and the same scenario parameters are safe with the clean image.

## Function-level ground truth

- Module: Control
- Package: `vehicle_cmd_gate`
- File: `control/vehicle_cmd_gate/src/vehicle_cmd_gate.cpp`
- Function: `VehicleCmdGate::publishControlCommands`
- Injection point: after `filterControlCommand()`, before `control_cmd_pub_->publish()`
- Mutation: overwrite final speed with `20 m/s` and acceleration with `+3 m/s^2`
- Activation: engaged autonomous control with no system emergency
- Runtime oracle: `FI-CTRL-002 activated`

## Representative propagation evidence

Case: `merging, ve=10, xa=85, xf=10`, clean/source `CS`, faulty `Aa`.

- Controller speed range: `0 .. 13.1471 m/s`
- Controller acceleration range: `-5.0 .. -0.5 m/s^2`
- Published gate speed: exactly `20.0 m/s`
- Published gate acceleration: exactly `+3.0 m/s^2`
- Actual ego maximum speed: `16.6001 m/s`
- Initial ego speed: `10.0 m/s`

Thus the evidence chain is complete:

```text
VehicleCmdGate mutation
  -> final command is overwritten after normal limits
  -> /control/command/control_cmd records 20 m/s, +3 m/s^2
  -> ego accelerates to 16.60 m/s despite controller braking
  -> clean CS becomes faulty Aa collision
```

## Screened cases

| ve | xa | xf | clean/source | faulty |
|---:|---:|---:|:---:|:---:|
| 0 | 200 | 10 | CS | Aa |
| 0 | 200 | 20 | CS | Aa |
| 0 | 205 | 5 | CS | Aa |
| 0 | 210 | 10 | CS | Aa |
| 10 | 85 | 10 | CS | Aa |
| 10 | 85 | 20 | CS | Aa |
| 10 | 90 | 5 | CS | Aa |
| 10 | 95 | 10 | PS | Aa |
| 15 | 85 | 10 | CS | Aa |
| 15 | 85 | 20 | CS | Aa |
| 15 | 90 | 5 | CS | Aa |
| 15 | 125 | 15 | PS | Aa |

All twelve runs have rosbags with `scene.yaml` Ground Truth. The representative
rosbag is stored at:

`/home/ray/AutowareRecordings/FI-CTRL-002/merging-probe/FI-CTRL-002_merging_ve-10p0_xf-10p0_xa-85p0`
