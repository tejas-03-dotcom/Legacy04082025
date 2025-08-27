import asyncio
from playwright.async_api import async_playwright

USERNAME = "test_ciqmi@spglobal.com"
PASSWORD = "Monsoon@123"
URL = "https://www.capitaliq.com"


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
        try:
            # Try for 3 seconds to find any known cookie accept button
            await page.wait_for_selector("text='Accept All Cookies'", timeout=3000)
            # If found, click it
            accept_btn = page.locator("text='Accept All Cookies'")

            if await accept_btn.is_visible():
                await accept_btn.click()
                print("✅ 'Accept All Cookies' clicked.")
            else:
                print("⚠️ Cookie button not visible.")
        except:
            # No cookie popup appeared — safe to continue
            print("ℹ️ No cookie popup appeared. Continuing.")

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
        await page.fill("#float_createEditPanel__binderName", "UploadDocumentBinder11")
        await page.click("#float_createEditPanel__BinderSaveCancel__saveBtn")
        await page.wait_for_timeout(5000)
        binder_locator = page.locator("#folderTreeScroller > div > div:nth-child(2)")

        """if await binder_locator.is_visible():
            text = await binder_locator.inner_text()
            if "UploadDocument Binder" in text:
                print("✅ 'UploadDocument Binder' found in the element.")
            else:
                print("❌ 'UploadDocument Binder' not found in the element.")
        else:
            print("❌ Element not visible.")"""
        # Step 6: Upload a document
        await page.click("#layout_uploadLink")
        await page.wait_for_timeout(10000)
        await page.wait_for_selector("#floataddDocumentModal_ctl00 > tbody > tr > td:nth-child(2)")
        await page.wait_for_timeout(5000)


        #close the browser
        await browser.close()

asyncio.run(run())
