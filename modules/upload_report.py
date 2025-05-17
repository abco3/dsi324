import streamlit as st
import pandas as pd
from utils.db import connect_db

def upload_reports_page():
    st.title("อัปโหลดข้อมูลรายงาน")

    if "upload_done" not in st.session_state:
        st.session_state.upload_done = False

    uploaded_file = st.file_uploader("เลือกไฟล์ Excel", type=["xlsx"], key="uploader")

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl", dtype={"volunteer_id": str})

            df.columns = [str(col).strip() if pd.notna(col) else f"col_{i}" for i, col in enumerate(df.columns)]
            df = df.where(pd.notnull(df), None)
            df = df[df["volunteer_id"].notnull() & (df["volunteer_id"].astype(str).str.strip() != "")]

            st.write("ตัวอย่างข้อมูล:")
            st.dataframe(df.head(20))

            if not st.session_state.upload_done:
                if st.button("อัปโหลดข้อมูล", key="upload_btn"):
                    conn = connect_db()
                    if conn is None:
                        st.error("❌ ไม่สามารถเชื่อมต่อฐานข้อมูลได้")
                        return

                    cursor = conn.cursor()
                    try:
                        for _, row in df.iterrows():
                            clean_row = row.dropna()
                            columns = ', '.join(f"`{col}`" for col in clean_row.index)
                            placeholders = ', '.join(['%s'] * len(clean_row))
                            sql = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
                            cursor.execute(sql, tuple(clean_row.values))
                        conn.commit()

                        st.session_state.upload_done = True
                        st.rerun()

                    except Exception as e:
                        conn.rollback()
                        st.error(f"❌ เกิดข้อผิดพลาดในการอัปโหลดข้อมูล: {e}")
                    finally:
                        cursor.close()
                        conn.close()
            else:
                st.success("✅ อัปโหลดข้อมูลสำเร็จ")

        except Exception as e:
            st.error(f"❌ ไม่สามารถอ่านไฟล์ Excel: {e}")

    if uploaded_file is not None and uploaded_file.name != st.session_state.get("last_uploaded_file"):
        st.session_state.upload_done = False
        st.session_state.last_uploaded_file = uploaded_file.name
        st.rerun() 