import streamlit as st
import pandas as pd
import re
import itertools

# =========================================
# 1. สมองกล: สูตรที่ 9 (The Statistical Fusion)
# =========================================
def my_custom_formula_updated(top_T, bot_T, top_P, bot_P):
    try:
        # สกัดเอาเฉพาะ "ตัวเลข" เท่านั้น และเติม 0 ด้านหน้า
        top_T_clean = re.sub(r'\D', '', str(top_T)).zfill(3)
        bot_T_clean = re.sub(r'\D', '', str(bot_T)).zfill(2)
        top_P_clean = re.sub(r'\D', '', str(top_P)).zfill(3)
        bot_P_clean = re.sub(r'\D', '', str(bot_P)).zfill(2)

        # ดึงค่าหลักตัวเลข
        t1_T = int(top_T_clean[0])
        t3_T = int(top_T_clean[2])
        b2_T = int(bot_T_clean[1])
        t3_P = int(top_P_clean[2])

        # 🎯 ชุดที่ 1: ดักสถิติ 5 ตัว (ฐาน + พี่น้อง + เงา + เลขสถิติ)
        base = (t1_T + b2_T) % 10
        set_1 = [base, (base + 1) % 10, (base + 2) % 10, (base + 5) % 10, (base + 8) % 10]

        # 🎯 ชุดที่ 2: เลขหน่วงกันพลาด 3 ตัว
        lag = (t3_T + t3_P) % 10
        set_2 = [lag, (lag + 1) % 10, (lag + 9) % 10]
        
        return set_1, set_2
    except Exception as e:
        return [], []

# =========================================
# 2. ฟังก์ชันจับคู่เลขวิน (Win Generator)
# =========================================
def generate_win_numbers(pool):
    # จับคู่ 2 ตัว (สำหรับ 2 ตัวบน และ 2 ตัวล่าง)
    win_2 = list(itertools.combinations(pool, 2))
    win_2_str = ", ".join([f"{a}{b}" for a, b in win_2])
    
    # จับคู่ 3 ตัว (สำหรับ 3 ตัวบน)
    win_3 = list(itertools.combinations(pool, 3))
    win_3_str = ", ".join([f"{a}{b}{c}" for a, b, c in win_3])
    
    # เพิ่มเลขเบิ้ล (กรณีอยากกันเหนียว)
    doubles = ", ".join([f"{a}{a}" for a in pool])
    
    return win_2_str, win_3_str, doubles, len(win_2), len(win_3)

# =========================================
# 3. ฟังก์ชันทำความสะอาดข้อมูล (สำหรับ CSV)
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
# 4. ฟังก์ชัน Backtest ทดสอบความแม่นยำ
# =========================================
def run_detailed_backtest(df):
    results_list = []
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
# 5. ส่วนแสดงผล UI (Streamlit)
# =========================================
st.set_page_config(page_title="Statistical Fusion V9", page_icon="📈")
st.title("📈 The Statistical Fusion (เป้าหมาย 95%)")

tab1, tab2 = st.tabs(["🔍 คำนวณรายรอบ + จับคู่วิน", "📊 ทดสอบสถิติ CSV"])

with tab1:
    st.subheader("กรอกข้อมูลเพื่อสร้างชุดเลขแทง")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**รอบปัจจุบัน (T)**")
        top_T = st.text_input("บนปัจจุบัน", placeholder="เช่น 240", key="t_t")
        bot_T = st.text_input("ล่างปัจจุบัน", placeholder="เช่น 02", key="b_t")
    with c2:
        st.markdown("**รอบก่อนหน้า (P)**")
        top_P = st.text_input("บนก่อนหน้า", placeholder="เช่น 746", key="t_p")
        bot_P = st.text_input("ล่างก่อนหน้า", placeholder="เช่น 91", key="b_p")

    if st.button("🚀 คำนวณเลขพยากรณ์และจับคู่วิน"):
        if top_T and bot_T and top_P and bot_P:
            s1, s2 = my_custom_formula_updated(top_T, bot_T, top_P, bot_P)
            
            if len(s1) > 0 and len(s2) > 0:
                # รวมเลขเด่น ตัดตัวซ้ำ และเรียงลำดับใหม่ให้สวยงาม
                pool = sorted(list(set(s1 + s2)))
                
                st.success(f"🎯 กลุ่มเลขเด่นที่คำนวณได้ ({len(pool)} ตัว): **{', '.join(map(str, pool))}**")
                
                # นำเลขไปเข้าเครื่องกำเนิดเลขวิน
                win_2, win_3, doubles, count_2, count_3 = generate_win_numbers(pool)
                
                st.markdown("---")
                st.markdown("### 📋 ชุดเลขนำไปใช้งานจริง (Copy ไปแทงได้เลย)")
                
                st.info(f"**🟢 วิน 2 ตัว (นำไปกด 2 ตัวบน / 2 ตัวล่าง + กดกลับเลขด้วย):**\n\nมีทั้งหมด {count_2} ชุด\n\n`{win_2}`")
                
                st.warning(f"**🟡 วิน 3 ตัว (นำไปกด 3 ตัวบนโต๊ด หรือ 6 กลับ):**\n\nมีทั้งหมด {count_3} ชุด\n\n`{win_3}`")
                
                st.error(f"**🔴 เลขเบิ้ลกันพลาด (สำหรับคนชอบดักเบิ้ล):**\n\n`{doubles}`")
            else:
                st.error("❌ เกิดข้อผิดพลาดในการคำนวณ โปรดตรวจสอบว่ากรอกเฉพาะ 'ตัวเลข' เท่านั้น")
        else:
            st.error("⚠️ กรุณากรอกข้อมูลให้ครบทั้ง 4 ช่องเพื่อความแม่นยำสูงสุด")

with tab2:
    uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        cleaned_df = clean_and_prepare_data(df)
        if len(cleaned_df) > 2:
            report_df, h_t, a_t, h_b, a_b = run_detailed_backtest(cleaned_df)
            st.success(f"วิเคราะห์สำเร็จ! ความแม่นยำบน: {a_t:.2f}% | ล่าง: {a_b:.2f}%")
            
            # การไฮไลต์สีเขียวเมื่อทายถูก
            st.dataframe(report_df.style.apply(lambda r: ['background-color: #d4edda' if (r['ผลบน'] == '✅ เข้า' or r['ผลล่าง'] == '✅ เข้า') else '' for _ in r], axis=1))
