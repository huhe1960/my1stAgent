"""
主程序入口
演示Agent的基本使用
"""
import json
from llm_client import LLMClient
from agent import Agent


def load_config(config_path: str = "config.json") -> dict:
    """加载配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """主函数"""
    print("=" * 50)
    print("🤖 简单智能体 Agent 启动")
    print("=" * 50)
    
    # 加载配置
    try:
        config = load_config()
        api_config = config["api"]
        agent_config = config["agent"]
    except FileNotFoundError:
        print("❌ 错误: 找不到 config.json 文件")
        return
    except Exception as e:
        print(f"❌ 错误: 配置文件加载失败 - {e}")
        return
    
    # 初始化LLM客户端
    print(f"\n📡 连接到API: {api_config['base_url']}")
    print(f"📦 使用模型: {api_config['model']}")
    
    try:
        llm_client = LLMClient(
            base_url=api_config["base_url"],
            api_key=api_config["api_key"],
            model=api_config["model"],
            timeout=api_config.get("timeout", 30)
        )
    except Exception as e:
        print(f"❌ LLM客户端初始化失败: {e}")
        return
    
    # 初始化Agent
    agent = Agent(
        llm_client=llm_client,
        max_iterations=agent_config.get("max_iterations", 10)
    )
    
    print("\n✅ Agent初始化成功！")
    print("\n💡 提示: 输入 'quit' 或 'exit' 退出")
    print("-" * 50)
    
    # 对话循环
    while True:
        try:
            user_input = input("\n👤 您: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "退出"]:
                print("\n👋 再见！")
                break
            
            # Agent处理并回复
            print("\n🤖 Agent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")


if __name__ == "__main__":
    main()

