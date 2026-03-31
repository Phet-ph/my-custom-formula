import streamlit as st
import itertools
import pandas as pd # นำเข้า pandas สำหรับจัดการไฟล์ CSV

# =========================================
# 1. สมองกล: ฟังก์ชันสมการของคุณ
# =========================================
def my_custom_formula_updated(top_str, bottom_str):
    t1 = int(str(top_str).zfill(3)[0])  # เติม 0 ด้านหน้าถ้าไม่ครบ 3 หลัก
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
# 2. ฟังก์ชันทดสอบความแม่นยำ (Backtesting)
# =========================================
def evaluate_accuracy(df):
    total_rounds = len(df) - 1
    hits_top = 0
    hits_bottom = 0
    
    # วนลูปตรวจทีละรอบเทียบกับผลของรอบถัดไป
    for i in range(total_rounds):
        curr_top = str(df.iloc[i]['top']).zfill(3)
        curr_bot = str(df.iloc[i]['bottom']).zfill(2)
        
        next_top = str(df.iloc[i+1]['top']).zfill(3)
        next_bot = str(df.iloc[i+1]['bottom']).zfill(2)
        
        # นำข้อมูลรอบปัจจุบันเข้าสมการ
        set1, set2 = my_custom_formula_updated(curr_top, curr_bot)
        
        # รวมเลขเด่นที่ได้ทั้งหมด
        predicted_digits = set(set1).union(set(set2))
        
        # ตรวจสอบว่ามีเลขเด่นโผล่ไปในรอบถัดไปหรือไม่
        if any(str(d) in next_top for d in predicted_digits):
            hits_top += 1
            
        if any(str(d) in next_bot for d in predicted_digits):
            hits_bottom += 1
            
    # คำนวณเป็นเปอร์เซ็นต์
    top_acc = (hits_top / total_rounds) * 100 if total_rounds > 0 else 0
    bot_acc = (hits_bottom / total_rounds) * 100 if total_rounds > 0 else 0
    
    return total_rounds, hits_top, top_acc, hits_bottom, bot_acc

# =========================================
# 3. ส่วนแสดงผล (Frontend UI)
# =========================================
st.set_page_config(page_title="ระบบวิเคราะห์ตัวเลขขั้นสูง", page_icon="🧮", layout="centered")

st.title("🧮 ระบบวิเคราะห์ตัวเลข (Custom Algorithm)")
st.markdown("---")

# สร้างหน้าต่าง 2 แท็บ
tab1, tab2 = st.tabs(["🔍 คำนวณรายรอบ (Manual)", "📊 ทดสอบความแม่นยำ (Backtest CSV)"])

# -----------------------------------------
# แท็บที่ 1: ระบบกรอกข้อมูลแบบแมนนวล (ระบบเดิม)
# -----------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        top_input = st.text_input("กรอกเลขบน (3 หลัก)", max_chars=3, placeholder="เช่น 825", key="t1")
    with col2:
        bottom_input = st.text_input("กรอกเลขล่าง (2 หลัก)", max_chars=2, placeholder="เช่น 35", key="b1")

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
                st.info(f"🔮 **สัญญาณพิเศษ:** พบเลข **6** หรือ **9** (โอกาสออกเลขตอง / 69 / 96)")

            if len(common_numbers) > 0:
                intersect_str = ', '.join(map(str, common_numbers))
                st.error(f"🚨 **พบเลขชน:** **[ {intersect_str} ]** (อาจออกเลขเบิ้ล/ตอง)")
                
                two_digits = []
                for num1 in result_set1:
                    for num2 in result_set2:
                        two_digits.extend([f"{num1}{num2}", f"{num2}{num1}"])
                two_digits = sorted(list(set(two_digits)))
                
                st.write("🎲 **จับคู่เลขหลักสิบ (2 ตัว):**")
                st.code(" | ".join(two_digits))
        else:
            st.error("⚠️ ข้อมูลไม่ถูกต้อง: กรุณากรอกตัวเลขให้ครบถ้วน")

# -----------------------------------------
# แท็บที่ 2: ระบบอัปโหลด CSV (ระบบใหม่)
# -----------------------------------------
with tab2:
    st.subheader("📁 อัปโหลดไฟล์ประวัติ (CSV)")
    st.markdown("ไฟล์ต้องมีคอลัมน์ชื่อ **top** (เลขบน 3 ตัว) และ **bottom** (เลขล่าง 2 ตัว)")
    
    uploaded_file = st.file_uploader("เลือกไฟล์ CSV 88 รอบของคุณ", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # อ่านไฟล์ CSV
            df = pd.read_csv(uploaded_file)
            
            # เช็คว่าคอลัมน์ถูกต้องไหม
            if 'top' in df.columns and 'bottom' in df.columns:
                st.success(f"✅ โหลดข้อมูลสำเร็จ พบทั้งหมด {len(df)} รอบการออกรางวัล")
                
                with st.spinner('กำลังประมวลผลอัลกอริทึมย้อนหลัง...'):
                    # รันฟังก์ชัน Backtest
                    rounds, hit_t, acc_t, hit_b, acc_b = evaluate_accuracy(df)
                
                st.markdown("### 🏆 ผลการทดสอบความแม่นยำของสมการ (Backtest Results)")
                st.markdown(f"ทดสอบจากข้อมูลทั้งหมด: **{rounds}** รอบ (ไม่รวมรอบล่าสุดที่ยังไม่ออกผล)")
                
                # นำเสนอเป็น Dashboard สวยงาม
                m_col1, m_col2 = st.columns(2)
                
                with m_col1:
                    st.metric(label="🎯 ความแม่นยำ (เข้าเลขบน)", value=f"{acc_t:.2f}%", delta=f"เข้า {hit_t} จาก {rounds} รอบ")
                    
                with m_col2:
                    st.metric(label="🎯 ความแม่นยำ (เข้าเลขล่าง)", value=f"{acc_b:.2f}%", delta=f"เข้า {hit_b} จาก {rounds} รอบ", delta_color="normal")

                st.info("💡 **เกณฑ์การวิเคราะห์:** ระบบจะคำนวณเลขเด่นจากรอบปัจจุบัน แล้วตรวจสอบว่า 'เลขเด่นเหล่านั้น ไปปรากฏอยู่ในผลรางวัลของรอบถัดไป' หรือไม่")
                
                # แสดงตัวอย่างข้อมูล
                with st.expander("ดูตัวอย่างข้อมูลที่อัปโหลด (5 แถวแรก)"):
                    st.dataframe(df.head())
                    
            else:
                st.error("❌ ไม่พบคอลัมน์ 'top' หรือ 'bottom' ในไฟล์ CSV กรุณาตรวจสอบหัวคอลัมน์ในไฟล์ของคุณ")
                
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
