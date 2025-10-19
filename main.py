from selenium import webdriver
from selenium.webdriver.common.by import By
import os

ACCOUNT_EMAIL = "lordwaylon@gmail.com"
ACCOUNT_PASSWORD = "waytooeasyofapassword"
GYM_URL = "https://appbrewery.github.io/gym/"


def login():
    pass

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

