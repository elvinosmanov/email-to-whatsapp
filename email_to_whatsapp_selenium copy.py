# email_to_whatsapp_selenium.py
import imaplib
import email
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuration
EMAIL_PROVIDER = "gmail"
EMAIL_USER = "bakugan192@gmail.com"
EMAIL_PASSWORD = "euufouuulhfjxkwx"
WHATSAPP_PHONE = "+994554261998"
CHECK_INTERVAL = 20  # seconds (reduced for testing)

# IMAP server settings
IMAP_SERVERS = {
    "gmail": "imap.gmail.com",
    "mailru": "imap.mail.ru",
    "yahoo": "imap.mail.yahoo.com",
    "outlook": "imap-mail.outlook.com",
    "yandex": "imap.yandex.com"
}

# Global variables
mail_connection = None
browser = None

def setup_browser():
    """Setup Chrome browser for WhatsApp Web"""
    global browser

    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=./whatsapp_session")
    chrome_options.add_argument("--profile-directory=Default")

    print("🌐 Opening Chrome browser...")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://web.whatsapp.com")

    print("📱 Please scan QR code with your phone if needed...")
    print("   Waiting 20 seconds for login...")
    time.sleep(20)

    return browser

def connect_to_email():
    """Establish and maintain email connection"""
    global mail_connection
    try:
        imap_server = IMAP_SERVERS.get(EMAIL_PROVIDER, "imap.gmail.com")
        print(f"📧 Connecting to {EMAIL_PROVIDER.upper()} as: {EMAIL_USER}")
        mail_connection = imaplib.IMAP4_SSL(imap_server)
        mail_connection.login(EMAIL_USER, EMAIL_PASSWORD)
        print("✅ Email login successful! Staying connected...")
        return True
    except Exception as e:
        print(f"❌ Email connection error: {e}")
        mail_connection = None
        return False

def send_to_whatsapp_selenium(filepath):
    """Send image to WhatsApp using Selenium"""
    global browser

    try:
        filename = os.path.basename(filepath)
        file_ext = os.path.splitext(filename)[1].lower()

        # Convert PNG to JPG if needed
        if file_ext == '.png':
            print(f"🔄 Converting PNG to JPG...")
            from PIL import Image
            img = Image.open(filepath)
            rgb_img = img.convert('RGB')
            jpg_path = filepath.replace('.png', '.jpg')
            rgb_img.save(jpg_path, 'JPEG', quality=95)
            filepath = jpg_path
            filename = os.path.basename(jpg_path)

        abs_filepath = os.path.abspath(filepath)
        print(f"📤 Sending to WhatsApp: {filename}")

        wait = WebDriverWait(browser, 30)

        # Check if we're already in the correct chat
        current_url = browser.current_url
        if 'Shift schedule' not in browser.title and '/chat/' not in current_url:
            need_search = True
        else:
            try:
                header = browser.find_element(By.XPATH, '//span[contains(text(), "Shift schedule")]')
                print("✓ Already in correct chat")
                need_search = False
            except:
                need_search = True

        if need_search:
            print("🔍 Searching for group 'Shift schedule'...")

            try:
                search_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
            except:
                search_box = browser.find_element(By.XPATH, '//div[@title="Search input textbox"]')

            search_box.click()
            time.sleep(0.3)
            search_box.send_keys(Keys.COMMAND + 'a')
            time.sleep(0.1)
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.3)
            search_box.send_keys("Shift schedule")
            print("✓ Typed group name")
            time.sleep(1)

            try:
                group_chat = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//span[@title="Shift schedule"]'))
                )
                group_chat.click()
                print("✓ Opened group chat")
                time.sleep(1)
            except:
                print("⚠️  Could not find group 'Shift schedule'")
                first_result = browser.find_element(By.XPATH, '//div[@role="listitem"]')
                first_result.click()
                time.sleep(1)

        # Click attachment button
        print("📎 Looking for attachment button...")
        attachment_btn = None
        attachment_selectors = [
            (By.XPATH, '//div[@title="Attach"]'),
            (By.XPATH, '//button[@aria-label="Attach"]'),
            (By.XPATH, '//span[@data-icon="plus"]'),
        ]

        for by, selector in attachment_selectors:
            try:
                attachment_btn = browser.find_element(by, selector)
                if attachment_btn and attachment_btn.is_displayed():
                    attachment_btn.click()
                    print("✓ Clicked attachment button")
                    time.sleep(1)
                    break
            except:
                continue

        # Find Photos & Videos input
        print("🖼️  Looking for Photos & Videos input...")
        time.sleep(0.5)

        file_inputs = browser.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
        photo_input = None
        for inp in file_inputs:
            accept = inp.get_attribute('accept') or ''
            if 'video' in accept and 'image' in accept:
                photo_input = inp
                break

        if photo_input:
            print("✓ Found Photos & Videos input")
            photo_input.send_keys(abs_filepath)
            print("✓ File selected")

        # Wait for preview and send
        print("⏳ Waiting for preview...")
        time.sleep(3)

        print("📤 Looking for send button...")

        # Try multiple approaches to find and click send button
        send_clicked = False

        # Method 1: Find by new data-icon (wds-ic-send-filled)
        try:
            send_icon = browser.find_element(By.CSS_SELECTOR, 'span[data-icon="wds-ic-send-filled"]')
            send_btn = send_icon.find_element(By.XPATH, './ancestor::button')
            send_btn.click()
            print("✅ Sent to WhatsApp group! (Method 1)")
            send_clicked = True
        except Exception as e:
            print(f"   Method 1 failed: {e}")

        # Method 2: Click icon directly with JavaScript
        if not send_clicked:
            try:
                send_icon = browser.find_element(By.CSS_SELECTOR, 'span[data-icon="wds-ic-send-filled"]')
                browser.execute_script("arguments[0].parentElement.click();", send_icon)
                print("✅ Sent to WhatsApp group! (Method 2)")
                send_clicked = True
            except Exception as e:
                print(f"   Method 2 failed: {e}")

        # Method 3: Find any button with send icon title
        if not send_clicked:
            try:
                send_btn = browser.find_element(By.XPATH, '//button[.//title[contains(text(), "send")]]')
                send_btn.click()
                print("✅ Sent to WhatsApp group! (Method 3)")
                send_clicked = True
            except Exception as e:
                print(f"   Method 3 failed: {e}")

        # Method 4: Press Enter key
        if not send_clicked:
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                ActionChains(browser).send_keys(Keys.ENTER).perform()
                print("✅ Sent to WhatsApp group! (Method 4 - Enter key)")
                send_clicked = True
            except Exception as e:
                print(f"   Method 4 failed: {e}")

        if not send_clicked:
            print("⚠️  Could not find send button, please click manually")
            time.sleep(10)
        else:
            time.sleep(1)

    except Exception as e:
        print(f"❌ WhatsApp send error: {e}")
        import traceback
        traceback.print_exc()

def process_single_email(mail_conn, email_id, folder_name):
    """Process a single email"""
    try:
        _, msg_data = mail_conn.fetch(email_id, "(RFC822)")

        if not msg_data or not msg_data[0]:
            print(f"⚠️  Could not fetch email from {folder_name}")
            return

        email_body = email.message_from_bytes(msg_data[0][1])

        print(f"\n📋 Email from {folder_name}:")
        print(f"   Subject: {email_body.get('Subject', 'No subject')}")
        print(f"   From: {email_body.get('From', 'Unknown')}")

        has_attachment = False
        for part in email_body.walk():
            filename = part.get_filename()
            if filename:
                has_attachment = True
                filepath = os.path.join(os.getcwd(), filename)

                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        with open(filepath, 'wb') as f:
                            f.write(payload)

                        print(f"📥 Downloaded: {filename}")
                        send_to_whatsapp_selenium(filepath)

                        time.sleep(1)
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        jpg_path = filepath.replace('.png', '.jpg')
                        if os.path.exists(jpg_path) and jpg_path != filepath:
                            os.remove(jpg_path)

                        print("✓ Attachment processed\n")
                except Exception as e:
                    print(f"❌ Error processing attachment: {e}")

        if not has_attachment:
            print("⚠️  Email has no attachments")

        mail_conn.store(email_id, '+FLAGS', '\\Seen')
        print("✓ Email marked as read\n")

    except Exception as e:
        print(f"❌ Error processing email: {e}")

def check_emails():
    """Check emails using existing connection"""
    global mail_connection

    try:
        if mail_connection is None:
            if not connect_to_email():
                return

        # Process inbox
        mail_connection.select("inbox")
        _, inbox_messages = mail_connection.search(None, 'UNSEEN SUBJECT "Shift Schedule"')
        if inbox_messages[0]:
            print(f"📬 Found {len(inbox_messages[0].split())} new email(s) in Inbox")
            for email_id in inbox_messages[0].split():
                process_single_email(mail_connection, email_id, "inbox")

        # Process spam
        try:
            mail_connection.select('[Gmail]/Spam')
            _, spam_messages = mail_connection.search(None, 'UNSEEN SUBJECT "Shift Schedule"')
            if spam_messages[0]:
                print(f"🗑️  Found {len(spam_messages[0].split())} new email(s) in Spam")
                for email_id in spam_messages[0].split():
                    process_single_email(mail_connection, email_id, "spam")
        except:
            pass

    except (imaplib.IMAP4.abort, imaplib.IMAP4.error) as e:
        print(f"⚠️  Connection lost: {e}. Reconnecting...")
        mail_connection = None
        connect_to_email()
    except Exception as e:
        print(f"❌ Error: {e}")

# Main program
print("=" * 60)
print("📧 Email → WhatsApp Monitor (Selenium Version)")
print("=" * 60)
print(f"Email: {EMAIL_USER}")
print(f"WhatsApp: {WHATSAPP_PHONE}")
print(f"Check interval: {CHECK_INTERVAL} seconds")
print("=" * 60)

try:
    setup_browser()
    connect_to_email()

    print("\n✅ Setup complete! Monitoring started...\n")

    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for new emails...")
        check_emails()
        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n\n👋 Stopping monitor...")
    if browser:
        browser.quit()
    print("Goodbye!")
except Exception as e:
    print(f"\n❌ Fatal error: {e}")
    if browser:
        browser.quit()
