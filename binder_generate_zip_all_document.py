import asyncio
import os
from playwright.async_api import async_playwright

#from Binder.binder_generate_pdf_all_document import download_report
from download_manager import manage_download
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def generate_as_zip_binder_all_document():
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)
        documentsAndReports="https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx"
        await page.goto(documentsAndReports)
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("#_pageHeader_PageHeaderLabel")
        print(" ✅redirected to Documents and Reports successfully")
        await page.wait_for_selector("#folderTreeScroller > div > div:nth-child(2) > div:nth-child(2)")
        binder= "#layout_folder_frb-90308440 > table > tbody > tr > td.fldrName"
        await page.click(binder)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder successfully")
        await page.click("#layout_folder_frb-90308440 > table > tbody > tr > td.fldrMenu")
        await page.wait_for_timeout(5000)

        save_path = await manage_download(
            page,
            button_selector="#rc_dlZip",   # 🔹 Replace with actual selector
            download_path="D:\Legacy04082025\downloads",             # Folder where file should be saved
            file_name="BinderReport123.zip"           # Fallback name if CIQ doesn't send one
        )

        if save_path:
            print("🎉 Download complete:", save_path)
        else:
            print("❌ Download failed.")
    await browser.close()

asyncio.run(generate_as_zip_binder_all_document())
