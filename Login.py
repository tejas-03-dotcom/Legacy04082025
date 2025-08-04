import time
from playwright.sync_api import sync_playwright
from pyautogui import click


def main():
    with sync_playwright() as p:
        # Launch a browser (Chromium in this case)
        browser = p.chromium.launch(headless=False)  # Set headless=True for headless mode
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto("https://www.capitaliq.com")  # Replace with the actual URL

        # Fill in the login form
        page.locator("//*[@id='input28']").fill("test_ciqmi@spglobal.com")
        page.locator("//*[@id='form20']/div[2]/input").click()
        #page.wait_for_selector("//*[@id='input62']")
        page.locator("xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[1]/div[4]/div/div[2]/span/input").fill("Monsoon@123")
        # Click the login button
        page.locator("xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[2]/input").click()  # Replace with the correct selector
        # Wait for navigation or a specific element
        page.wait_for_load_state("networkidle")
        time.sleep(30)
        print("Login successful!")
        browser.close()

if __name__ == "__main__":
    main()