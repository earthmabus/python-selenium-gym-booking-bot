from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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

