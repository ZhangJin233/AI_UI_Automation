# Optional: Disable telemetry
# os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Optional: Set the OLLAMA host to a remote server
# os.environ.get("OLLAMA_HOST")

import asyncio
import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama

from browser_use import Agent, BrowserSession
from browser_use.agent.views import AgentHistoryList

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
url = os.environ.get("URL")
domain = os.environ.get("DOMAIN")
customer = os.environ.get("CUSTOMER")

sensitive_data = {
    "x_user": f"{username}",
    "x_password": f"{password}",
    "x_url": f"{url}",
    "x_customer": f"{customer}",
}

task = """
        1. 打开 {{x_url}} 并等待加载完成
        2. 找到Sign In to Pulse下面的输入框输入私人访问用户名 {{x_user}}
        3. 点击"Next"
        4. 在密码输入框输入私人访问密码 {{x_password}}
        5. 点击"Sign in"
        6. 等待页面加载完成
        7. 在顶部导航栏的右侧,找DPI
        8. 在DPI文字旁边有带灰色下拉箭头,点击灰色下拉箭头输入{{x_customer}} 并按下回车
        9. 等待页面加载完成并截图
        10. 保存当前customer的cookie到txt文件
        """

browser_session = BrowserSession(allowed_domains=[f"{domain}"])


async def run_search() -> AgentHistoryList:
    agent = Agent(
        task=task,
        llm=ChatOllama(
            # model="gemma3:latest",  # You can change this to your preferred model
            model="qwen3:latest",
            num_ctx=32000,
        ),
        sensitive_data=sensitive_data,
        browser_session=browser_session,
    )

    result = await agent.run()
    return result


async def main():
    result = await run_search()
    print("\n\n", result)


if __name__ == "__main__":
    asyncio.run(main())
