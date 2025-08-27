import sys
import asyncio
import warnings
from playwright.async_api import async_playwright
#wwill think about this import later

# 🚫 Suppress "closed pipe" ResourceWarnings from asyncio
warnings.filterwarnings("ignore", category=ResourceWarning)

# 🛠️ Fix for Windows event loop (to prevent transport issues)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def run_with_login(login_func, main_logic_func):
    """
    Generic runner for scripts using login and a main page logic function.

    Parameters:
    - login_func: a coroutine returning (playwright, browser, page)
    - main_logic_func: a coroutine accepting (page) to execute test steps
    """
    async with async_playwright() as p:
        playwright, browser, page = await login_func()

        try:
            await main_logic_func(page)
        finally:
            await browser.close()
