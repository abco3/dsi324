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


# check email, password
def verify_user_password(email, password):
    conn = connect_db()
    if conn is None:
        return False, None

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT password, role FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result and result['password'] == password:
            return True, result['role']
        return False, None
    finally:
        cursor.close()
        conn.close()


# check otp
def verify_otp(email, otp_code):
    conn = connect_db()
    if conn is None:
        return False

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT otp_secret FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            totp = pyotp.TOTP(result['otp_secret'])
            return totp.verify(otp_code)
        return False
    finally:
        cursor.close()
        conn.close()

# get reports data
def get_reports_by_volunteer_id(volunteer_id):
    with connect_db() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM reports WHERE volunteer_id = %s ORDER BY created_at ASC", (volunteer_id,))
            return cursor.fetchall()

#get id name from reports
def get_unique_volunteer_ids_from_reports():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT DISTINCT volunteer_id, first_name, last_name
    FROM reports
    ORDER BY volunteer_id
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

# get reports data
def get_latest_report_by_volunteer_id(volunteer_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM reports
    WHERE volunteer_id = %s
    ORDER BY created_at DESC
    LIMIT 1
    """
    cursor.execute(query, (volunteer_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

# get id name from volunteers
def get_all_volunteers():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT volunteer_id, first_name, last_name FROM volunteers ORDER BY volunteer_id"
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

# get volunteer data by ID
def get_volunteer_by_id(volunteer_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM volunteers WHERE volunteer_id = %s"
    cursor.execute(query, (volunteer_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

# get all reports data
def get_all_reports():
    conn = connect_db()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM reports ORDER BY created_at DESC"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
        conn.close()