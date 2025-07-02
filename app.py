import streamlit as st
from PIL import Image
import io
import zipfile
import os

st.title("🖼️ Bulk Image Resize & Compress Tool (JPEG ≤ 200KB)")

uploaded_files = st.file_uploader(
    "Upload multiple images", accept_multiple_files=True,
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"]
)

# Aspect Ratio
st.subheader("🔢 Aspect Ratio")
preset_ratios = {
    "1:1 (Square)": (1, 1),
    "4:3 (Classic Monitor)": (4, 3),
    "5:4 (Photo Print)": (5, 4),
    "16:9 (Widescreen)": (16, 9),
    "Custom": None
}
preset = st.selectbox("Choose aspect ratio", list(preset_ratios.keys()), index=2)  # Default to "5:4"
if preset != "Custom":
    aspect_w, aspect_h = preset_ratios[preset]
else:
    col1, col2 = st.columns(2)
    with col1:
        aspect_w = st.number_input("Aspect Ratio Width", value=5)
    with col2:
        aspect_h = st.number_input("Aspect Ratio Height", value=4)
target_ratio = aspect_w / aspect_h

# Crop toggle - disabled by default
apply_crop = st.checkbox("✂️ Crop to Aspect Ratio", value=False)

# Resize settings
st.subheader("📐 Resize Dimensions")
out_w = st.number_input("Final Width (px)", value=600)
out_h = st.number_input("Final Height (px)", value=480)
final_size = (int(out_w), int(out_h))

# File size constraint
max_file_size_kb = 200

# Process images
if st.button("📸 Process Images") and uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for file in uploaded_files:
            try:
                img = Image.open(file).convert("RGB")
                w, h = img.size

                # Optional cropping
                if apply_crop:
                    current_ratio = w / h
                    if current_ratio > target_ratio:
                        new_w = int(h * target_ratio)
                        left = (w - new_w) // 2
                        box = (left, 0, left + new_w, h)
                    else:
                        new_h = int(w / target_ratio)
                        top = (h - new_h) // 2
                        box = (0, top, w, top + new_h)
                    img = img.crop(box)

                # Resize image
                resized = img.resize(final_size, Image.Resampling.LANCZOS)

                # Compress to JPEG ≤ 200KB
                for quality in range(85, 10, -5):
                    buffer = io.BytesIO()
                    resized.save(buffer, format="JPEG", quality=quality)
                    size_kb = buffer.tell() / 1024
                    if size_kb <= max_file_size_kb:
                        buffer.seek(0)
                        base_name = os.path.splitext(file.name)[0]
                        zip_file.writestr(f"{base_name}.jpg", buffer.read())
                        st.success(f"✔️ {file.name} → {size_kb:.1f} KB (q={quality})")
                        break
                else:
                    st.warning(f"⚠️ {file.name} couldn't be compressed under 200KB.")

            except Exception as e:
                st.error(f"❌ Error with {file.name}: {e}")

    st.download_button("📦 Download ZIP", zip_buffer.getvalue(), "compressed_images.zip", "application/zip")
