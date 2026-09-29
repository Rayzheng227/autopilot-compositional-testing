# FI-CTRL-003: brake-command polarity inversion

After normal `VehicleCmdGate` filtering, every negative longitudinal
acceleration is converted to its positive magnitude. The target speed is raised
to at least `actual_speed + 5 m/s`, preserving a coherent accelerating command.
The mutation is active only while autonomous control is engaged and no system
emergency is active.

The runtime activation oracle is `FI-CTRL-003 activated`. The log contains the
original post-filter command, mutated command, and actual ego speed.
