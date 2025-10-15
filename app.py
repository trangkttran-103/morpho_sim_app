import streamlit as st
import os

# --- CẤU HÌNH ---
VIDEO_FOLDER = "videos"

# --- 1. GIỚI HẠN SINH HỌC ---
MAX_HEIGHT = 30.0  # cm, phát triển tối đa
MIN_HEIGHT = 5.0   # cm, phát triển thấp nhất

# --- 2. HÀM DỰ ĐOÁN KIỂU HÌNH ---
def predict_growth(water, fertilizer, light):
    """
    Mô phỏng biểu hiện thường biến của cây trồng.
    Ba yếu tố: Nước, Phân, Ánh sáng.
    Mỗi yếu tố có mức ảnh hưởng phi tuyến (logistic) đến tăng trưởng.
    """

    # Chuẩn hóa giá trị (đưa về thang 0–1)
    water_score = min(water / 500, 1.0)
    fertilizer_score = min(fertilizer / 5.0, 1.0)
    light_score = min(light / 10.0, 1.0)

    # Tính điểm tăng trưởng tổng hợp (giá trị phi tuyến, có tương tác)
    growth_index = (0.4 * water_score**1.2 +
                    0.3 * fertilizer_score**1.1 +
                    0.3 * light_score**1.3)

    # Quy đổi sang chiều cao (cm)
    height = MIN_HEIGHT + growth_index * (MAX_HEIGHT - MIN_HEIGHT)
    height = round(height, 2)

    # --- 3. PHÂN LOẠI KIỂU HÌNH ---
    if water_score < 0.5 and water_score < fertilizer_score and water_score < light_score:
        label = "WaterDeficient"
        desc = "Cây héo, còi cọc do thiếu nước. Lá rũ và tốc độ sinh trưởng chậm."
    elif fertilizer_score < 0.5 and fertilizer_score < water_score and fertilizer_score < light_score:
        label = "NutrientDeficient"
        desc = "Cây kém phát triển, lá nhạt màu do thiếu dinh dưỡng."
    elif light_score < 0.5 and light_score < water_score and light_score < fertilizer_score:
        label = "LightDeficient"
        desc = "Cây mảnh, ít lá, do ánh sáng yếu. Hiện tượng vươn dài để tìm sáng."
    else:
        label = "Optimal"
        desc = "Cây phát triển tối ưu với điều kiện môi trường cân bằng."

    return height, label, desc

# --- 4. GIAO DIỆN STREAMLIT ---
st.set_page_config(page_title="🌱 Mô phỏng thường biến sinh học", layout="wide")
st.title("🌿 Mô phỏng Biểu hiện Thường biến của Cây trồng")
st.caption("Cùng kiểu gen, nhưng biểu hiện kiểu hình thay đổi theo môi trường.")

col1, col2 = st.columns([1, 1.3])

with col1:
    st.header("⚙️ Điều chỉnh yếu tố môi trường")

    water = st.slider("💧 Nước (ml/ngày)", 100, 500, 300, step=10)
    fertilizer = st.slider("🌾 Phân bón (g/ngày)", 0.0, 5.0, 2.5, step=0.1)
    light = st.slider("🌤 Ánh sáng (giờ/ngày)", 4, 10, 7, step=1)

    if st.button("🔍 Mô phỏng phát triển", type="primary"):
        height, label, desc = predict_growth(water, fertilizer, light)
        st.session_state.update({"height": height, "label": label, "desc": desc})

        st.metric("🌿 Chiều cao dự đoán", f"{height} cm")
        st.success(f"**Trạng thái sinh trưởng:** {label}")

with col2:
    st.header("🎞️ Kết quả mô phỏng")

    if "label" in st.session_state:
        video_path = os.path.join(VIDEO_FOLDER, f"{st.session_state['label']}.mp4")

        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"⚠️ Chưa tìm thấy video cho {st.session_state['label']} trong thư mục {VIDEO_FOLDER}/")

        st.markdown(f"**Phân tích:** {st.session_state['desc']}")
        st.markdown(f"**Giới hạn sinh học:** {MIN_HEIGHT} – {MAX_HEIGHT} cm")
    else:
        st.info("Chọn điều kiện và nhấn 'Mô phỏng phát triển' để bắt đầu.")
