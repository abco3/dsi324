import mysql.connector
import pyotp
import qrcode
import os
from getpass import getpass
from datetime import datetime
from pathlib import Path

# setting connect
db_config = {
    "host": "mysql",
    "user": "root",
    "password": "1234",
    "database": "test324"
}

def connect_db():
    return mysql.connector.connect(**db_config)

def create_acc():
    print("🔐Create Account")
    email = input("Enter email: ")
    password = input("Enter password: ")
    role = input("Enter role: ")

    # create OTP secret and URI
    otp_secret = pyotp.random_base32()
    otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=email, issuer_name="DSI324 App")

    # store to DB
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, password, role, otp_secret, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (email, password, role, otp_secret, datetime.now()))
    conn.commit()

    # create and store: qr_img
    #path
    qr_dir = Path(__file__).resolve().parent / "qr_img"
    qr_dir.mkdir(exist_ok=True)
    qr_path = qr_dir / f"qr_{email.replace('@', '_at_')}.png"

    #create
    img = qrcode.make(otp_uri)
    img.save(qr_path)  

    print("✅Account created!")
    print(f"Secret: {otp_secret}")
    print(f"QR saved to: {qr_path.resolve()}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_acc()