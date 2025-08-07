import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from telegram import Bot

# Configuration
TELEGRAM_BOT_TOKEN = '8049406807:AAGhuUh9fOm5wt7OvTobuRngqY0ZNBMxlHE'
TELEGRAM_CHAT_ID = '-1002311125652'
IVAS_URL = 'https://ivasms.com/panel/login'
IVAS_USERNAME = 'imdigitalvasu@gmail.com'
IVAS_PASSWORD = '@Vasu2412'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_panel(driver):
    driver.get(IVAS_URL)
    time.sleep(3)
    driver.find_element(By.NAME, "username").send_keys(IVAS_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(IVAS_PASSWORD + Keys.RETURN)
    time.sleep(5)

def get_latest_otp(driver):
    driver.get("https://ivasms.com/panel/inbox")  # Update if different
    time.sleep(3)

    try:
        otp_element = driver.find_element(By.CSS_SELECTOR, ".otp-message-class")  # Replace with actual selector
        return otp_element.text
    except Exception:
        return None

def format_otp_message(raw_otp):
    return f"🔔 *New OTP Received*\n\n{raw_otp}"

def send_to_telegram(msg):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode='Markdown')

def main():
    driver = start_driver()
    last_otp = None
    try:
        login_to_panel(driver)
        while True:
            otp = get_latest_otp(driver)
            if otp and otp != last_otp:
                message = format_otp_message(otp)
                send_to_telegram(message)
                last_otp = otp
            time.sleep(30)
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
