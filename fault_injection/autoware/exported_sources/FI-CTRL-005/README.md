# FI-CTRL-005: internal command-filter brake loss

Inside `filterControlCommand()`, a filtered braking result is replaced by a
coasting result before filter state is updated. The publish function is not
modified; it publishes the naturally propagated faulty filter output.
