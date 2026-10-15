FROM autoware-v1-determinism:local

USER root
COPY map_based_prediction_node.cpp.patch /tmp/FI-PRED-001.patch

RUN cd /autoware \
    && patch --batch --forward -p1 < /tmp/FI-PRED-001.patch \
    && . /opt/ros/humble/setup.sh \
    && colcon build --packages-select map_based_prediction --parallel-workers 4 \
         --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release \
    && rm /tmp/FI-PRED-001.patch

LABEL org.cctest.fault.id="FI-PRED-001" \
      org.cctest.fault.module="Prediction" \
      org.cctest.fault.function="MapBasedPredictionNode::objectsCallback" \
      org.cctest.fault.activation="one or more predicted objects before publish"
