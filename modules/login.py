import streamlit as st
import time
from utils.db import verify_user_password


def login_page():
    st.title("เข้าสู่ระบบ")

    if "logging_in" not in st.session_state:
        st.session_state.logging_in = False

    if "login_success" not in st.session_state:
        st.session_state.login_success = False

    if st.session_state.login_success:
        st.success("✅ เข้าสู่ระบบสำเร็จ ...")
        time.sleep(1)
        st.session_state.page = "otp"
        st.rerun()

    if not st.session_state.logging_in:
        with st.form("login_form"):
            email = st.text_input("อีเมล")
            password = st.text_input("รหัสผ่าน", type="password")
            submit = st.form_submit_button("เข้าสู่ระบบ")

            if submit:
                st.session_state.logging_in = True
                if '@hvbma.or.th' not in email:
                    st.error("อีเมลไม่ถูกต้อง")
                    st.session_state.logging_in = False
                elif not (email and password):
                    st.error("โปรดระบุอีเมลและรหัสผ่าน")
                    st.session_state.logging_in = False
                else:
                    valid, role = verify_user_password(email, password)
                    if not valid:
                        st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")
                        st.session_state.logging_in = False
                    else:
                        # success
                        st.session_state.temp_email = email
                        st.session_state.temp_role = role
                        st.session_state.login_success = True
                        st.rerun() 