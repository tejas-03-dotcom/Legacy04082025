import sys
import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login


async def way_to_binder_documentsAndReports_byUrl():
    async with async_playwright() as p:
        playwright, browser, page = await login()
    binder_url = "https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx"
    await page.goto(binder_url, timeout=60000)
    await page.wait_for_load_state()
    print("✅ Navigated to Documents and Reports page.")
    await page.wait_for_timeout(5000)

    #close browser
    await browser.close()


asyncio.run(way_to_binder_documentsAndReports_byUrl())
