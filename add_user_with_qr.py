import pyotp
import qrcode
import mysql.connector
from pathlib import Path

# connect MySQL
conn = mysql.connector.connect(
    host="mysql", user="root", password="1234", database="test324"
)
cursor = conn.cursor()

# email and password
email = "kk@dome.tu.ac.th"
password = "test1"
otp_secret = pyotp.random_base32()

# to DB
cursor.execute(
    "INSERT INTO users (email, password, otp_secret) VALUES (%s, %s, %s)",
    (email, password, otp_secret)
)
conn.commit()

# gen QR Code
uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=email, issuer_name="DSI324 App")
img = qrcode.make(uri)
img_path = Path(f"qr_{email.replace('@', '_at_')}.png")
img.save(img_path)

print(f"✅ Account Create!\nSecret: {otp_secret}\nQR saved: {img_path}")

cursor.close()
conn.close()
