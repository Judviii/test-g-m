# Test Task for G&M
## Description
The script automates the process of logging in to LinkedIn and uploading a user's profile photo, taking into account the possibility of a reCAPTCHA. The main stages of the script:

- Login to LinkedIn: Using Selenium, the script opens the LinkedIn login page, enters the username and password, and processes possible reCAPTCHAs. If one appears, the script either waits 45 seconds for it to be manually resolved or provides for automatic resolution via the 2captcha API.

- Getting a profile photo: After a successful login, the script goes to the user's profile page, finds the photo, and downloads it to the local computer.

- Logging: All actions, including successes or errors, are recorded in the out.log file to track the script's execution.

## Prerequisites

### Before you can run this script, make sure you have the following installed:

- Python 3.12
- Google Chrome (selenium use it for automation)
- pip (Python package installer) 

## Running script with Python
```shell
    git clone https://github.com/Judviii/test-g-m.git
    cd test-g-m
    
    # on macOS
    python3 -m venv venv
    source venv/bin/activate
    # on Windows
    python -m venv venv
    venv\Scripts\activate
    
    pip install -r requirements.txt

    # create an .env file in the root directory of project,
    # use env.sample as example.

    # The script will use email and password for login automation,
    # so it is important to specify them in the .env file
    
    # on macOS
    python3 main.py
    # on Windows
    python main.py

    # The profile picture will be saved in the project folder,
    # under the name profile_picture.jpg after the script completes,
    # logs will be written to the out.log file.

```

## Recaptcha problem
- I wrote a function that sees it and gives you 45 seconds to solve it, or passes it to the 2Captcha service (but it's a paid service, you need to get your API key).
- If it doesn't catch your recaptcha, I've left instructions in the code at lines 96-99 on how to stop the process for 45 seconds so you can go through it yourself.
- Also, you can leave time.sleep(45) in the linkedin_login function instead of comments "# Catching recaptcha" (lines 40 or 90), depending on whether it's before or after the login.
- I haven't encountered this problem during development, which is why it's quite difficult for me to write a proper recapcha intercept.
