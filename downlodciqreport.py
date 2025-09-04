import os


async def download_report(page, download_button_selector, save_path):
    # Ensure the download button is visible
    await page.wait_for_selector(download_button_selector, state="visible", timeout=20000)
    download_button = await page.query_selector(download_button_selector)

    if download_button:
        # Wait for the download to start
        async with page.expect_download() as download_info:
            await download_button.click()
        download = await download_info.value

        # Ensure the save directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the downloaded file
        await download.save_as(save_path)
        print(f"✅ Report downloaded and saved to {save_path}")
    else:
        print("❌ 'Download' button not found or not clickable.")
