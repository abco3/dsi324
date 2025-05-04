import mysql.connector
from mysql.connector import Error
import streamlit as st
import pyotp

# connect DB
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="1234",
            database="test324",
            use_unicode=True
        )
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SET time_zone = '+07:00'")
            cursor.execute("SET NAMES utf8mb4;")
            cursor.execute("SET CHARACTER SET utf8mb4;")
            print("Connected to MySQL database with utf8mb4 encoding")
        return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None



# insert data
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


# check user credentials
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


#for search page & view volunteer data page
def get_volunteer_by_id(volunteer_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM volunteers WHERE volunteer_id = %s"
        cursor.execute(query, (volunteer_id,))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Error while fetching volunteer: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_all_volunteer_ids_and_names():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT volunteer_id, first_name, last_name FROM volunteers")
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error while fetching volunteers: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_reports_by_volunteer_id(volunteer_id):
    with connect_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM reports WHERE volunteer_id = %s ORDER BY created_at ASC", (volunteer_id,))
            return cursor.fetchall()