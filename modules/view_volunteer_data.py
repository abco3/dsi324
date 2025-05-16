import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db import get_unique_volunteer_ids_from_reports, get_latest_report_by_volunteer_id, get_reports_by_volunteer_id


def view_volunteer_data_page():
    st.title("ตรวจสอบข้อมูลอาสาสมัคร")

    volunteers = get_unique_volunteer_ids_from_reports()
    if not volunteers:
        st.warning("ไม่พบข้อมูลรายงานของอาสาสมัคร")
        return

    options = [f"{v['volunteer_id']} - {v['first_name']} {v['last_name']}" for v in volunteers]
    selected = st.selectbox("ระบุเลขประจำตัวหรือชื่อของอาสาสมัคร", options)

    if st.button("ค้นหา"):
        volunteer_id = int(selected.split(" - ")[0])

        volunteer = get_latest_report_by_volunteer_id(volunteer_id)
        reports = get_reports_by_volunteer_id(volunteer_id)

        if not volunteer:
            st.error("ไม่พบข้อมูลรายงานของอาสาสมัคร")
            return

        st.subheader("ข้อมูลทั่วไป")

        col_id = st.columns(1)[0]
        with col_id:
            st.markdown(f"**เลขประจำตัวอาสาสมัคร:** {volunteer['volunteer_id']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**คำนำหน้า:** {volunteer['prefix']}")
            st.markdown(f"**ชุมชน:** {volunteer['community']}")           
        with col2:
            st.markdown(f"**ชื่อ:** {volunteer['first_name']}")
            st.markdown(f"**แขวง/ตำบล:** {volunteer['sub_district']}")
        with col3:
            st.markdown(f"**นามสกุล:** {volunteer['last_name']}")
            st.markdown(f"**เขต/อำเภอ:** {volunteer['district']}")

        st.subheader("รายงานผลการปฏิบัติงาน")

        if reports:
            st.markdown(f"**จำนวนครั้งที่กรอกข้อมูล:** {len(reports)} ครั้ง")

            for i, report in enumerate(reports, 1):
                with st.expander(f"รายงานครั้งที่ {i}"):
                    created_date = report.get("created_at")
                    if isinstance(created_date, datetime):
                        created_str = created_date.strftime("%d/%m/%Y เวลา %H:%M")
                    else:
                        created_str = str(created_date)

                    st.markdown(f"**วันที่กรอกข้อมูล:** {created_str}")

                    report_data = {
                        k: v for k, v in report.items()
                        if k not in ["created_at", "birth_date", "age", "id"]
                    }

                    df = pd.DataFrame.from_dict(report_data, orient='index', columns=["column"])
                    df.reset_index(inplace=True)
                    df.columns = ["column", "input"]
                    st.dataframe(df, use_container_width=True)