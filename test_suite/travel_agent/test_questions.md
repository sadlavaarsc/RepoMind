# 旅行agent 测试问题集

## 项目概述
这是一个基于大语言模型（LLM）的智能旅行助手 Agent 项目，实现了 ReAct（Reasoning + Acting）模式。

---

## 问题 1: 简单 - 项目介绍

**难度**: 简单

**问题**: 这个项目是做什么的？

**期望索引的文件**:
- agent.py
- prompt.py
- ai_client.py
- get_weather.py

**期望索引的关键函数/类**:
- OpenAICompatibleClient (ai_client.py)
- get_weather (get_weather.py)
- get_attraction (get_attraction.py)

**标准答案**:
这个项目是一个基于大语言模型（LLM）的**智能旅行助手 Agent**。它实现了 ReAct（Reasoning + Acting）模式，能够理解用户请求，自主规划步骤并调用工具来完成任务。

主要功能模块如下：
1. **提示词工程**: 在 prompt.py 中定义了 AGENT_SYSTEM_PROMPT，设定了助手身份、可用工具列表及严格的输出格式（Thought-Action）。
2. **模型调用**: 通过 ai_client.py 中的 OpenAICompatibleClient 类及其 generate 函数，对接大语言模型 API 生成回复。
3. **代理逻辑**: agent.py 是核心执行文件，负责维护对话历史，解析模型输出的行动指令，调用本地工具（如 get_weather.py 中的 get_weather 函数），并将执行结果（Observation）反馈给模型，形成闭环。
4. **工具能力**: 目前实现了查询天气（get_weather）和根据天气推荐景点（get_attraction）的功能。

**参考文件**:
- agent.py
- prompt.py
- ai_client.py
- get_weather.py

---

## 问题 2: 简单 - 工具函数列表

**难度**: 简单

**问题**: 有哪些可用的工具函数？

**期望索引的文件**:
- agent.py
- prompt.py
- get_weather.py
- get_attraction.py

**期望索引的关键函数/类**:
- get_weather (get_weather.py)
- get_attraction (get_attraction.py)
- available_tools (agent.py)

**标准答案**:
根据提供的代码上下文，系统中主要定义了以下两个可用的工具函数，它们在 agent.py 的 available_tools 字典中被注册，并在 prompt.py 的系统提示中进行了说明：

1. **get_weather**
   - **功能**: 查询指定城市的天气信息（目前支持上海、北京、广州、深圳、杭州等有限城市）。
   - **定义位置**: get_weather.py 文件中的 get_weather 函数。

2. **get_attraction**
   - **功能**: 根据城市和天气情况，使用 Tavily Search API 搜索并返回优化的旅游景点推荐。
   - **定义位置**: get_attraction.py 文件中的 get_attraction 函数。

**参考文件**:
- agent.py
- get_weather.py
- get_attraction.py
- prompt.py

---

## 问题 3: 简单 - 支持城市查询

**难度**: 简单

**问题**: get_weather 函数支持哪些城市？

**期望索引的文件**:
- get_weather.py

**期望索引的关键函数/类**:
- get_weather (get_weather.py)

**标准答案**:
get_weather 函数支持以下城市（中英文都支持）：

1. 上海 / Shanghai
2. 北京 / Beijing
3. 广州 / Guangzhou
4. 深圳 / Shenzhen
5. 杭州 / Hangzhou

这些城市的天气数据在 get_weather.py 的 weather_data 字典中硬编码定义。

**参考文件**:
- get_weather.py

---

## 问题 4: 简单 - 查找文件

**难度**: 简单

**问题**: 找到 prompt.py 文件

**期望索引的文件**:
- prompt.py

**期望索引的关键函数/类**:
- AGENT_SYSTEM_PROMPT (prompt.py)

**标准答案**:
prompt.py 文件位于项目根目录下，该文件定义了 AGENT_SYSTEM_PROMPT 系统提示词，用于指导旅行助手 Agent 的行为。

**参考文件**:
- prompt.py

---

## 问题 5: 中等 - 主循环工作原理

**难度**: 中等

**问题**: agent.py 中的主循环是如何工作的？

**期望索引的文件**:
- agent.py

**期望索引的关键函数/类**:
- 主循环 (agent.py 第34-92行)
- 可用工具字典 available_tools

**标准答案**:
agent.py 中的主循环采用 ReAct（Reasoning + Acting）模式，工作流程如下：

1. **初始化**: 配置 LLM 客户端（API_KEY、BASE_URL、MODEL_ID），设置用户请求，初始化对话历史。

2. **主循环**（最多运行5次）:
   - **构建 Prompt**: 将对话历史拼接为完整提示词
   - **调用 LLM**: 使用 OpenAICompatibleClient.generate() 获取模型输出
   - **解析输出**: 使用正则表达式提取 Thought 和 Action
   - **执行 Action**:
     - 如果是 "Finish[答案]" 格式，任务结束
     - 如果是工具调用，解析工具名和参数，从 available_tools 字典中查找并执行
   - **记录观察**: 将工具执行结果作为 Observation 加入对话历史

3. **关键特性**:
   - 使用正则表达式截断多余的 Thought-Action 对
   - 支持两种 Action 格式：function_name() 和 function_name(arg_name="arg_value")
   - 最大循环次数限制为5次

**参考文件**:
- agent.py

---

## 问题 6: 中等 - LLM 客户端配置

**难度**: 中等

**问题**: 如何配置 LLM 客户端？

**期望索引的文件**:
- agent.py
- ai_client.py

**期望索引的关键函数/类**:
- OpenAICompatibleClient (ai_client.py)
- API_KEY, BASE_URL, MODEL_ID (agent.py)

**标准答案**:
配置 LLM 客户端的步骤如下：

1. **环境准备**:
   - 从环境变量获取 QWEN_API_KEY
   - 设置 BASE_URL 为 "https://dashscope.aliyuncs.com/compatible-mode/v1"
   - 设置 MODEL_ID 为 "qwen3.5-plus"

2. **初始化客户端**:
   - 导入 OpenAICompatibleClient 类
   - 传入 model、api_key、base_url 三个参数
   - 创建客户端实例

3. **使用方法**:
   - 调用 generate() 方法，传入 prompt 和 system_prompt 参数
   - 获取模型返回的文本内容

**代码示例**:
```python
llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)
output = llm.generate(prompt, system_prompt=SYSTEM_PROMPT)
```

**参考文件**:
- agent.py
- ai_client.py

---

## 问题 7: 中等 - 输出解析逻辑

**难度**: 中等

**问题**: 模型输出的解析逻辑在哪里？

**期望索引的文件**:
- agent.py

**期望索引的关键函数/类**:
- Action 匹配正则 (agent.py)
- 工具调用解析逻辑

**标准答案**:
模型输出的解析逻辑在 agent.py 中，主要包含以下几个部分：

1. **截断多余输出**:
   - 使用正则表达式 `r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)'`
   - 只保留第一个 Thought-Action 对

2. **解析 Action**:
   - 使用正则表达式 `r"Action: (.*)"` 提取 Action 内容
   - 检测是否为 "Finish[答案]" 格式

3. **解析工具调用**:
   - 支持两种格式：
     - `function_name(arg_name="arg_value")`
     - `function_name()`
   - 使用 `re.findall(r'(\w+)="([^"]*)"', args_str)` 提取关键字参数

4. **错误处理**:
   - 如果无法解析 Action，返回错误提示
   - 如果工具名不存在，返回 "未定义的工具" 错误

**参考文件**:
- agent.py

---

## 问题 8: 复杂 - ReAct 工作流程

**难度**: 复杂

**问题**: 详细解释这个 ReAct 代理的完整工作流程

**期望索引的文件**:
- agent.py
- prompt.py
- ai_client.py
- get_weather.py

**期望索引的关键函数/类**:
- OpenAICompatibleClient.generate (ai_client.py)
- 主循环 (agent.py)
- AGENT_SYSTEM_PROMPT (prompt.py)
- get_weather (get_weather.py)

**标准答案**:
这个 ReAct（Reasoning + Acting）代理的完整工作流程如下：

### 1. 系统初始化阶段
- 加载环境变量 QWEN_API_KEY
- 初始化 OpenAICompatibleClient，配置 model、api_key、base_url
- 定义用户请求（如查询上海天气并推荐景点）
- 初始化对话历史列表 prompt_history

### 2. 提示词工程（prompt.py）
- AGENT_SYSTEM_PROMPT 定义：
  - 助手角色设定
  - 可用工具列表（get_weather、get_attraction）
  - 严格的输出格式要求：Thought: ... Action: ...
  - Action 的两种形式：工具调用 或 Finish[答案]

### 3. ReAct 循环（agent.py）
每次循环包含以下步骤：

**步骤 A: 构建提示词**
- 将 prompt_history 中所有消息用换行符拼接

**步骤 B: 调用 LLM 思考**
- 调用 llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
- 模型输出 Thought（思考过程）和 Action（行动计划）

**步骤 C: 解析并执行 Action**
- 使用正则提取 Action 内容
- 如果是 Finish[答案]，任务结束
- 如果是工具调用：
  - 解析工具名和参数
  - 从 available_tools 字典查找对应函数
  - 执行函数获取结果

**步骤 D: 反馈观察结果**
- 将工具执行结果包装为 "Observation: {result}"
- 加入 prompt_history
- 进入下一循环

### 4. 关键设计亮点
- 最大循环次数限制（5次）防止无限循环
- 输出截断确保每次只有一对 Thought-Action
- 灵活的工具调用格式支持
- 完整的对话历史维护

**参考文件**:
- agent.py
- prompt.py
- ai_client.py
- get_weather.py

---

## 问题 9: 复杂 - 添加新工具

**难度**: 复杂

**问题**: 如果我想添加一个新工具函数，需要修改哪些文件？

**期望索引的文件**:
- agent.py
- prompt.py

**期望索引的关键函数/类**:
- available_tools (agent.py)
- AGENT_SYSTEM_PROMPT (prompt.py)

**标准答案**:
添加一个新工具函数需要修改以下文件：

### 1. 创建工具函数文件
- 新建一个 Python 文件（如 get_hotel.py）
- 定义工具函数，接收所需参数
- 函数应返回字符串格式的结果

### 2. 修改 agent.py
- 导入新工具函数：`from get_hotel import get_hotel`
- 在 available_tools 字典中注册：`"get_hotel": get_hotel`

### 3. 修改 prompt.py
- 在 AGENT_SYSTEM_PROMPT 的 "可用工具" 部分添加新工具说明
- 格式：`- get_hotel(city: str): 查询指定城市的酒店推荐。`

### 完整示例
假设添加 get_hotel 工具：

**get_hotel.py**:
```python
def get_hotel(city: str) -> str:
    return f"{city}的推荐酒店：五星级酒店A，四星级酒店B"
```

**agent.py 修改**:
```python
from get_hotel import get_hotel
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
    "get_hotel": get_hotel,  # 新增
}
```

**prompt.py 修改**:
在可用工具列表中添加：
```
- `get_hotel(city: str)`: 查询指定城市的酒店推荐。
```

**参考文件**:
- agent.py
- prompt.py

---

## 问题 10: 复杂 - 局限性分析

**难度**: 复杂

**问题**: 分析这个代理的局限性和可能的改进方向

**期望索引的文件**:
- agent.py
- prompt.py
- get_weather.py
- ai_client.py

**期望索引的关键函数/类**:
- 主循环 (agent.py)
- get_weather (get_weather.py)
- OpenAICompatibleClient (ai_client.py)

**标准答案**:
### 当前代理的局限性

1. **天气数据限制**
   - get_weather 只支持5个城市，数据硬编码
   - 无实时天气API集成

2. **工具数量有限**
   - 只有2个工具函数
   - 无法处理复杂的旅行规划（如机票、酒店预订）

3. **循环次数限制**
   - 最多5次循环，复杂任务可能无法完成
   - 没有智能的终止判断

4. **错误处理简单**
   - 工具调用失败时只有简单错误提示
   - 无重试机制

5. **输出解析脆弱**
   - 依赖严格的正则匹配
   - 模型输出格式稍有变化就会解析失败

6. **无记忆持久化**
   - 对话历史只在内存中
   - 程序重启后丢失

### 可能的改进方向

1. **增强工具生态**
   - 集成真实天气 API（如 OpenWeatherMap）
   - 添加酒店、机票、景点详情查询工具
   - 支持多步旅行规划

2. **改进执行引擎**
   - 实现更智能的循环终止条件
   - 添加工具调用重试机制
   - 支持并行工具调用

3. **优化提示词工程**
   - 添加更详细的错误恢复指导
   - 支持更灵活的输出格式
   - 添加示例对话

4. **增强持久化**
   - 对话历史保存到文件/数据库
   - 支持会话恢复
   - 添加用户偏好记忆

5. **改进错误处理**
   - 更友好的错误提示
   - 自动纠错机制
   - 人工介入选项

**参考文件**:
- agent.py
- prompt.py
- get_weather.py
- ai_client.py
