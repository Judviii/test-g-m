import os
import logging
import requests
from dotenv import load_dotenv

logging.basicConfig(filename="out.log", level=logging.INFO)
load_dotenv()

logging.info("Start")
LINKEDIN_LOGIN = os.environ["LINKEDIN_LOGIN"]
LINKEDIN_PASS = os.environ["LINKEDIN_PASS"]

def linkedin_login():
    pass


def get_linkedin_profile_picture_url():
    pass


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
    image_url = get_linkedin_profile_picture_url()
    download_image(image_url, "image.jpg")


if __name__ == "__main__":
    main()
