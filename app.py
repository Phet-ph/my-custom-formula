import streamlit as st
import pandas as pd

# --- ฟังก์ชันหลักสำหรับไฮไลท์สีในตาราง ---
def highlight_hits(row):
    """
    ฟังก์ชันกำหนดสี: ถ้าทายถูก (Hit) ให้เป็นสีเขียวอ่อน
    """
    style = [''] * len(row)
    if row['ผลลัพธ์บน'] == '✅ เข้า' or row['ผลลัพธ์ล่าง'] == '✅ เข้า':
        return ['background-color: #d4edda; color: #155724'] * len(row) # สีเขียวอ่อน
    return style

# =========================================
# 2. ฟังก์ชันทดสอบความแม่นยำ (เวอร์ชันเก็บรายละเอียดรายรอบ)
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

        # คำนวณจากสมการ
        set1, set2 = my_custom_formula_updated(curr_top, curr_bot)
        predicted_digits = set(set1).union(set(set2))
        pred_str = ", ".join(map(str, sorted(list(predicted_digits))))

        # ตรวจสอบผล
        is_hit_top = any(str(d) in next_top for d in predicted_digits)
        is_hit_bot = any(str(d) in next_bot for d in predicted_digits)

        if is_hit_top: hits_top += 1
        if is_hit_bot: hits_bottom += 1

        # เก็บข้อมูลลงตารางรายงาน
        results_list.append({
            "รอบที่": i + 1,
            "เลขฐาน (บน/ล่าง)": f"{curr_top} / {curr_bot}",
            "เลขเด่นที่คำนวณได้": pred_str,
            "ผลออก (รอบถัดไป)": f"{next_top} / {next_bot}",
            "ผลลัพธ์บน": "✅ เข้า" if is_hit_top else "❌ หลุด",
            "ผลลัพธ์ล่าง": "✅ เข้า" if is_hit_bot else "❌ หลุด"
        })

    report_df = pd.DataFrame(results_list)
    top_acc = (hits_top / total_rounds) * 100
    bot_acc = (hits_bottom / total_rounds) * 100

    return report_df, hits_top, top_acc, hits_bottom, bot_acc

# =========================================
# ในส่วนของ Tab 2 (Backtest CSV)
# =========================================
# (ส่วนการโหลดไฟล์เหมือนเดิม แต่ปรับการแสดงผลด้านล่าง)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'top' in df.columns and 'bottom' in df.columns:
        with st.spinner('กำลังประมวลผลตารางรายงาน...'):
            report_df, hit_t, acc_t, hit_b, acc_b = run_detailed_backtest(df)

        # แสดง Metrics สรุปผล
        st.markdown("### 🏆 สรุปภาพรวมความแม่นยำ")
        m1, m2 = st.columns(2)
        m1.metric("ความแม่นยำบน", f"{acc_t:.2f}%", f"เข้า {hit_t} รอบ")
        m2.metric("ความแม่นยำล่าง", f"{acc_b:.2f}%", f"เข้า {hit_b} รอบ")

        st.markdown("---")
        st.markdown("### 📊 ตารางวิเคราะห์รายรอบ (Backtest Table)")
        st.write("แถวที่มี **ไฮไลท์สีเขียว** คือรอบที่สมการคำนวณเข้าเป้าอย่างน้อย 1 ตำแหน่ง")

        # นำตารางมาใส่การไฮไลท์สี และแสดงผล
        styled_df = report_df.style.apply(highlight_hits, axis=1)
        
        # ใช้ st.dataframe เพื่อให้เลื่อนดูข้อมูลได้สะดวก
        st.dataframe(styled_df, use_container_width=True, height=500)

        # เพิ่มปุ่มดาวน์โหลดรายงาน
        csv_report = report_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลดรายงานผลการทดสอบ (.csv)",
            data=csv_report,
            file_name='backtest_report.csv',
            mime='text/csv',
        )
