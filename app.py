import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Urine Strip Analyzer", layout="centered")

st.title("🧪 ระบบวิเคราะห์แถบตรวจปัสสาวะ")
st.write("Glucose / Protein (Cybow 2GP)")

uploaded = st.file_uploader("อัปโหลดภาพแถบตรวจ", type=["jpg", "png", "jpeg"])
test_type = st.selectbox("เลือกชนิดการตรวจ", ["Glucose", "Protein"])

glucose_ref = {
    "Negative": (255,255,255),
    "+": (255,255,180),
    "++": (255,255,120),
    "+++": (255,255,60)
}

protein_ref = {
    "Negative": (255,255,255),
    "+": (180,255,180),
    "++": (120,255,120),
    "+++": (60,255,60)
}

def avg_color(img):
    arr = np.array(img)
    return np.mean(arr.reshape(-1,3), axis=0)

def match(c, ref):
    return min(ref, key=lambda k: np.linalg.norm(c - ref[k]))

risk_map = {"Negative":5, "+":25, "++":55, "+++":80}

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="ภาพที่อัปโหลด", use_container_width=True)

    color = avg_color(img)
    level = match(color, glucose_ref if test_type=="Glucose" else protein_ref)
    risk = risk_map[level]

    st.subheader(f"ผลตรวจ: {level}")
    st.progress(risk/100)
    st.write(f"ความเสี่ยง: **{risk}%**")

    if risk <= 30:
        st.success("ความเสี่ยงต่ำ")
    elif risk <= 60:
        st.warning("ความเสี่ยงปานกลาง")
    else:
        st.error("ความเสี่ยงสูง ควรพบแพทย์")
