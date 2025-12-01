#!/bin/bash

echo "==============================="
echo "     BACKUP TOOL SETUP"
echo "==============================="

# 1️⃣ STORAGE PERMISSION (automatic yes)
yes | termux-setup-storage
sleep 2

# 2️⃣ UPDATE PACKAGES
pkg update -y
pkg upgrade -y
pkg update -y
pkg install python -y
pkg install clang -y
pkg install rust -y
pkg install cargo -y
pkg install libffi libffi-dev -y
pkg install openssl openssl-tool -y
pkg install openssl-dev -y
pkg install binutils -y

# 4️⃣ INSTALL REQUIRED PYTHON MODULES
pip install --upgrade python-telegram-bot aiofiles requests cryptography --quiet

# 5️⃣ REMOVE OLD STOP FLAG
STOP_FLAG="/sdcard/.stop_backup"
if [ -f "$STOP_FLAG" ]; then
    rm -f "$STOP_FLAG"
fi

# 6️⃣ MAKE SCRIPTS EXECUTABLE
[ -f "backup.py" ] && chmod +x backup.py
[ -f "stop_tool.py" ] && chmod +x stop_tool.py

# 7️⃣ CREATE SHORTCUTS
echo "python $(pwd)/backup.py" > $PREFIX/bin/backup
chmod +x $PREFIX/bin/backup

echo "python $(pwd)/stop_tool.py" > $PREFIX/bin/stopbackup
chmod +x $PREFIX/bin/stopbackup

echo "==============================="
echo "   SETUP COMPLETE ✅"
echo "   Start Command: backup | "
echo "==============================="
