import base64, hashlib, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SECRET_FILE = "secret.enc"

def make_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_data(token, chat_id, password):
    key = make_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    data = json.dumps({"token": token, "chat_id": chat_id}).encode()
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(cipher.iv + encrypted)

def decrypt_data(password):
    key = make_key(password)
    raw = base64.b64decode(open(SECRET_FILE, "rb").read())
    iv = raw[:16]
    encrypted = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    try:
        data = unpad(cipher.decrypt(encrypted), AES.block_size)
        obj = json.loads(data)
        return obj["token"], obj["chat_id"]
    except:
        print("❌ Wrong password.")
        exit()
