# FI-CTRL-004: brake-command omission

When the final post-filter command requests negative acceleration, the brake is
dropped: acceleration becomes zero and target speed is held at least at the
current ego speed. The runtime oracle is `FI-CTRL-004 activated`.
