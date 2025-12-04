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
whatsapp_logged_in = False

def setup_browser():
    """Setup Chrome browser for WhatsApp Web"""
    global browser

    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=./whatsapp_session")  # Save login session
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
            # We need to search for the group
            need_search = True
        else:
            # We're already in a chat, verify it's the right one
            try:
                # Check if chat header shows "Shift schedule"
                header = browser.find_element(By.XPATH, '//span[contains(text(), "Shift schedule")]')
                print("✓ Already in correct chat")
                need_search = False
            except:
                need_search = True

        if need_search:
            # Step 1: Search for the group
            print("🔍 Searching for group 'Shift schedule'...")

            # Click on search box
            try:
                search_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
            except:
                # Try alternative search box selector
                search_box = browser.find_element(By.XPATH, '//div[@title="Search input textbox"]')

            # Clear any existing text first
            search_box.click()
            time.sleep(0.3)

            # Select all and delete (Cmd+A on Mac, Ctrl+A on others)
            search_box.send_keys(Keys.COMMAND + 'a')  # For Mac
            time.sleep(0.1)
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.3)

            # Type group name
            search_box.send_keys("Shift schedule")
            print("✓ Typed group name")
            time.sleep(1)

            # Step 2: Click on the group from search results
            try:
                group_chat = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//span[@title="Shift schedule"]'))
                )
                group_chat.click()
                print("✓ Opened group chat")
                time.sleep(1)
            except:
                print("⚠️  Could not find group 'Shift schedule'")
                print("   Trying to click first search result...")
                first_result = browser.find_element(By.XPATH, '//div[@role="listitem"]')
                first_result.click()
                time.sleep(1)

        # Step 3: Click attachment button to open menu
        print("📎 Looking for attachment button...")

        attachment_btn = None
        attachment_selectors = [
            (By.XPATH, '//div[@title="Attach"]'),
            (By.XPATH, '//button[@aria-label="Attach"]'),
            (By.XPATH, '//span[@data-icon="plus"]'),
            (By.XPATH, '//span[@data-icon="attach-menu-plus"]'),
            (By.XPATH, '//div[@aria-label="Attach"]'),
            (By.CSS_SELECTOR, 'span[data-icon="plus"]'),
            (By.CSS_SELECTOR, 'span[data-icon="clip"]'),
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

        if not attachment_btn:
            print("⚠️  Could not find attachment button")
            print("🔍 Debug: Looking for all clickable elements...")
            # Try to find any button-like element with attach/plus
            try:
                all_buttons = browser.find_elements(By.TAG_NAME, 'button')
                for btn in all_buttons:
                    aria_label = btn.get_attribute('aria-label') or ''
                    title = btn.get_attribute('title') or ''
                    if 'attach' in aria_label.lower() or 'attach' in title.lower():
                        btn.click()
                        print("✓ Found and clicked attachment button")
                        time.sleep(1)
                        break
            except:
                pass

        # Step 4: Find the Photos & Videos file input
        print("🖼️  Looking for Photos & Videos input...")

        try:
            # After clicking attach, multiple file inputs appear
            # We need the one that accepts images/videos (not stickers)
            time.sleep(0.5)

            file_inputs = browser.find_elements(By.CSS_SELECTOR, 'input[type="file"]')

            # Find the input that accepts image/* and video/*
            photo_input = None
            for inp in file_inputs:
                accept = inp.get_attribute('accept') or ''
                # The photo/video input has accept="image/*,video/mp4,video/3gpp,video/quicktime"
                if 'video' in accept and 'image' in accept:
                    photo_input = inp
                    break

            if photo_input:
                print("✓ Found Photos & Videos input")
                photo_input.send_keys(abs_filepath)
                print("✓ File selected")
            else:
                # Fallback: try any image input
                for inp in file_inputs:
                    accept = inp.get_attribute('accept') or ''
                    if 'image' in accept:
                        print("⚠️  Using alternative image input")
                        inp.send_keys(abs_filepath)
                        print("✓ File selected")
                        break

        except Exception as e:
            print(f"❌ Error selecting file: {e}")
            print("🔍 Available file inputs:")
            file_inputs = browser.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            for i, inp in enumerate(file_inputs):
                print(f"  Input {i}: accept={inp.get_attribute('accept')}")
            raise

        # Step 5: Wait for preview and send
        print("⏳ Waiting for preview...")
        time.sleep(2)

        # Find and click send button
        print("📤 Looking for send button...")

        send_btn = None
        send_selectors = [
            (By.XPATH, '//span[@data-icon="send"]'),
            (By.XPATH, '//button[@aria-label="Send"]'),
            (By.XPATH, '//div[@aria-label="Send"]'),
            (By.CSS_SELECTOR, 'span[data-icon="send"]'),
            (By.XPATH, '//span[@data-testid="send"]'),
        ]

        # Use shorter wait time for send button
        short_wait = WebDriverWait(browser, 5)  # Only wait 5 seconds max

        for by, selector in send_selectors:
            try:
                send_btn = short_wait.until(EC.element_to_be_clickable((by, selector)))
                if send_btn:
                    send_btn.click()
                    print("✅ Sent to WhatsApp group!")
                    time.sleep(1)
                    break
            except:
                continue

        if not send_btn:
            print("⚠️  Could not find send button automatically")
            print("   Please click Send manually in the browser")
            time.sleep(10)  # Give user time to click manually

    except Exception as e:
        print(f"❌ WhatsApp send error: {e}")
        print(f"   File: {abs_filepath}")
        import traceback
        traceback.print_exc()

def check_emails():
    """Check emails using existing connection"""
    global mail_connection

    try:
        # Reconnect if needed
        if mail_connection is None:
            if not connect_to_email():
                return

        # Process inbox emails
        mail_connection.select("inbox")
        _, inbox_messages = mail_connection.search(None, 'UNSEEN SUBJECT "Shift Schedule"')
        if inbox_messages[0]:
            print(f"📬 Found {len(inbox_messages[0].split())} new email(s) in Inbox")
            for email_id in inbox_messages[0].split():
                process_single_email(mail_connection, email_id, "inbox")

        # Process spam folder emails
        try:
            mail_connection.select('[Gmail]/Spam')
            _, spam_messages = mail_connection.search(None, 'UNSEEN SUBJECT "Shift Schedule"')
            if spam_messages[0]:
                print(f"🗑️  Found {len(spam_messages[0].split())} new email(s) in Spam folder")
                for email_id in spam_messages[0].split():
                    process_single_email(mail_connection, email_id, "spam")
        except Exception as e:
            # Spam folder might have different name or not accessible
            pass

    except (imaplib.IMAP4.abort, imaplib.IMAP4.error) as e:
        print(f"⚠️  Connection lost: {e}. Reconnecting...")
        mail_connection = None
        connect_to_email()
    except Exception as e:
        print(f"❌ Error: {e}")

def process_single_email(mail_conn, email_id, folder_name):
    """Process a single email from a specific folder"""
    try:
        # Get email
        _, msg_data = mail_conn.fetch(email_id, "(RFC822)")

        if not msg_data or not msg_data[0]:
            print(f"⚠️  Could not fetch email {email_id} from {folder_name}")
            return

        email_body = email.message_from_bytes(msg_data[0][1])

        # Debug: print email structure
        print(f"\n📋 Email from {folder_name}:")
        print(f"   Subject: {email_body.get('Subject', 'No subject')}")
        print(f"   From: {email_body.get('From', 'Unknown')}")
        print(f"   Content-Type: {email_body.get_content_type()}")
        print(f"   Is multipart: {email_body.is_multipart()}")

        # Find attachment
        has_attachment = False
        part_count = 0
        for part in email_body.walk():
            part_count += 1
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            print(f"   Part {part_count}: {content_type}, Disposition: {content_disposition}")

            filename = part.get_filename()
            if filename:
            try:
                # Get email
                _, msg_data = mail_connection.fetch(email_id, "(RFC822)")

                if not msg_data or not msg_data[0]:
                    print(f"⚠️  Could not fetch email {email_id}")
                    continue

                email_body = email.message_from_bytes(msg_data[0][1])

                # Debug: print email structure
                print(f"📋 Email structure:")
                print(f"   Subject: {email_body.get('Subject', 'No subject')}")
                print(f"   From: {email_body.get('From', 'Unknown')}")
                print(f"   Content-Type: {email_body.get_content_type()}")
                print(f"   Is multipart: {email_body.is_multipart()}")

                # Find attachment
                has_attachment = False
                part_count = 0
                for part in email_body.walk():
                    part_count += 1
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))

                    print(f"   Part {part_count}: {content_type}, Disposition: {content_disposition}")

                    filename = part.get_filename()
                    if filename:
                        has_attachment = True
                        filepath = os.path.join(os.getcwd(), filename)

                        try:
                            # Save attachment
                            payload = part.get_payload(decode=True)
                            if payload:
                                with open(filepath, 'wb') as f:
                                    f.write(payload)

                                print(f"📥 Downloaded: {filename}")

                                # Send to WhatsApp
                                send_to_whatsapp_selenium(filepath)

                                # Clean up
                                time.sleep(1)
                                if os.path.exists(filepath):
                                    os.remove(filepath)
                                # Remove jpg if we converted from png
                                jpg_path = filepath.replace('.png', '.jpg')
                                if os.path.exists(jpg_path) and jpg_path != filepath:
                                    os.remove(jpg_path)

                                print("✓ Attachment processed\n")
                            else:
                                print(f"⚠️  Could not decode attachment: {filename}")
                        except Exception as e:
                            print(f"❌ Error processing attachment {filename}: {e}")

                if not has_attachment:
                    print("⚠️  Email has no attachments, skipping...")

                # Mark as read
                mail_connection.store(email_id, '+FLAGS', '\\Seen')
                print("✓ Email marked as read\n")

            except Exception as e:
                print(f"❌ Error processing email {email_id}: {e}")
                import traceback
                traceback.print_exc()

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

# Setup
try:
    setup_browser()
    connect_to_email()

    print("\n✅ Setup complete! Monitoring started...\n")

    # Main loop
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
