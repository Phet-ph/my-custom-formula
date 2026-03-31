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
        
        if len(common_numbers) > 0:
            intersect_str = ', '.join(map(str, common_numbers))
            st.error(f"🚨 **สัญญาณพิเศษ 1:** พบเลขชนกันคือ **[ {intersect_str} ]** \n\n**คำแนะนำ:** รอบนี้อาจจะออก **เลขเบิ้ล** หรือ **เลขตอง**!")

        # 2. วิเคราะห์หาเลข "6" หรือ "9"
        # รวมเลขทั้งหมดจากทั้ง 2 ชุดเพื่อตรวจสอบ
        all_numbers = set(result_set1).union(set(result_set2))
        
        if 6 in all_numbers or 9 in all_numbers:
            # ใช้สีม่วง (info/warning) เพื่อแยกความแตกต่างจากการเตือนเลขชน
            st.info(f"🔮 **สัญญาณพิเศษ 2:** พบเลข **6** หรือ **9** ในกลุ่มเลขเด่น \n\n**คำแนะนำ:** มีโอกาสที่จะเกิด **เลขตอง** หรืออาจมีเลขจับคู่ **69** หรือ **96** ออกมาให้เห็น!")

        # -----------------------------------------
        # แสดงผลลัพธ์ตัวเลขปกติแบบกล่องสวยงาม
        # -----------------------------------------
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.info("🎯 **เลขเด่นชุดที่ 1**")
            st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>{', '.join(map(str, result_set1))}</h2>", unsafe_allow_html=True)
            
        with res_col2:
            st.warning("🎯 **เลขเด่นชุดที่ 2**")
            st.markdown(f"<h2 style='text-align: center; color: #ff7f0e;'>{', '.join(map(str, result_set2))}</h2>", unsafe_allow_html=True)
            
    else:
        st.error("⚠️ ข้อมูลไม่ถูกต้อง: กรุณากรอกเลขบนให้ครบ 3 หลัก และเลขล่าง 2 หลัก (เฉพาะตัวเลขเท่านั้น)")
