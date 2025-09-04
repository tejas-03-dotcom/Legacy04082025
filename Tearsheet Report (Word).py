import asyncio
import os
from playwright.async_api import async_playwright
from TestLoginLegacy import login


async def generate_tearsheet_report_word():
    async with async_playwright() as p:
        playwright, browser, page = await login()

    # Step 3: Hover and navigate to Report Builder
    await page.hover("div.tmbButtonBarContainerLeft div")
    await page.wait_for_timeout(1000)
    await page.get_by_role("link", name="Report Builder").click()
    await page.wait_for_load_state("load")
    print("✅ Report Builder page loaded.")

    # Step 4: Open Entity Selector
    await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog__esLink")
    print("✅ Entity selection modal opened.")

    # Step 5: Search for entity
    search_box = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es_searchbox"
    await page.wait_for_selector(search_box, timeout=10000)
    await page.fill(search_box, "Bank of America Corporation")
    await page.wait_for_timeout(3000)

    # Step 6: Select the first result
    await page.keyboard.press("ArrowDown")
    await page.keyboard.press("Enter")

    # Optional: Select from the tree view (adjust selector as needed)
    await page.click(
        "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div")

    # Step 7: Save entity selection
    await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
    await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")
    print("✅ Entity selection saved.")

    # Step 8: Save as template
    await page.wait_for_load_state("load")
    await page.wait_for_timeout(2000)
    # Click on Capital IQ Templates

    await page.click("#_templatesFilmstrip__filmstripDS_ctl02__ciqTempRb_span > label")  # Replace with actual selector
    print("✅ Clicked on Capital IQ Templates.")

    # Click on Quick Report option
    await page.click("#RepBldrTemplateImg7")  # Replace with actual selector
    print("✅ Clicked on Tearsheet Report word option.")
    await page.wait_for_timeout(5000)
    await page.wait_for_selector("body > div.wrapper", state="visible", timeout=20000)

    # Locate and click the "Download" option inside the wrapper
    download_button = await page.query_selector("body > div.wrapper >> text='Download'")
    if download_button:
        async with page.expect_download() as download_info:
            await download_button.wait_for(state="visible", timeout=10000)
            if download_button.clickable:
                download_button.click()

        download = await download_info.value
    else:
        print("❌ 'Download' option not found.")
    download = await download_info.value

    # Save the report to a specific folder
    save_folder = "D:\Legacy04082025\downloads"  # Update this path
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, "TearsheetReportword.docx")
    await download.save_as(save_path)
    print(f"✅ Report downloaded and saved to {save_path}")
    # Close the browser
    await browser.close()


# Run the async function
asyncio.run(generate_tearsheet_report_word())
