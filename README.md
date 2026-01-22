# 最简单的智能体 Agent 框架 The simplist agent

这是一个用于学习和理解智能体（Agent）基本架构的简单实现。

## 技术架构

```
┌─────────────────┐
│   Main Entry    │  ← 主程序入口
└────────┬────────┘
         │
┌────────▼────────┐
│  Agent Core     │  ← 核心Agent类，管理对话循环
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐  ┌──▼──────┐
│ LLM   │  │ Tools   │  ← 工具系统
│Client │  │ System  │
└───┬───┘  └─────────┘
    │
┌───▼───────────────┐
│  Local LLM API    │  ← 本地大模型API (DeepSeek/Qwen等)
│  (localhost:8000) │
└───────────────────┘
```

## 核心组件说明

### 1. LLM Client (`llm_client.py`)
- 负责与本地大模型API通信
- 支持标准的OpenAI兼容API格式
- 处理请求/响应和错误处理

### 2. Tool System (`tools.py`)
- 定义可用的工具（函数）
- 工具描述和参数schema
- 工具执行逻辑

### 3. Agent Core (`agent.py`)
- 核心对话循环
- 工具调用决策
- 多轮对话管理
- 迭代执行直到完成任务

## 部署步骤

### 1. 环境准备

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置本地API

编辑 `config.json`，设置你的本地API地址：

```json
{
  "api": {
    "base_url": "http://localhost:8000/v1",  // 你的本地API地址
    "api_key": "your-api-key-here",
    "model": "deepseek-chat"  // 或 "qwen" 等
  }
}
```

### 3. 测试连接（可选）

在运行Agent之前，可以先测试API连接：

```bash
python test_connection.py
```

### 4. 运行Agent

```bash
python main.py
```

## 工作原理

1. **用户输入** → Agent接收用户问题
2. **LLM推理** → 调用本地大模型分析问题
3. **工具决策** → LLM决定是否需要调用工具
4. **工具执行** → 如果需要，执行相应工具
5. **结果整合** → 将工具结果返回给LLM
6. **生成回答** → LLM基于工具结果生成最终答案
7. **循环迭代** → 重复2-6直到完成任务

## 示例对话

```
用户: 帮我计算 123 + 456
Agent: 正在计算...
       调用工具: calculator(123, 456)
       结果: 579
       回答: 123 + 456 = 579
```

## 扩展开发

- 添加新工具：在 `tools.py` 中定义新函数
- 修改Agent行为：编辑 `agent.py` 中的提示词
- 支持更多API：修改 `llm_client.py` 的请求格式
