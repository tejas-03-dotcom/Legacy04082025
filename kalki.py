import asyncio
import os
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
import xlwings as xw


async def manage_download(page, button_selector, download_dir):
    try:
        # Ensure download folder exists
        os.makedirs(download_dir, exist_ok=True)

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


async def generate_as_pwez_binder_all_document():
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
            "Excel": "#GenerateBinderLink3 > img",
            "Word": "#GenerateBinderLink2 > img",
            "PDF": "#GenerateBinderLink1 > img",
            "ZIP": "#GenerateBinderLink4 > img",
        }
        #just for testing purposes
        download_dir = r"D:\Legacy04082025\downloads"
        results = {}
        for doc_type, selector in buttons.items():
            results[doc_type] = await manage_download(page, selector, download_dir)

        await browser.close()
        return results

    @xw.func
    def run_capitaliq_download():
        """Runs CapitalIQ download and returns file paths to Excel"""
        results = asyncio.run(generate_as_pwez_binder_all_document())
        return str(results)
""" original code
        for doc_type, selector in buttons.items():
            print(f"\n⬇️ Trying to download {doc_type}...")
            await manage_download(page, selector, r"D:\Legacy04082025\downloads")
"""


async def main():
    await generate_as_pwez_binder_all_document()

if __name__ == "__main__":
    asyncio.run(main())