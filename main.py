import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re

from selenium.webdriver.support.wait import WebDriverWait

ACCOUNT_EMAIL = "lordwaylon@gmail.com"
ACCOUNT_PASSWORD = "waytooeasyofapassword"
GYM_URL = "https://appbrewery.github.io/gym/"

MAX_ELEMENT_WAIT_TIME_IN_SEC = 5


def login():
    # wait until the login button becomes present
    elem_login_btn = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME_IN_SEC).until(EC.presence_of_element_located((By.ID, "login-button")))
    elem_login_btn.click()

    # wait until the submit button becomes present to fill in account info and click the submit button
    elem_submit_btn = WebDriverWait(driver, MAX_ELEMENT_WAIT_TIME_IN_SEC).until(EC.presence_of_element_located((By.ID, "submit-button")))

    elem_email_input = driver.find_element(By.ID, "email-input")
    elem_email_input.clear()
    elem_email_input.send_keys(ACCOUNT_EMAIL)

    elem_password_input = driver.find_element(By.ID, "password-input")
    elem_password_input.clear()
    elem_password_input.send_keys(ACCOUNT_PASSWORD)

    elem_submit_btn.submit()

def book_class():
    pass

def handle_wait():
    pass

# extracts class, date, and time from a button name
# example name: "book-button-spin-2025-10-25-0800"
# - class: spin
# - date: 2025-10-25
# - time: 0800
# returns None if the format is invalid
def extract_class_date_time(button_name: str):
    pattern = re.compile(r"^book-button-(?P<class>[a-zA-Z]+)-(?P<date>\d{4}-\d{2}-\d{2})-(?P<time>\d{4})$")

    match = pattern.match(button_name)
    if match:
        cls = match.group("class")
        date = match.group("date")
        time = match.group("time")
        return {
            "class": cls,
            "date": date,
            "time": time
        }

    return None


# configure chrome to stay open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# store user data for the gym into a local directory
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# navigate to the gym's website
driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)

# log into the website
login()

# wait for the schedule page to load
driver.implicitly_wait(2)

# find the next Tuesday at 6 PM class and book it or join the wait list
elem_booking_elements = driver.find_elements(By.CSS_SELECTOR, "[id^='book']")
print(f'there are {len(elem_booking_elements)}')
for e in elem_booking_elements:
    print(f"{e.get_attribute('id')} - {e.text}")
    print(extract_class_date_time(e.get_attribute('id')))

