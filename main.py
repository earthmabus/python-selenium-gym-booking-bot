import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
import datetime as dt
from dateutil.relativedelta import relativedelta

from selenium.webdriver.support.wait import WebDriverWait

ACCOUNT_EMAIL = "lordwaylon@gmail.com"
ACCOUNT_PASSWORD = "waytooeasyofapassword"
GYM_URL = "https://appbrewery.github.io/gym/"

MAX_ELEMENT_WAIT_TIME_IN_SEC = 5

DAY_OF_WEEK_MONDAY = 0
DAY_OF_WEEK_TUESDAY = 1
DAY_OF_WEEK_WEDNESDAY = 2
DAY_OF_WEEK_THURSDAY = 3
DAY_OF_WEEK_FRIDAY = 4
DAY_OF_WEEK_SATURDAY = 5
DAY_OF_WEEK_SUNDAY = 6

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
# - datetime: 2025-10-25
# - time: 0800
# returns None if the format is invalid
def extract_class_date_time(button_name: str):
    pattern = re.compile(r"^book-button-(?P<class>[a-zA-Z]+)-(?P<date>\d{4}-\d{2}-\d{2})-(?P<time>\d{4})$")

    match = pattern.match(button_name)
    if match:
        cls = match.group("class")
        date = match.group("date")
        tm = match.group("time")
        return {
            "button_name": button_name,
            "class": cls,
            "datetime": dt.datetime.strptime(f'{date}-{tm}', "%Y-%m-%d-%H%M")
        }

    return None

def book_or_joinwait_for_next_tuesday_6pm_class():
    elem_booking_elements = driver.find_elements(By.CSS_SELECTOR, "[id^='book']")
    for e in elem_booking_elements:
        c = extract_class_date_time(e.get_attribute('id'))

        if c['datetime'].weekday() == DAY_OF_WEEK_TUESDAY and c['datetime'].hour == 18:
            print(c)
            e.click()
            print(f'clicked on {c["button_name"]}')

            # verify the course was booked
            confirm = verify_booking(c)
            if confirm:
                print("you are verified for the class")

            break

def verify_booking(course_booking_dict):
    all_bookings = get_all_bookings()

    retval = False
    for booking in all_bookings:
        if booking['class'] == course_booking_dict['class'] and booking['datetime'] == course_booking_dict['datetime']:
            retval = True
            break

    return retval

# returns a list of { class, datetime, booking_status }
def get_all_bookings():
    '''Retrieves a list of classes that the user has booked according to the "My Bookings" page'''

    # navigate to the "My Bookings" page
    driver.implicitly_wait(1)
    elem_mybookings_btn = driver.find_element(By.ID, "my-bookings-link")
    elem_mybookings_btn.click()

    # wait for the page to load
    driver.implicitly_wait(1)

    # create a list of dictionary of { class, datetime, booking_status}
    # grab the full list of courses
    all_bookings = []
    elem_booking_elements = driver.find_elements(By.CSS_SELECTOR, "[id^='booking-card-booking_']")
    for e in elem_booking_elements:
        # navigate to each booking block and get the contents of the first <p> tag which should contain:
        # "When: Mon, Oct 20, 5:00 PM"
        first_p_elem = e.find_element(By.CSS_SELECTOR, "p")

        text_when, text_datetime = first_p_elem.text.split(" ", 1)
        #print(f"text_datetime = {text_datetime}")

        # text_datetime = "Mon, Oct 20, 5:00 PM"
        # add in the current year so that we can convert this to a datetime
        # "When: Mon, Oct 20, 2025, 5:00 PM"
        current_dt = dt.datetime.now()
        text_datetime_with_year = re.sub(r"(\w{3}, \w{3} \d{1,2}),", rf"\1, {current_dt.year},", text_datetime)
        #print(f"text_datetime_with_year = {text_datetime_with_year}")

        # text_datetime_with_year = "Tue, Oct 21, 2025, 6:00 PM"
        # Note: it's possible that the booking could actually be for NEXT year and not this year, thus the year that was just added in could be incorrect... if the month in text_datetime is less than the current month, that's probably the case and we should increment the year
        booking_date = dt.datetime.strptime(text_datetime_with_year, "%a, %b %d, %Y, %I:%M %p")
        if booking_date < current_dt:
            booking_date = booking_date + relativedelta(years=1)

        # get the booking_class
        booking_class = e.get_attribute("data-class-type")

        # get the status of the booking
        booking_status = e.get_attribute("data-booking-status")

        all_bookings.append({
            "class": booking_class,
            "datetime": booking_date,
            "booking_status": booking_status
        })

    return all_bookings

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
book_or_joinwait_for_next_tuesday_6pm_class()
