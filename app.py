import streamlit as st
import mysql.connector 
from mysql.connector import Error

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

# Function to check user credentials
def check_user_credentials(email, password):
    conn = connect_db()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()  
        if result is None:
            return False  
        stored_password = result[0]  
        if stored_password == password:
            return True  
        return False  
    except Error as e:
        print(f"Error while checking credentials: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


# Login page
def login():
    st.title("Login to Your Account")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if '@dome.tu.ac.th' in email:
            if email and password:
                if check_user_credentials(email, password):  
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.username = email  
                    st.session_state.page = "Home"  # Set page to "Home" after login
                else:
                    st.error("Incorrect email or password.")  
            else:
                st.error("Please enter both email and password.")
        else:
            st.error("Invalid email domain. Please use a valid organization email.")

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
        birth_date = st.date_input("วันเกิด")
    with col4:
        gender = st.radio("เพศ", ["ชาย", "หญิง", "อื่นๆ"])

    sub_district = st.text_input("แขวง/ตำบล")
    district = st.text_input("เขต/อำเภอ")
    province = st.text_input("จังหวัด")

    st.subheader("การดำเนินงาน")
    operation_month = st.selectbox("ประจำเดือน", [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ])
    operation_year = st.number_input("ปี พ.ศ.", min_value=2500, max_value=2600, value=2568)

    st.markdown("1. การป้องกันและเฝ้าระวังปัญหายาเสพติดในชุมชนและโรงเรียน")

    col_q1_1, col_res1_1 = st.columns(2)
    with col_q1_1:
        st.markdown("1.1 ให้ความรู้เรื่องยาและสารเสพติด/บุหรี่/บุหรี่ไฟฟ้า/เครื่องดื่มแอลกอฮอล์แก่เยาวชนและประชาชน (รรายบุคคล, เสียงตามสาย, Line, Tiktok ฯลฯ)")
    with col_res1_1:
        st.number_input("ครั้ง", min_value=0, key="prevention1_times")
        st.number_input("ราย (คน)", min_value=0, key="prevention1_people")

    col_q1_2, col_res1_2 = st.columns(2)
    with col_q1_2:
        st.markdown("1.2 จัดกิจกรรมรณรงค์ป้องกันยาและสารเสพติด/บุหรี่/บุหรี่ไฟฟ้า/เครื่องดื่มแอลกอฮอล์")
    with col_res1_2:
        st.number_input("ครั้ง", min_value=0, key="prevention2_times")

    col_q1_3, col_res1_3 = st.columns(2)
    with col_q1_3:
        st.markdown("1.3 เฝ้าระวังภัยยาเสพติด (กีดขวาง, ตักเตือน, แจ้งเบาะแส)")
    with col_res1_3:
        st.number_input("ครั้ง", min_value=0, key="prevention3_times")

    col_q1_4, col_res1_4 = st.columns(2)
    with col_q1_4:
        st.markdown("1.4 ให้ความรู้/จัดกิจกรรมเพื่อพัฒนาทักษะสมอง (EF) ในเด็กปฐมวัย")
    with col_res1_4:
        st.number_input("ครั้ง", min_value=0, key="prevention4_times")
        st.number_input("ราย (คน)", min_value=0, key="prevention4_people")

    col_q1_5, col_res1_5 = st.columns(2)
    with col_q1_5:
        st.markdown("1.5 แจ้งเบาะแสยาเสพติดแก่หน่วยงานที่เกี่ยวข้อง")
    with col_res1_5:
        st.number_input("ครั้ง", min_value=0, key="prevention5_times")

    st.subheader("2. การช่วยเหลือ สนับสนุน ด้านการบำบัดฟื้นฟูผู้เสพ/ผู้ติดยาเสพติดในชุมชน")

    col_q2_1, col_res2_1 = st.columns(2)
    with col_q2_1:
        st.markdown("2.1 ให้คำปรึกษาเบื้องต้น/ให้กำลังใจ")
    with col_res2_1:
        st.number_input("ครั้ง", min_value=0, key="treatment1_times")
        st.number_input("ราย (คน)", min_value=0, key="treatment1_people")

    col_q2_2, col_res2_2 = st.columns(2)
    with col_q2_2:
        st.markdown("2.2 ชักชวน/นำส่งเข้ารับการบำบัด")
    with col_res2_2:
        st.number_input("ครั้ง", min_value=0, key="treatment2_times")

    col_q2_3, col_res2_3 = st.columns(2)
    with col_q2_3:
        st.markdown("2.3 ติดตาม/ดูแลช่วยเหลือภายหลังการบำบัด")
    with col_res2_3:
        st.number_input("ครั้ง", min_value=0, key="treatment3_times")
        st.number_input("ราย (คน)", min_value=0, key="treatment3_people")

    col_q2_4, col_res2_4 = st.columns(2)
    with col_q2_4:
        st.markdown("2.4 ให้ความรู้/จัดกิจกรรมเพื่อพัฒนาทักษะสมอง (EF) ในเด็กปฐมวัย")
    with col_res2_4:
        st.number_input("ครั้ง", min_value=0, key="prevention4_times_q2") # แก้ key ไม่ให้ซ้ำ
        st.number_input("ราย (คน)", min_value=0, key="prevention4_people_q2") # แก้ key ไม่ให้ซ้ำ

    col_q2_5, col_res2_5 = st.columns(2)
    with col_q2_5:
        st.markdown("2.5 แจ้งเบาะแสยาเสพติดแก่หน่วยงานที่เกี่ยวข้อง")
    with col_res2_5:
        st.number_input("ครั้ง", min_value=0, key="prevention5_times_q2") # แก้ key ไม่ให้ซ้ำ

    st.subheader("3. การพัฒนาศักยภาพตนเองและเครือข่าย")

    col_q3_1, col_res3_1 = st.columns(2)
    with col_q3_1:
        st.markdown("3. ให้ความรู้/จัดกิจกรรมเพื่อพัฒนาทักษะสมอง (EF) ในเด็กปฐมวัย")
    with col_res3_1:
        st.number_input("ครั้ง", min_value=0, key="prevention1_times_q3") # แก้ key ไม่ให้ซ้ำ
        st.number_input("ราย (คน)", min_value=0, key="prevention1_people_q3") # แก้ key ไม่ให้ซ้ำ

    st.subheader("4. ปัญหา/อุปสรรคในการดำเนินงาน (ถ้ามี)")

    col_q4_1, col_res4_1 = st.columns(2)
    with col_q4_1:
        st.markdown("4.1 ให้ความรู้/จัดกิจกรรมเพื่อพัฒนาทักษะสมอง (EF) ในเด็กปฐมวัย")
    with col_res4_1:
        st.number_input("ครั้ง", min_value=0, key="prevention1_times_q4_1") # แก้ key ไม่ให้ซ้ำ

    col_q4_2, col_res4_2 = st.columns(2)
    with col_q4_2:
        st.markdown("4.2 ให้ความรู้/จัดกิจกรรมเพื่อพัฒนาทักษะสมอง (EF) ในเด็กปฐมวัย")
    with col_res4_2:
        st.number_input("ครั้ง", min_value=0, key="prevention1_times_q4_2") # แก้ key ไม่ให้ซ้ำ

    st.subheader("5. การพัฒนาศักยภาพตนเองและเครือข่าย")

    col_q5_1, col_res5_1 = st.columns(2)
    with col_q5_1:
        st.markdown("5. ให้คำปรึกษาเบื้องต้น/ให้กำลังใจ")
    with col_res5_1:
        st.number_input("ครั้ง", min_value=0, key="treatment1_times_q5") # แก้ key ไม่ให้ซ้ำ
        st.number_input("ราย (คน)", min_value=0, key="treatment1_people_q5") # แก้ key ไม่ให้ซ้ำ

    st.subheader("6. งานอื่น ๆ ตามสภาพปัญหายาเสพติดในชุมชน")
    suggestions = st.text_area("โปรดระบุ")

    if st.button("บันทึกข้อมูลอาสาสมัคร"): # เปลี่ยนชื่อปุ่ม
        data = {
            "คำนำหน้า": prefix,
            "ชื่อ": first_name,
            "นามสกุล": last_name,
            "เลขประจำตัวอาสาสมัคร": volunteer_id,
            "วันเกิด": birth_date,
            "เพศ": gender,
            "เบอร์โทรศัพท์": phone_number,
            "ชุมชน": community,
            "แขวง/ตำบล": sub_district,
            "เขต/อำเภอ": district,
            "จังหวัด": province,
            "ประจำเดือน": operation_month,
            "ปี พ.ศ.": operation_year,
            "ป้องกันและเฝ้าระวัง 1.1 ครั้ง": st.session_state.prevention1_times,
            "ป้องกันและเฝ้าระวัง 1.1 ราย": st.session_state.prevention1_people,
            "ป้องกันและเฝ้าระวัง 1.2 ครั้ง": st.session_state.prevention2_times,
            "ป้องกันและเฝ้าระวัง 1.2 ราย": st.session_state.prevention2_people,
            "ป้องกันและเฝ้าระวัง 1.3 ครั้ง": st.session_state.prevention3_times,
            "ป้องกันและเฝ้าระวัง 1.3 ราย": st.session_state.prevention3_people,
            "ป้องกันและเฝ้าระวัง 1.4 ครั้ง": st.session_state.prevention4_times,
            "ป้องกันและเฝ้าระวัง 1.4 ราย": st.session_state.prevention4_people,
            "ป้องกันและเฝ้าระวัง 1.5 ครั้ง": st.session_state.prevention5_times,
            "ช่วยเหลือ บำบัด 2.1 ครั้ง": st.session_state.treatment1_times,
            "ช่วยเหลือ บำบัด 2.1 ราย": st.session_state.treatment1_people,
            "ช่วยเหลือ บำบัด 2.2 ครั้ง": st.session_state.treatment2_times,
            "ช่วยเหลือ บำบัด 2.2 ราย": st.session_state.treatment2_people,
            "ช่วยเหลือ บำบัด 2.3 ครั้ง": st.session_state.treatment3_times,
            "ช่วยเหลือ บำบัด 2.3 ราย": st.session_state.treatment3_people,
            "พัฒนาศักยภาพ 3.1 ครั้ง": st.session_state.develop1_times,
            "พัฒนาศักยภาพ 3.2 ครั้ง": st.session_state.develop2_times,
            "ข้อเสนอแนะ": suggestions,
        }
        st.write("ข้อมูลที่กรอก:")
        st.write(data)
        st.success("บันทึกข้อมูลเรียบร้อยแล้ว!") # แทนที่ด้วยการบันทึกลงฐานข้อมูลจริง

# Main function to control navigation
def main():
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login()  # Show login page if not logged in
    else:
        # Check if page state is set
        if 'page' not in st.session_state:
            st.session_state.page = "Home"  # Default to "Home" page if not set
        
        # Use sidebar for page selection
        page = st.sidebar.selectbox("Choose an option", ["Home", "Enter Data"])

        if page == "Home":
            st.session_state.page = "Home"
            st.title(f"Welcome, {st.session_state.username}!")
            st.write("You are now logged in.")
            st.write("Please select an option from the menu.")
        
        elif page == "Enter Data":
            st.session_state.page = "Enter Data"
            data_entry_page()  # Show the data entry page

if __name__ == '__main__':
    main()