import streamlit as st
import pandas as pd
import re

# =========================================
# 1. สมองกล: สูตรที่ 8 (The Oracle Matrix)
# =========================================
def my_custom_formula_updated(top_T, bot_T, top_P, bot_P):
    # ดึงค่าหลักตัวเลข
    t1_T = int(str(top_T).zfill(3)[0])
    t3_T = int(str(top_T).zfill(3)[2])
    b2_T = int(str(bot_T).zfill(2)[1])
    t3_P = int(str(top_P).zfill(3)[2])

    # 🎯 ชุดที่ 1: ดักสถิติ 5 ตัว (ฐาน + พี่น้อง + เงา + เลขสถิติ)
    base = (t1_T + b2_T) % 10
    set_1 = [base, (base + 1) % 10, (base + 2) % 10, (base + 5) % 10, (base + 8) % 10]

    # 🎯 ชุดที่ 2: เลขหน่วงกันพลาด 3 ตัว
    lag = (t3_T + t3_P) % 10
    set_2 = [lag, (lag + 1) % 10, (lag + 9) % 10]
    
    # รวมกลุ่มเลขและตัดตัวซ้ำออก
    combined_pool = sorted(list(set(set_1 + set_2)))
    return combined_pool

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
# 3. ส่วนแสดงผล UI (Streamlit)
# =========================================
st.set_page_config(page_title="Statistical Fusion V9", page_icon="📈")
st.title("📈 The Statistical Fusion (เป้าหมาย 95%) + Win Generator")

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
    if all([top_T, bot_T, top_P, bot_P]):
        # 1. คำนวณเลขเด่น
        pool =  my_custom_formula_updated(top_T, bot_T, top_P, bot_P)
        st.success(f"🎯 กลุ่มเลขเด่นที่คำนวณได้ ({len(pool)} ตัว): **{', '.join(map(str, pool))}**")
        
        # 2. สร้างเลขวิน
        win_2, win_3, doubles, count_2, count_3 = generate_win_numbers(pool)
        
        st.markdown("---")
        st.markdown("### 📋 ชุดเลขนำไปใช้งานจริง (Copy ไปแทงได้เลย)")
        
        st.info(f"**🟢 วิน 2 ตัว (นำไปกด 2 ตัวบน / 2 ตัวล่าง + กดกลับเลขด้วย):**\n\nมีทั้งหมด {count_2} ชุด\n\n`{win_2}`")
        
        st.warning(f"**🟡 วิน 3 ตัว (นำไปกด 3 ตัวบนโต๊ด หรือ 6 กลับ):**\n\nมีทั้งหมด {count_3} ชุด\n\n`{win_3}`")
        
        st.error(f"**🔴 เลขเบิ้ลกันพลาด (สำหรับคนชอบดักเบิ้ล):**\n\n`{doubles}`")
        
    else:
        st.error("กรุณากรอกข้อมูลให้ครบทั้ง 4 ช่องเพื่อความแม่นยำสูงสุด")
