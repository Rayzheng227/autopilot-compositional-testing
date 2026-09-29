#!/usr/bin/env python3
"""Extract the longitudinal command propagation chain from an Autoware rosbag."""

import argparse
import json
import math
from collections import defaultdict

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


TOPICS = {
    "/planning/scenario_planning/lane_driving/trajectory": "trajectory",
    "/planning/scenario_planning/trajectory": "scenario_trajectory",
    "/control/trajectory_follower/control_cmd": "controller_cmd",
    "/control/command/control_cmd": "gated_cmd",
    "/control/vehicle_cmd_gate/is_filter_activated": "gate_filter",
    "/vehicle/status/velocity_status": "velocity_status",
    "/localization/kinematic_state": "odometry",
}


def values_for(kind, message):
    if kind in {"trajectory", "scenario_trajectory"}:
        return [float(point.longitudinal_velocity_mps) for point in message.points]
    if kind in {"controller_cmd", "gated_cmd"}:
        return [float(message.longitudinal.speed), float(message.longitudinal.acceleration)]
    if kind == "velocity_status":
        return [float(message.longitudinal_velocity)]
    if kind == "odometry":
        return [float(message.twist.twist.linear.x)]
    if kind == "gate_filter":
        return [
            bool(message.is_activated),
            bool(message.is_activated_on_speed),
            bool(message.is_activated_on_acceleration),
            bool(message.is_activated_on_jerk),
            bool(message.is_activated_on_steering),
            bool(message.is_activated_on_steering_rate),
        ]
    return []


def summarize(series):
    flat = [value for sample in series for value in sample if math.isfinite(value)]
    summary = {
        "messages": len(series),
        "samples": len(flat),
        "min": min(flat) if flat else None,
        "max": max(flat) if flat else None,
        "mean": sum(flat) / len(flat) if flat else None,
    }
    if series and len(series[0]) == 2:
        speeds = [sample[0] for sample in series]
        accelerations = [sample[1] for sample in series]
        summary.update({
            "speed_min": min(speeds), "speed_max": max(speeds),
            "acceleration_min": min(accelerations),
            "acceleration_max": max(accelerations),
        })
    return summary


def summarize_filter(series):
    labels = ["any", "speed", "acceleration", "jerk", "steering", "steering_rate"]
    return {
        "messages": len(series),
        "activated_counts": {
            label: sum(bool(sample[index]) for sample in series)
            for index, label in enumerate(labels)
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bag")
    args = parser.parse_args()

    storage_options = rosbag2_py.StorageOptions(uri=args.bag, storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions("cdr", "cdr")
    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)
    types = {item.name: item.type for item in reader.get_all_topics_and_types()}
    selected_types = {name: get_message(types[name]) for name in TOPICS if name in types}
    series = defaultdict(list)

    while reader.has_next():
        topic, data, _ = reader.read_next()
        if topic not in selected_types:
            continue
        message = deserialize_message(data, selected_types[topic])
        series[TOPICS[topic]].append(values_for(TOPICS[topic], message))

    print(json.dumps({
        name: summarize_filter(samples) if name == "gate_filter" else summarize(samples)
        for name, samples in series.items()
    }, indent=2))


if __name__ == "__main__":
    main()
