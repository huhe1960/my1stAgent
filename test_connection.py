"""
快速测试脚本
用于验证本地API连接是否正常
"""
import json
import requests
from llm_client import LLMClient


def test_api_connection(config_path: str = "config.json"):
    """测试API连接"""
    print("=" * 50)
    print("🔍 测试本地API连接")
    print("=" * 50)
    
    # 加载配置
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        api_config = config["api"]
    except FileNotFoundError:
        print("❌ 错误: 找不到 config.json 文件")
        return False
    except Exception as e:
        print(f"❌ 错误: 配置文件加载失败 - {e}")
        return False
    
    base_url = api_config["base_url"]
    api_key = api_config["api_key"]
    model = api_config["model"]
    
    print(f"\n📡 API地址: {base_url}")
    print(f"📦 模型: {model}")
    print(f"🔑 API Key: {api_key[:10]}..." if len(api_key) > 10 else f"🔑 API Key: {api_key}")
    
    # 测试简单请求
    print("\n🧪 发送测试请求...")
    try:
        client = LLMClient(base_url, api_key, model)
        
        test_messages = [
            {"role": "user", "content": "你好，请回复'连接成功'"}
        ]
        
        response = client.chat(test_messages)
        content = client.extract_content(response)
        
        print(f"✅ 连接成功！")
        print(f"📝 模型回复: {content}")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 无法连接到API服务器")
        print("💡 请确保:")
        print("   1. 本地大模型API服务正在运行")
        print("   2. API地址配置正确")
        print("   3. 端口未被占用")
        return False
    except requests.exceptions.Timeout:
        print("❌ 连接超时: API服务器响应时间过长")
        return False
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_api_connection()
    if success:
        print("\n✅ 测试通过！可以运行 python main.py 启动Agent")
    else:
        print("\n❌ 测试失败！请检查配置和API服务")

