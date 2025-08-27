import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def manage_download(page, button_selector: str, download_path: str = "downloads", custom_name: str = None):
    """
    Handles file download triggered by clicking a selector.
    Works even if a new popup tab opens (BinderWaitingIndicator.aspx).
    Auto-detects file type (PDF, Excel, Word, etc.) and applies correct extension.
    """

    os.makedirs(download_path, exist_ok=True)

    try:
        # Expect popup window when clicking download
        async with page.context.expect_page() as popup_info:
            await page.click(button_selector)

        popup = await popup_info.value
        await popup.wait_for_load_state("networkidle")

        # Wait for actual download event inside popup
        async with popup.expect_download() as download_info:
            # In many cases popup triggers download automatically
            await popup.wait_for_timeout(3000)

        download = await download_info.value

        # Server-suggested filename (e.g. "ReportBinder.pdf" or "Export.xlsx")
        suggested_name = download.suggested_filename
        ext = Path(suggested_name).suffix  # extract .pdf, .xls, .xlsx, etc.

        # Use user-provided name + detected extension OR fallback to suggested
        if custom_name:
            filename = f"{Path(custom_name).stem}{ext}"
        else:
            filename = suggested_name

        save_path = os.path.join(download_path, filename)
        await download.save_as(save_path)

        print(f"✅ Download saved: {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Download failed for selector {button_selector}: {e}")
        return None


async def generate_as_pdf_binder_all_document():
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        documentsAndReports = "https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx"
        await page.goto(documentsAndReports)
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("#_pageHeader_PageHeaderLabel")
        print(" ✅ redirected to Documents and Reports successfully")

        await page.wait_for_selector("#folderTreeScroller > div > div:nth-child(2) > div:nth-child(2)")
        binder = "#layout_folder_frb-90308440 > table > tbody > tr > td.fldrName"
        await page.click(binder)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder successfully")

        # Example usage: works for PDF, Excel, Word, etc.
        save_path = await manage_download(
            page,
            button_selector="#GenerateBinderLink1 > img",  # Example: download button
            download_path=r"D:\Legacy04082025\downloads",
            custom_name="Ganesha_word"   # Extension will be auto-added
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
        else:
            print("❌ Download failed.")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(generate_as_pdf_binder_all_document())
