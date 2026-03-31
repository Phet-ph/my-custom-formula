import streamlit as st
import pandas as pd
import itertools


  
  # สูตรที่ 8: The Oracle Matrix (เป้าหมายสูงสุด 95%)
def my_custom_formula_updated(top_T, bot_T, top_P, bot_P):
    # รอบปัจจุบัน (T)
    t1_T = int(str(top_T).zfill(3)[0])
    t2_T = int(str(top_T).zfill(3)[1])
    t3_T = int(str(top_T).zfill(3)[2])
    b1_T = int(str(bot_T).zfill(2)[0])
    b2_T = int(str(bot_T).zfill(2)[1])

    # รอบก่อนหน้า (P)
    t3_P = int(str(top_P).zfill(3)[2])

    # 🎯 ชุดที่ 1: "The Core Oracle" (ร้อยบนT + สิบบนT + หน่วยบนP)
    # ใช้แกนกลาง 3 จุดเพื่อสร้างสเต็ป 3-6-9
    oracle_num = (t1_T + t2_T + t3_P) % 10
    set_1 = [oracle_num, (oracle_num + 3) % 10, (oracle_num + 6) % 10, (oracle_num + 9) % 10]

    # 🎯 ชุดที่ 2: "The Guard Matrix" (สิบบนT + สิบล่างT) และเลขพี่น้อง+เงา
    # ดักทางเลขเฉี่ยวและเลขตรงข้าม
    guard_base = (t2_T + b1_T) % 10
    # ใช้ฐานเดิม, พี่น้องซ้าย-ขวา, และเงาสะท้อน(+5)
    set_2 = [guard_base, (guard_base + 1) % 10, (guard_base + 9) % 10, (guard_base + 5) % 10]
    
    return set_1, set_2

# =========================================
# 2. ฟังก์ชันทำความสะอาดข้อมูล (Auto-Data Cleaner)
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
# 3. ฟังก์ชันทดสอบความแม่นยำ (อัปเดตการแสดงผลตาราง)
# =========================================
def run_detailed_backtest(df):
    results_list = []
    # เริ่มที่รอบที่ 1 (ซึ่งคือรอบที่ 2 ในตาราง) เพื่อให้มีข้อมูลย้อนหลัง i-1
    total_rounds = len(df) - 1
    hits_top = 0
    hits_bottom = 0

    for i in range(1, total_rounds):
        # ข้อมูลรอบปัจจุบัน (T)
        curr_top = df.iloc[i]['top']
        curr_bot = df.iloc[i]['bottom']
        
        # ข้อมูลรอบก่อนหน้า (P) - นี่คือหัวใจของ Two-Period Lag
        prev_top = df.iloc[i-1]['top']
        prev_bot = df.iloc[i-1]['bottom']
        
        # ข้อมูลรอบถัดไป (Next) เพื่อเอาไว้ตรวจผล
        next_top = str(df.iloc[i+1]['top']).zfill(3)
        next_bot = str(df.iloc[i+1]['bottom']).zfill(2)

        # เรียกใช้สูตรที่ 5
        set1, set2 = my_custom_formula_updated(curr_top, curr_bot, prev_top, prev_bot)
        
        # 📌 [จุดที่แก้ไข] สร้างข้อความแยกชุดที่ 1 และชุดที่ 2 คั่นด้วย /
        str_set1 = ", ".join(map(str, set1))
        str_set2 = ", ".join(map(str, set2))
        pred_str_display = f"{str_set1} / {str_set2}"

        # นำมารวมกันเป็น Set เพื่อใช้ตรวจคำตอบ (ไม่ให้ตรวจเลขซ้ำเบิ้ล)
        predicted_digits = set(set1).union(set(set2))

        is_hit_top = any(str(d) in next_top for d in predicted_digits)
        is_hit_bot = any(str(d) in next_bot for d in predicted_digits)

        if is_hit_top: hits_top += 1
        if is_hit_bot: hits_bottom += 1

        results_list.append({
            "ลำดับคิว": i + 1,
            "เลขฐาน (บน/ล่าง)": f"{curr_top} / {curr_bot}",
            "เลขเด่นที่ได้ (ช1 / ช2)": pred_str_display,  # 📌 แสดงผลแบบมี /
            "ผลรอบถัดไป": f"{next_top} / {next_bot}",
            "ผลลัพธ์บน": "✅ เข้า" if is_hit_top else "❌ หลุด",
            "ผลลัพธ์ล่าง": "✅ เข้า" if is_hit_bot else "❌ หลุด"
        })

    report_df = pd.DataFrame(results_list)
    top_acc = (hits_top / total_rounds) * 100 if total_rounds > 0 else 0
    bot_acc = (hits_bottom / total_rounds) * 100 if total_rounds > 0 else 0

    return report_df, hits_top, top_acc, hits_bottom, bot_acc

# =========================================
# 4. ฟังก์ชันไฮไลท์สีตาราง
# =========================================
def highlight_hits(row):
    if row['ผลลัพธ์บน'] == '✅ เข้า' or row['ผลลัพธ์ล่าง'] == '✅ เข้า':
        return ['background-color: #d4edda; color: #155724'] * len(row)
    return [''] * len(row)

# =========================================
# 5. ส่วนแสดงผล (Frontend UI)
# =========================================
st.set_page_config(page_title="ระบบวิเคราะห์ตัวเลขขั้นสูง", page_icon="🧮", layout="centered")

st.title("🧮 ระบบวิเคราะห์ตัวเลข (Custom Algorithm)")
st.markdown("---")

tab1, tab2 = st.tabs(["🔍 คำนวณรายรอบ (Manual)", "📊 ทดสอบความแม่นยำ (Backtest CSV)"])

with tab1:
    col1, col2 = st.columns(2)
    top_input = col1.text_input("กรอกเลขบน (3 หลัก)", max_chars=3, placeholder="เช่น 825", key="man_top")
    bottom_input = col2.text_input("กรอกเลขล่าง (2 หลัก)", max_chars=2, placeholder="เช่น 35", key="man_bot")

    if st.button("🚀 ประมวลผลสมการ", use_container_width=True):
        if len(top_input) == 3 and len(bottom_input) == 2 and top_input.isdigit() and bottom_input.isdigit():
            result_set1, result_set2 = my_custom_formula_updated(top_input, bottom_input)
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.info("🎯 **เลขเด่นชุดที่ 1**")
                st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>{', '.join(map(str, result_set1))}</h2>", unsafe_allow_html=True)
            with res_col2:
                st.warning("🎯 **เลขเด่นชุดที่ 2**")
                st.markdown(f"<h2 style='text-align: center; color: #ff7f0e;'>{', '.join(map(str, result_set2))}</h2>", unsafe_allow_html=True)
                
            common_numbers = set(result_set1).intersection(set(result_set2))
            all_numbers = set(result_set1).union(set(result_set2))
            
            st.markdown("---")
            if 6 in all_numbers or 9 in all_numbers:
                st.info("🔮 **สัญญาณพิเศษ:** พบเลข **6** หรือ **9** (โอกาสออกเลขตอง / 69 / 96)")

            if len(common_numbers) > 0:
                intersect_str = ', '.join(map(str, common_numbers))
                st.error(f"🚨 **พบเลขชน:** **[ {intersect_str} ]** (อาจออกเลขเบิ้ล/ตอง)")
                
                two_digits = []
                for num1 in result_set1:
                    for num2 in result_set2:
                        two_digits.extend([f"{num1}{num2}", f"{num2}{num1}"])
                two_digits = sorted(list(set(two_digits)))
                
                st.success("✨ **ระบบทำการจับคู่เลขหลักสิบให้อัตโนมัติ**")
                st.code(" | ".join(two_digits))
        else:
            st.error("⚠️ ข้อมูลไม่ถูกต้อง: กรุณากรอกตัวเลขให้ครบถ้วน")

with tab2:
    st.subheader("📁 อัปโหลดไฟล์ประวัติ (CSV)")
    st.markdown("ระบบจะกวาดหาตัวเลขจากทุกคอลัมน์อัตโนมัติ ไม่ต้องจัดรูปแบบไฟล์ใหม่!")
    
    uploaded_file = st.file_uploader("เลือกไฟล์ CSV ประวัติของคุณ", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            has_top_bot = any('top' in str(c).lower() or 'bottom' in str(c).lower() for c in df.columns)
            
            if has_top_bot:
                cleaned_df = clean_and_prepare_data(df)
                
                if len(cleaned_df) < 2:
                    st.error("❌ ไม่พบข้อมูลตัวเลขที่สมบูรณ์เพียงพอ (ต้องการอย่างน้อย 2 รอบ)")
                else:
                    st.success(f"🧹 AI ทำความสะอาดข้อมูลสำเร็จ! ดึงข้อมูลรวมกันได้ทั้งหมด **{len(cleaned_df)}** รอบ")
                    
                    with st.spinner('กำลังประมวลผลสถิติและสร้างตารางรายงาน (อาจใช้เวลา 2-3 วินาที)...'):
                        report_df, hit_t, acc_t, hit_b, acc_b = run_detailed_backtest(cleaned_df)

                    st.markdown("### 🏆 สรุปภาพรวมความแม่นยสูตรที่ 7 - The Infinity Loopวงจรเลขไหลอินฟินิตี้")
                    m1, m2 = st.columns(2)
                    m1.metric("ความแม่นยำ (เข้าเลขบน)", f"{acc_t:.2f}%", f"เข้า {hit_t} รอบ")
                    m2.metric("ความแม่นยำ (เข้าเลขล่าง)", f"{acc_b:.2f}%", f"เข้า {hit_b} รอบ")

                    st.markdown("---")
                    st.markdown("### 📊 ตารางวิเคราะห์รายรอบ (Backtest Table)")
                    
                    styled_df = report_df.style.apply(highlight_hits, axis=1)
                    st.dataframe(styled_df, use_container_width=True, height=500)

                    csv_report = report_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="📥 ดาวน์โหลดรายงานผลการทดสอบ (.csv)",
                        data=csv_report,
                        file_name='backtest_report_highlighted.csv',
                        mime='text/csv',
                    )
            else:
                st.error("❌ ไม่พบคอลัมน์ 'top' หรือ 'bottom' ในไฟล์ CSV")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการรันระบบ: {e}")
