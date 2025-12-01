import os

STOP_FLAG = "/sdcard/.stop_backup"
PASSWORD = "12345"   # same as backup.py

print("=== STOP BACKUP TOOL ===")
p = input("Enter password: ")

if p != PASSWORD:
    print("❌ Wrong password!")
    exit()

open(STOP_FLAG, "w").write("STOP")
print("🛑 Backup will stop safely.")
