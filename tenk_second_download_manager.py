# download_manager.py
import os
from playwright.async_api import Page, Download

async def manage_download(page: Page, button_selectors: list[str], download_path: str = "downloads", file_name: str = None) -> str | None:
    """
    Handles file downloads for multiple document types.
    - Tries each selector until one succeeds
    - Waits for the download event
    - Saves with server-provided filename unless file_name override is given
    """

    os.makedirs(download_path, exist_ok=True)

    for selector in button_selectors:
        try:
            # Trigger download
            async with page.expect_download() as download_info:
                await page.click(selector, timeout=10000)

            download: Download = await download_info.value

            # Get filename from server or use provided override
            suggested_name = download.suggested_filename
            filename = file_name or suggested_name

            save_path = os.path.join(download_path, filename)
            await download.save_as(save_path)

            print(f"✅ Download successful via {selector} → {save_path}")
            return save_path

        except Exception as e:
            print(f"⚠️ Selector {selector} failed: {e}")
            continue

    print("❌ All selectors failed to download.")
    return None
