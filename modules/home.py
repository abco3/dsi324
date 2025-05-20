import fsspec
import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# ============ lakeFS config ============
ACCESS_KEY = "access_key"
SECRET_KEY = "secret_key"
lakefs_endpoint = "http://lakefs-dev:8000/"
repo = "dust-concentration"
branch = "main"
base_path = f"{repo}/{branch}/pm_data.parquet"

storage_options = {
    "key": ACCESS_KEY,
    "secret": SECRET_KEY,
    "client_kwargs": {
        "endpoint_url": lakefs_endpoint
    }
}
fs = fsspec.filesystem("s3", **storage_options, cache_regions=False)

# ============  Helper: AQI level ============ 
def get_aqi_level_and_color(aqi):
    if aqi <= 50:
        return "Unhealthy", "#00E400"
    elif aqi <= 100:
        return "Moderate", "#FFFF00"
    elif aqi <= 150:
        return "Sensitive", "#FF7E00"
    elif aqi <= 200:
        return "Unhealthy", "#FF0000"
    elif aqi <= 300:
        return "Severe", "#8F3F97"
    else:
        return "Hazardous", "#7E0023"

def get_latest_date_path():
    fs.invalidate_cache(f"{base_path}/")
    paths = fs.glob(f"{base_path}/year=*/month=*/day=*")
    if not paths:
        return None
    def extract_date(p):
        parts = p.split("/")
        y = int(parts[-3].split("=")[1])
        m = int(parts[-2].split("=")[1])
        d = int(parts[-1].split("=")[1])
        return datetime(y, m, d)
    return max(paths, key=extract_date)

def get_latest_hour_key():
    date_path = get_latest_date_path()
    if not date_path:
        return "no-data"
    fs.invalidate_cache(f"{date_path}/")
    hour_paths = fs.glob(f"{date_path}/hour=*")
    hour_paths = sorted(hour_paths, key=lambda p: int(p.split("/")[-1].split("=")[1]))
    if not hour_paths:
        return f"{date_path}-no-hour"
    def extract_hour(p):
        return int(p.split("/")[-1].split("=")[1])
    latest_hour = max([extract_hour(p) for p in hour_paths])
    return f"{date_path}-hour={latest_hour}"

@st.cache_data(ttl=300)
def load_latest_day_data(key):
    _ = key
    now = datetime.now()
    date_path = get_latest_date_path()
    if not date_path:
        return pd.DataFrame(), now, None, False
    fs.invalidate_cache(f"{date_path}/")
    hour_paths = fs.glob(f"{date_path}/hour=*")
    if not hour_paths:
        return pd.DataFrame(), now, None, False

    expected_files = len(hour_paths)
    dfs = []
    for p in hour_paths:
        try:
            df_part = pd.read_parquet(f"s3a://{p}", storage_options=storage_options)
            dfs.append(df_part)
        except Exception:
            pass
    is_complete = len(dfs) == expected_files
    if not is_complete:
        return pd.DataFrame(), now, None, False

    df = pd.concat(dfs, ignore_index=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    return df, now, None, True

    #thai_time = cache_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Bangkok"))
    #st.caption(f"🕑 ข้อมูลล่าสุดเมื่อ: {thai_time.strftime('%d/%m/%Y %H:%M:%S')}")

# ============ HOME PAGE ============ 
def home_page():
    st.image("img/logo41.jpg",use_container_width=True)
    
    cache_key = get_latest_hour_key()
    df, cache_time, _, is_complete = load_latest_day_data(cache_key)

    # ============ Filter by latest hour ============
    hour_paths = fs.glob(f"{get_latest_date_path()}/hour=*")
    def extract_hour(p): return int(p.split("/")[-1].split("=")[1])
    available_hours = [extract_hour(p) for p in hour_paths]
    latest_hour = max(available_hours)

    df_latest = df[df['timestamp'].dt.hour == latest_hour].copy()
    df_latest["AQI_level"], df_latest["AQI_color"] = zip(*df_latest["AQI.aqi"].apply(get_aqi_level_and_color))

    daily_mean_aqi = df_latest["AQI.aqi"].mean()
    daily_mean_pm25 = df_latest["PM25.value"].mean()
    level, color = get_aqi_level_and_color(daily_mean_aqi)

    thai_now = datetime.now().astimezone(ZoneInfo("Asia/Bangkok"))

    def thai_month_name(month_num):
        months = [
            "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ]
        return months[month_num - 1]

    thai_date_str = (
        f"วันที่ {thai_now.day} "
        f"{thai_month_name(thai_now.month)} "
        f"{thai_now.year + 543}, "
        f"เวลา {thai_now.strftime('%H:%M:%S')}"
    )

    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        st.markdown(f"""
            <div style="
                background-color:{color};
                padding: 0.6rem 1rem;
                border-radius: 10px;
                text-align: center;
                color: white;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 0.85rem; font-weight: bold;">ค่าเฉลี่ย AQI</div>
                <div style="font-size: 0.9rem; font-weight: bold;">AQI {daily_mean_aqi:.0f} - {level}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="
                background-color:#1338BE;
                padding: 0.6rem 1rem;
                border-radius: 10px;
                text-align: center;
                color: white;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 0.85rem; font-weight: bold;">ค่าเฉลี่ย PM2.5</div>
                <div style="font-size: 0.9rem; font-weight: bold;">{daily_mean_pm25:.1f} µg/m³</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col1:
        st.markdown(f"""
            <div style="
                background-color: #f0f0f0;
                padding: 0.6rem 1rem;
                border-radius: 10px;
                font-size: 0.9rem;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                color: #333;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
                display: inline-block;
                width: fit-content;
                margin: 0 auto;
                text-align: center;
            ">
                {thai_date_str}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    st.markdown(f"""
        <div style='font-family: "Kanit", sans-serif; margin-top: 1rem; text-align: left;'>
            <span style='font-size: 1.5rem; color: black; font-weight: bold;'>
                ยินดีต้อนรับคุณ {st.session_state.username}
            </span>
        </div>
     """, unsafe_allow_html=True)

    st.markdown("")

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