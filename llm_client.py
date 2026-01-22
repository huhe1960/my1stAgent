"""
LLM API客户端
支持OpenAI兼容的API格式（DeepSeek、Qwen等）
"""
import json
import requests
from typing import Dict, List, Optional


class LLMClient:
    """大语言模型API客户端"""
    
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 30):
        """
        初始化LLM客户端
        
        Args:
            base_url: API基础URL，如 http://localhost:8000/v1
            api_key: API密钥
            model: 模型名称
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.chat_endpoint = f"{self.base_url}/chat/completions"
    
    def chat(self, messages: List[Dict], temperature: float = 0.7) -> Dict:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表，格式: [{"role": "user", "content": "..."}]
            temperature: 温度参数，控制随机性
        
        Returns:
            API响应字典
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.chat_endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def chat_with_tools(self, messages: List[Dict], tools: List[Dict], 
                       temperature: float = 0.7) -> Dict:
        """
        发送带工具调用的聊天请求
        
        Args:
            messages: 消息列表
            tools: 工具定义列表
            temperature: 温度参数
        
        Returns:
            API响应字典，可能包含tool_calls
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.chat_endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def extract_content(self, response: Dict) -> str:
        """
        从API响应中提取文本内容
        
        Args:
            response: API响应字典
        
        Returns:
            消息内容
        """
        if "choices" in response and len(response["choices"]) > 0:
            choice = response["choices"][0]
            message = choice.get("message", {})
            return message.get("content", "")
        return ""
    
    def extract_tool_calls(self, response: Dict) -> List[Dict]:
        """
        从API响应中提取工具调用
        
        Args:
            response: API响应字典
        
        Returns:
            工具调用列表
        """
        if "choices" in response and len(response["choices"]) > 0:
            choice = response["choices"][0]
            message = choice.get("message", {})
            tool_calls = message.get("tool_calls", [])
            return tool_calls
        return []

