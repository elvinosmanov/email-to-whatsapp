# Email to WhatsApp Monitor

Automatically forwards shift schedule emails from Gmail to WhatsApp group.

## For Windows Users (No Python Required)

### Download & Run:
1. Download `EmailToWhatsApp.exe` from the [Releases](../../releases) page
2. Make sure Google Chrome is installed
3. Double-click `EmailToWhatsApp.exe` to run
4. Scan QR code with your phone when prompted
5. The program will run continuously

### Configuration:
Edit these lines in the .py file before building, or edit the .exe with a text editor:
- Email: `bakugan192@gmail.com`
- Email Password: `euufouuulhfjxkwx`
- WhatsApp Group: `Shift schedule`

## Requirements:
- Windows 8 or higher
- Google Chrome browser installed
- Internet connection
- WhatsApp account

## How It Works:
1. Monitors Gmail inbox and spam folder
2. Looks for emails with "Shift Schedule" in subject
3. Downloads image attachments
4. Sends to WhatsApp group with caption
5. Checks every 20 seconds (configurable)

## Troubleshooting:
- **ChromeDriver error**: Make sure Chrome is installed
- **Email login failed**: Check email and app password
- **WhatsApp not opening**: Install Chrome browser
- **Group not found**: Make sure group name matches exactly
