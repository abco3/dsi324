import streamlit as st
import pandas as pd
from datetime import datetime
from modules.data_entry import calculate_age
from utils.db import get_volunteer_by_id, get_all_volunteer_ids_and_names, get_reports_by_volunteer_id


def view_volunteer_data_page():
    st.title("ตรวจสอบข้อมูลอาสาสมัคร")

    # search volunteer
    volunteers = get_all_volunteer_ids_and_names()
    if not volunteers:
        st.warning("ไม่พบข้อมูลอาสาสมัคร")
        return

    options = [f"{v['volunteer_id']} - {v['first_name']} {v['last_name']}" for v in volunteers]
    selected = st.selectbox("ระบุเลขประจำตัวหรือชื่อของอาสาสมัคร", options)

    if st.button("ค้นหา"):
        volunteer_id = int(selected.split(" - ")[0])

        volunteer = get_volunteer_by_id(volunteer_id)
        reports = get_reports_by_volunteer_id(volunteer_id)

        if not volunteer:
            st.error("ไม่พบข้อมูลอาสาสมัคร")
            return

        # volunteer details
        st.subheader("ข้อมูลทั่วไป")

        col_id = st.columns(1)[0]
        with col_id:
            st.markdown(f"**เลขประจำตัวอาสาสมัคร:** {volunteer['volunteer_id']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**คำนำหน้า:** {volunteer['prefix']}")
            st.markdown(f"**เบอร์โทร:** {volunteer['phone_number']}")
        with col2:
            st.markdown(f"**ชื่อ:** {volunteer['first_name']}")
            st.markdown(f"**ชุมชน:** {volunteer['community']}")
        with col3:
            st.markdown(f"**นามสกุล:** {volunteer['last_name']}")
            st.markdown(f"**ศูนย์บริการ:** {volunteer['service']}")

        # age from birthday
        birth_date = volunteer["birth_date"]
        # check --datetime or not
        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()
        age = calculate_age(birth_date)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown(f"**เพศ:** {volunteer['gender']}")
            st.markdown(f"**แขวง/ตำบล:** {volunteer['sub_district']}")
        with col5:
            st.markdown(f"**วันเกิด:** {birth_date.strftime('%d/%m/%Y')}")
            st.markdown(f"**เขต/อำเภอ:** {volunteer['district']}")
        with col6:
            st.markdown(f"**อายุ:** {age} ปี")
            st.markdown(f"**จังหวัด:** {volunteer['province']}")

        # report deatails
        st.subheader("รายงานผลการปฏิบัติงาน")

        if reports:
            st.markdown(f"**จำนวนครั้งที่กรอกข้อมูล:** {len(reports)} ครั้ง")

            for i, report in enumerate(reports, 1):
                with st.expander(f"รายงานครั้งที่ {i}"):

                    # show date/time
                    created_date = report["created_at"].strftime("%d/%m/%Y เวลา %H:%M") if isinstance(report["created_at"], (datetime, str)) else str(report["created_at"])
                    st.markdown(f"**วันที่กรอกข้อมูล:** {created_date}")

                    # del created_at from dict
                    report_data = {k: v for k, v in report.items() if k != "created_at"}

                    df = pd.DataFrame([report_data])
                    df.set_index('id', inplace=True)
                    st.dataframe(df.style.hide(axis="index"))
        else:
            st.info("ไม่มีรายงานของอาสาสมัคร")