import streamlit as st
import time
from utils.db import verify_otp


def otp_page():
    st.title("ยืนยันตัวตนด้วยรหัส OTP")

    email = st.session_state.get("temp_email", "")
    role = st.session_state.get("temp_role", "")

    if not email:
        st.warning("กรุณาเข้าสู่ระบบด้วยอีเมลและรหัสผ่านก่อน")
        st.session_state.page = "login"
        st.rerun()

    # Init session states
    if "otp_status" not in st.session_state:
        st.session_state.otp_status = None
    if "otp_attempted" not in st.session_state:
        st.session_state.otp_attempted = False

    # redirect after success
    if st.session_state.otp_status == "success":
        st.success("✅ รหัส OTP ถูกต้อง เข้าสู่หน้าหลัก ...")
        time.sleep(1)
        st.session_state.user_email = email
        st.session_state.username = email.split('@')[0]
        st.session_state.role = role
        st.session_state.logged_in = True
        st.session_state.page = "หน้าหลัก"
        st.rerun()
        return

    # Show OTP Form
    with st.form("otp_form"):
        otp_input = st.text_input("รหัส OTP", type="password")
        submitted = st.form_submit_button("ยืนยัน")

        if submitted:
            st.session_state.otp_attempted = True
            if verify_otp(email, otp_input):
                st.session_state.otp_status = "success"
                st.rerun()
            else:
                st.session_state.otp_status = "error"

        if st.session_state.otp_attempted and st.session_state.otp_status == "error":
            st.error("รหัส OTP ไม่ถูกต้อง")

    # return
    if st.session_state.otp_status not in ["success", None]:
        if st.button("กลับไปหน้าเข้าสู่ระบบ"):
            st.session_state.temp_email = ""
            st.session_state.temp_role = ""
            st.session_state.otp_status = None
            st.session_state.otp_attempted = False
            st.session_state.login_success = False   
            st.session_state.logging_in = False      
            st.session_state.page = "login"
            st.rerun()