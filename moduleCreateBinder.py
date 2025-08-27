# playwright_module.py
import asyncio
from playwright.async_api import async_playwright
#use later when you want to import this module
async def handle_cookie_popup(page):
    try:
        await page.wait_for_selector("text='Accept All Cookies'", timeout=3000)
        accept_btn = page.locator("text='Accept All'")
        if await accept_btn.is_visible():
            await accept_btn.click()
            print("✅ 'Accept All Cookies' clicked.")
        else:
            print("⚠️ Cookie button not visible.")
    except:
        print("ℹ️ No cookie popup appeared.")

async def login(page, url, username, password):
    await page.goto(url)
    await page.wait_for_selector('#input28', timeout=15000)
    await page.fill('#input28', username)
    await page.click('#form20 input[type="submit"]')

    await page.wait_for_selector('#input60', timeout=15000)
    await page.fill('#input60', password)
    await page.click('#form52 input[type="submit"]')

    await page.wait_for_selector("#ctl05_ciqImage", timeout=20000)
    print("✅ Login successful.")

async def create_binder(page, binder_name):
    await page.hover("#tmbButton1")
    await page.wait_for_timeout(5000)
    print("✅ Hovered over Binder button.")
    await page.click("#__tmbFlyout1 > table > tbody > tr > td:nth-child(1) > ul > li:nth-child(3) > a:nth-child(2)")
    await page.wait_for_load_state()
    print("✅ Navigated to Binder page.")
    await page.wait_for_timeout(10000)

    await page.click("#layout__newFolderButton_MenuButton")
    await page.wait_for_timeout(2000)
    await page.click("#layout__newFolderButton_newBinderLink_0")
    await page.wait_for_timeout(2000)

    await page.wait_for_selector("#float_createEditPanel", timeout=10000)
    await page.fill("#float_createEditPanel__binderName", binder_name)
    await page.click("#float_createEditPanel__BinderSaveCancel__saveBtn")
    print(f"✅ Binder '{binder_name}' created successfully.")
    await page.wait_for_timeout(5000)

async def run(url, username, password, binder_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()

        await login(page, url, username, password)
        await handle_cookie_popup(page)
        await create_binder(page, binder_name)

        await browser.close()


"""# test_main.py
import asyncio
from playwright_module import run

USERNAME = "test_sfsdf.com"
PASSWORD = "ddddffff"
URL = "https://www.usertesting.com"
BINDER_NAME = "BinderRenny"

asyncio.run(run(URL, USERNAME, PASSWORD, BINDER_NAME))"""