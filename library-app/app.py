import streamlit as st
import calendar
from datetime import date

st.title("📚 図書委員当番表（全8クラス・週替わり）")

# --- 1. 当番グループの自動生成 ---
# 1組から8組まで、各学年の同じ組をセットにします
# 例: [["3-1", "2-1", "1-1"], ["3-2", "2-2", "1-2"], ..., ["3-8", "2-8", "1-8"]]
duty_groups = [[f"3-{i}", f"2-{i}", f"1-{i}"] for i in range(1, 9)]

# 5月1日は「3-2, 2-2, 1-2」から始めたいので、リストを調整
# 2組(index 1)を先頭にするために、リストを並び替えます
# 2組, 3組, ..., 8組, 1組 の順番
duty_groups = duty_groups[1:] + duty_groups[:1]

with st.sidebar:
    st.header("表示設定")
    year = st.number_input("年", value=2026, min_value=2024)
    month = st.selectbox("月", list(range(1, 13)), index=4) # 5月

if st.button("当番表を生成"):
    cal = calendar.Calendar(firstweekday=0)
    days = cal.itermonthdays2(year, month)
    
    st.subheader(f"📅 {year}年{month}月の当番")

    # 基準となる2026年5月1日の週番号を取得
    base_date = date(2026, 5, 1)
    base_week = base_date.isocalendar()[1] # 年間の週番号
    base_year = base_date.isocalendar()[0] # ISO年
    
    results = []
    
    for day, weekday in days:
        if day == 0 or weekday >= 5: # 土日除外
            continue
        
        current_date = date(year, month, day)
        iso_val = current_date.isocalendar()
        current_year = iso_val[0]
        current_week = iso_val[1]
        
        # 週の差分を計算（年をまたぐ場合も考慮）
        # 簡易的に基準週からの経過週数を計算
        week_diff = (current_year - base_year) * 52 + (current_week - base_week)
        
        # 8つのグループをループ
        group_index = week_diff % len(duty_groups)
        current_group = duty_groups[group_index]
        
        group_str = " / ".join(current_group)
        weekday_name = "月火水木金"[weekday]
        
        results.append({
            "日付": f"{month}/{day:02d} ({weekday_name})",
            "今週の当番": group_str
        })

    # 表示
    st.table(results)

st.info("5月1日の週を「2組セット」として、毎週月曜に次の組へ交代します。")
