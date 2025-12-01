from secure import encrypt_data

token = input("Enter Telegram Bot Token: ").strip()
chat_id = input("Enter Chat ID: ").strip()
password = input("Set Encryption Password: ")

enc = encrypt_data(token, chat_id, password)

open("secret.enc", "wb").write(enc)
print("✔ secret.enc created successfully")
