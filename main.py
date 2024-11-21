import os
import logging
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from webdriver_manager.chrome import ChromeDriverManager


# Setup logginig basicConfig and load variables from the .env file
logging.basicConfig(filename="out.log", level=logging.INFO)
load_dotenv()

# Global variables
LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login/uk/"
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "Test_login")
LINKEDIN_PASS = os.getenv("LINKEDIN_PASS", "Test_pass")
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", None)


# A function to automate the login process in LinkedIn
# time.sleep(2) in function used to protect against blocking
def linkedin_login(
        driver: WebDriver,
        login_url: str,
        email: str,
        password: str
) -> None:
    try:
        driver.get(login_url)
        # Catching recaptcha
        sitekey = recaptcha_present(driver=driver)
        if sitekey:
            logging.info(f"Recaptcha spotted before login. Sitekey: {sitekey}")
            recaptcha_solve(captcha_page_url=login_url, sitekey=sitekey)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        logging.info("Successfully opened the LinkedIn login page.")
    except TimeoutException:
        logging.critical("Linkedin site not accecible.")
        raise

    try:
        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(email)
        time.sleep(2)
        logging.info("Username field filled.")
    except NoSuchElementException:
        logging.critical("Username field not found.")
        raise

    try:
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        time.sleep(2)
        logging.info("Password field filled.")
    except NoSuchElementException:
        logging.critical("Password field not found.")
        raise

    try:
        # Turn off the “Remember me” checkbox to avoid LinkedIn notifications
        # about a new device when you log in automatically
        auto_login_off = driver.find_element(By.ID, "rememberMeOptIn-checkbox")
        driver.execute_script("arguments[0].click();", auto_login_off)
        logging.info("Remember me checkbox off")
    except NoSuchElementException:
        logging.warning("Remember me checkbox not found.")

    try:
        login_button = driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        )
        login_button.click()
        logging.info("Login button clicked.")
    except NoSuchElementException:
        logging.critical("Login button not found.")
        raise

    # Catching recaptcha
    sitekey = recaptcha_present(driver=driver)
    if sitekey:
        logging.info(f"Recaptcha spotted after login. Sitekey: {sitekey}")
        recaptcha_solve(captcha_page_url=login_url, sitekey=sitekey)

    # Uncomment the line below,
    # if the function does not detect recaptcha but you have it,
    # it will give you 45 seconds to solve it yourself
    # time.sleep(45)

    try:
        WebDriverWait(driver, 10).until(
            EC.url_contains("/feed")
        )
        logging.info("Successful login.")
    except TimeoutException:
        logging.critical(
            "Login failed. Please make sure that your email and password "
            "are correct in the .env file."
        )
        raise


# Function to get profile picture url
def get_linkedin_profile_picture_url(driver: WebDriver) -> str:
    try:
        my_profile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ember-view.block"))
        )
        my_profile.click()
        logging.info("Redirect to your profile.")
    except (TimeoutException, NoSuchElementException) as ex:
        logging.critical("Redirect to your profile failed, button not found.")
        raise ex

    try:
        profile_picture_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "img.profile-photo-edit__preview")
            )
        )
        profile_picture_url = profile_picture_element.get_attribute("src")
        print("Picture Url", profile_picture_url)
        logging.info("Picture url taken.")
    except (TimeoutException, NoSuchElementException) as ex:
        logging.critical("Get picture url failed.")
        raise ex

    return profile_picture_url


# A function that detects recaptcha
def recaptcha_present(driver: WebDriver) -> None | str:
    try:
        recaptcha_element = driver.find_element(By.CLASS_NAME, "g-recaptcha")
        sitekey = recaptcha_element.get_attribute("data-sitekey")
        return sitekey
    except NoSuchElementException:
        return None


# This function gives time to resolve the captcha if it was captured,
# or transmits information to the 2captcha service to resolve it
def recaptcha_solve(captcha_page_url: str, sitekey: str) -> None:
    """
    Pauses execution for 45 seconds,
    allowing the user to manually solve the recaptcha.
    A more automated solution can be implemented
    with the 2captcha API (for a fee).
    To do this, uncomment the commented line,
    and delete time.sleep(45)
    """
    time.sleep(45)
    # recaptcha_solve_with_2captcha(captcha_page_url, sitekey)


# Function that connects to 2captcha API and solves recaptcha
def recaptcha_solve_with_2captcha(
        captcha_page_url: str,
        sitekey: str,
        api_key=CAPTCHA_API_KEY
) -> None:
    solver = TwoCaptcha(api_key)
    response = solver.recaptcha(sitekey=sitekey, url=captcha_page_url)
    code = response["code"]
    logging.info(f"Recaptcha solver, code:{code}")


# Function that downloads images from a link to a project folder
def download_image(image_url: str, file_name: str) -> None:
    logging.info("Starting download image")
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
            logging.info(f"Download succes: {file_name}")
    else:
        logging.critical(f"Wrong image url, more info: {response.status_code}")


# The main function in which all processes are launched
def main() -> None:
    logging.info(f"Script start: {datetime.now()}")
    options = Options()
    # Uncomment line below to run script in headless mode.
    # But do it only if you know that there will be no recaptcha!
    # options.add_argument("--headless=new")
    service = ChromeService(ChromeDriverManager().install())
    with webdriver.Chrome(options=options, service=service) as driver:
        linkedin_login(
            driver=driver,
            email=LINKEDIN_EMAIL,
            password=LINKEDIN_PASS,
            login_url=LINKEDIN_LOGIN_URL
        )
        profile_picture_url = get_linkedin_profile_picture_url(driver=driver)
        file_name = "profile_picture.jpg"
        download_image(profile_picture_url, file_name)


if __name__ == "__main__":
    main()
