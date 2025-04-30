import streamlit as st
import datetime
from list import districts_bangkok, subdistricts_by_district
from utils.db import insert_data_to_db


# data entry page
def data_entry_page():
    st.title("แบบรายงานผลการปฏิบัติงานอาสาสมัครสาธารณสุขกรุงเทพมหานคร ด้านการป้องกันและแก้ไขปัญหายาเสพติด")
    st.subheader("กรอกข้อมูลทั่วไป")

    col1, col2 = st.columns(2)
    with col1:
        volunteer_id = st.text_input("เลขประจำตัวอาสาสมัคร")
        if volunteer_id and not volunteer_id.isdigit():
            st.error("กรุณากรอกเฉพาะตัวเลขสำหรับเลขประจำตัวอาสาสมัคร")
        first_name = st.text_input("ชื่อ")
        phone_number = st.text_input("เบอร์โทรศัพท์")
        
    with col2:
        prefix = st.selectbox("คำนำหน้า", ["นาย", "นาง", "นางสาว"])
        last_name = st.text_input("นามสกุล")
        community = st.text_input("ชุมชน")

    col3, col4 = st.columns(2)
    with col3:
        birth_date = st.date_input(
            "วันเกิด",
            value=datetime.date(2000, 1, 1),               
            min_value=datetime.date(1900, 1, 1),          
            max_value=datetime.date.today()                
        )
    with col4:
        gender = st.radio("เพศ", ["ชาย", "หญิง"])

    district_list = list(subdistricts_by_district.keys())
    district = st.selectbox("เขต/อำเภอ", district_list)

    selected_district = st.session_state.get("district")
    if district:
         sub_district_options = subdistricts_by_district.get(district, [])
    else:
        sub_district_options = []
    sub_district = st.selectbox("แขวง/ตำบล", sub_district_options, key="sub_district")
    province = st.selectbox("จังหวัด", ["กรุงเทพมหานคร"])

    st.subheader("การดำเนินงาน")
    operation_month = st.selectbox("ประจำเดือน", [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ])
    operation_year = st.number_input("ปี พ.ศ.", min_value=2500, max_value=2600, value=2568)

    st.subheader("1. การป้องกันและเฝ้าระวังปัญหายาเสพติดในชุมชนและโรงเรียน")

    col_q1_1, col_res1_1 = st.columns(2)
    with col_q1_1:
        st.markdown("1.1 ให้ความรู้เรื่องยาและสารเสพติด/บุหรี่/บุหรี่ไฟฟ้า/เครื่องดื่มแอลกอฮอล์แก่เยาวชนและประชาชน (รายบุคคล, เสียงตามสาย, Line, Tiktok ฯลฯ)")
    with col_res1_1:
        st.number_input("ครั้ง", min_value=0, key="q1_prevention1_times")
        st.number_input("ราย (คน)", min_value=0, key="q1_prevention1_people")

    col_q1_2, col_res1_2 = st.columns(2)
    with col_q1_2:
        st.markdown("1.2 จัดกิจกรรมรณรงค์ป้องกันยาและสารเสพติด/บุหรี่/บุหรี่ไฟฟ้า/เครื่องดื่มแอลกอฮอล์")
    with col_res1_2:
        st.number_input("ครั้ง", min_value=0, key="q1_prevention2_times")

    col_q1_3, col_res1_3 = st.columns(2)
    with col_q1_3:
        st.markdown("1.3 เฝ้าระวังปัญหายาและสารเสพติด(กัญชา,กระท่อม,บุหรี่,บุหรี่ไฟฟ้า,เครื่องดื่มแอลกอฮอล์)ของเยาวชน และประชาชน/ร้านค้าในชุมชน/รอบโรงเรียน")
    with col_res1_3:
        st.number_input("ครั้ง", min_value=0, key="q1_prevention3_times")

    col_q1_4, col_res1_4 = st.columns(2)
    with col_q1_4:
        st.markdown("1.4 ให้ความรู้/จัดกิจกรรมเพื่อพัฒนาทักษะสมอง (EF) ในเด็กปฐมวัย")
    with col_res1_4:
        st.number_input("ครั้ง", min_value=0, key="q1_prevention4_times")
        st.number_input("ราย (คน)", min_value=0, key="q1_prevention4_people")

    col_q1_5, col_res1_5 = st.columns(2)
    with col_q1_5:
        st.markdown("1.5 แจ้งเบาะแสเรื่องยาเสพติดแก่หน่วยงานที่เกี่ยวข้อง")
    with col_res1_5:
        st.number_input("ครั้ง", min_value=0, key="q1_prevention5_times")

    st.subheader("2. การช่วยเหลือ สนับสนุน ด้านการบำบัดฟื้นฟูผู้เสพ/ผู้ติดยาและสารเสพติดในชุมชน")

    col_q2_1, col_res2_1 = st.columns(2)
    with col_q2_1:
        st.markdown("2.1 ร่วมค้นหาคัดกรอง/แนะนำ/ส่งต่อผู้ใช้,ผู้เสพผู้ติดยาและสารเสพติดเข้าสู่ระบบการบำบัดรักษา")
    with col_res2_1:
        st.number_input("ครั้ง", min_value=0, key="q2_treatment1_times")
        st.number_input("ราย (คน)", min_value=0, key="q2_treatment1_people")

    col_q2_2, col_res2_2 = st.columns(2)
    with col_q2_2:
        st.markdown("2.2 ร่วมจัดทำทะเบียนผู้ใช้,ผู้เสพ,ผู้ติดยาและสารเสพติด/ร่วมจัดทำแผนการดูแลผู้มีปัญหายาและเสพติด")
    with col_res2_2:
        st.number_input("ครั้ง", min_value=0, key="q2_treatment2_times")

    col_q2_3, col_res2_3 = st.columns(2)
    with col_q2_3:
        st.markdown("2.3 เฝ้าระวัง/ค้นหา/คัดกรอง ผู้มีอาการทางจิตจากการใช้ยาและสารเสพติดเข้าสู่กระบวนการบำบัดรักษา")
    with col_res2_3:
        st.number_input("ครั้ง", min_value=0, key="q2_treatment3_times")
        st.number_input("ราย (คน)", min_value=0, key="q2_treatment3_people")

    col_q2_4, col_res2_4 = st.columns(2)
    with col_q2_4:
        st.markdown("2.4 ร่วมติดตาม/ดูแลการกินยาทุกวันของผู้ป่วยจิตเวชจากการใช้ยาเสพติด")
    with col_res2_4:
        st.number_input("ครั้ง", min_value=0, key="q2_treatment4_times") 
        st.number_input("ราย (คน)", min_value=0, key="q2_treatment4_people") 

    col_q2_5, col_res2_5 = st.columns(2)
    with col_q2_5:
        st.markdown("2.5 ร่วมซ้อมแผนการเผชิญเหตุบุคคลคลุ้มคลั่งจากการใช้ยาและสารเสพติดในชุมชน")
    with col_res2_5:
        st.number_input("ครั้ง", min_value=0, key="q2_treatment5_times") 

    st.subheader("3. การช่วยเหลือสนับสนุนด้านการติดตามดูแลช่วยเหลือผู้ใช้, ผู้เสพ, ผู้ติดยาและสารเสพติดที่ผ่านการบำบัดรักษาในชุมชน")

    col_q3_1, col_res3_1 = st.columns(2)
    with col_q3_1:
        st.markdown("3. การช่วยเหลือสนับสนุนด้านการติดตามดูแลช่วยเหลือผู้ใช้, ผู้เสพ, ผู้ติดยาและสารเสพติดที่ผ่านการบำบัดรักษาในชุมชน")
    with col_res3_1:
        st.number_input("ครั้ง", min_value=0, key="q3_assistance_times") 
        st.number_input("ราย (คน)", min_value=0, key="q3_assistance_people") 

    st.subheader("4.การมีส่วนร่วมกับภาคีเครือข่ายด้านการป้องกันและแก้ไขปัญหายาและสารเสพติด")

    col_q4_1, col_res4_1 = st.columns(2)
    with col_q4_1:
        st.markdown("4.1 เข้าร่วมเวทีประชาคม/ประชุม/อบรม/ศึกษาดูงาน ด้านการป้องและแก้ไขปัญหายาและสารเสพติด")
    with col_res4_1:
        st.number_input("ครั้ง", min_value=0, key="q4_engaging1_times") 

    col_q4_2, col_res4_2 = st.columns(2)
    with col_q4_2:
        st.markdown("4.2 ร่วมกิจกรรมป้องกันยาและสารเสพติดกับหน่วยงานอื่น ๆ เช่น วันต่อต้านยาเสพติด")
    with col_res4_2:
        st.number_input("ครั้ง", min_value=0, key="q4_engaging2_times")

    st.subheader("5. การให้คำปรึกษา/แนะนำแก่ผู้มีปัญหาเรื่องยาและสารเสพติด")

    col_q5_1, col_res5_1 = st.columns(2)
    with col_q5_1:
        st.markdown("5. การให้คำปรึกษา/แนะนำแก่ผู้มีปัญหาเรื่องยาและสารเสพติด")
    with col_res5_1:
        st.number_input("ครั้ง", min_value=0, key="q5_consult_times")
        st.number_input("ราย (คน)", min_value=0, key="q5_consult_people")

    st.subheader("6. งานอื่น ๆ ตามสภาพปัญหายาเสพติดในชุมชน")
    suggestions = st.text_area("โปรดระบุ", key="q6_others")

    st.subheader("หมายเหตุ")
    suggestions_note = st.text_area("โปรดระบุ", key="notes")

    if st.button("บันทึกข้อมูลอาสาสมัคร"):
        data = {
            "volunteer_id": volunteer_id,
            "prefix": prefix,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "community": community,
            "birth_date": birth_date.isoformat() if birth_date else None,
            "gender": gender,
            "sub_district": st.session_state.sub_district,
            "district": district,
            "province": province,
            "operation_month": operation_month,
            "operation_year": operation_year,
            "q1_prevention1_times": st.session_state.q1_prevention1_times,
            "q1_prevention1_people": st.session_state.q1_prevention1_people,
            "q1_prevention2_times": st.session_state.q1_prevention2_times,
            "q1_prevention3_times": st.session_state.q1_prevention3_times,
            "q1_prevention4_times": st.session_state.q1_prevention4_times,
            "q1_prevention4_people": st.session_state.q1_prevention4_people,
            "q1_prevention5_times": st.session_state.q1_prevention5_times,
            "q2_treatment1_times": st.session_state.q2_treatment1_times,
            "q2_treatment1_people": st.session_state.q2_treatment1_people,
            "q2_treatment2_times": st.session_state.q2_treatment2_times,
            "q2_treatment3_times": st.session_state.q2_treatment3_times,
            "q2_treatment3_people": st.session_state.q2_treatment3_people,
            "q2_treatment4_times": st.session_state.q2_treatment4_times, 
            "q2_treatment4_people": st.session_state.q2_treatment4_people, 
            "q2_treatment5_times": st.session_state.q2_treatment5_times,
            "q3_assistance_times": st.session_state.q3_assistance_times, 
            "q3_assistance_people": st.session_state.q3_assistance_people, 
            "q4_engaging1_times": st.session_state.q4_engaging1_times, 
            "q4_engaging2_times": st.session_state.q4_engaging2_times, 
            "q5_consult_times": st.session_state.q5_consult_times, 
            "q5_consult_people": st.session_state.q5_consult_people, 
            "q6_others": suggestions,
            "notes": suggestions_note
        }
        st.write("ข้อมูลที่กรอก:")
        st.write(data)

        insert_data_to_db(data)