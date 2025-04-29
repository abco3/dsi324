import streamlit as st
import mysql.connector 
import datetime
import time
import pandas as pd
import pyotp
import qrcode
import os
from mysql.connector import Error
from list import districts_bangkok, subdistricts_by_district


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit&display=swap');

    html, body, div, p, label, input, textarea, button, h1, h2, h3, h4, h5, h6, span {
        font-family: 'Kanit', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)


# Function to connect to the database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="1234",  
            database="test324"  
        )
        if conn.is_connected():
            print("Connected to MySQL database")
        return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# Function to insert data
def insert_data_to_db(data):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # prepare SQL INSERT
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
        values = list(data.values())

        cursor.execute(sql, values)
        conn.commit()

        st.success("✅ บันทึกข้อมูลสำเร็จ")

    except mysql.connector.Error as err:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Function to check user credentials
def check_user_credentials(email, password, otp_code):
    conn = connect_db()
    if conn is None:
        return False, None

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT password, otp_secret, role FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result is None:
            print("No user found.")
            return False, None
        
        if result['password'] != password:
            print(f"Password mismatch. Stored: {result['password']} Input: {password}")
            return False, None

        # OTP check
        totp = pyotp.TOTP(result['otp_secret'])
        otp_generated = totp.now()
        print(f"Generated OTP: {otp_generated} - Input OTP: {otp_code}")

        if not totp.verify(otp_code):
            print("OTP verification failed.")
            return False, None

        return True, result['role']

    except Error as e:
        print(f"Error while checking credentials: {e}")
        return False, None
    finally:
        cursor.close()
        conn.close()


# Login page
def login():
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


#Create Account page
def create_account_page():
    st.title("สร้างบัญชี")

    new_email = st.text_input("อีเมล")
    new_password = st.text_input("รหัสผ่าน", type="password")
    new_role = st.selectbox("บทบาท", ["user", "admin", "dev"])

    if st.button("สร้างบัญชี"):
        # OTP Secret
        totp = pyotp.TOTP(pyotp.random_base32())
        otp_secret = totp.secret

        # add to db
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, password, role, otp_secret)
            VALUES (%s, %s, %s, %s)
        """, (new_email, new_password, new_role, otp_secret))
        conn.commit()

        # create QR Code
        otp_uri = totp.provisioning_uri(name=new_email, issuer_name="DSI324 App")
        img = qrcode.make(otp_uri)
        img_path = f"qr_img/qr_{new_email.replace('@', '_at_')}.png"
        os.makedirs("qr_img", exist_ok=True)
        img.save(img_path)

        st.success("✅ สร้างบัญชีสำเร็จ")

        st.markdown("🔎แสกน QR Code นี้ด้วย Google Authenticator🔎")
        st.image(img_path, width=200)


# Data entry page
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


# Function Monitor Data
def view_reports_page():

    st.title("รายงานจากอาสาสมัคร")
    conn = connect_db()
    if conn:
        df = pd.read_sql("SELECT * FROM reports", conn)

        df.set_index('id', inplace=True)
        conn.close()
        st.dataframe(df.style.hide(axis="index"))

    else:
        st.error("Can't connect to Database.")


# Main function to control navigation
def main():
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login()  # Show login page if not logged in
    else:
        # Set default page if not set
        if 'page' not in st.session_state:
            st.session_state.page = "หน้าหลัก"

        role = st.session_state.get("role", "")  # role from login

        # Prepare page options based on role
        page_options = ["หน้าหลัก"]
        if role in ["admin", "dev"]:
            page_options.extend(["กรอกข้อมูล", "รายงาน"])
        elif role == "user":
            page_options.append("รายงาน")
        if role == "dev":
            page_options.append("สร้างบัญชี")

        # Sidebar selection
        page = st.sidebar.selectbox("เมนู", page_options)

        # Page routing
        if page == "หน้าหลัก":
            st.session_state.page = "หน้าหลัก"
            st.title(f"ยินดีต้อนรับคุณ {st.session_state.username}")
            st.write("คุณเข้าสู่ระบบเรียบร้อย")
            st.write("โปรดเลือกหน้าที่ต้องการจากเมนูทางด้านซ้าย")

            # confirm logout
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

        elif page == "กรอกข้อมูล":
            if role in ["admin", "dev"]:
                st.session_state.page = "กรอกข้อมูล"
                data_entry_page()

        elif page == "รายงาน":
            if role in ["admin", "dev", "user"]:
                st.session_state.page = "รายงาน"
                view_reports_page()

        elif page == "สร้างบัญชี":
            if role == "dev":
                st.session_state.page = "สร้างบัญชี"
                create_account_page()
                

if __name__ == "__main__":
    main()