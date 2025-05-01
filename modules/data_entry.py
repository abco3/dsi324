import streamlit as st
import datetime
from datetime import datetime
from utils.db import get_volunteer_by_id, insert_data_to_db


# calculate age
def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


# data entry page
def data_entry_page():
    st.subheader("แบบรายงานผลการปฏิบัติงานอาสาสมัครสาธารณสุขกรุงเทพมหานคร ด้านการป้องกันและแก้ไขปัญหายาเสพติด")

    volunteer = st.session_state.get("selected_volunteer")
    if not volunteer:
        st.error("ไม่พบข้อมูลอาสาสมัคร")
        return
    
    st.subheader("ข้อมูลอาสาสมัคร")

    col_id = st.columns(1)[0]
    with col_id:
        st.markdown(f"**รหัสอาสาสมัคร:** {volunteer['volunteer_id']}")

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
            "volunteer_id": volunteer["volunteer_id"],
            "prefix": volunteer["prefix"],
            "first_name": volunteer["first_name"],
            "last_name": volunteer["last_name"],
            "phone_number": volunteer["phone_number"],
            "community": volunteer["community"],
            "service": volunteer["service"],
            "birth_date": volunteer["birth_date"],
            "gender": volunteer["gender"],
            "age": age,
            "sub_district": volunteer["sub_district"],
            "district": volunteer["district"],
            "province": volunteer["province"],
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