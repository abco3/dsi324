import re
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.db import get_all_reports


# ============= dashboard page function =============
def dashboard_page():
    all_reports = get_all_reports()
    
    if not all_reports:
        st.warning("ไม่มีข้อมูลรายงานในระบบ")
        return

    df = pd.DataFrame(all_reports)

    col_title = st.columns(1)[0]
    with col_title:
        st.markdown("## แดชบอร์ด")

    # ============= sidebar filter options =============
    years = sorted(df["operation_year"].unique(), reverse=True)
    months = sorted(df["operation_month"].unique())
    subdistricts = sorted(df["sub_district"].dropna().unique())

    coln1, coln2, coln3 = st.columns([1.9, 1.9, 2])
    with coln1:
        st.markdown("##### สกอร์การ์ด")
    
    with coln2:
        pass
    
    with coln3:
        st.markdown("##### ฟิลเตอร์")

    # ============ layout: scorecard left & center, filters on right =============
    col1, col2, col3 = st.columns([1.9, 1.9, 2])
    # ============ filter controls =============
    with col3:
        selected_year = st.selectbox("เลือกปี", ["ทั้งหมด"] + years)
        selected_month = st.selectbox("เลือกเดือน", ["ทั้งหมด"] + months)
        selected_subdistrict = st.selectbox("เลือกแขวง", ["ทั้งหมด"] + subdistricts)

    # ============ valid_reports_df filter =============
    filtered_df = df.copy()

    question_cols = [col for col in filtered_df.columns if re.match(r"^q[1-5]_", col)]

    valid_reports_df = filtered_df[filtered_df[question_cols].sum(axis=1) > 0]

    if selected_year != "ทั้งหมด":
        valid_reports_df = valid_reports_df[valid_reports_df["operation_year"] == selected_year]

    if selected_month != "ทั้งหมด":
        valid_reports_df = valid_reports_df[valid_reports_df["operation_month"] == selected_month]

    if selected_subdistrict != "ทั้งหมด":
        valid_reports_df = valid_reports_df[valid_reports_df["sub_district"] == selected_subdistrict]

    total_activities = valid_reports_df.filter(regex="_times$").sum().sum()
    total_people = valid_reports_df.filter(regex="_people$").sum().sum()
    total_reports = len(valid_reports_df)

    # ============  df_volunteer filter =============
    df_volunteer = df.copy()
    
    if selected_year != "ทั้งหมด":
        df_volunteer = df_volunteer[df_volunteer["operation_year"] == selected_year]
    if selected_month != "ทั้งหมด":
        df_volunteer = df_volunteer[df_volunteer["operation_month"] == selected_month]
    if selected_subdistrict != "ทั้งหมด":
        df_volunteer = df_volunteer[df_volunteer["sub_district"] == selected_subdistrict]

    # ============ scorecard =============
    with col1:
        st.markdown("")
        st.markdown(f"""
            <div style="
                background-color:#1ac230;         
                padding: 1rem 1.5rem; 
                border-radius: 12px;
                text-align: center;                   
                color: white;
                margin-bottom: 1rem;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 1.1rem;">ยอดรายงาน (ครั้ง)</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{total_reports:,}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="
                background-color:#004aad;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 1.1rem;">ยอดกิจกรรม (ครั้ง)</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{total_activities:,}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("")
        st.markdown(f"""
            <div style="
                background-color:#1ac230;
                padding: 1rem 1.5rem;                 
                border-radius: 12px;
                text-align: center;
                color: white;
                margin-bottom: 1rem;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 1.1rem;">ยอดอาสาสมัคร (ราย)</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{ df_volunteer["volunteer_id"].nunique():,}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="
                background-color:#004aad;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                text-align: center;
                color: white;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 1.1rem;">ยอดผู้เข้าร่วม (ราย)</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{total_people:,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")

    # ============ barchart and piechart =============
    colnn1, colnn3 = st.columns([2.2, 1.5])
    with colnn1:
        st.markdown("##### ยอดกิจกรรมในแต่ละหัวข้อ")
    
    with colnn3:
        st.markdown("##### อัตราส่วนกิจกรรมในแต่ละแขวง")

    colbar, colpie = st.columns([1.6, 1])

    with colbar:
        # ============ setting =============
        times_cols = valid_reports_df.filter(regex=r"_times$").columns

        activity_groups = {}

        for col in times_cols:
            match = re.match(r"^q(\d+)_.*_times$", col)
            if match:
                topic = match.group(1)
                if topic not in activity_groups:
                    activity_groups[topic] = []
                activity_groups[topic].append(col)

        topic_name_map = {
            "1": "ป้องกัน",
            "2": "บำบัด",
            "3": "ติดตาม",
            "4": "เครือข่าย",
            "5": "ให้คำปรึกษา"
        }

        # sum every q
        activity_labels = []
        activity_sums = []

        for topic, cols in sorted(activity_groups.items(), key=lambda x: int(x[0])):
            total = valid_reports_df[cols].sum().sum()
            activity_labels.append(topic_name_map.get(topic, f"หัวข้อ {topic}")) 
            activity_sums.append(total)
        
        # ============ barchart =============
        # color
        custom_colors = ["#f98309", "#ffa10e", "#fabc04", "#ffde59", "#ffebcd"]

        # label with value (high -> low)
        sorted_data = sorted(zip(activity_labels, activity_sums), key=lambda x: x[1], reverse=True)

        sorted_labels = [label for label, _ in sorted_data]
        sorted_values = [value for _, value in sorted_data]
        bar_colors = custom_colors[:len(sorted_labels)]

        fig_bar = go.Figure(data=[
            go.Bar(
                x=sorted_labels,
                y=sorted_values,
                marker=dict(
                    color=bar_colors,
                    line=dict(width=0)
                ),
                name="จำนวนกิจกรรม",
                showlegend=False,
                text=[f"{v:,.0f}" for v in sorted_values],
                textposition='outside',
                textfont=dict(
                    family="Kanit",
                    size=12,
                    color="black"
                )
            )
        ])

        y_max = max(sorted_values)
        y_range_max = int(y_max * 1.12)

        # ============ layout =============
        fig_bar.update_layout(
            title=dict(
                text="",
                font=dict(family="Kanit", size=16, color="black"),
                x=0.5
            ),
            barmode="group",
            xaxis_title="หัวข้อกิจกรรม",
            yaxis_title="จำนวน (ครั้ง)",
            font=dict(family="Kanit", size=15),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(family="Kanit", color="black"),
                title_font=dict(size=15, family="Kanit", color="black")
            ),
            yaxis=dict(
                range=[0, y_range_max],
                tickformat=",",
                tickfont=dict(family="Kanit", color="black"),
                title_font=dict(size=15, family="Kanit", color="black")
            ),
#            legend=dict(
#               orientation="h",
#                yanchor="bottom",
#                y=-0.3,
#                xanchor="center",
#                x=0.5
#            ),
            margin=dict(l=20, r=20, t=80, b=80),
            height=400
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # ============= pie chart =============
    with colpie:

        # setting for interactive up to u
        pie_base_df = df.copy()
        if selected_year != "ทั้งหมด":
            pie_base_df = pie_base_df[pie_base_df["operation_year"] == selected_year]
        if selected_month != "ทั้งหมด":
            pie_base_df = pie_base_df[pie_base_df["operation_month"] == selected_month]
        #if selected_subdistrict != "ทั้งหมด":
         #    pie_base_df = pie_base_df[pie_base_df["sub_district"] == selected_subdistrict]

        # merge *_times
        times_cols = pie_base_df.filter(regex=r"_times$").columns
        pie_df = pie_base_df.groupby("sub_district")[times_cols].sum()
        pie_df["total_times"] = pie_df.sum(axis=1)
        pie_df = pie_df[pie_df["total_times"] > 0].sort_values("total_times", ascending=False).head(3).reset_index()

        pie_colors = ["#107c42", "#14b72a", "#64ce12", "#a3dc17", "#d4ee93"]

        fig_pie = go.Figure(data=[
            go.Pie(
                labels=pie_df["sub_district"],
                values=pie_df["total_times"],
                textinfo='percent',
                insidetextorientation='radial',
                hole=0.4,
                marker=dict(colors=pie_colors[:len(pie_df)])
            )
        ])

        fig_pie.update_layout(
            font=dict(family="Kanit", size=13),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.125,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color="black")
            ),
            margin=dict(l=20, r=20, t=40, b=80),
            height=400
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # ============ linechart =============
    st.markdown("##### ยอดผู้เข้าร่วมกิจกรรมในแต่ละเดือน")

    df_line_base = df.copy()

    if selected_year != "ทั้งหมด":
        df_line_base = df_line_base[df_line_base["operation_year"] == selected_year]

    if selected_subdistrict != "ทั้งหมด":
        df_line_base = df_line_base[df_line_base["sub_district"] == selected_subdistrict]

    thai_month_map = {
        "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4,
        "พฤษภาคม": 5, "มิถุนายน": 6, "กรกฎาคม": 7, "สิงหาคม": 8,
        "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12,
    }

    thai_month_abbr = {
        1: "ม.ค.", 2: "ก.พ.", 3: "มี.ค.", 4: "เม.ย.",
        5: "พ.ค.", 6: "มิ.ย.", 7: "ก.ค.", 8: "ส.ค.",
        9: "ก.ย.", 10: "ต.ค.", 11: "พ.ย.", 12: "ธ.ค."
    }

    df_line_base["month_num"] = df_line_base["operation_month"].map(thai_month_map)
    df_line_base["year_gregorian"] = df_line_base["operation_year"] - 543
    df_line_base["operation_date"] = pd.to_datetime(
        df_line_base["year_gregorian"].astype(str) + "-" + df_line_base["month_num"].astype(str) + "-01"
    )

    people_cols = df_line_base.filter(regex="_people$").columns
    df_line = df_line_base.groupby("operation_date")[people_cols].sum().sum(axis=1).reset_index()
    df_line.columns = ["date", "total_people"]

    # label เดือน + พ.ศ.
    df_line["label"] = df_line["date"].dt.month.map(thai_month_abbr) + " " + (df_line["date"].dt.year + 543).astype(str)

    # plot
    fig_line = px.line(
        df_line,
        x="label",
        y="total_people",
        labels={"label": "เดือน", "total_people": "จำนวนผู้เข้าร่วม (ราย)"},
    )

    # layout
    fig_line.update_traces(
        line_color="#004aad",
        mode="lines+markers",  
        marker=dict(size=8, color="#004aad")
    )

    fig_line.update_layout(
        font=dict(family="Kanit", size=16),
        height=400,
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis=dict(
            title_font=dict(size=15, color="black"),
            tickfont=dict(color="black")
        ),
        yaxis=dict(
            title_font=dict(size=15, color="black"),
            tickfont=dict(color="black")
        ))

    st.plotly_chart(fig_line, use_container_width=True)

    # ============ volunteer check submit =============
    st.markdown("""
        <div style='font-family: "Kanit", sans-serif; margin-top: 1rem; text-align: center;'>
            <span style='font-size: 1.25rem; color: black; font-weight: bold;'>
                อัตราส่วนยอดการส่งรายงานของอาสาสมัคร
            </span>
        </div>
    """, unsafe_allow_html=True)
    colnnn1, colnnn3 = st.columns([2.2, 1])
    with colnnn1:
        st.markdown("""
            <div style='font-family: "Kanit", sans-serif; margin-top: 1rem;'>
                <span style='font-size: 1.25rem; color: black; font-weight: bold;'>
                    รายชื่ออาสาสมัครที่
                    <span style='color: #d20d0d;'>ไม่ส่งรายงาน</span>              
                </span>
                <span style='font-size: 0.9rem; color: #808495; font-weight: normal;'>
                    (แสดงสูงสุด 500 รายการ)
                </span>
            </div>
        """, unsafe_allow_html=True)
    
    with colnnn3:
        pass
    
    st.markdown("")

    coltable, colpie2 = st.columns([1.6, 1])

    with coltable:

        question_cols = [col for col in df.columns if re.match(r"^q[1-5]_", col)]
        df_missing = df.copy()

        if selected_year != "ทั้งหมด":
            df_missing = df_missing[df_missing["operation_year"] == selected_year]
        if selected_month != "ทั้งหมด":
            df_missing = df_missing[df_missing["operation_month"] == selected_month]
        if selected_subdistrict != "ทั้งหมด":
            df_missing = df_missing[df_missing["sub_district"] == selected_subdistrict]

        df_missing["has_answer"] = df_missing[question_cols].sum(axis=1) > 0
        df_missing = df_missing[df_missing["has_answer"] == False]

        column_rename_map_missing = {
            "id": "รหัส",
            "volunteer_id": "เลขอาสาสมัคร",
            "prefix": "คำนำหน้า",
            "first_name": "ชื่อ",
            "last_name": "นามสกุล",
            "community": "ชุมชน",
            "sub_district": "แขวง",
            "operation_month": "เดือน",
            "operation_year": "ปี",
        }

        df_missing_display = df_missing[list(column_rename_map_missing.keys())].rename(columns=column_rename_map_missing)

        if 'รหัส' in  df_missing_display.columns:
             df_missing_display =  df_missing_display.set_index('รหัส').sort_index()

        st.dataframe(df_missing_display.head(500))

    with colpie2:
        
        df_pie2 = df.copy()

        if selected_year != "ทั้งหมด":
            df_pie2 = df_pie2[df_pie2["operation_year"] == selected_year]
        if selected_month != "ทั้งหมด":
            df_pie2 = df_pie2[df_pie2["operation_month"] == selected_month]
        if selected_subdistrict != "ทั้งหมด":
            df_pie2 = df_pie2[df_pie2["sub_district"] == selected_subdistrict]

        question_cols = [col for col in df_pie2.columns if re.match(r"^q[1-5]_", col)]
        df_pie2["has_answer"] = df_pie2[question_cols].sum(axis=1) > 0

        summary_pie = df_pie2["has_answer"].value_counts().reset_index()
        summary_pie.columns = ["answered", "count"]
        summary_pie["label"] = summary_pie["answered"].map({
            True: "อาสาสมัครที่ส่งรายงาน",
            False: "อาสาสมัครที่ไม่ส่งรายงาน"
        })

        pie_colors = ["#d7d7d7", "#d20d0d"]

        fig_pie = go.Figure(data=[
            go.Pie(
                labels=summary_pie["label"],
                values=summary_pie["count"],
                textinfo='percent',
                insidetextorientation='radial',
                #hole=0.4,
                marker=dict(colors=pie_colors[:len(summary_pie)])
            )
        ])

        fig_pie.update_layout(
            font=dict(family="Kanit", size=13),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.125,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color="black")
            ),
            margin=dict(l=20, r=20, t=40, b=80),
            height=400
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # ============ table (dataframe) =============
    st.markdown("""
        <div style='font-family: "Kanit", sans-serif; margin-top: 1rem;'>
            <span style='font-size: 1.25rem; color: black; font-weight: bold;'>
                รายงานทั้งหมด 
            </span>
            <span style='font-size: 0.9rem; color: #808495; font-weight: normal;'>
                (แสดงสูงสุด 500 รายการ)
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    display_df = valid_reports_df.copy()

    column_rename_map = {
        "id": "รหัส",
        "volunteer_id": "เลขอาสาสมัคร",
        "prefix": "คำนำหน้า",
        "first_name": "ชื่อ",
        "last_name": "นามสกุล",
        "community": "ชุมชน",
        "sub_district": "แขวง",
        "district": "เขต",
        "operation_month": "เดือน",
        "operation_year": "ปี",
        "q1_prevention1_times": "ข้อ 1.1 (ครั้ง)",
        "q1_prevention1_people": "ข้อ 1.1 (ราย)",
        "q1_prevention2_times": "ข้อ 1.2 (ครั้ง)",
        "q1_prevention3_times": "ข้อ 1.3 (ครั้ง)",
        "q1_prevention4_times": "ข้อ 1.4 (ครั้ง)",
        "q1_prevention4_people": "ข้อ 1.4 (ราย)",
        "q1_prevention5_times": "ข้อ 1.5 (ครั้ง)",
        "q2_treatment1_times": "ข้อ 2.1 (ครั้ง)",
        "q2_treatment1_people": "ข้อ 2.1 (ราย)",
        "q2_treatment2_times": "ข้อ 2.2 (ครั้ง)",
        "q2_treatment3_times": "ข้อ 2.3 (ครั้ง)",
        "q2_treatment3_people": "ข้อ 2.3 (ราย)",
        "q2_treatment4_times": "ข้อ 2.4 (ครั้ง)",
        "q2_treatment4_people": "ข้อ 2.4 (ราย)",
        "q2_treatment5_times": "ข้อ 2.5 (ครั้ง)",
        "q3_assistance_times": "ข้อ 3 (ครั้ง)",
        "q3_assistance_people": "ข้อ 3 (ราย)",
        "q4_engaging1_times": "ข้อ 4.1 (ครั้ง)",
        "q4_engaging2_times": "ข้อ 4.2 (ครั้ง)",
        "q5_consult_times": "ข้อ 5 (ครั้ง)",
        "q5_consult_people": "ข้อ 5 (ราย)",
        "q6_others": "อื่น ๆ",
        "notes": "หมายเหตุ",
        "created_at": "กรอกเมื่อ",
        
    }

    display_df = display_df.rename(columns=column_rename_map)

    if 'รหัส' in display_df.columns:
        display_df = display_df.set_index('รหัส').sort_index()

    st.dataframe(display_df.head(500))

# ==================== done ! ==================== 