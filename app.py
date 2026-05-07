import streamlit as st
import calendar
from datetime import date

st.set_page_config(page_title="図書委員当番表", layout="centered")
st.title("📚 図書委員当番表")

# 1組から8組までのセットを生成
duty_groups = [[f"3-{i}", f"2-{i}", f"1-{i}"] for i in range(1, 9)]

# 【調整ポイント】
# 5/11の週が「3組セット(index 2)」になるように、
# 5/4の週(GW)を「2組セット(index 1)」として基準日を設定します。
duty_groups = duty_groups

with st.sidebar:
    st.header("表示設定")
    year = st.number_input("年", value=2026, min_value=2024)
    month = st.selectbox("月", list(range(1, 13)), index=4)

if st.button("当番表を生成"):
    cal = calendar.Calendar(firstweekday=0)
    days = cal.itermonthdays2(year, month)
    
    st.subheader(f"📅 {year}年{month}月")

    # 基準を5月4日の週（第19週）に設定
    base_date = date(2026, 5, 4) 
    base_week = base_date.isocalendar()[1]
    
    results = []
    for day, weekday in days:
        if day == 0 or weekday >= 5:
            continue
        
        current_date = date(year, month, day)
        current_week = current_date.isocalendar()[1]
        
        # 5/4の週から数えて何週目かを計算
        # 5/4の週=0(2組), 5/11の週=1(3組) ... となるように設定
        week_diff = current_week - base_week
        
        # 2組セットから開始したいので +1 する
        group_index = (week_diff + 1) % len(duty_groups)
        current_group = " / ".join(duty_groups[group_index])
        
        weekday_name = "月火水木金"[weekday]
        results.append({"日付": f"{month}/{day:02d}({weekday_name})", "当番クラス": current_group})

    st.table(results)
