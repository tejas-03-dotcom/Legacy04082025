import os
import re
from pathlib import Path
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

# ----------------- Helpers -----------------
def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name)

def extract_filename_from_headers(headers: dict, fallback_name: str) -> str:
    content_disp = headers.get("content-disposition", "")
    match = re.search(r'filename="?([^"]+)"?', content_disp)
    return sanitize_filename(match.group(1)) if match else sanitize_filename(fallback_name)

def is_file_response(response) -> bool:
    ct = response.headers.get("content-type", "").lower()
    return any(x in ct for x in ["excel", "spreadsheet", "rtf", "pdf", "msword", "octet-stream"])

# ----------------- Unified download manager -----------------
async def manage_download(page: Page, button_selector: str, download_path: str, file_name: str, wait_time=5000):
    """
    Handles any document download triggered by a button click.
    Works for:
    - Direct downloads
    - Popup/new tab downloads (Binder RTF/PDF)
    - Same-tab navigation downloads
    - AJAX / Fetch / XHR downloads (Excel)
    """
    await page.wait_for_selector(button_selector, state="visible", timeout=20000)
    os.makedirs(download_path, exist_ok=True)
    save_path = os.path.join(download_path, file_name)

    # Flag to detect network-based download
    downloaded = False

    # 1) Listen for network responses (XHR / Fetch) that return a file
    async def response_handler(response):
        nonlocal downloaded, save_path
        if downloaded:
            return  # Only save first match
        if is_file_response(response):
            headers = response.headers
            final_name = extract_filename_from_headers(headers, file_name)
            save_path = os.path.join(download_path, final_name)
            body = await response.body()
            Path(save_path).write_bytes(body)
            print(f"✅ File captured from network response: {save_path}")
            downloaded = True

    page.on("response", response_handler)

    # 2) Try direct download via Playwright
    try:
        async with page.expect_download(timeout=15000) as dl_info:
            await page.click(button_selector)
        download = await dl_info.value
        headers = await download.headers()
        final_name = extract_filename_from_headers(headers, file_name)
        save_path = os.path.join(download_path, final_name)
        await download.save_as(save_path)
        print(f"✅ Direct download saved: {save_path}")
        return save_path
    except PlaywrightTimeoutError:
        pass

    # 3) Try popup/new tab
    try:
        async with page.expect_popup(timeout=15000) as popup_info:
            await page.click(button_selector)
        popup_page = await popup_info.value
        await popup_page.wait_for_load_state("load")

        # Wait for any file response in popup
        response = await popup_page.wait_for_response(is_file_response, timeout=30000)
        headers = response.headers
        final_name = extract_filename_from_headers(headers, file_name)
        save_path = os.path.join(download_path, final_name)
        body = await response.body()
        Path(save_path).write_bytes(body)
        print(f"✅ File saved from popup: {save_path}")
        await popup_page.close()
        return save_path
    except PlaywrightTimeoutError:
        pass

    # 4) Try same-tab navigation
    try:
        async with page.expect_navigation(timeout=15000) as nav_info:
            await page.click(button_selector)
        response = await nav_info.value
        headers = response.headers
        final_name = extract_filename_from_headers(headers, file_name)
        save_path = os.path.join(download_path, final_name)
        body = await response.body()
        Path(save_path).write_bytes(body)
        print(f"✅ File saved from navigation: {save_path}")
        return save_path
    except PlaywrightTimeoutError:
        pass

    # 5) Wait a short while to catch any XHR download triggered
    await page.wait_for_timeout(wait_time)
    if downloaded:
        return save_path

    print(f"❌ No download detected for selector: {button_selector}")
    return None
