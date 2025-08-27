import os
from playwright.async_api import Page


async def manage_download(
    page: Page,
    button_selector: str,
    download_path: str = "downloads",
    file_name: str = None,
    wait_time: int = 120000
) -> str | None:
    """
    Generic Download Manager for Playwright.
    - Clicks a button to trigger download (handles popup windows).
    - Saves file using server-provided filename (from headers) unless overridden.
    - Works for all file types (pdf, docx, xlsx, zip, etc.).

    Args:
        page (Page): Playwright page object.
        button_selector (str): CSS selector for the download button.
        download_path (str): Local folder where files will be saved.
        file_name (str): Optional custom filename.
        wait_time (int): Wait time (ms) after popup opens before expecting download.

    Returns:
        str | None: Full path of saved file or None if failed.
    """

    os.makedirs(download_path, exist_ok=True)

    try:
        # Handle case where download triggers a popup first
        async with page.context.expect_page() as popup_info:
            await page.click(button_selector)

        popup = await popup_info.value
        await popup.wait_for_load_state("networkidle")

        # Wait for file download event inside popup
        async with popup.expect_download() as download_info:
            await popup.wait_for_timeout(wait_time)

        download = await download_info.value

        # Use server-provided filename unless custom provided
        suggested_name = download.suggested_filename
        filename = file_name or suggested_name

        save_path = os.path.join(download_path, filename)
        await download.save_as(save_path)

        print(f"✅ Download saved: {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Download failed for selector {button_selector}: {e}")
        return None
