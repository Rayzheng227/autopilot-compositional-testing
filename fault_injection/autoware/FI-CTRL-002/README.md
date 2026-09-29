# FI-CTRL-002: post-filter longitudinal command corruption

This fault is injected after `VehicleCmdGate` completes normal command
filtering. While autonomous control is engaged and no system emergency is
active, it replaces the final longitudinal command with `20 m/s` and
`+3 m/s^2`. Lateral steering is unchanged.

## Ground truth

- Module: Control
- Package: `vehicle_cmd_gate`
- File: `control/vehicle_cmd_gate/src/vehicle_cmd_gate.cpp`
- Function: `VehicleCmdGate::publishControlCommands`
- Fault model: actuator-command overwrite after safety filtering
- Activation oracle: `FI-CTRL-002 activated`
- Expected propagation: ignored stop/brake command -> excessive ego motion ->
  ego collides with arriving vehicle -> `Ae` / `ego_fault`

The activation log records the unmodified post-filter command, injected
command, and current vehicle speed. Rosbag topics
`/control/trajectory_follower/control_cmd`, `/control/command/control_cmd`, and
`/vehicle/status/velocity_status` provide the corresponding propagation chain.
