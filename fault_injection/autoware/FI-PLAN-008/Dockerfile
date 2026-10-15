FROM autoware-v1-determinism:local
USER root
COPY motion_velocity_smoother_node.cpp.patch /tmp/FI-PLAN-008.patch
RUN cd /autoware \
    && patch --batch --forward -p1 < /tmp/FI-PLAN-008.patch \
    && . /opt/ros/humble/setup.sh \
    && colcon build --packages-select motion_velocity_smoother --parallel-workers 4 \
         --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release \
    && rm /tmp/FI-PLAN-008.patch
LABEL org.cctest.fault.id="FI-PLAN-008" \
      org.cctest.fault.module="Planning" \
      org.cctest.fault.function="MotionVelocitySmootherNode::calcTrajectoryVelocity" \
      org.cctest.fault.activation="optimizer input contains stop points"
