import streamlit as st
from modules.login import login_page
from modules.data_entry import data_entry_page
from modules.view_reports import view_reports_page
from modules.create_account import create_account_page


# Main function to control navigation
def main():
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()  # Show login page if not logged in
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