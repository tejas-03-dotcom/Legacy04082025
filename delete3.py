import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login

async def generate_ten_k_from_tearsheet():
    async with async_playwright() as p:
        playwright, browser, page = await login()

        await page.wait_for_selector("#_pageHeader > div:nth-child(1) > span.cPageTitle_subHeader", timeout=5000)
        print("✅ Dashboard page loaded.")

        await page.click("#SearchTopBar")
        await page.wait_for_timeout(2000)

        await page.fill("#SearchTopBar", "Bank of America Corporation")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)

        await page.click("#SR0 > td.NameCell > div > span > a")
        print("✅ Navigated to the entity page.")

        await page.wait_for_selector("#ll_7_48_406", timeout=15000)
        print("✅ Entity page loaded.")

        tearsheet_locator = page.locator("#ll_7_48_406")
        if not await tearsheet_locator.is_visible():
            print("❌ Tearsheets page is not visible.")
            await browser.close()
            return

        toolbar = page.locator("#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar")
        await toolbar.wait_for(timeout=5000)

        if await toolbar.is_visible():
            print("✅ Toolbar is visible.")
        else:
            print("❌ Toolbar is not visible.")
            await browser.close()
            return

        ten_k_button_selector = "#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar > ul > li:nth-child(8) > a > div"
        ten_k_button = page.locator(ten_k_button_selector)
        await ten_k_button.wait_for(state="visible", timeout=5000)

        # Start waiting for the first popup BEFORE clicking
        first_popup_promise = page.wait_for_event("popup")
        await ten_k_button.click()
        first_popup = await first_popup_promise
        await first_popup.wait_for_load_state()
        print("✅ First popup (10-K) loaded.")

        # Now handle iframe in first popup to find and click #pdfImg
        pdf_img_selector = "#pdfImg"

        frames = first_popup.frames
        print(f"First popup has {len(frames)} frames:")
        for i, frame in enumerate(frames):
            print(f" Frame {i}: {frame.url}")

        target_frame = None
        for frame in frames:
            try:
                await frame.wait_for_selector(pdf_img_selector, timeout=1000)
                target_frame = frame
                print(f"Found '#pdfImg' in frame: {frame.url}")
                break
            except Exception:
                pass

        if target_frame is None:
            print("❌ Could not find '#pdfImg' in any iframe inside first popup.")
            await first_popup.screenshot(path="first_popup_debug.png")
            await browser.close()
            return

        await target_frame.wait_for_selector(pdf_img_selector, timeout=30000)
        print("✅ '#pdfImg' found in iframe, clicking now...")

        # Prepare for second popup before clicking
        second_popup_promise = first_popup.wait_for_event("popup")
        await target_frame.click(pdf_img_selector)
        second_popup = await second_popup_promise
        await second_popup.wait_for_load_state()
        print("✅ Second popup (save report) loaded.")

        # Here you can add code to download/save report, e.g.
        # await second_popup.click("selector_for_save_button") or
        # await second_popup.pdf(path="report.pdf")

        await browser.close()

asyncio.run(generate_ten_k_from_tearsheet())
