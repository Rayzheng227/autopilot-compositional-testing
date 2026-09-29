# FI-PLAN-005

This fault corrupts the final trajectory inside
`MotionVelocitySmootherNode::publishTrajectory()`, after all normal velocity,
acceleration, jerk, and stop constraints have been applied. Every trajectory
point is overwritten with 40 m/s and +3 m/s² immediately before publication.

Activation marker: `FI-PLAN-005 activated: final trajectory overwritten`.
