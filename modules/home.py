import streamlit as st

def home_page():
    st.title(f"ยินดีต้อนรับคุณ {st.session_state.username}")
    st.write("คุณเข้าสู่ระบบเรียบร้อย")
    st.write("โปรดเลือกหน้าที่ต้องการจากเมนูทางด้านซ้าย")

    if st.session_state.get("confirm_logout", False):
        st.warning("ยืนยันที่จะออกจากระบบใช่หรือไม่")
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("✅ ยืนยัน", key="confirm_yes", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        with col2:
            if st.button("❌ ยกเลิก", key="confirm_no", use_container_width=True):
                st.session_state.confirm_logout = False
                st.rerun()
        with col3:
            pass
    else:
        if st.button("ออกจากระบบ", key="logout_btn"):
            st.session_state.confirm_logout = True
            st.rerun()