import sys
import time
import os
import psutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurations
URL = "https://www.geninvinci.invincix.com/login"
USERNAME = "suraj.mallick@invincix.com"
PASSWORD = "MAXOUT@11uwu"

# Determine action based on the argument: check-in or check-out
ACTION = sys.argv[1] if len(sys.argv) > 1 else "checkin"

def kill_existing_chrome():
    """Kill existing Chrome processes to avoid conflicts."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def perform_login():
    kill_existing_chrome()

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Create a unique user-data directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    user_data_dir = f"/tmp/selenium_user_data_{timestamp}_{os.getpid()}"
    os.makedirs(user_data_dir, exist_ok=True)
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    driver = None

    try:
        print("Starting Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL)
        print(f"Opened URL: {URL}")

        wait = WebDriverWait(driver, 30)

        # Enter username
        print("Locating email field...")
        email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#email.form-control")))
        email_field.send_keys(USERNAME)
        print("Entered username.")

        # Enter password
        print("Locating password field...")
        password_field = driver.find_element(By.CSS_SELECTOR, "input#password.form-control")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        print("Submitted login form.")

        # Wait for login to process
        time.sleep(10)

        # Verify login success by checking navbar
        login_failed = True
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navbar")))
            print("Navbar element found. Login confirmed successful.")
            login_failed = False
        except:
            print("Login unsuccessful: Navbar not found.")

        # If login successful, perform action based on check-in or check-out
        if not login_failed:
            try:
                if ACTION == "checkin":
                    print("Checking for check-in button...")
                    checkin_button = driver.find_elements(By.CSS_SELECTOR, "a.btn.btn-primary#checkinId")
                    if checkin_button:
                        checkin_button[0].click()
                        print("Check-in successful.")
                    else:
                        print("Check-in not available or already checked in.")
                else:
                    print("Checking for check-out button...")
                    checkout_button = driver.find_elements(By.CSS_SELECTOR, "a.btn.btn-primary#checkoutId")
                    if checkout_button:
                        checkout_button[0].click()
                        print("Check-out successful.")
                    else:
                        print("Check-out not available or already checked out.")
            except Exception as e:
                print(f"Failed to perform {ACTION}: {e}")

        # Final check based on login status
        if login_failed:
            print("Login failed.")
            with open("page_source.html", "w") as f:
                f.write(driver.page_source)
            print("Saved page source for troubleshooting.")
        else:
            print(f"{ACTION.capitalize()} process completed successfully.")

        print(f"Final URL after login attempt: {driver.current_url}")

    except Exception as e:
        print(f"Login error occurred: {e}")

    finally:
        if driver:
            print("Closing driver...")
            driver.quit()
        try:
            import shutil
            shutil.rmtree(user_data_dir, ignore_errors=True)
            print("Cleaned up user data directory.")
        except Exception as cleanup_error:
            print(f"Failed to clean up user data directory: {cleanup_error}")

if __name__ == "__main__":
    print(f"Starting {ACTION} process...")
    perform_login()
    print(f"{ACTION.capitalize()} process finished.")

