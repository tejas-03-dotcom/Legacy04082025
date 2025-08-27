import asyncio
from playwright.async_api import async_playwright
#no longer needed
USERNAME = "test_ciqmi@spglobal.com"
PASSWORD = "Monsoon@123"
URL = "https://www.capitaliq.com"


async def handle_cookies(page):
    """Handle cookie consent dialogs with multiple fallback strategies"""
    cookie_selectors = [
        "text='Accept All Cookies'",
        "text='Accept All'",
        "button:has-text('Accept')",
        "#cookie-accept",
        ".cookie-accept",
        "//button[contains(., 'Accept')]"
    ]

    for selector in cookie_selectors:
        try:
            await page.wait_for_selector(selector, timeout=3000)
            accept_btn = page.locator(selector).first
            if await accept_btn.is_visible():
                await accept_btn.click()
                print(f"✅ Clicked cookie accept using selector: {selector}")
                await page.wait_for_timeout(1000)  # Let the dialog disappear
                return True
        except:
            continue

    print("ℹ️ No cookie popup appeared or couldn't find accept button")
    return False


async def upload_file(page, file_path):
    """Handle file upload with robust waiting and error handling"""
    try:
        async with page.expect_file_chooser(timeout=20000) as fc_info:
            await page.click("#layout_uploadLink")
        file_chooser = await fc_info.value
        await file_chooser.set_files(file_path)
        print("✅ File selected for upload")

        # Wait for upload to complete
        await page.wait_for_selector(".upload-complete, #upload-success", timeout=60000)
        print("✅ File upload completed successfully")
        return True
    except Exception as e:
        print(f"❌ File upload failed: {str(e)}")
        await page.screenshot(path="upload_error.png")
        return False


async def run():
    async with async_playwright() as p:
        # Use persistent context to maintain cookies between sessions
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./user_data",
            headless=False,
            slow_mo=50,
            args=["--start-maximized"]
        )
        page = await browser.new_page()

        try:
            # Step 1: Login
            await page.goto(URL, wait_until="load")
            print("ℹ️ Page loaded")

            # Handle cookies before login if they appear
            await handle_cookies(page)

            await page.wait_for_selector('#input28', timeout=15000)
            await page.fill('#input28', USERNAME)
            await page.click('#form20 input[type="submit"]')
            print("ℹ️ Username submitted")

            await page.wait_for_selector('#input60', timeout=15000)
            await page.fill('#input60', PASSWORD)
            await page.click('#form52 input[type="submit"]')
            print("ℹ️ Password submitted")

            # Step 2: Confirm login
            await page.wait_for_selector("#ctl05_ciqImage", timeout=20000)
            print("✅ Login successful.")

            # Check for cookies again after login
            await handle_cookies(page)

            # Step 3: Hover and navigate to Binder
            await page.hover("#tmbButton1")
            await page.wait_for_timeout(2000)  # Reduced from 5000
            print("✅ Hovered over Binder button.")

            # More reliable navigation using text content
            await page.click("text='Binder' >> visible=true")
            await page.wait_for_load_state("networkidle")
            print("✅ Navigated to Binder page.")

            # Step 4: Create a new Binder
            await page.click("#layout__newFolderButton_MenuButton")
            await page.wait_for_timeout(1000)  # Reduced from 2000
            await page.click("#layout__newFolderButton_newBinderLink_0")
            await page.wait_for_timeout(1000)  # Reduced from 2000

            # Step 5: Fill in Binder details
            await page.wait_for_selector("#float_createEditPanel", timeout=10000)
            await page.fill("#float_createEditPanel__binderName", "UploadDocumentBinder11")
            await page.click("#float_createEditPanel__BinderSaveCancel__saveBtn")
            await page.wait_for_selector("text='UploadDocumentBinder11'", timeout=10000)
            print("✅ Binder created successfully")

            # Step 6: Upload a document
            file_path = "path/to/your/document.pdf"  # Update this path
            await upload_file(page, file_path)

        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            await page.screenshot(path="error.png")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())