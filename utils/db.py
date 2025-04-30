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
            database="test324"  
        )
        if conn.is_connected():
            print("Connected to MySQL database")
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