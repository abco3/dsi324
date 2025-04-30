import streamlit as st
import time
from utils.db import check_user_credentials

# Login page
def login_page():
    st.title("เข้าสู่ระบบ")

    if "logging_in" not in st.session_state:
        st.session_state.logging_in = False

    # Form section
    with st.form("login_form"):
        
        email = st.text_input("อีเมล", disabled=st.session_state.logging_in)
        password = st.text_input("รหัสผ่าน", type="password", disabled=st.session_state.logging_in)
        otp_code = st.text_input("รหัส OTP", type="password", disabled=st.session_state.logging_in)

        if not st.session_state.logging_in:
            submit = st.form_submit_button("เข้าสู่ระบบ")
        else:
            st.markdown("")
            submit = False

    # Handle login
    if submit:
        if '@hvbma.or.th' not in email:
            st.error("อีเมลไม่ถูกต้อง")
        elif not (email and password and otp_code):
            st.error("โปรดระบุ อีเมล รหัสผ่าน และรหัส OTP")
        else:
            ok, role = check_user_credentials(email, password, otp_code)
            if not ok:
                st.error("อีเมล รหัสผ่าน หรือรหัส OTP ไม่ถูกต้อง")
            else:
                # cant duplicate login
                local_part = email.split('@')[0]
                st.session_state.user_email = email 
                st.session_state.username = local_part
                st.session_state.role = role
                st.session_state.logging_in = True
                st.rerun()

    # login success
    elif st.session_state.logging_in:
        st.success("✅ เข้าสู่ระบบสำเร็จ ...")
        time.sleep(1)
        st.session_state.logged_in = True
        st.session_state.page = "หน้าหลัก"
        st.session_state.logging_in = False
        st.rerun()