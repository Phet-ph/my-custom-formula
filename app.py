import streamlit as st
import itertools # นำเข้าเครื่องมือสำหรับจับคู่ตัวเลข

# =========================================
# 1. สมองกล: ฟังก์ชันสมการของคุณ
# =========================================
def my_custom_formula_updated(top_str, bottom_str):
    t1 = int(top_str[0])  # หลักร้อยบน
    t2 = int(top_str[1])  # หลักสิบบน
    b1 = int(bottom_str[0])  # หลักสิบล่าง
    b2 = int(bottom_str[1])  # หลักหน่วยล่าง

    # ชุดที่ 1
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
        
        # แสดงผลลัพธ์ปกติแบบกล่อง
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.info("🎯 **เลขเด่นชุดที่ 1**")
            st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>{', '.join(map(str, result_set1))}</h2>", unsafe_allow_html=True)
        with res_col2:
            st.warning("🎯 **เลขเด่นชุดที่ 2**")
            st.markdown(f"<h2 style='text-align: center; color: #ff7f0e;'>{', '.join(map(str, result_set2))}</h2>", unsafe_allow_html=True)
            
        st.markdown("---")

        # -----------------------------------------
        # 🔍 วิเคราะห์และแจ้งเตือนพิเศษ
        # -----------------------------------------
        common_numbers = set(result_set1).intersection(set(result_set2))
        all_numbers = set(result_set1).union(set(result_set2))
        
        # สัญญาณพิเศษ 2: ตรวจหาเลข 6 หรือ 9
        if 6 in all_numbers or 9 in all_numbers:
            st.info(f"🔮 **สัญญาณพิเศษ:** พบเลข **6** หรือ **9** \n\n**คำแนะนำ:** มีโอกาสที่จะเกิด **เลขตอง** หรืออาจมีเลขจับคู่ **69** หรือ **96** ออกมาให้เห็น!")

        # สัญญาณพิเศษ 1 + สมการที่ 3: ตรวจหาเลขชนและจับคู่
        if len(common_numbers) > 0:
            intersect_str = ', '.join(map(str, common_numbers))
            st.error(f"🚨 **พบเลขชน:** คือ **[ {intersect_str} ]** (อาจออกเลขเบิ้ล/ตอง)")
            
            st.success("✨ **สมการที่ 3: ระบบทำการจับคู่เลขหลักสิบและหลักร้อยโดยอัตโนมัติ**")
            
            # --- กระบวนการจับคู่เลข ---
            # 1. จับคู่หลักสิบ (2 ตัว) แบบไขว้ชุด 1 และ ชุด 2 (ไป-กลับ)
            two_digits = []
            for num1 in result_set1:
                for num2 in result_set2:
                    two_digits.append(f"{num1}{num2}")
                    two_digits.append(f"{num2}{num1}")
            two_digits = sorted(list(set(two_digits))) # ลบตัวซ้ำและเรียงลำดับ
            
            # 2. จับคู่หลักร้อย (3 ตัว) โดยดึงจากเลขเด่นทั้งหมดมารวมกัน
            three_digits = []
            unique_all = list(all_numbers)
            if len(unique_all) >= 3:
                # สร้างกลุ่มตัวเลข 3 ตัว แบบไม่ซ้ำกัน
                for combo in itertools.combinations(unique_all, 3):
                    three_digits.append(f"{combo[0]}{combo[1]}{combo[2]}")
            
            # แสดงผลการจับคู่
            st.write("🎲 **ตัวเลขจับคู่หลักสิบ (2 ตัว):**")
            st.code(" | ".join(two_digits))
            
            if three_digits:
                st.write("🎲 **ตัวเลขจับคู่หลักร้อย (3 ตัว โต๊ด):**")
                st.code(" | ".join(three_digits))

    else:
        st.error("⚠️ ข้อมูลไม่ถูกต้อง: กรุณากรอกเลขบนให้ครบ 3 หลัก และเลขล่าง 2 หลัก (เฉพาะตัวเลขเท่านั้น)")
