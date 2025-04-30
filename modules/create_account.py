import streamlit as st
import pyotp
import qrcode
import os
from utils.db import connect_db


#Create Account page
def create_account_page():
    st.title("สร้างบัญชี")

    new_email = st.text_input("อีเมล")
    new_password = st.text_input("รหัสผ่าน", type="password")
    new_role = st.selectbox("บทบาท", ["user", "admin", "dev"])

    if st.button("สร้างบัญชี"):
        # OTP Secret
        totp = pyotp.TOTP(pyotp.random_base32())
        otp_secret = totp.secret

        # add to db
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, password, role, otp_secret)
            VALUES (%s, %s, %s, %s)
        """, (new_email, new_password, new_role, otp_secret))
        conn.commit()

        # create QR Code
        otp_uri = totp.provisioning_uri(name=new_email, issuer_name="DSI324 App")
        img = qrcode.make(otp_uri)
        img_path = f"qr_img/qr_{new_email.replace('@', '_at_')}.png"
        os.makedirs("qr_img", exist_ok=True)
        img.save(img_path)

        st.success("✅ สร้างบัญชีสำเร็จ")

        st.markdown("🔎แสกน QR Code นี้ด้วย Google Authenticator🔎")
        st.image(img_path, width=200)