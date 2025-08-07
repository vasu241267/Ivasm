import time
import threading
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from telegram import Bot
from flask import Flask

# Configuration
TELEGRAM_BOT_TOKEN = '8049406807:AAGhuUh9fOm5wt7OvTobuRngqY0ZNBMxlHE'
TELEGRAM_CHAT_ID = '-1002311125652'
IVAS_URL = 'https://ivasms.com/panel/login'
IVAS_USERNAME = 'imdigitalvasu@gmail.com'
IVAS_PASSWORD = '@Vasu2412'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Flask app for web service (required by Koyeb)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ OTP bot is running!"

def start_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options)

def login_to_panel(driver):
    driver.get(IVAS_URL)
    time.sleep(3)
    driver.find_element(By.NAME, "username").send_keys(IVAS_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(IVAS_PASSWORD + Keys.RETURN)
    time.sleep(5)

def get_latest_otp(driver):
    driver.get("https://ivasms.com/panel/inbox")
    time.sleep(3)
    try:
        otp_element = driver.find_element(By.CSS_SELECTOR, ".otp-message-class")  # Replace with actual selector
        return otp_element.text
    except:
        return None

def format_otp_message(raw_otp):
    return f"🔔 *New OTP Received*\n\n{raw_otp}"

def send_to_telegram(msg):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode='Markdown')

def otp_bot_loop():
    driver = start_driver()
    last_otp = None
    try:
        login_to_panel(driver)
        while True:
            otp = get_latest_otp(driver)
            if otp and otp != last_otp:
                send_to_telegram(format_otp_message(otp))
                last_otp = otp
            time.sleep(30)
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    threading.Thread(target=otp_bot_loop).start()
    app.run(host="0.0.0.0", port=8080)
