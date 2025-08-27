import asyncio
from TestLoginLegacy import login
from playwright.async_api import async_playwright

async def handle_cookie_popup(page):
    try:
        # Adjust text selector if button text is different
        await page.wait_for_selector("text='Accept All'", timeout=3000)
        accept_btn = page.locator("text='Accept All'")
        if await accept_btn.is_visible():
            await accept_btn.click()
            print("✅ 'Accept All Cookies' clicked.")
        else:
            print("⚠️ Cookie button not visible.")
    except:
        print("ℹ️ No cookie popup appeared.")

async def generate_QuickReport_from_tearsheet():
    async with async_playwright() as p:
        # 🧼 Use login() — it should handle browser launch
        playwright, browser, page = await login()
        #Step 1: Navigate to a specific element
        #await page.goto("https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx")
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
        #updated line
        print("✅ Entity page loaded.")
        # Step 6: check if the page is a tearsheet
        tearsheet_locator = page.locator("#ll_7_48_406")
        if await tearsheet_locator.is_visible():
            print("✅ Tearsheets page is visible.")
        else:
            print("❌ Tearsheets page is not visible.")
            return
        # Step 7: Check if the 'Quick Report' button is visible
        quickreport_locator = page.locator("#CompanyHeaderInfo_OnePagePDF_ReportImage > div > img")
        if await quickreport_locator.is_visible():
            print("✅ 'Quick Report' button is visible.")
            await handle_cookie_popup(page)
            await page.wait_for_timeout(2000)

            # Step 8: Click on the 'Quick Report' button
            await quickreport_locator.click()
            await page.wait_for_timeout(5000)
            print("✅ 'Quick Report' button clicked.")
            #Step 9: check if the Quick reprot pdf is downloaded.


            await page.wait_for_timeout(2000)
            await browser.close()
    # Run the coroutine
asyncio.run(generate_QuickReport_from_tearsheet())
