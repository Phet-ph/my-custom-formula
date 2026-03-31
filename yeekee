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
    if row['ผลลัพธ์บน'] == '✅ เข้า' or row['ผลลัพธ์ล่าง'] == '✅ เข้า':
        return ['background-color: #d4edda; color: #155724'] * len(row)
    return [''] * len(row)

# =========================================
# 4. ส่วนแสดงผล (Frontend UI)
# =========================================
st.set_page_config(page_title="ระบบวิเคราะห์ตัวเลขขั้นสูง", page_icon="🧮", layout="centered")

st.title("🧮 ระบบวิเคราะห์ตัวเลข (Custom Algorithm)")
st.markdown("---")

# สร้างหน้าต่าง 2 แท็บ
tab1, tab2 = st.tabs(["🔍 คำนวณรายรอบ (Manual)", "📊 ทดสอบความแม่นยำ (Backtest CSV)"])

# -----------------------------------------
# แท็บที่ 1: ระบบกรอกข้อมูลแบบแมนนวล
# -----------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    # ปรับวิธีเขียนให้อ่านง่ายและลดปัญหาการเว้นวรรคตกหล่น
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

# -----------------------------------------
# แท็บที่ 2: ระบบอัปโหลด CSV & ไฮไลท์ตาราง
# -----------------------------------------
with tab2:
    st.subheader("📁 อัปโหลดไฟล์ประวัติ (CSV)")
    st.markdown("ไฟล์ต้องมีคอลัมน์ชื่อ **top** (เลขบน 3 ตัว) และ **bottom** (เลขล่าง 2 ตัว)")
    
    uploaded_file = st.file_uploader("เลือกไฟล์ CSV ประวัติของคุณ", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'top' in df.columns and 'bottom' in df.columns:
                st.success(f"✅ โหลดข้อมูลสำเร็จ พบทั้งหมด {len(df)} รอบ")
                
                with st.spinner('กำลังคำนวณสถิติและสร้างตารางรายงาน...'):
                    report_df, hit_t, acc_t, hit_b, acc_b = run_detailed_backtest(df)

                st.markdown("### 🏆 สรุปภาพรวมความแม่นยำ")
                m1, m2 = st.columns(2)
                m1.metric("ความแม่นยำ (เข้าเลขบน)", f"{acc_t:.2f}%", f"เข้า {hit_t} รอบ")
                m2.metric("ความแม่นยำ (เข้าเลขล่าง)", f"{acc_b:.2f}%", f"เข้า {hit_b} รอบ")

                st.markdown("---")
                st.markdown("### 📊 ตารางวิเคราะห์รายรอบ (Backtest Table)")
                st.write("แถวที่มี **ไฮไลท์สีเขียว** คือรอบที่สมการคำนวณเข้าเป้าอย่างน้อย 1 ตำแหน่ง")

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
            st.error(f"❌ เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
