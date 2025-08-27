import asyncio
import os
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def manage_download(page, button_selector, download_dir):
    try:
        async with page.expect_event("popup") as popup_info:
            await page.click(button_selector)
        try:
            popup = await popup_info.value
            print("📂 Popup detected for download")

            async with popup.expect_download(timeout=60000) as download_info:
                download = await download_info.value
        except Exception:
            # fallback → maybe no popup, try main page download
            async with page.expect_download(timeout=60000) as download_info:
                download = await download_info.value

        # Extract server-provided filename
        suggested_name = download.suggested_filename
        save_path = os.path.join(download_dir, suggested_name)

        await download.save_as(save_path)
        print(f"🎉 Download complete: {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Download failed for selector {button_selector}: {e}")
        return None


async def generate_as_excel_binder_all_document():
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)

        await page.goto("https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx")
        await page.wait_for_selector("#_pageHeader_PageHeaderLabel")
        print(" ✅ Redirected to Documents and Reports successfully")

        binder = "#layout_folder_frb-90308440 > table > tbody > tr > td.fldrName"
        await page.click(binder)
        await page.wait_for_timeout(3000)
        print("✅ Clicked on binder successfully")

        # Different download buttons
        buttons = {
            "PDF": "#layout_optionsButton_generatePDFLink_txt_0"
        }

        for doc_type, selector in buttons.items():
            print(f"\n⬇️ Trying to download {doc_type}...")

            try:
                # Click the menu button to open dropdown
                await page.click("#layout_optionsButton_MenuButton", timeout=10000)

                # Wait for the specific download option to appear
                await page.wait_for_selector(selector, state="visible", timeout=15000)

                # Attempt download with retries
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        await manage_download(page, selector, r"D:\Legacy04082025\downloads")
                        break
                    except PlaywrightTimeoutError:
                        if attempt < max_retries - 1:
                            print(f"⌛ Retrying {doc_type} download ({attempt + 1}/{max_retries})...")
                            await page.reload()
                            await page.wait_for_selector(binder)
                            await page.click(binder)
                            await page.wait_for_timeout(2000)
                            await page.click("#layout_optionsButton_MenuButton")
                        else:
                            print(f"❌ Max retries exceeded for {doc_type}")
                            raise
            except Exception as e:
                print(f"⚠️ Error processing {doc_type}: {e}")
                # Capture screenshot for debugging
                await page.screenshot(path=f"error_{doc_type.lower()}.png")
                print(f"📸 Saved screenshot as error_{doc_type.lower()}.png")

        await browser.close()


asyncio.run(generate_as_excel_binder_all_document())