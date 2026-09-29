FROM autoware-v1-determinism:local

USER root
COPY vehicle_cmd_gate.cpp.patch /tmp/FI-CTRL-003.patch

RUN cd /autoware \
    && patch --batch --forward -p1 < /tmp/FI-CTRL-003.patch \
    && . /opt/ros/humble/setup.sh \
    && colcon build --packages-select vehicle_cmd_gate --parallel-workers 4 \
         --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release \
    && rm /tmp/FI-CTRL-003.patch

LABEL org.cctest.fault.id="FI-CTRL-003" \
      org.cctest.fault.module="Control" \
      org.cctest.fault.function="VehicleCmdGate::publishControlCommands" \
      org.cctest.fault.activation="post-filter acceleration < 0 while engaged"
