# import sys
import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
async def delete_binder():
    async with async_playwright() as p:
        """playwright, browser, page= await login()"""
    """browser = await p.chromium.launch(headless=False, slow_mo=50)
    page = await browser.new_page()"""
    playwright, browser, page = await login()
    await page.goto("https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx")
    await page.wait_for_load_state()

    # await page.click()
    binder_list = "#folderTreeScroller > div"
    await page.wait_for_selector(binder_list, timeout=5000)
    print("✅ Binder list loaded.")
    binder= "#layout_folder_frb-90308440"
    await page.wait_for_selector(binder, timeout=5000)
    print("✅ Binder loaded.")
    await page.click(binder)
    await page.wait_for_timeout(5000)
    # Step 4: Click on the option
    await page.click("#layout_folder_frb-90308440 > table > tbody > tr > td.fldrMenu")
    await page.wait_for_timeout(2000)
    # Step 5: Click on the 'Delete' option
    delete = "#rc_delete"
    await page.click(delete)
    await page.wait_for_timeout(2000)

    # Step 6: Confirm deletion






    # close browser
    await browser.close()


asyncio.run(delete_binder())


