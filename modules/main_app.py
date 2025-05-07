import streamlit as st
from modules.login import login_page
from modules.otp import otp_page
from modules.data_entry import data_entry_page
from modules.view_reports import view_reports_page
from modules.create_account import create_account_page
from modules.search_volunteer import search_volunteer_page
from modules.view_volunteer_data import view_volunteer_data_page

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:

        if st.session_state.get("page") == "otp":
            otp_page()
        else:
            login_page()
        return

    if 'page' not in st.session_state:
        st.session_state.page = "หน้าหลัก"

    role = st.session_state.get("role", "")

    # create menu
    page_options = ["หน้าหลัก"]
    if role in ["admin", "dev"]:
        page_options.extend(["รายงาน", "ค้นหา", "ตรวจสอบ"])

    #temporary add page
    if st.session_state.page == "กรอกข้อมูล":
        insert_index = page_options.index("ค้นหา") + 1
        page_options.insert(insert_index, "กรอกข้อมูล")

    if role == "user":
        page_options.append("รายงาน")
    if role == "dev":
        page_options.append("สร้างบัญชี")

    # selectbox check
    if st.session_state.page not in page_options:
        st.session_state.page = "หน้าหลัก"  # default

    selected_page = st.sidebar.selectbox("เมนู", page_options, index=page_options.index(st.session_state.page))
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    # Routing
    if st.session_state.page == "หน้าหลัก":
        st.title(f"ยินดีต้อนรับคุณ {st.session_state.username}")
        st.write("คุณเข้าสู่ระบบเรียบร้อย")
        st.write("โปรดเลือกหน้าที่ต้องการจากเมนูทางด้านซ้าย")

        if st.session_state.get("confirm_logout", False):
            st.warning("ต้องการออกจากระบบใช่หรือไม่")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ ใช่", key="confirm_yes", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
            with col2:
                if st.button("❌ ไม่", key="confirm_no", use_container_width=True):
                    st.session_state.confirm_logout = False
                    st.rerun()
        else:
            if st.button("ออกจากระบบ", key="logout_btn"):
                st.session_state.confirm_logout = True
                st.rerun()

    elif st.session_state.page == "กรอกข้อมูล":
        if role in ["admin", "dev"] and "selected_volunteer" in st.session_state:
            data_entry_page()
        else:
            st.warning("ไม่สามารถเข้าถึงหน้านี้ได้โดยตรง")
            st.session_state.page = "หน้าหลัก"
            st.rerun()

    elif st.session_state.page == "รายงาน":
        if role in ["admin", "dev", "user"]:
            view_reports_page()

    elif st.session_state.page == "ค้นหา":
        if role in ["admin", "dev"]:
            search_volunteer_page()

    elif st.session_state.page == "สร้างบัญชี":
        if role == "dev":
            create_account_page()

    elif st.session_state.page == "ตรวจสอบ":
        if role in ["admin", "dev"]:
            view_volunteer_data_page()