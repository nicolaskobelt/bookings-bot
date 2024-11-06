from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests
import logging
import logging.handlers
import time
import os

email = os.environ["USERNAME"]
pwd = os.environ["PASSWORD"]
webhook = "https://hooks.slack.com/services/"

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Initialize the Chrome driver
driver = webdriver.Chrome(options)

daysRange = 2 # Days reservation restriction

def denyCookies(driver):
    driver.find_element(By.CSS_SELECTOR, "#eucookielaw > div.conCookie > a:nth-child(1)").click()

current_day = datetime.now().strftime('%A')

day_action = {
    'Monday': 'Engine', # wed class
    'Tuesday': 'WOD', # thursday class
    'Wednesday': 'WOD', # friday class
    'Thursday': 'Weekend MegaWod', # saturday class
    'Friday': 'Weekend WOD', # sunday class
    'Saturday': 'WOD', # monday class
    'Sunday': 'WEIGHTLIFTING' # thursday class
}

classToBook = day_action.get(current_day, "WOD")

try:
    driver.get("https://aimharder.com/login")

    denyCookies(driver)

    email_field = driver.find_element(By.NAME, "mail")
    password_field = driver.find_element(By.NAME, "pw")

    email_field.send_keys(email)
    password_field.send_keys(pwd)

    password_field.send_keys(Keys.RETURN)

    logger.info('Logging success for user: ' + email)

    time.sleep(5)

    driver.find_element(By.CSS_SELECTOR, "#menuSwiperCon > div.swiper-wrapper > div > a.ahMenuOp.ahPicReservations").click()
    button = driver.find_element(By.ID, "nextDay")

    for i in range(daysRange):
        button.click()
        time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, "#select2-filtroClases-container").click()

    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/span/span/span[1]/input"))
    )
    input_field.send_keys(classToBook)
    input_field.send_keys(Keys.ENTER)

    booking_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Reservar"))
    )
    booking_link.click()

    logger.info(classToBook + ' was booked succesfully!')

    time.sleep(5);

except Exception as e:
    logger.error(f"An error occurred: {e}")
    # Perform API POST request
    payload = {
        "attachments": [
		    {
		        "color": "#df0000",
                "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Error to book class" + classToBook,
                    },
                },
                {
                    "type": 'section',
                    "text": {
                        "text": str(e),
                        "type": "mrkdwn",
                    },
                },
                ]
            }
        ]
    }
    headers = { "Content-Type": "application/json" }
    response = requests.post(webhook, json=payload, headers=headers)
    if response.status_code == 200:
        logger.info("Error reported successfully.")
    else:
        logger.error(f"Failed to report error: {response.status_code}")

finally:
    driver.quit()
