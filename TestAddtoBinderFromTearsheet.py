import asyncio
from TestLoginLegacy import login
from playwright.async_api import async_playwright
from test_handleCookie import handle_cookie_popup



async def add_to_binder_from_tearsheet():
    async with async_playwright() as p:
        # 🧼 Use login() — it should handle browser launch
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        # Step 1: Navigate to a specific element
        # await page.goto("https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx")
        await page.wait_for_selector("#_pageHeader > div:nth-child(1) > span.cPageTitle_subHeader", timeout=5000)
        print("✅ Dashboard page loaded.")
        # Step 2: Click on the search box
        await page.click("#SearchTopBar")
        await page.wait_for_timeout(2000)
        # Step 3: Type the entity name
        await page.fill("#SearchTopBar", "Bank of America Corporation")
        await page.wait_for_timeout(3000)
        # Step 4: Press Enter to search
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)
        # Step 5: Click on the first result
        await page.click("#SR0 > td.NameCell > div > span > a")
        # Wait for the entity page to load\
        print("✅ Navigated to the entity page.")
        # Wait for tearsheet section (or another known element) instead of networkidle
        await page.wait_for_selector("#ll_7_48_406", timeout=15000)
        print("✅ Entity page loaded.")
        # updated line
        print("✅ Entity page loaded.")
        # Step 6: check if the page is a tearsheet
        tearsheet_locator = page.locator("#ll_7_48_406")
        if await tearsheet_locator.is_visible():
            print("✅ Tearsheets page is visible.")
        else:
            print("❌ Tearsheets page is not visible.")
            return
        # Step 7: Check if the 'Add to Binder' button is visible
        # add_to_binder_locator = page.locator("[title='Add word Report To Binder']")
        add_to_binder_locator = page.locator(xpath="//*[@id='CompanyHeaderInfo_ctl22']")
        if await add_to_binder_locator.is_visible():
            print("✅ 'Add to Binder' button is visible.")
            # Step 8: Click on the 'Add to Binder' button
            await add_to_binder_locator.click()
            await page.wait_for_timeout(5000)
            print("✅ 'Add to Binder' button clicked.")
        else:
            print("❌ 'Add to Binder' button is not visible.")
            return
        await page.click("#CompanyHeaderInfo_ctl27 > span")
        # Step 9: click on the 'Add to Binder' option
        # await page.click("#CompanyHeaderInfo_ctl22")
        await page.wait_for_timeout(2000)
        await browser.close()
# Run the coroutine
asyncio.run(add_to_binder_from_tearsheet())
