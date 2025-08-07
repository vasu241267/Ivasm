from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from telegram import Bot
import threading
from flask import Flask

# Config (Move to environment variables in prod)
TELEGRAM_BOT_TOKEN = '7311288614:AAHecPFp5NnBrs4dJiR_l9lh1GB3zBAP_Yo'
TELEGRAM_CHAT_ID = '-1002445692794'
IVAS_URL = 'https://ivasms.com/panel/login'
IVAS_USERNAME = 'imdigitalvasu@gmail.com'
IVAS_PASSWORD = '@Vasu2412'

# Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"

    # Correct path
    service = Service("/usr/lib/chromium-browser/chromedriver")

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
    otp_text = driver.find_element(By.CSS_SELECTOR, ".otp-message-class").text  # Update this!
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
