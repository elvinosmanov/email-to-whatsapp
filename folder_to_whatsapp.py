import pywhatkit as kit
import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCH_FOLDER = os.path.expanduser("~/Desktop/ShiftSchedules")  # Folder to watch
WHATSAPP_PHONE = "+994554261998"  # Your WhatsApp number

# Create folder if it doesn't exist
os.makedirs(WATCH_FOLDER, exist_ok=True)

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath)

        # Only process image files
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            return

        print(f"\n📁 New file detected: {filename}")

        # Wait a moment for file to finish writing
        time.sleep(2)

        # Send to WhatsApp
        try:
            print(f"📤 Sending to WhatsApp...")
            kit.sendwhats_image(
                WHATSAPP_PHONE,
                filepath,
                f"Shift Schedule - {filename}",
                wait_time=15,
                tab_close=True
            )
            print("✅ Sent successfully!")

            # Move to processed folder
            processed_folder = os.path.join(WATCH_FOLDER, "Sent")
            os.makedirs(processed_folder, exist_ok=True)
            new_path = os.path.join(processed_folder, filename)
            os.rename(filepath, new_path)
            print(f"📦 Moved to: {processed_folder}")

        except Exception as e:
            print(f"❌ Error: {e}")

print("="*50)
print("📂 Folder Monitor Started!")
print("="*50)
print(f"Watching folder: {WATCH_FOLDER}")
print(f"WhatsApp number: {WHATSAPP_PHONE}")
print("\n💡 Drop shift schedule files into this folder and they'll be sent automatically!")
print("Press Ctrl+C to stop\n")

# Start watching
event_handler = NewFileHandler()
observer = Observer()
observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("\n\n👋 Stopped monitoring")

observer.join()
