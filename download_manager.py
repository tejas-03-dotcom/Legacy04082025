import os
import re
import uuid
from pathlib import Path
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


def sanitize_filename(name: str) -> str:
    """
    Remove invalid characters from filename for cross-platform safety.
    """
    return re.sub(r'[<>:"/\\|?*]', "_", name)


def extract_filename_from_headers(headers: dict, fallback_name: str) -> str:
    """
    Extract filename from Content-Disposition header if present.
    """
    content_disp = headers.get("content-disposition", "")
    match = re.search(r'filename="?([^"]+)"?', content_disp)
    if match:
        return sanitize_filename(match.group(1))
    return sanitize_filename(fallback_name)


async def manage_download(page: Page, button_selector: str, download_path: str, file_name: str):
    """
    Handles file saving triggered by a button click.
    Supports:
    - Direct downloads
    - Popup/tab documents (BinderWaitingIndicator.aspx)
    - Same-page navigation (redirect to file)

    :return: Full path to saved file or None
    """
    await page.wait_for_selector(button_selector, state="visible", timeout=20000)
    os.makedirs(download_path, exist_ok=True)

    # 1) Direct download
    try:
        async with page.expect_download(timeout=15000) as download_info:
            await page.click(button_selector)
        download = await download_info.value

        headers = await download.headers()
        final_name = extract_filename_from_headers(headers, file_name)
        save_path = os.path.join(download_path, final_name)

        await download.save_as(save_path)
        print(f"✅ Direct download saved: {save_path}")
        return save_path

    except PlaywrightTimeoutError:
        print("⚠️ No direct download detected, trying popup...")

    # 2) Popup/tab (BinderWaitingIndicator.aspx or similar)
    try:
        async with page.expect_popup(timeout=15000) as popup_info:
            await page.click(button_selector)

        popup_page = await popup_info.value
        await popup_page.wait_for_load_state("load")

        # Wait for a response with typical file headers
        response = await popup_page.wait_for_response(
            lambda r: "BinderWaitingIndicator" in r.url or "report" in r.url.lower(),
            timeout=30000
        )

        headers = response.headers
        final_name = extract_filename_from_headers(headers, file_name)
        save_path = os.path.join(download_path, final_name)

        body = await response.body()
        Path(save_path).write_bytes(body)

        print(f"✅ Popup download saved: {save_path}")
        await popup_page.close()
        return save_path

    except PlaywrightTimeoutError:
        print("⚠️ No popup download detected, checking same-tab navigation...")

    # 3) Same-tab navigation
    try:
        async with page.expect_navigation(timeout=15000) as nav_info:
            await page.click(button_selector)

        response = await nav_info.value

        headers = response.headers
        final_name = extract_filename_from_headers(headers, file_name)
        save_path = os.path.join(download_path, final_name)

        body = await response.body()
        Path(save_path).write_bytes(body)

        print(f"✅ Navigation download saved: {save_path}")
        return save_path

    except PlaywrightTimeoutError:
        print("❌ No download, popup, or navigation detected for:", button_selector)
        return None
