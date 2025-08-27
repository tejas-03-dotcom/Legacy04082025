import asyncio
from playwright.async_api import async_playwright

USERNAME = "test_ciqmi@spglobal.com"
PASSWORD = "Monsoon@123"
URL = "https://www.capitaliq.com"


async def handle_cookie_popup(page):
    try:
        # Adjust text selector if button text is different
        await page.wait_for_selector("text='Accept All Cookies'", timeout=3000)
        accept_btn = page.locator("text='Accept All'")
        if await accept_btn.is_visible():
            await accept_btn.click()
            print("✅ 'Accept All Cookies' clicked.")
        else:
            print("⚠️ Cookie button not visible.")
    except:
        print("ℹ️ No cookie popup appeared.")


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()

        # Step 1: Login
        await page.goto(URL)
        await page.wait_for_selector('#input28', timeout=15000)
        await page.fill('#input28', USERNAME)
        await page.click('#form20 input[type="submit"]')

        await page.wait_for_selector('#input60', timeout=15000)
        await page.fill('#input60', PASSWORD)
        await page.click('#form52 input[type="submit"]')

        # Step 2: Confirm login
        await page.wait_for_selector("#ctl05_ciqImage", timeout=20000)
        print("✅ Login successful.")

        # Handle cookie popup after login
        await handle_cookie_popup(page)

        # Step 3: Hover and navigate to Binder
        await page.hover("#tmbButton1")
        await page.wait_for_timeout(5000)
        print("✅ Hovered over Binder button.")
        await page.click("#__tmbFlyout1 > table > tbody > tr > td:nth-child(1) > ul > li:nth-child(3) > a:nth-child(2)")
        await page.wait_for_load_state()
        print("✅ Navigated to Binder page.")
        await page.wait_for_timeout(10000)

        # Step 4: Create a new Binder
        await page.click("#layout__newFolderButton_MenuButton")
        await page.wait_for_timeout(2000)
        await page.click("#layout__newFolderButton_newBinderLink_0")
        await page.wait_for_timeout(2000)

        # Step 5: Fill in Binder details
        await page.wait_for_selector("#float_createEditPanel", timeout=10000)
        await page.fill("#float_createEditPanel__binderName", "BinderRenny1234")
        await page.click("#float_createEditPanel__BinderSaveCancel__saveBtn")
        print("✅ Binder created successfully.")
        await page.wait_for_timeout(5000)
        # ✅ Handle cookie popup again (it may appear now)
        await handle_cookie_popup(page)

        # Close browser
        await browser.close()


asyncio.run(run())
