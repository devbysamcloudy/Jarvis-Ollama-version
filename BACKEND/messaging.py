import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# ─── EMAIL (Gmail SMTP) ──────────────────────────────────────────────────────
# Setup: Enable 2FA on Gmail → Google Account → Security → App Passwords → create one
# Add to .env: GMAIL_ADDRESS and GMAIL_APP_PASSWORD

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(to, subject, body):
    """Send an email via Gmail SMTP."""
    try:
        if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
            return "Email not configured. Add GMAIL_ADDRESS and GMAIL_APP_PASSWORD to .env"

        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return f"📧 Email sent to {to}\nSubject: {subject}"

    except smtplib.SMTPAuthenticationError:
        return "Email auth failed. Check GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env"
    except Exception as e:
        return f"Email error: {str(e)}"


# ─── WHATSAPP (Twilio) ───────────────────────────────────────────────────────
# Setup: twilio.com/try-twilio → free trial → WhatsApp Sandbox
# Add to .env: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM
# TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886" (Twilio sandbox number)
# Recipient must first send "join <sandbox-word>" to the sandbox number

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")


def send_whatsapp(to_number, message):
    """Send a WhatsApp message via Twilio."""
    try:
        try:
            from twilio.rest import Client
        except ImportError:
            return "Twilio not installed. Run: pip install twilio"

        if not TWILIO_SID or not TWILIO_TOKEN:
            return "WhatsApp not configured. Add TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN to .env"

        # Normalize number
        if not to_number.startswith("+"):
            to_number = "+" + to_number
        to_whatsapp = f"whatsapp:{to_number}"

        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=to_whatsapp,
        )

        return f"💬 WhatsApp sent to {to_number}\nSID: {msg.sid}"

    except Exception as e:
        return f"WhatsApp error: {str(e)}"


# ─── INSTAGRAM (Browser Automation via pyautogui + webbrowser) ──────────────
# Note: Instagram's official API does not support sending DMs from personal accounts.
# This uses pywhatkit's Instagram module OR selenium as a fallback.
# Requires: pip install selenium webdriver-manager
# The browser will open and automate the DM — keep the window visible.

def send_instagram_dm(username, message):
    """Send an Instagram DM by automating the browser."""
    try:
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            return "Selenium not installed. Run: pip install selenium webdriver-manager"

        INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
        INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

        if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
            return "Instagram not configured. Add INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD to .env"

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        # Uncomment below for headless (no visible browser window):
        # options.add_argument("--headless")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        wait = WebDriverWait(driver, 15)

        # Login
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys(INSTAGRAM_USERNAME)
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(INSTAGRAM_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Dismiss popups
        try:
            not_now = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']")))
            not_now.click()
            time.sleep(2)
        except Exception:
            pass

        try:
            not_now2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not now']")))
            not_now2.click()
            time.sleep(2)
        except Exception:
            pass

        # Navigate to DM with user
        driver.get(f"https://www.instagram.com/direct/new/")
        time.sleep(3)

        search = wait.until(EC.presence_of_element_located((By.NAME, "queryBox")))
        search.send_keys(username)
        time.sleep(2)

        # Select user from results
        user_result = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(text(), '{username}')]")
        ))
        user_result.click()
        time.sleep(1)

        # Click Next
        next_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[text()='Next' or text()='Chat']")
        ))
        next_btn.click()
        time.sleep(2)

        # Type and send message
        msg_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//textarea[@placeholder='Message...'] | //div[@aria-label='Message']")
        ))
        msg_box.send_keys(message)
        msg_box.send_keys(Keys.RETURN)
        time.sleep(2)

        driver.quit()
        return f"📸 Instagram DM sent to @{username}"

    except Exception as e:
        return f"Instagram DM error: {str(e)}"