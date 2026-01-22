"""
核心Agent类
实现智能体的对话循环和工具调用逻辑
"""
import json
from typing import List, Dict, Optional
from llm_client import LLMClient
from tools import TOOLS, execute_tool


class Agent:
    """智能体核心类"""
    
    def __init__(self, llm_client: LLMClient, max_iterations: int = 10):
        """
        初始化Agent
        
        Args:
            llm_client: LLM客户端实例
            max_iterations: 最大迭代次数（防止无限循环）
        """
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        self.conversation_history: List[Dict] = []
        
        # 系统提示词
        self.system_prompt = """你是一个有用的AI助手。你可以使用工具来帮助用户解决问题。
当需要使用工具时，请调用相应的工具函数。
如果工具执行结果已经足够回答问题，请直接给出答案。"""
    
    def add_message(self, role: str, content: str, tool_calls: Optional[List] = None):
        """
        添加消息到对话历史
        
        Args:
            role: 角色（user/assistant/tool）
            content: 消息内容
            tool_calls: 工具调用列表（可选）
        """
        message = {"role": role, "content": content}
        if tool_calls:
            message["tool_calls"] = tool_calls
        self.conversation_history.append(message)
    
    def process_tool_calls(self, tool_calls: List[Dict]) -> List[Dict]:
        """
        处理工具调用
        
        Args:
            tool_calls: 工具调用列表
        
        Returns:
            工具执行结果消息列表
        """
        tool_messages = []
        
        for tool_call in tool_calls:
            tool_id = tool_call.get("id")
            function = tool_call.get("function", {})
            tool_name = function.get("name")
            arguments_str = function.get("arguments", "{}")
            
            # 解析参数
            try:
                arguments = json.loads(arguments_str)
            except json.JSONDecodeError:
                arguments = {}
            
            # 执行工具
            print(f"  🔧 调用工具: {tool_name}({arguments})")
            tool_result = execute_tool(tool_name, arguments)
            print(f"  ✅ 工具结果: {tool_result}")
            
            # 添加工具结果到消息历史
            tool_message = {
                "role": "tool",
                "content": tool_result,
                "tool_call_id": tool_id
            }
            tool_messages.append(tool_message)
            self.conversation_history.append(tool_message)
        
        return tool_messages
    
    def chat(self, user_input: str) -> str:
        """
        处理用户输入并返回回复
        
        Args:
            user_input: 用户输入
        
        Returns:
            Agent的回复
        """
        # 添加用户消息
        self.add_message("user", user_input)
        
        # 迭代执行，直到获得最终答案
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n[迭代 {iteration}]")
            
            # 构建消息列表（包含系统提示和完整对话历史）
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            
            # 调用LLM（带工具支持）
            response = self.llm_client.chat_with_tools(messages, TOOLS)
            
            # 提取响应
            assistant_message = response["choices"][0]["message"]
            content = assistant_message.get("content", "")
            tool_calls = assistant_message.get("tool_calls")
            
            # 添加助手消息到历史
            self.add_message("assistant", content, tool_calls)
            
            # 如果有工具调用，执行工具
            if tool_calls:
                tool_messages = self.process_tool_calls(tool_calls)
                # 工具消息已经通过process_tool_calls添加到conversation_history
                # 继续循环，让LLM基于工具结果生成回复
                continue
            else:
                # 没有工具调用，返回最终答案
                return content
        
        return "达到最大迭代次数，请简化您的问题。"

