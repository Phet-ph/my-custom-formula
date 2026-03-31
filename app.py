import streamlit as st
import pandas as pd
import itertools

# =========================================
# 1. สมองกล: ฟังก์ชันสมการของคุณ
# =========================================
def my_custom_formula_updated(top_str, bottom_str):
    t1 = int(str(top_str).zfill(3)[0])
    t2 = int(str(top_str).zfill(3)[1])
    b1 = int(str(bottom_str).zfill(2)[0])
    b2 = int(str(bottom_str).zfill(2)[1])

    # ชุดที่ 1
    start_num = (t1 + b1) % 10  
    set_1 = [start_num, (start_num + 3) % 10, (start_num + 6) % 10]

    # ชุดที่ 2
    set_2 = [(t2 + b1) % 10, (b1 + b2) % 10]

    return set_1, set_2

# =========================================
# 2. ฟังก์ชันทดสอบความแม่นยำ (Backtest รายรอบ)
# =========================================
def run_detailed_backtest(df):
    results_list = []
    total_rounds = len(df) - 1
    hits_top = 0
    hits_bottom = 0

    for i in range(total_rounds):
        curr_top = str(df.iloc[i]['top']).zfill(3)
        curr_bot = str(df.iloc[i]['bottom']).zfill(2)
        next_top = str(df.iloc[i+1]['top']).zfill(3)
        next_bot = str(df.iloc[i+1]['bottom']).zfill(2)

        set1, set2 = my_custom_formula_updated(curr_top, curr_bot)
        predicted_digits = set(set1).union(set(set2))
        pred_str = ", ".join(map(str, sorted(list(predicted_digits))))

        is_hit_top = any(str(d) in next_top for d in predicted_digits)
        is_hit_bot = any(str(d) in next_bot for d in predicted_digits)

        if is_hit_top: hits_top += 1
        if is_hit_bot: hits_bottom += 1

        results_list.append({
            "รอบที่": i + 1,
            "เลขฐาน (บน/ล่าง)": f"{curr_top} / {curr_bot}",
            "เลขเด่นที่ได้": pred_str,
            "ผลรอบถัดไป": f"{next_top} / {next_bot}",
            "ผลลัพธ์บน": "✅ เข้า" if is_hit_top else "❌ หลุด",
            "ผลลัพธ์ล่าง": "✅ เข้า" if is_hit_bot else "❌ หลุด"
        })

    report_df = pd.DataFrame(results_list)
    top_acc = (hits_top / total_rounds) * 100 if total_rounds > 0 else 0
    bot_acc = (hits_bottom / total_rounds) * 100 if total_rounds > 0 else 0

    return report_df, hits_top, top_acc, hits_bottom, bot_acc

# =========================================
# 3. ฟังก์ชันไฮไลท์สีตาราง
# =========================================
def highlight_hits(row):
    # ถ้าเข้าเป้าบน หรือ เข้าเป้าล่าง ให้ระบายสีเขียวอ่อนทั้งบรรทัด
    if row['ผลลัพธ์บน'] == '✅ เข้า' or row['ผลลัพธ์ล่าง'] == '✅ เข้า':
        return ['background-color: #d4edda; color: #155724'] * len(row)
    return [''] * len(row)

# =========================================
# 4. ส่วนแสดงผล (Frontend UI)
# =========================================
st.set_page_config(page_title="ระบบวิเคราะห์ตัวเลขขั้นสูง", page_icon="🧮", layout="centered")

st.title("🧮 ระบบวิเคราะห์ตัวเลข (Custom Algorithm)")
st.markdown("---")

tab1, tab2 = st.tabs(["🔍 คำนวณรายรอบ (Manual)", "📊 ทดสอบความแม่นยำ (Backtest CSV)"])

# -----------------------------------------
# แท็บที่ 1: ระบบกรอกข้อมูลแบบแมนนวล
# -----------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        top_input = st.text_input("กรอกเลขบน (3 หลัก)", max_chars=3, placeholder="เช่น 825", key="man_top")
    with col2:
        bottom_input = st.text_input("กรอกเลขล่าง (2 หลัก)", max_chars=2, placeholder="เช่น 35", key="man_bot")

    if st.button("🚀 ประมวลผลสมการ", use_container_width=True):
        if len(top_input) == 3 and len(bottom_input) == 2 and top_input.isdigit() and bottom_input.isdigit():
            result_set1, result_set2 = my_custom_formula_updated(top_input, bottom_input)
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.info("🎯 **เลขเด่นชุดที่ 1**")
                st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>{', '.join(map(str, result_set1))}</h2>", unsafe_allow_html=True)
            with res_col2:
                st.warning("🎯 **เลขเด่นชุดที่ 2
