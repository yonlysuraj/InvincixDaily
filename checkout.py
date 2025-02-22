import os
import sys
import logging
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
LOG_FILE = "checkout.log"
LAST_RUN_FILE = "last_checkout.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Print logs to console as well
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)

# Fetch credentials from environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Ensure environment variables exist
if not EMAIL or not PASSWORD:
    logging.error("❌ ERROR: EMAIL or PASSWORD environment variables are not set.")
    sys.exit(1)

# Prevent multiple runs by checking last execution time
if os.path.exists(LAST_RUN_FILE):
    with open(LAST_RUN_FILE, "r") as file:
        last_run_time_str = file.read().strip()

    if last_run_time_str:
        last_run_time = datetime.strptime(last_run_time_str, "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.now() - last_run_time

        if time_diff < timedelta(hours=12):
            logging.warning(f"⚠️ Script already ran {time_diff.seconds // 3600} hours ago. Skipping execution.")
            logging.info("✅ Script completed successfully. (Skipped due to recent execution)")
            sys.exit(0)

# Configure headless browser
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs without opening a browser window
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

def capture_screenshot(name="checkout_error.png"):
    """Capture screenshot for debugging and save to file."""
    driver.save_screenshot(name)
    logging.info(f"📸 Screenshot saved as {name}")

try:
    logging.info("🚀 Starting Check-Out Process")

    # Open login page
    driver.get("https://www.geninvinci.invincix.com/login")
    logging.info("🌐 Opened login page.")

    # Enter credentials
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(EMAIL)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    logging.info("🔑 Entered credentials.")

    # Click login button
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnLogin")))
    login_button.click()
    logging.info("✅ Clicked login button.")

    # Wait for login confirmation
    WebDriverWait(driver, 15).until(EC.url_changes("https://www.geninvinci.invincix.com/login"))
    logging.info("🎉 Login successful.")

    # Navigate to Check-Out page
    checkout_url = "https://www.geninvinci.invincix.com/attendance/checkout"
    driver.get(checkout_url)
    logging.info("📍 Navigated to Check-Out page.")

    # Check if already checked out
    try:
        checkout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnCheckOut")))
        checkout_button.click()
        logging.info("✅ Check-Out successful.")
    except:
        logging.warning("⚠️ Already checked out manually, skipping check-out.")
        logging.info("✅ Script completed successfully. (Skipped check-out)")

    # Save last execution timestamp
    with open(LAST_RUN_FILE, "w") as file:
        file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

except Exception as e:
    logging.error(f"❌ Error occurred: {str(e)}")
    capture_screenshot()

finally:
    driver.quit()
    logging.info("🚪 Browser closed.")
