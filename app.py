import streamlit as st

# =========================================
# 1. สมองกล: ฟังก์ชันสมการของคุณ
# =========================================
def my_custom_formula_updated(top_str, bottom_str):
    t1 = int(top_str[0])  # หลักร้อยบน
    t2 = int(top_str[1])  # หลักสิบบน
    b1 = int(bottom_str[0])  # หลักสิบล่าง
    b2 = int(bottom_str[1])  # หลักหน่วยล่าง

    # ชุดที่ 1: หลักร้อยบน (t1) + หลักสิบล่าง (b1)
    start_num = (t1 + b1) % 10  
    set_1 = [start_num, (start_num + 3) % 10, (start_num + 6) % 10]

    # ชุดที่ 2
    set_2 = [(t2 + b1) % 10, (b1 + b2) % 10]

    return set_1, set_2

# =========================================
# 2. ส่วนแสดงผล (Frontend UI)
# =========================================
st.set_page_config(page_title="ระบบคำนวณสมการความน่าจะเป็น", page_icon="🧮", layout="centered")

st.title("🧮 ระบบคำนวณเลขเด่น (Custom Algorithm)")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    top_input = st.text_input("กรอกเลขบน (3 หลัก)", max_chars=3, placeholder="เช่น 825")

with col2:
    bottom_input = st.text_input("กรอกเลขล่าง (2 หลัก)", max_chars=2, placeholder="เช่น 35")

st.markdown("---")

if st.button("🚀 ประมวลผลสมการ", use_container_width=True):
    if len(top_input) == 3 and len(bottom_input) == 2 and top_input.isdigit() and bottom_input.isdigit():
        
        result_set1, result_set2 = my_custom_formula_updated(top_input, bottom_input)
        
        st.success("✅ คำนวณสมการสำเร็จ!")
        
        # -----------------------------------------
        # 🔍 ฟีเจอร์วิเคราะห์และแจ้งเตือนพิเศษ
        # -----------------------------------------
        # 1. วิเคราะห์หา "เลขชน" (Intersection)
        common_numbers = set(result_set1).intersection(set(result_set2))
        
        if len(common_
