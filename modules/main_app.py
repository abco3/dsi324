import streamlit as st
from modules.login import login_page
from modules.otp import otp_page
from modules.home import home_page
from modules.search_volunteer import search_volunteer_page
from modules.dashboard import dashboard_page
from modules.check_volunteer import check_volunteer_page
from modules.data_entry import data_entry_page
from modules.upload_report import upload_reports_page
from modules.upload_volunteer import upload_volunteers_page
from modules.create_account import create_account_page
from modules.weather import weather_page

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
    if role in ["user", "admin"]:
        page_options.extend(["แดชบอร์ด", "สภาพอากาศ", "ค้นหา", "ตรวจสอบ", "อัปโหลดรายงาน"])

    #temporary add page
    if st.session_state.page == "กรอกข้อมูล":
        insert_index = page_options.index("ค้นหา") + 1
        page_options.insert(insert_index, "กรอกข้อมูล")

    if role == "visitor":
        page_options.extend(["แดชบอร์ด", "สภาพอากาศ"])
    if role == "admin":
        page_options.extend(["อัปโหลดอาสาสมัคร", "สร้างบัญชี"])

    # selectbox check
    if st.session_state.page not in page_options:
        st.session_state.page = "หน้าหลัก"  # default

    selected_page = st.sidebar.selectbox("เมนู", page_options, index=page_options.index(st.session_state.page))
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    # Routing
    if st.session_state.page == "หน้าหลัก":
        home_page()

    elif st.session_state.page == "กรอกข้อมูล":
        if role in ["user", "admin"] and "selected_volunteer" in st.session_state:
            data_entry_page()
        else:
            st.warning("ไม่สามารถเข้าถึงหน้านี้ได้โดยตรง")
            st.session_state.page = "หน้าหลัก"
            st.rerun()

    elif st.session_state.page == "แดชบอร์ด":
        if role in ["visitor", "admin", "user"]:
            dashboard_page()

    elif st.session_state.page == "ค้นหา":
        if role in ["user", "admin"]:
            search_volunteer_page()

    elif st.session_state.page == "สร้างบัญชี":
        if role == "admin":
            create_account_page()

    elif st.session_state.page == "ตรวจสอบ":
        if role in ["user", "admin"]:
            check_volunteer_page()
    
    elif st.session_state.page == "อัปโหลดรายงาน":
        if role in ["user", "admin"]:
            upload_reports_page()
    
    elif st.session_state.page == "อัปโหลดอาสาสมัคร":
        if role == "admin":
            upload_volunteers_page()
            
    elif st.session_state.page == "สภาพอากาศ":
        if role in ["visitor", "admin", "user"]:
            weather_page()