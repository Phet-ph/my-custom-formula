import streamlit as st

# =========================================
# 1. สมองกล: ฟังก์ชันสมการของคุณ
# =========================================
def my_custom_formula_updated(top_str, bottom_str):
    """
    ฟังก์ชันคำนวณตามสูตรเฉพาะ (รับค่าเป็นข้อความเพื่อรักษาเลข 0 นำหน้า)
    """
    # ดึงตัวเลขแต่ละตำแหน่ง
    t1 = int(top_str[0])  # หลักร้อยบน
    t2 = int(top_str[1])  # หลักสิบบน
    
    b1 = int(bottom_str[0])  # หลักสิบล่าง
    b2 = int(bottom_str[1])  # หลักหน่วยล่าง

    # ขั้นตอนที่ 1: หาเลขชุดแรก
    start_num = (t1 + b2) % 10  
    set_1 = [start_num, (start_num + 3) % 10, (start_num + 6) % 10]

    # ขั้นตอนที่ 2: หาเลขชุดที่สอง
    set_2 = [(t2 + b1) % 10, (b1 + b2) % 10]

    return set_1, set_2

# =========================================
# 2. ส่วนแสดงผล (Frontend UI)
# =========================================
# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ระบบคำนวณสมการความน่าจะเป็น", page_icon="🧮", layout="centered")

st.title("🧮 ระบบคำนวณเลขเด่น (Custom Algorithm)")
st.markdown("---")

# จัดหน้าจอเป็น 2 คอลัมน์สำหรับรับข้อมูล
col1, col2 = st.columns(2)

with col1:
    top_input = st.text_input("กรอกเลขบน (3 หลัก)", max_chars=3, placeholder="เช่น 825")

with col2:
    bottom_input = st.text_input("กรอกเลขล่าง (2 หลัก)", max_chars=2, placeholder="เช่น 35")

st.markdown("---")

# ปุ่มกดสำหรับรันสมการ
if st.button("🚀 ประมวลผลสมการ", use_container_width=True):
    # ตรวจสอบความถูกต้องของข้อมูล (ต้องเป็นตัวเลขและครบหลัก)
    if len(top_input) == 3 and len(bottom_input) == 2 and top_input.isdigit() and bottom_input.isdigit():
        
        # ส่งข้อมูลเข้าสมการ
        result_set1, result_set2 = my_custom_formula_updated(top_input, bottom_input)
        
        st.success("✅ คำนวณสมการสำเร็จ!")
        
        # แสดงผลลัพธ์แบบกล่องสวยงาม
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.info("🎯 **เลขเด่นชุดที่ 1**")
            # แปลง List เป็นข้อความเพื่อให้ดูง่าย
            st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>{', '.join(map(str, result_set1))}</h2>", unsafe_allow_html=True)
            
        with res_col2:
            st.warning("🎯 **เลขเด่นชุดที่ 2**")
            st.markdown(f"<h2 style='text-align: center; color: #ff7f0e;'>{', '.join(map(str, result_set2))}</h2>", unsafe_allow_html=True)
            
    else:
        st.error("⚠️ ข้อมูลไม่ถูกต้อง: กรุณากรอกเลขบนให้ครบ 3 หลัก และเลขล่าง 2 หลัก (เฉพาะตัวเลขเท่านั้น)")
