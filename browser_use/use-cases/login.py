import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserProfile, BrowserSession
from dotenv import load_dotenv


load_dotenv()

# 使用最简化的格式提供敏感数据
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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", google_api_key=os.environ.get("GEMINI_API_KEY")
)

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
browser_profile = BrowserProfile(
    # NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
    # executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    user_data_dir="~/.config/browseruse/profiles/default",  # 使用新的配置文件路径
    headless=False,
)
browser_session = BrowserSession(
    browser_profile=browser_profile, allowed_domains=[f"{domain}"]
)

agent = Agent(
    task=task,
    llm=llm,
    use_vision=True,  # 启用视觉能力
    sensitive_data=sensitive_data,
    browser_session=browser_session,
    max_actions_per_step=3,  # 限制每步操作数量
    # save_conversation_path="logs/conversation",
)


async def main():

    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
