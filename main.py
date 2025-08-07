import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from telegram import Bot
import threading
from flask import Flask

# Config from environment variables
TELEGRAM_BOT_TOKEN = "8049406807:AAGhuUh9fOm5wt7OvTobuRngqY0ZNBMxlHE"
TELEGRAM_CHAT_ID = "-1002311125652"
IVAS_URL = 'https://ivasms.com/panel/login'
IVAS_USERNAME = "imdigitalvasu@gmail.com"
IVAS_PASSWORD = "@Vasu2412"

# Debug: Check Chromedriver existence
print("Check chromedriver exists:", os.path.exists("/usr/bin/chromedriver"))

# Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"

    # Use webdriver-manager to get the correct Chromedriver
    service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=chrome_options)

def login_to_panel(driver):
    driver.get(IVAS_URL)
    time.sleep(3)
    driver.find_element(By.NAME, "username").send_keys(IVAS_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(IVAS_PASSWORD + Keys.RETURN)
    time.sleep(5)

def get_latest_otp(driver):
    driver.get("https://ivasms.com/panel/inbox")
    time.sleep(3)
    # Fallback to a more robust selector if .otp-message-class fails
    try:
        otp_text = driver.find_element(By.CSS_SELECTOR, ".otp-message-class").text
    except:
        otp_text = driver.find_element(By.XPATH, "//*[contains(text(), 'OTP')]").text
    return otp_text

def format_otp_message(raw_otp):
    return f"🔔 *New OTP Received*\n\n{raw_otp}"

def send_to_telegram(msg):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode='Markdown')

def otp_bot_loop():
    driver = start_driver()
    try:
        login_to_panel(driver)
        while True:
            otp = get_latest_otp(driver)
            message = format_otp_message(otp)
            send_to_telegram(message)
            time.sleep(30)
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

# Start the Selenium bot in a background thread
threading.Thread(target=otp_bot_loop, daemon=True).start()

# Flask app to keep Koyeb web service running
app = Flask(__name__)

@app.route('/')
def home():
    return '🔒 OTP Bot is running on Koyeb!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
