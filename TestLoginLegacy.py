from playwright.async_api import async_playwright

USERNAME = "test_ciqmi@spglobal.com"
PASSWORD = "Monsoon@123"
URL = "https://www.capitaliq.com"

async def login():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False, slow_mo=50)
    page = await browser.new_page()

    # Step 1: Go to login page
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
    await page.wait_for_timeout(5000)

    # Return browser and page to continue automation
    return playwright, browser, page
