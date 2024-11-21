import os
import logging
import requests
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

logging.basicConfig(filename="out.log", level=logging.INFO)
load_dotenv()

logging.info("Start")
LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login/uk/"
LINKEDIN_LOGIN = os.environ["LINKEDIN_LOGIN"]
LINKEDIN_PASS = os.environ["LINKEDIN_PASS"]


def linkedin_login(login_url: str, driver: WebDriver):
    driver.get(login_url)

    auto_login_off = driver.find_element(By.ID, "rememberMeOptIn-checkbox")
    driver.execute_script("arguments[0].click();", auto_login_off)
    time.sleep(5)

    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(LINKEDIN_LOGIN)
    time.sleep(5)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(LINKEDIN_PASS)
    time.sleep(5)

    login_button = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )
    login_button.click()
    time.sleep(5)


def get_linkedin_profile_picture_url(driver: WebDriver) -> str:
    my_profile = driver.find_element(By.CSS_SELECTOR, ".ember-view.block")
    my_profile.click()
    time.sleep(5)

    profile_picture_element = driver.find_element(
        By.CSS_SELECTOR, "img.profile-photo-edit__preview"
    )
    profile_picture_url = profile_picture_element.get_attribute("src")
    print("Picture Url", profile_picture_url)
    time.sleep(5)

    return profile_picture_url


def captcha_detect():
    pass


def download_image(image_url, file_name):
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
    else:
        print(f"{response.status_code}")


def main():
    with webdriver.Chrome() as driver:
        linkedin_login(login_url=LINKEDIN_LOGIN_URL, driver=driver)
        profile_picture_url = get_linkedin_profile_picture_url(driver=driver)
        file_name = "profile_picture.jpg"
        download_image(profile_picture_url, file_name)


if __name__ == "__main__":
    main()
