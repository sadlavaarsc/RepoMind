# CueZero 测试问题集

## 项目概述
CueZero 是一个结合深度强化学习和蒙特卡洛树搜索（MCTS）的高性能台球AI系统。

---

## 问题 1: 简单 - 项目介绍

**难度**: 简单

**问题**: CueZero 是什么项目？

**期望索引的文件**:
- README.md
- README_zh.md

**期望索引的关键函数/类**:
- （项目级，无特定函数）

**标准答案**:
CueZero 是一个高性能台球 AI 系统，结合了深度强化学习和专门设计的连续动作蒙特卡洛树搜索（MCTS）。它解决了高维连续状态和动作空间中具有复杂物理动力学的决策问题。

**关键亮点**:
- 81维状态表示，5维连续动作空间
- 紧凑模型（约160K参数）
- 专门的 MCTS 实现54倍搜索空间缩减
- 相对于规则基代理95%胜率
- 两种 MCTS 模式：Full（强性能）和 Fast（实时推理）

**参考文件**:
- README.md
- README_zh.md

---

## 问题 2: 简单 - 物理引擎

**难度**: 简单

**问题**: 这个项目使用了什么物理引擎？

**期望索引的文件**:
- README.md
- cuezero/env/physics_wrapper.py
- cuezero/env/billiards_env.py

**期望索引的关键函数/类**:
- BilliardsEnv
- simulate_with_timeout

**标准答案**:
CueZero 使用 **pooltool** 作为台球物理引擎。

pooltool 是一个专门为台球游戏设计的物理引擎，提供精确的台球运动模拟。在 CueZero 中：
- physics_wrapper.py 提供了带超时保护的物理模拟函数 `simulate_with_timeout`
- billiards_env.py 中的 BilliardsEnv 类封装了完整的台球环境
- 支持真实的台球物理规则和碰撞检测

**参考文件**:
- README.md
- cuezero/env/physics_wrapper.py
- cuezero/env/billiards_env.py

---

## 问题 3: 简单 - 模型大小

**难度**: 简单

**问题**: 模型有多大？

**期望索引的文件**:
- README.md
- cuezero/models/dual_network.py

**期望索引的关键函数/类**:
- DualNetwork
- SharedFeatureExtractor
- PolicyHead
- ValueHead

**标准答案**:
CueZero 的模型非常紧凑，只有约 **160K 参数**。

尽管台球比传统棋盘游戏更复杂，但通过精心设计的架构实现了小模型强性能：

**模型架构**:
- **共享特征提取器**: 2层全连接 + GRU 用于时空融合
- **策略头**: 2层全连接用于5维动作预测
- **价值头**: 2层全连接用于胜率估计
- **总参数量**: 仅约160K

**为什么这么小**: 智能的架构设计优先考虑基本特征（球位置、速度、球袋状态），同时避免不必要的复杂性。

**参考文件**:
- README.md
- cuezero/models/dual_network.py

---

## 问题 4: 简单 - MCTS 模式

**难度**: 简单

**问题**: MCTS 有哪两种模式？

**期望索引的文件**:
- README.md
- cuezero/mcts/search.py

**期望索引的关键函数/类**:
- MCTS
- MCTS.__init__

**标准答案**:
CueZero 的 MCTS 有两种模式：**Fast** 和 **Full**。

| 特性 | MCTS-Full | MCTS-Fast |
|------|-----------|-----------|
| 模拟次数 | 150 | 30 |
| 最大深度 | 4 | 2 |
| 超时时间 | 15s | 3s |
| 决策时间 | ~3分钟（消费级PC） | ~1秒（消费级PC） |
| 对比Basic胜率 | 95% | 90% |
| 用途 | 强性能、离线 | 实时对战、Web UI |

**MCTS-Fast**: 180倍速度提升，仅损失5%胜率。

**参考文件**:
- README.md
- cuezero/mcts/search.py

---

## 问题 5: 中等 - 状态动作空间

**难度**: 中等

**问题**: 状态和动作空间的维度是多少？

**期望索引的文件**:
- README.md
- cuezero/mcts/search.py
- cuezero/env/state_encoder.py

**期望索引的关键函数/类**:
- MCTS.action_min
- MCTS.action_max
- StateEncoder

**标准答案**:
CueZero 的状态和动作空间维度如下：

**状态空间**: **81维**
- 包含球的位置、速度、球袋状态等信息
- 连续3局状态作为输入（3 × 81维）

**动作空间**: **5维连续动作**
- V0: 击球速度（范围 0.5 → 8.0）
- phi: 水平角度（范围 0° → 360°）
- theta: 垂直角度（范围 0° → 90°）
- a: 击球点水平偏移（范围 -0.5 → 0.5）
- b: 击球点垂直偏移（范围 -0.5 → 0.5）

即使粗略离散化，也有约243,000+种潜在组合。

**参考文件**:
- README.md
- cuezero/mcts/search.py
- cuezero/env/state_encoder.py

---

## 问题 6: 中等 - DualNetwork 架构

**难度**: 中等

**问题**: DualNetwork 的架构是怎样的？

**期望索引的文件**:
- cuezero/models/dual_network.py
- README.md

**期望索引的关键函数/类**:
- DualNetwork
- SharedFeatureExtractor
- PolicyHead
- ValueHead

**标准答案**:
DualNetwork（双网络）的架构设计如下：

### 1. SharedFeatureExtractor（共享特征提取器）
- **输入**: Batch × 3 × 81（连续三局状态向量）
- **空间特征提取**: 2层全连接网络（81→128→128）+ LayerNorm
- **时序特征融合**: GRU层（输入128，隐藏128）
- **输出**: Batch × 128（融合后的特征向量）
- **融合方式**: 最后一局特征 + 三局特征均值

### 2. PolicyHead（策略网络头）
- **输入**: Batch × 128（融合特征）
- **结构**: 2层全连接（128→128→5）+ Dropout(0.1)
- **输出**: Batch × 5（0-1范围的动作参数）
- **激活**: Sigmoid输出0-1范围

### 3. ValueHead（价值网络头）
- **输入**: Batch × 128（融合特征）
- **结构**: 2层全连接（128→128→1）
- **输出**: Batch × 1（胜率预测）

### 4. 动作映射
- PolicyHead.map_actions() 将0-1范围映射到实际动作范围：
  - V0: 0.5 + 7.5 × raw
  - phi: 360 × raw
  - 等等

**参考文件**:
- cuezero/models/dual_network.py
- README.md

---

## 问题 7: 中等 - 运行 CLI 对战

**难度**: 中等

**问题**: 如何运行 CLI 对战？

**期望索引的文件**:
- README.md
- scripts/cli_game.py

**期望索引的关键函数/类**:
- create_agent
- BilliardsEnv
- MCTSAgent

**标准答案**:
运行 CLI 对战的方法如下：

### 基本命令
```bash
# CLI: MCTS-Fast vs BasicAgent（5局）
python scripts/cli_game.py --agent-a mcts_fast --agent-b basic --games 5

# Human vs MCTS-Full（3局）
python scripts/cli_game.py --agent-a human --agent-b mcts_full --games 3

# MCTS-Fast vs BasicAgentPro（10局）
python scripts/cli_game.py --agent-a mcts_fast --agent-b basic_pro --games 10

# 查看所有选项
python scripts/cli_game.py --help
```

### 可用的 Agent 类型
| 类型 | 描述 | 用途 |
|------|------|------|
| human | 人类玩家（CLI/Web UI） | 人机对战 |
| mcts_fast | 快速MCTS（30模拟，深度2，3秒） | 实时对战、Web UI |
| mcts_full | 完整MCTS（150模拟，深度4，15秒） | 强性能、离线 |
| policy | 策略网络直接输出 | 快速推理 |
| basic | 启发式规则基 | 基线对比 |
| basic_pro | 增强物理基 | 高级基线 |
| random | 随机动作 | 测试、调试 |

### 主要功能
- 显示比分和胜率统计
- 支持切换先后手和球类型
- 展示比赛进度和结果

**参考文件**:
- README.md
- scripts/cli_game.py

---

## 问题 8: 复杂 - MCTS 连续动作优化

**难度**: 复杂

**问题**: 详细解释 MCTS 搜索是如何为连续动作空间优化的？

**期望索引的文件**:
- README.md
- cuezero/mcts/search.py
- cuezero/mcts/node.py

**期望索引的关键函数/类**:
- MCTS
- MCTSNode
- simulate_with_timeout

**标准答案**:
CueZero 的 MCTS 为连续动作空间进行了专门优化：

### 挑战
5维连续动作空间，即使粗略离散化也有约243,000+种潜在组合。

### 解决方案

#### 1. Ghost Ball 启发式
- 几何生成约30个高质量候选动作
- 基于台球物理原理，优先考虑有意义的击球

#### 2. 策略引导剪枝
- 使用神经网络策略预测候选动作的优先级
- 保留前2/3的候选（66%缩减）
- 结合启发式和学习到的知识

#### 3. 结果
- **暴力搜索**: 243,000 种组合
- **CueZero**: 仅 4,500 次评估
- **缩减**: 54倍更小的搜索空间！

### MCTS 节点结构（MCTSNode）
- state_seq: 状态序列
- parent: 父节点
- children: 子节点字典
- depth: 深度
- N: 访问次数
- W: 总价值
- Q: 平均价值
- P: 先验概率

### 混合评估策略
结合神经网络预测和物理模拟：
- **早期深度**: 更多模拟（准确但慢）
- **晚期深度**: 更多网络（快但略不准确）
- **动态权重**: 基于搜索深度平滑过渡

### 两种 MCTS 模式
| 特性 | Full | Fast |
|------|------|------|
| n_simulations | 150 | 30 |
| max_depth | 4 | 2 |
| max_search_time | 15s | 3s |

**参考文件**:
- README.md
- cuezero/mcts/search.py
- cuezero/mcts/node.py

---

## 问题 9: 复杂 - 训练 Pipeline

**难度**: 复杂

**问题**: 完整的训练 pipeline 包括哪些步骤？

**期望索引的文件**:
- README.md
- scripts/train.py
- scripts/selfplay.py
- cuezero/training/trainer.py
- cuezero/training/loss.py
- cuezero/training/replay_buffer.py

**期望索引的关键函数/类**:
- Trainer
- ReplayBuffer
- train.py
- selfplay.py

**标准答案**:
CueZero 的完整训练 pipeline 包括以下步骤：

### 1. 预训练阶段（~200 epochs）
- 在 BasicAgent 数据上训练
- 学习基本的击球技能
- 建立初始策略和价值网络

### 2. 自我对弈训练阶段（~600 epochs）
- 使用 MCTS 引导的数据生成
- 自我对弈产生训练数据
- 迭代改进模型
- 关键优化：启发式搜索相比纯 RL 加速3-5倍

### 3. 补充训练阶段（~200 epochs）
- 专门化的精细调整
- 针对特定场景优化
- 总训练量：约1000 epochs 达到完整性能

### 核心训练组件

#### Trainer 类（cuezero/training/trainer.py）
- train_step(): 单步训练
- train_epoch(): 单轮训练
- train(): 多轮训练
- save_model() / load_model(): 模型保存加载

#### 损失函数（cuezero/training/loss.py）
- 策略损失：拟合 MCTS 搜索的策略
- 价值损失：预测胜率
- 组合损失：策略损失 + 价值损失

#### 经验回放（cuezero/training/replay_buffer.py）
- 存储自我对弈数据
- 批量采样训练
- 打破数据相关性

### 训练脚本
- **scripts/train.py**: 主训练脚本
- **scripts/selfplay.py**: 自我对弈数据生成
- **scripts/evaluate.py**: 模型评估

### 硬件配置
**训练集群（思源-1）**:
- CPU: Intel Xeon ICX Platinum 8358
- GPU: NVIDIA HGX A100

**消费级部署**:
- MCTS-Fast 可在标准笔记本/台式机上运行

**参考文件**:
- README.md
- scripts/train.py
- scripts/selfplay.py
- cuezero/training/trainer.py
- cuezero/training/loss.py
- cuezero/training/replay_buffer.py

---

## 问题 10: 复杂 - 工程亮点分析

**难度**: 复杂

**问题**: 分析这个项目的工程亮点和技术创新

**期望索引的文件**:
- README.md
- cuezero/mcts/search.py
- cuezero/models/dual_network.py
- cuezero/env/billiards_env.py
- scripts/cli_game.py

**期望索引的关键函数/类**:
- MCTS
- DualNetwork
- BilliardsEnv
- simulate_with_timeout

**标准答案**:
CueZero 项目的工程亮点和技术创新包括：

### 1. 紧凑模型架构应对复杂任务
**挑战**: 台球本质上比国际象棋/围棋等传统棋盘游戏更复杂，具有连续物理、随机结果和高维状态/动作空间。

**解决方案**: 精心设计的轻量级网络：
- 共享特征提取器：2层FC + GRU用于时空融合
- 策略头：2层FC用于5D动作预测
- 价值头：2层FC用于胜率估计
- 总参数：仅约160K（极其紧凑！）

**为什么有效**: 智能架构设计优先考虑基本特征（球位置、速度、球袋状态），同时避免不必要的复杂性。模型虽小但性能强劲。

### 2. 连续动作空间的专用 MCTS
**挑战**: 5D连续动作空间，即使粗略离散化也有约243,000+种潜在组合。

**解决方案**:
- **Ghost Ball 启发式**: 几何生成约30个高质量候选
- **策略引导剪枝**: 保留前2/3候选（66%缩减）
- **结果**: 54倍更小的搜索空间（4,500次评估 vs 243,000组合）

### 3. 双 MCTS 模式适应不同场景
| 特性 | MCTS-Full | MCTS-Fast |
|------|-----------|-----------|
| 模拟次数 | 150 | 30 |
| 最大深度 | 4 | 2 |
| 超时 | 15s | 3s |
| 决策时间 | ~3分钟 | ~1秒 |
| 胜率 vs Basic | 95% | 90% |
| 用途 | 强性能 | 实时、Web UI |

**MCTS-Fast**: 180倍速度提升，仅5%胜率 trade-off。

### 4. 高效训练 Pipeline
- **预训练**: ~200 epochs 在 BasicAgent 数据上（学习基本击球）
- **自我对弈训练**: ~600 epochs 使用 MCTS 引导数据生成
- **补充训练**: ~200 epochs 专门化精细调整
- **总计**: ~1000 epochs 达到完整性能

**关键优化**: 启发式搜索相比纯 RL 加速3-5倍。

### 5. 混合评估策略
结合神经网络预测和物理模拟：
- **早期深度**: 更多模拟（准确但慢）
- **晚期深度**: 更多网络（快但略不准确）
- **动态权重**: 基于搜索深度平滑过渡

### 6. 完整的工程化实现
- **多种接口**: CLI、Web UI、REST API
- **灵活配置**: YAML配置文件
- **完整文档**: 安装、训练、性能、技术深度文档
- **多种 Agent**: Human、MCTS-Full/Fast、Policy、Basic、BasicPro、Random

### 7. 竞争性性能
| 对手 | 胜率 | 备注 |
|------|------|------|
| BasicAgent | 95% | 贝叶斯优化基，初学者水平 |
| BasicAgentPro | 80% | 高级物理基，约85%胜率 vs BasicAgent，经验玩家水平 |

**测试条件**: 120局，4×轮换（先后手×球类型分布）

### 8. 物理模拟集成
- 集成 pooltool 物理引擎
- simulate_with_timeout 带超时保护
- 精确的台球运动模拟

**参考文件**:
- README.md
- cuezero/mcts/search.py
- cuezero/models/dual_network.py
- cuezero/env/billiards_env.py
- scripts/cli_game.py
