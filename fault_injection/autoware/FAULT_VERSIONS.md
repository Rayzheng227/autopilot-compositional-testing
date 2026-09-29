# Autoware 故障版本与场景说明

本文档是 Autoware 故障注入版本的对外索引。新增、删除或重新验证故障时，应同时更新本文档、`catalog.yaml`、`experiments.yaml` 和对应 batch JSON。

## 统一定义

- 干净版本：`autoware-v1-determinism:local`，同一参数下结果确定。
- 故障版本：一次只在 ego（v1）的一个代码位置注入一个故障；v2 保持干净。
- 严格有效场景：干净版本无故障，故障版本出现由 ego 负责的 `Aa` 或 `Ae`。
- `ve`：ego 初始速度；`xa`、`xf`：CCTest 场景中的纵向位置参数。参数语义和坐标系仍以对应 vista 实现为准。
- Ground Truth：每份录制目录的 `scene.yaml` 保存故障 ID、模块、包、源文件、函数、注入点、代码变化、触发条件和责任依据。

## 版本总览

| 故障 ID | 模块 | 修改函数 | 一键场景数 | 严格成功数 | 负对照数 | 故障镜像 |
|---|---|---|---:|---:|---:|---|
| FI-CTRL-002 | Control | `VehicleCmdGate::publishControlCommands` | 12 | 12 | 0 | `autoware-cctest-fault:fi-ctrl-002` |
| FI-CTRL-003 | Control | `VehicleCmdGate::publishControlCommands` | 6 | 6 | 0 | `autoware-cctest-fault:fi-ctrl-003` |
| FI-PLAN-005 | Planning | `MotionVelocitySmootherNode::publishTrajectory` | 17 | 14 | 3 | `autoware-cctest-fault:fi-plan-005` |

## FI-CTRL-002：Gate 后纵向命令覆盖

### 修改了什么

- 源文件：`control/vehicle_cmd_gate/src/vehicle_cmd_gate.cpp`
- 函数：`VehicleCmdGate::publishControlCommands`
- 注入位置：正常 `filterControlCommand()` 完成后、最终控制命令发布前。
- 修改：自动驾驶已 engaged 且无系统 emergency 时，将最终纵向速度强制设为 `20 m/s`，加速度设为 `+3 m/s²`；横向转向保持不变。
- 触发日志：`FI-CTRL-002 activated`，同时输出注入前后命令和实际车速。
- 因果解释：规划与上游控制仍可产生停车/制动意图，但最终 Gate 命令被 ego 自身覆盖，导致 ego 继续加速并碰撞。
- 补丁：[`FI-CTRL-002/vehicle_cmd_gate.cpp.patch`](FI-CTRL-002/vehicle_cmd_gate.cpp.patch)

### 场景与参数

场景类型为 `merging`。选择安全区与事故边界附近的参数，是为了确保干净版能够合流或安全停车，同时让“忽略制动”在有限仿真时间内传播为碰撞。

| ve | xa | xf | 干净结果 | 故障结果 | 状态/选择原因 |
|---:|---:|---:|:---:|:---:|---|
| 0 | 200 | 10 | CS | Aa | 已验证；静止起步后的强制加速穿越合流冲突区 |
| 0 | 200 | 20 | CS | Aa | 已验证；改变冲突车位置，检验参数邻域稳定性 |
| 0 | 205 | 5 | CS | Aa | 已验证；靠近安全/碰撞边界 |
| 0 | 210 | 10 | CS | Aa | 已验证；扩大 `xa` 覆盖 |
| 10 | 85 | 10 | CS | Aa | 已验证；运动中 ego 的代表性合流点 |
| 10 | 85 | 20 | CS | Aa | 已验证；同一 `xa` 下改变 `xf` |
| 10 | 90 | 5 | CS | Aa | 已验证；安全边界扩展点 |
| 10 | 95 | 10 | PS | Aa | 已验证；证明故障也能破坏 `PS` 类型安全基线 |
| 15 | 85 | 10 | CS | Aa | 已验证；更高 ego 初速 |
| 15 | 85 | 20 | CS | Aa | 已验证；更高初速下改变冲突车位置 |
| 15 | 90 | 5 | CS | Aa | 已验证；更高初速的边界点 |
| 15 | 125 | 15 | PS | Aa | 已验证；远离原参数簇的泛化点 |

场景文件：[`batches/merging-fi-ctrl-002-screen.json`](batches/merging-fi-ctrl-002-screen.json)

## FI-CTRL-003：制动命令符号反转

### 修改了什么

- 源文件：`control/vehicle_cmd_gate/src/vehicle_cmd_gate.cpp`
- 函数：`VehicleCmdGate::publishControlCommands`
- 注入位置：正常 Gate 过滤后、发布前。
- 修改：仅当最终加速度小于 0 时，将制动加速度取绝对值变为正加速，并令目标速度至少为 `实际速度 + 5 m/s`。
- 触发日志：`FI-CTRL-003 activated`。
- 因果解释：这是比固定覆盖更接近执行器极性/配置错误的故障；只有 ego 真正请求制动时才激活，故障后 ego 将制动解释为加速。
- 补丁：[`FI-CTRL-003/vehicle_cmd_gate.cpp.patch`](FI-CTRL-003/vehicle_cmd_gate.cpp.patch)

### 场景与参数

沿用 FI-CTRL-002 已确认安全且确实产生制动请求的 6 个 `merging` 场景。这样可以隔离比较两种 Control 故障模型，并保证 polarity inversion 的激活条件实际成立。

| ve | xa | xf | 干净结果 | 故障结果 |
|---:|---:|---:|:---:|:---:|
| 0 | 200 | 10 | CS | Aa |
| 0 | 200 | 20 | CS | Aa |
| 0 | 205 | 5 | CS | Aa |
| 0 | 210 | 10 | CS | Aa |
| 10 | 85 | 10 | CS | Aa |
| 10 | 85 | 20 | CS | Aa |

场景文件：[`batches/merging-fi-ctrl-003-screen.json`](batches/merging-fi-ctrl-003-screen.json)

## FI-PLAN-005：平滑后最终轨迹覆盖

### 修改了什么

- 源文件：`planning/motion_velocity_smoother/src/motion_velocity_smoother_node.cpp`
- 函数：`MotionVelocitySmootherNode::publishTrajectory`
- 注入位置：速度、加速度、jerk 和停车约束全部完成后，最终轨迹发布前。
- 修改：把最终轨迹每个点的速度覆盖为 `40 m/s`，加速度覆盖为 `+3 m/s²`，包括原停车点。
- 触发日志：`FI-PLAN-005 activated: final trajectory overwritten`，包含点数和覆盖前最大速度。
- 因果解释：故障位于 ego Planning 最终输出边界；同参数干净轨迹安全，只有 ego 的最终规划轨迹发生变化。
- 补丁：[`FI-PLAN-005/motion_velocity_smoother_node.cpp.patch`](FI-PLAN-005/motion_velocity_smoother_node.cpp.patch)

### 场景与参数

场景类型为 `crossing_with_yield_signs`。参数围绕干净版 `PS` 区域与 `PUp1` 边界搜索：只把干净版为 `PS` 的点纳入故障 batch。`xa=132/134/136, xf=5` 的干净结果为 `PUp1`，因此只作为边界证据，不进入故障 batch；到 `xa=138, xf=5` 恢复为 `PS`，故纳入测试。

| ve | xa | xf | 干净结果 | 故障结果 | 类型 |
|---:|---:|---:|:---:|:---:|---|
| 5 | 130 | 10 | PS | PS | 负对照 |
| 5 | 130 | 20 | PS | PS | 负对照 |
| 5 | 130 | 40 | PS | PS | 负对照 |
| 5 | 132 | 7.9 | PS | Aa | 严格成功 |
| 5 | 132 | 15 | PS | Aa | 严格成功 |
| 5 | 133 | 7.9 | PS | Aa | 严格成功 |
| 5 | 134 | 7.9 | PS | Aa | 严格成功 |
| 5 | 134 | 15 | PS | Aa | 严格成功 |
| 5 | 136 | 7.9 | PS | Aa | 严格成功 |
| 5 | 136 | 15 | PS | Aa | 严格成功 |
| 5 | 138 | 5 | PS | Aa | 严格成功；跨过干净版 `PUp1` 边界后的首个安全点 |
| 5 | 138 | 15 | PS | Aa | 严格成功 |
| 10 | 118 | 15 | PS | Aa | 严格成功；较高初速参数带 |
| 10 | 118 | 25 | PS | Aa | 严格成功 |
| 10 | 120 | 20 | PS | Aa | 严格成功；原始代表点 |
| 10 | 122 | 15 | PS | Aa | 严格成功 |
| 10 | 122 | 25 | PS | Aa | 严格成功 |

场景文件：[`batches/crossing-fi-plan-005-search.json`](batches/crossing-fi-plan-005-search.json)

## 对外发布核心代码

推荐公开本目录，而不是发布三份完整 Autoware fork：

1. 补丁文件精确表示代码级 Ground Truth，可直接审查修改行。
2. 每个 Dockerfile 从同一干净基准构建，确保版本可复现。
3. batch JSON 和本文档解释场景数量、参数来源和验证状态。
4. `export_fault_sources.sh` 可从本机已构建镜像导出每个版本修改后的完整核心 `.cpp` 文件和 SHA-256 清单。

执行：

```bash
bash fault_injection/autoware/export_fault_sources.sh
```

默认输出到 `fault_injection/autoware/exported_sources/`。将该目录与本目录一起提交到 GitHub/GitLab 后，外部用户既能浏览完整故障源文件，也能通过 `.patch` 检查准确差异。公开时还应记录基准 Autoware revision：`896fd1418b25c1501bad7f9b0116af1c0c8dd941`。

镜像本身若也要供外部拉取，建议推送至 GHCR，并使用不可变标签，例如：

```bash
docker tag autoware-cctest-fault:fi-plan-005 ghcr.io/<owner>/autoware-cctest-fault:fi-plan-005-r1
docker push ghcr.io/<owner>/autoware-cctest-fault:fi-plan-005-r1
```

镜像通常很大，论文复现优先发布补丁、Dockerfile、基准 revision 和场景清单；容器仓库作为可选加速分发渠道。
