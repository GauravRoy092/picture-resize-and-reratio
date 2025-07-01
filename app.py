
import streamlit as st
from PIL import Image
import os
import io
import zipfile

st.title("🖼️ Bulk Image Crop & Resize Tool")

uploaded_files = st.file_uploader("Upload multiple images", accept_multiple_files=True, type=["jpg", "jpeg", "png", "webp"])

col1, col2 = st.columns(2)
with col1:
    aspect_w = st.number_input("Aspect Ratio Width", value=5)
with col2:
    aspect_h = st.number_input("Aspect Ratio Height", value=4)
target_ratio = aspect_w / aspect_h

out_w = st.number_input("Final Width", value=600)
out_h = st.number_input("Final Height", value=480)
final_size = (int(out_w), int(out_h))

if st.button("📸 Process Images") and uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            try:
                img = Image.open(uploaded_file).convert("RGB")
                w, h = img.size
                current_ratio = w / h

                if current_ratio > target_ratio:
                    new_w = int(h * target_ratio)
                    left = (w - new_w) // 2
                    box = (left, 0, left + new_w, h)
                else:
                    new_h = int(w / target_ratio)
                    top = (h - new_h) // 2
                    box = (0, top, w, top + new_h)

                cropped = img.crop(box)
                resized = cropped.resize(final_size, Image.Resampling.LANCZOS)

                img_bytes = io.BytesIO()
                resized.save(img_bytes, format="JPEG")
                img_bytes.seek(0)
                zip_file.writestr(uploaded_file.name, img_bytes.read())

            except Exception as e:
                st.error(f"⚠️ Error with {uploaded_file.name}: {e}")

    st.success("✅ Done! Download your processed images:")
    st.download_button("📦 Download ZIP", zip_buffer.getvalue(), "resized_images.zip", "application/zip")
