# FI-PLAN-008: optimizer-input stop-constraint deletion

Stop points are removed from the internal trajectory before velocity smoothing.
The optimizer therefore receives a faulty constraint set and naturally produces
the published output. No published message is directly edited.
