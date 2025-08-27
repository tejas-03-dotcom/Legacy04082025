async def handle_cookie_popup(page):
    try:
        # Adjust text selector if button text is different
        await page.wait_for_selector("text='Accept All'", timeout=3000)
        accept_btn = page.locator("text='Accept All'")
        if await accept_btn.is_visible():
            await accept_btn.click()
            print("✅ 'Accept All Cookies' clicked.")
        else:
            print("⚠️ Cookie button not visible.")
    except:
        print("ℹ️ No cookie popup appeared.")
