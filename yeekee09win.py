import streamlit as st
import pandas as pd
import re

# =========================================
# 1. สมองกล: สูตรที่ 8 (The Oracle Matrix)
# =========================================
def my_custom_formula_updated(top_T, bot_T, top_P, bot_P):
   # ข้อมูลรอบปัจจุบัน (T)
    t1_T = int(str(top_T).zfill(3)[0]) # หลักร้อยบน
    t3_T = int(str(top_T).zfill(3)[2]) # หลักหน่วยบน
    b2_T = int(str(bot_T).zfill(2)[1]) # หลักหน่วยล่าง

    # ข้อมูลรอบก่อนหน้า (P)
    t3_P = int(str(top_P).zfill(3)[2]) # หลักหน่วยบนรอบก่อน

    # 🎯 ชุดที่ 1: "The Statistical Trap" (ดักสถิติ 5 ตัว)
    base = (t1_T + b2_T) % 10
    # ใช้ฐาน, พี่น้อง(+1, +2), เงา(+5), และเลขสถิติ(+8)
    set_1 = [base, (base + 1) % 10, (base + 2) % 10, (base + 5) % 10, (base + 8) % 10]

    # 🎯 ชุดที่ 2: "The Momentum Guard" (เลขกัน 3 ตัว)
    lag = (t3_T + t3_P) % 10
    # ใช้ค่าหน่วง, และเลขข้างเคียงซ้าย-ขวา
    set_2 = [lag, (lag + 1) % 10, (lag + 9) % 10]
    
    return set_1, set_2

# =========================================
# 2. ฟังก์ชันทำความสะอาดข้อมูล
# =========================================
def clean_and_prepare_data(df):
    top_cols = [c for c in df.columns if 'top' in str(c).lower()]
    bot_cols = [c for c in df.columns if 'bottom' in str(c).lower()]
    if len(top_cols) > 0 and len(bot_cols) > 0:
        min_len = min(len(top_cols), len(bot_cols))
        all_top = pd.concat([df[top_cols[i]] for i in range(min_len)], ignore_index=True)
        all_bot = pd.concat([df[bot_cols[i]] for i in range(min_len)], ignore_index=True)
        clean_df = pd.DataFrame({'top': all_top, 'bottom': all_bot})
    else:
        clean_df = df.copy()
    clean_df['top'] = clean_df['top'].astype(str).str.strip()
    clean_df['bottom'] = clean_df['bottom'].astype(str).str.strip()
    clean_df = clean_df[clean_df['top'].str.isnumeric() & clean_df['bottom'].str.isnumeric()]
    return clean_df.reset_index(drop=True)

# =========================================
# 3. ฟังก์ชัน Backtest แบบ Two-Period Lag
# =========================================
def run_detailed_backtest(df):
    results_list = []
    # เริ่มที่รอบที่ 1 เพื่อให้มี i-1 (รอบก่อนหน้า) มาคำนวณ
    total_rows = len(df)
    hits_top = 0
    hits_bottom = 0
    count = 0

    for i in range(1, total_rows - 1):
        curr_top = df.iloc[i]['top']
        curr_bot = df.iloc[i]['bottom']
        prev_top = df.iloc[i-1]['top']
        prev_bot = df.iloc[i-1]['bottom']
        
        next_top = str(df.iloc[i+1]['top']).zfill(3)
        next_bot = str(df.iloc[i+1]['bottom']).zfill(2)

        set1, set2 = my_custom_formula_updated(curr_top, curr_bot, prev_top, prev_bot)
        
        pred_str = f"{', '.join(map(str, set1))} / {', '.join(map(str, set2))}"
        predicted_digits = set(set1).union(set(set2))

        is_hit_top = any(str(d) in next_top for d in predicted_digits)
        is_hit_bot = any(str(d) in next_bot for d in predicted_digits)

        if is_hit_top: hits_top += 1
        if is_hit_bot: hits_bottom += 1
        count += 1

        results_list.append({
            "ลำดับคิว": i + 1,
            "เลขฐาน (บน/ล่าง)": f"{curr_top} / {curr_bot}",
            "เลขเด่น (ชุด1 / ชุด2)": pred_str,
            "ผลรอบถัดไป": f"{next_top} / {next_bot}",
            "ผลบน": "✅ เข้า" if is_hit_top else "❌ หลุด",
            "ผลล่าง": "✅ เข้า" if is_hit_bot else "❌ หลุด"
        })

    report_df = pd.DataFrame(results_list)
    t_acc = (hits_top / count * 100) if count > 0 else 0
    b_acc = (hits_bottom / count * 100) if count > 0 else 0
    return report_df, hits_top, t_acc, hits_bottom, b_acc

# =========================================
# 4. ส่วนแสดงผล UI
# =========================================
st.set_page_config(page_title="Oracle Matrix V8", page_icon="🔮")
st.title("🔮 The Oracle Matrix (95% Target)")

tab1, tab2 = st.tabs(["🔍 คำนวณรายรอบ", "📊 ทดสอบสถิติ CSV"])

with tab1:
    st.subheader("กรอกข้อมูลเพื่อพยากรณ์")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**รอบปัจจุบัน (T)**")
        top_T = st.text_input("บนปัจจุบัน", placeholder="เช่น 240", key="t_t")
        bot_T = st.text_input("ล่างปัจจุบัน", placeholder="เช่น 02", key="b_t")
    with c2:
        st.markdown("**รอบก่อนหน้า (P)**")
        top_P = st.text_input("บนก่อนหน้า", placeholder="เช่น 746", key="t_p")
        bot_P = st.text_input("ล่างก่อนหน้า", placeholder="เช่น 91", key="b_p")

    if st.button("🚀 คำนวณเลขพยากรณ์"):
        if all([top_T, bot_T, top_P, bot_P]):
            s1, s2 = my_custom_formula_updated(top_T, bot_T, top_P, bot_P)
            res1, res2 = st.columns(2)
            res1.info(f"🎯 ชุดที่ 1: {', '.join(map(str, s1))}")
            res2.warning(f"🎯 ชุดที่ 2: {', '.join(map(str, s2))}")
        else:
            st.error("กรุณากรอกข้อมูลให้ครบทั้งรอบปัจจุบันและรอบก่อนหน้า")

with tab2:
    uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        cleaned_df = clean_and_prepare_data(df)
        if len(cleaned_df) > 2:
            report_df, h_t, a_t, h_b, a_b = run_detailed_backtest(cleaned_df)
            st.success(f"วิเคราะห์สำเร็จ! ความแม่นยำบน: {a_t:.2f}% | ล่าง: {a_b:.2f}%")
            st.dataframe(report_df.style.apply(lambda r: ['background-color: #d4edda' if (r['ผลบน'] == '✅ เข้า' or r['ผลล่าง'] == '✅ เข้า') else '' for _ in r], axis=1))
