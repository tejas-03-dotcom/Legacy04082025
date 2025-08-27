import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login


async def generate_ten_k_from_tearsheet():
    async with async_playwright() as p:
        playwright, browser, page = await login()

        await page.wait_for_selector("#_pageHeader > div:nth-child(1) > span.cPageTitle_subHeader", timeout=5000)
        print("✅ Dashboard page loaded.")

        await page.click("#SearchTopBar")
        await page.wait_for_timeout(2000)

        await page.fill("#SearchTopBar", "Bank of America Corporation")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)

        await page.click("#SR0 > td.NameCell > div > span > a")
        print("✅ Navigated to the entity page.")

        await page.wait_for_selector("#ll_7_48_406", timeout=15000)
        print("✅ Entity page loaded.")

        tearsheet_locator = page.locator("#ll_7_48_406")
        if not await tearsheet_locator.is_visible():
            print("❌ Tearsheets page is not visible.")
            await browser.close()
            return

        toolbar = page.locator("#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar")
        await toolbar.wait_for(timeout=5000)

        if await toolbar.is_visible():
            print("✅ Toolbar is visible.")
        else:
            print("❌ Toolbar is not visible.")
            await browser.close()
            return

        ten_k_button_selector = "#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar > ul > li:nth-child(8) > a > div"
        ten_k_button = page.locator(ten_k_button_selector)
        await ten_k_button.wait_for(state="visible", timeout=5000)

        # Start waiting for the popup BEFORE clicking
        popup_promise = page.wait_for_event("popup")
        await ten_k_button.click()
        popup = await popup_promise  # Wait for the popup to actually open
        await popup.wait_for_load_state()
        print("✅ '10-K' button clicked and popup loaded.")

        # Example: take screenshot of popup page (optional)
        # await popup.screenshot(path="10k_popup.png")

        await browser.close()


asyncio.run(generate_ten_k_from_tearsheet())
