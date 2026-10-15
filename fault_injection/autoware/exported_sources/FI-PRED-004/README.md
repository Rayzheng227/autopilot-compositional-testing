# FI-PRED-004: tracked-velocity dropout

The tracked object's measured velocity is set to zero before map association,
maneuver inference, and path generation. Prediction then executes normally on
the corrupted internal observation. No published message is directly edited.
