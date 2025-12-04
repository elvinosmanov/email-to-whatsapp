import imaplib
import socket

EMAIL_USER = "elvinn.osmnanov@gmail.com"
EMAIL_PASSWORD = "uzukoopafyohkckl"

print("=" * 50)
print("Gmail IMAP Diagnostic Tool")
print("=" * 50)
print(f"\nAccount: {EMAIL_USER}")
print(f"Password length: {len(EMAIL_PASSWORD)}")
print(f"Password (first 4 chars): {EMAIL_PASSWORD[:4]}...")

# Test DNS resolution
print("\n1. Testing DNS resolution for imap.gmail.com...")
try:
    ip = socket.gethostbyname("imap.gmail.com")
    print(f"   ✓ Resolved to: {ip}")
except Exception as e:
    print(f"   ✗ DNS Error: {e}")

# Test connection
print("\n2. Testing SSL connection to imap.gmail.com:993...")
try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    print("   ✓ SSL connection established")

    # Test login
    print("\n3. Testing login...")
    try:
        result = mail.login(EMAIL_USER, EMAIL_PASSWORD)
        print(f"   ✓ Login successful! Result: {result}")

        # List folders
        print("\n4. Listing folders...")
        status, folders = mail.list()
        print(f"   ✓ Found {len(folders)} folders")

        mail.logout()
        print("\n" + "=" * 50)
        print("SUCCESS! Your Gmail IMAP is working!")
        print("=" * 50)

    except imaplib.IMAP4.error as e:
        print(f"   ✗ Login failed: {e}")
        print("\n" + "=" * 50)
        print("ISSUE: App Password is invalid")
        print("=" * 50)
        print("\nPossible causes:")
        print("1. App Password was not generated correctly")
        print("2. App Password was revoked")
        print("3. This is a Google Workspace account with restrictions")
        print("4. Less secure app access is still disabled")
        print("\nPlease:")
        print("- Go to: https://myaccount.google.com/apppasswords")
        print("- Delete the existing password")
        print("- Generate a NEW password")
        print("- Make sure you copy it exactly")

except Exception as e:
    print(f"   ✗ Connection error: {e}")
