import asyncio
from TestLoginLegacy import login
from playwright.async_api import async_playwright


async def generate_ten_k_from_tearsheet():
    async with async_playwright() as p:
        playwright, browser, page = await login()

        await page.wait_for_selector("#_pageHeader > div:nth-child(1) > span.cPageTitle_subHeader", timeout=10000)
        print("✅ Dashboard page loaded.")

        await page.click("#SearchTopBar")
        await page.wait_for_timeout(2000)

        await page.fill("#SearchTopBar", "Bank of America Corporation")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)

        await page.click("#SR0 > td.NameCell > div > span > a")
        print("✅ Navigated to the entity page.")

        await page.wait_for_selector("#ll_7_48_406", timeout=20000)
        print("✅ Entity page loaded.")

        tearsheet_locator = page.locator("#ll_7_48_406")
        if not await tearsheet_locator.is_visible():
            print("❌ Tearsheets page is not visible.")
            await browser.close()
            return

        toolbar = page.locator("#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar")
        await toolbar.wait_for(timeout=10000)

        if await toolbar.is_visible():
            print("✅ Toolbar is visible.")
        else:
            print("❌ Toolbar is not visible.")
            await browser.close()
            return

        ten_k_button_selector = "#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar > ul > li:nth-child(8) > a > div"

        ten_k_button = page.locator(ten_k_button_selector)
        await ten_k_button.wait_for(state="visible", timeout=10000)

        # Wait for first popup opening triggered by 10-K button click
        popup_promise = page.wait_for_event("popup")
        await ten_k_button.click()
        first_popup = await popup_promise
        await first_popup.wait_for_load_state()
        print("✅ First popup (10-K) loaded.")

        # Find iframe containing #pdfImg button
        frames = first_popup.frames
        print(f"First popup has {len(frames)} frames:")
        for i, frame in enumerate(frames):
            print(f" Frame {i}: {frame.url}")

        pdf_img_selector = "#pdfImg"
        target_frame = None
        for frame in frames:
            try:
                # Wait short time just to check presence
                await frame.wait_for_selector(pdf_img_selector, timeout=3000)
                target_frame = frame
                print(f"✅ '#pdfImg' found in iframe: {frame.url}")
                break
            except:
                continue

        if not target_frame:
            print("❌ '#pdfImg' not found in any iframe.")
            await browser.close()
            return

        print("✅ '#pdfImg' found, clicking now...")

        # Now try clicking #pdfImg and handle download / navigation / popup with longer timeouts

        try:
            # Wait for download event up to 60s (large document)
            download_promise = first_popup.wait_for_event("download", timeout=60000)
            await target_frame.click(pdf_img_selector)
            download = await download_promise
            path = await download.path()
            print(f"✅ Download started, saved to: {path}")

        except asyncio.TimeoutError:
            print("⚠️ Download not triggered within timeout, checking for popup or navigation...")
            """ except Exception as e:
            print(f"⚠️ Download not triggered or timeout: {e}")
            try:
                # fallback: maybe navigation in same frame
                async with first_popup.expect_navigation(timeout=120000):
                    await target_frame.click(pdf_img_selector)
                print("✅ Navigation happened after clicking '#pdfImg'.")
            except Exception as e_nav:
                print(f"⚠️ Navigation not triggered or timeout: {e_nav}")
                # fallback: check new page popup manually
                pages_before = browser.contexts[0].pages
                await target_frame.click(pdf_img_selector)
                await asyncio.sleep(10)  # wait longer for popup
                pages_after = browser.contexts[0].pages
                new_pages = [p for p in pages_after if p not in pages_before]
                if new_pages:
                    second_popup = new_pages[0]
                    await second_popup.wait_for_load_state(timeout=120000)
                    print("✅ Second popup loaded.")
                else:
                    print("❌ No popup, navigation, or download detected after clicking '#pdfImg'.")
                """
        print("✅ Script completed.")
        await browser.close()


asyncio.run(generate_ten_k_from_tearsheet())
