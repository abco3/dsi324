import streamlit as st
import time 
from utils.db import get_all_volunteer_ids_and_names, get_volunteer_by_id

def search_volunteer_page():
    st.title("ค้นหาอาสาสมัคร")

    volunteers = get_all_volunteer_ids_and_names()
    if not volunteers:
        st.warning("ไม่พบรายชื่ออาสาสมัครในระบบ")
        return

    options = [f"{v['volunteer_id']} - {v['first_name']} {v['last_name']}" for v in volunteers]
    selected = st.selectbox("ค้นหาเลขอาสาสมัครหรือชื่อ", options)

    if st.button("ค้นหา"):
        volunteer_id = int(selected.split(" - ")[0])
        volunteer = get_volunteer_by_id(volunteer_id)

        if volunteer:
            st.success("เข้าสู่หน้ากรอกข้อมูล ...")
            st.session_state.selected_volunteer = volunteer
            st.session_state.page = "กรอกข้อมูล" 
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ ไม่พบข้อมูลอาสาสมัครในระบบ")