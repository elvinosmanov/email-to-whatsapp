# email_to_whatsapp.py
import pywhatkit as kit
import imaplib
import email
import os
import time
from datetime import datetime
import pyautogui

# Configuration
# Supported providers: gmail, mailru, yahoo, outlook
EMAIL_PROVIDER = "gmail"  # Change this to: gmail, mailru, yahoo, outlook, yandex
EMAIL_USER = "bakugan192@gmail.com"  # Your Gmail account
EMAIL_PASSWORD = "euufouuulhfjxkwx"  # Gmail App Password (spaces removed)
WHATSAPP_GROUP_NAME = "Shift schedule"
WHATSAPP_PHONE = "+994554261998"
CHECK_INTERVAL = 60  # seconds

# IMAP server settings
IMAP_SERVERS = {
    "gmail": "imap.gmail.com",
    "mailru": "imap.mail.ru",
    "yahoo": "imap.mail.yahoo.com",
    "outlook": "imap-mail.outlook.com",
    "yandex": "imap.yandex.com"
}

# Global mail connection
mail_connection = None

def connect_to_email():
    """Establish and maintain email connection"""
    global mail_connection
    try:
        imap_server = IMAP_SERVERS.get(EMAIL_PROVIDER, "imap.gmail.com")
        print(f"Connecting to {EMAIL_PROVIDER.upper()} as: {EMAIL_USER}")
        mail_connection = imaplib.IMAP4_SSL(imap_server)
        mail_connection.login(EMAIL_USER, EMAIL_PASSWORD)
        print("✓ Login successful! Staying connected...")
        return True
    except Exception as e:
        print(f"Connection error: {e}")
        mail_connection = None
        return False

def check_emails():
    """Check emails using existing connection"""
    global mail_connection

    try:
        # Reconnect if needed
        if mail_connection is None:
            if not connect_to_email():
                return

        # Select inbox and search
        mail_connection.select("inbox")
        _, messages = mail_connection.search(None, 'UNSEEN SUBJECT "Shift Schedule"')

        if not messages[0]:
            return  # No new messages

        for email_id in messages[0].split():
            # Get email
            _, msg_data = mail_connection.fetch(email_id, "(RFC822)")
            email_body = email.message_from_bytes(msg_data[0][1])

            # Find attachment
            for part in email_body.walk():
                if part.get_filename():
                    filename = part.get_filename()
                    filepath = os.path.join(os.getcwd(), filename)

                    # Save attachment
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    print(f"📥 Downloaded: {filename}")

                    # Send to WhatsApp
                    send_to_whatsapp(filepath)

                    # Clean up
                    time.sleep(5)
                    if os.path.exists(filepath):
                        os.remove(filepath)

                    # Mark as read
                    mail_connection.store(email_id, '+FLAGS', '\\Seen')

    except (imaplib.IMAP4.abort, imaplib.IMAP4.error) as e:
        print(f"Connection lost: {e}. Reconnecting...")
        mail_connection = None
        connect_to_email()
    except Exception as e:
        print(f"Error: {e}")

def send_to_whatsapp(filepath):
    """Send image to WhatsApp using manual browser control"""
    try:
        filename = os.path.basename(filepath)
        file_ext = os.path.splitext(filename)[1].lower()

        # Convert PNG to JPG if needed
        if file_ext == '.png':
            print(f"Converting PNG to JPG...")
            from PIL import Image
            img = Image.open(filepath)
            rgb_img = img.convert('RGB')
            jpg_path = filepath.replace('.png', '.jpg')
            rgb_img.save(jpg_path, 'JPEG', quality=95)
            filepath = jpg_path
            filename = os.path.basename(jpg_path)
            file_ext = '.jpg'

        # Get absolute path
        abs_filepath = os.path.abspath(filepath)

        print(f"📤 Sending to WhatsApp: {filename}")
        print(f"   Opening WhatsApp Web...")

        # Open WhatsApp Web
        import webbrowser
        webbrowser.open(f'https://web.whatsapp.com/send?phone={WHATSAPP_PHONE.replace("+", "")}')

        # Wait for page to load
        print("   Waiting 15 seconds for WhatsApp Web to load...")
        time.sleep(15)

        # Click on attachment button (paperclip icon)
        print("   Looking for attachment button...")
        time.sleep(2)

        # Press Tab multiple times to reach attachment button, then Enter
        # Alternative: use pyautogui to click
        try:
            # Method 1: Try keyboard navigation
            pyautogui.press('tab', presses=5, interval=0.3)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)

            # Type file path in file dialog
            print(f"   Typing file path: {abs_filepath}")
            pyautogui.write(abs_filepath, interval=0.05)
            time.sleep(1)
            pyautogui.press('enter')

            # Wait for preview
            print("   Waiting for image preview...")
            time.sleep(3)

            # Press Enter to send
            print("   Sending...")
            pyautogui.press('enter')
            time.sleep(2)

            print("✅ Sent to WhatsApp!")

        except Exception as e:
            print(f"⚠️  Automation failed: {e}")
            print(f"   Please manually send: {abs_filepath}")

    except Exception as e:
        print(f"❌ WhatsApp error: {e}")

# Main loop
print("=" * 60)
print("📧 Email → WhatsApp Monitor Starting...")
print("=" * 60)
print(f"Email: {EMAIL_USER}")
print(f"WhatsApp: {WHATSAPP_PHONE}")
print(f"Check interval: {CHECK_INTERVAL} seconds")
print("=" * 60)

# Initial connection
connect_to_email()

while True:
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking for new emails...")
    check_emails()
    time.sleep(CHECK_INTERVAL)