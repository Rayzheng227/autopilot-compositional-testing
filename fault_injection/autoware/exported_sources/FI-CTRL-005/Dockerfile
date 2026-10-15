FROM autoware-v1-determinism:local
USER root
COPY vehicle_cmd_gate.cpp.patch /tmp/FI-CTRL-005.patch
RUN cd /autoware \
    && patch --batch --forward -p1 < /tmp/FI-CTRL-005.patch \
    && . /opt/ros/humble/setup.sh \
    && colcon build --packages-select vehicle_cmd_gate --parallel-workers 4 \
         --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release \
    && rm /tmp/FI-CTRL-005.patch
LABEL org.cctest.fault.id="FI-CTRL-005" \
      org.cctest.fault.module="Control" \
      org.cctest.fault.function="VehicleCmdGate::filterControlCommand" \
      org.cctest.fault.activation="internal filtered command requests braking"
