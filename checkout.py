import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def capture_screenshot(name="error_checkout.png"):
    driver.save_screenshot(name)
    print(f"Screenshot saved as {name}")

try:
    driver.get("https://www.geninvinci.invincix.com/login")
    print("Opened login page:", driver.title)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    print("Entered credentials")

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnLogin")))
    login_button.click()
    print("Clicked login button")

    WebDriverWait(driver, 15).until(EC.url_changes("https://www.geninvinci.invincix.com/login"))
    print("Login successful, current page:", driver.title)

    checkout_url = "https://www.geninvinci.invincix.com/attendance/checkout"
    driver.get(checkout_url)
    print("Navigated to Check-Out page:", driver.title)

    WebDriverWait(driver, 10).until(EC.url_changes(checkout_url))
    print("Check-Out successful")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    capture_screenshot()

finally:
    driver.quit()
    print("Browser closed")
