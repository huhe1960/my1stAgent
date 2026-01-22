"""
工具系统
定义Agent可以使用的工具（函数）
"""
import json
from typing import Dict, Any, List


# 工具函数实现
def calculator(expression: str) -> str:
    """
    计算器工具：执行数学表达式
    
    Args:
        expression: 数学表达式，如 "123 + 456"
    
    Returns:
        计算结果字符串
    """
    try:
        # 安全地执行数学表达式
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"


def get_weather(city: str) -> str:
    """
    获取天气信息（模拟）
    
    Args:
        city: 城市名称
    
    Returns:
        天气信息字符串
    """
    # 这里是模拟数据，实际应该调用真实天气API
    weather_data = {
        "北京": "晴天，温度 25°C",
        "上海": "多云，温度 22°C",
        "深圳": "小雨，温度 28°C"
    }
    return weather_data.get(city, f"{city}的天气信息暂不可用")


# 工具定义（用于LLM的tool calling）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算，支持加减乘除等基本运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，如 '123 + 456' 或 '10 * 5'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如 '北京'、'上海'"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# 工具函数映射
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_weather": get_weather
}


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """
    执行工具函数
    
    Args:
        tool_name: 工具名称
        arguments: 工具参数
    
    Returns:
        工具执行结果
    """
    if tool_name not in TOOL_FUNCTIONS:
        return f"未知工具: {tool_name}"
    
    try:
        func = TOOL_FUNCTIONS[tool_name]
        result = func(**arguments)
        return result
    except Exception as e:
        return f"工具执行错误: {str(e)}"

