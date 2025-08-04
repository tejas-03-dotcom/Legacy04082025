import asyncio
from playwright.async_api import async_playwright

USERNAME = "test_ciqmi@spglobal.com"
PASSWORD = "Monsoon@123"
URL = "https://www.capitaliq.com"


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()

        # Step 1: Login
        await page.goto(URL)
        await page.wait_for_selector('#input28', timeout=15000)
        await page.fill('#input28', USERNAME)
        await page.click('#form20 input[type="submit"]')

        await page.wait_for_selector('#input60', timeout=15000)
        await page.fill('#input60', PASSWORD)
        await page.click('#form52 input[type="submit"]')

        # Step 2: Confirm login
        await page.wait_for_selector("#ctl05_ciqImage", timeout=20000)
        print("✅ Login successful.")

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
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div")

        # Step 7: Save entity selection
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")
        print("✅ Entity selection saved.")

        # Step 8: Save as template
        await page.wait_for_load_state("load")
        await page.click("//*[@id='_rptOpts__rptOptsDS__optsDs__optsTog__templateSaveImg']")
        await page.wait_for_timeout(5000)

        print ("✅ Save as template modal opened.")
        """modal = page.locator("#_rptOpts__rptOptsDS__optsDs__optsTog_float_saveTemplateModal")
        await modal.wait_for(state="visible", timeout=10000)

        await page.fill("#_rptOpts__rptOptsDS__optsDs__optsTog_float_saveTemplateModal__templateSaveTxt", "Test Template")
        await page.wait_for_load_state("load")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_saveTemplateModal__templateSaveCancel__saveBtn")
        print("✅ Template saved as 'Test Template'.")"""

        # Keep browser open briefly for confirmation
        await page.wait_for_timeout(5000)

        # Optional: Close browser
        # await browser.close()

# Run the async function
asyncio.run(run())