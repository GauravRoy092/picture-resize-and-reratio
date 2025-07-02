
# # import streamlit as st
# # from PIL import Image
# # import os
# # import io
# # import zipfile

# # st.title("🖼️ Bulk Image Crop & Resize Tool")

# # uploaded_files = st.file_uploader("Upload multiple images", accept_multiple_files=True, type=["jpg", "jpeg", "png", "webp"])

# # col1, col2 = st.columns(2)
# # with col1:
# #     aspect_w = st.number_input("Aspect Ratio Width", value=5)
# # with col2:
# #     aspect_h = st.number_input("Aspect Ratio Height", value=4)
# # target_ratio = aspect_w / aspect_h

# # out_w = st.number_input("Final Width", value=600)
# # out_h = st.number_input("Final Height", value=480)
# # final_size = (int(out_w), int(out_h))

# # if st.button("📸 Process Images") and uploaded_files:
# #     zip_buffer = io.BytesIO()
# #     with zipfile.ZipFile(zip_buffer, "w") as zip_file:
# #         for uploaded_file in uploaded_files:
# #             try:
# #                 img = Image.open(uploaded_file).convert("RGB")
# #                 w, h = img.size
# #                 current_ratio = w / h

# #                 if current_ratio > target_ratio:
# #                     new_w = int(h * target_ratio)
# #                     left = (w - new_w) // 2
# #                     box = (left, 0, left + new_w, h)
# #                 else:
# #                     new_h = int(w / target_ratio)
# #                     top = (h - new_h) // 2
# #                     box = (0, top, w, top + new_h)

# #                 cropped = img.crop(box)
# #                 resized = cropped.resize(final_size, Image.Resampling.LANCZOS)

# #                 img_bytes = io.BytesIO()
# #                 resized.save(img_bytes, format="JPEG")
# #                 img_bytes.seek(0)
# #                 zip_file.writestr(uploaded_file.name, img_bytes.read())

# #             except Exception as e:
# #                 st.error(f"⚠️ Error with {uploaded_file.name}: {e}")

# #     st.success("✅ Done! Download your processed images:")
# #     st.download_button("📦 Download ZIP", zip_buffer.getvalue(), "resized_images.zip", "application/zip")
# import streamlit as st
# from PIL import Image
# import io
# import zipfile

# st.title("🖼️ Bulk Image Crop & Resize Tool")

# # Upload images
# uploaded_files = st.file_uploader("Upload multiple images", accept_multiple_files=True, type=["jpg", "jpeg", "png", "webp"])

# # Aspect ratio preset selector
# st.subheader("🔢 Choose Aspect Ratio")
# preset_ratios = {
#     "1:1 (Square)": (1, 1),
#     "4:3 (Classic Monitor)": (4, 3),
#     "5:4 (Photo Print)": (5, 4),
#     "16:9 (Widescreen)": (16, 9),
#     "Custom": None
# }
# preset = st.selectbox("Choose a preset or define custom", list(preset_ratios.keys()))

# # Handle aspect ratio input
# if preset != "Custom":
#     aspect_w, aspect_h = preset_ratios[preset]
# else:
#     col1, col2 = st.columns(2)
#     with col1:
#         aspect_w = st.number_input("Aspect Ratio Width", value=5)
#     with col2:
#         aspect_h = st.number_input("Aspect Ratio Height", value=4)
# target_ratio = aspect_w / aspect_h

# # Crop toggle
# apply_crop = st.checkbox("✂️ Crop to Aspect Ratio", value=True)

# # Resize dimensions
# st.subheader("📐 Output Resize Dimensions")
# out_w = st.number_input("Final Width (px)", value=600)
# out_h = st.number_input("Final Height (px)", value=480)
# final_size = (int(out_w), int(out_h))

# # Process images
# if st.button("📸 Process Images") and uploaded_files:
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w") as zip_file:
#         for uploaded_file in uploaded_files:
#             try:
#                 img = Image.open(uploaded_file).convert("RGB")
#                 w, h = img.size

#                 if apply_crop:
#                     current_ratio = w / h
#                     if current_ratio > target_ratio:
#                         new_w = int(h * target_ratio)
#                         left = (w - new_w) // 2
#                         box = (left, 0, left + new_w, h)
#                     else:
#                         new_h = int(w / target_ratio)
#                         top = (h - new_h) // 2
#                         box = (0, top, w, top + new_h)
#                     img = img.crop(box)

#                 # Resize
#                 resized = img.resize(final_size, Image.Resampling.LANCZOS)

#                 # Save to in-memory zip
#                 img_bytes = io.BytesIO()
#                 resized.save(img_bytes, format="JPEG")
#                 img_bytes.seek(0)
#                 zip_file.writestr(uploaded_file.name, img_bytes.read())

#             except Exception as e:
#                 st.error(f"⚠️ Error with {uploaded_file.name}: {e}")

#     st.success("✅ Done! Download your processed images:")
#     st.download_button("📦 Download ZIP", zip_buffer.getvalue(), "resized_images.zip", "application/zip")
import streamlit as st
from PIL import Image
import io
import zipfile
import os

# ---------------------------
# Header and UI Description
# ---------------------------
st.markdown("""
    <style>
        .title-text {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #ffffff;
        }
        .desc-text {
            font-size: 18px;
            line-height: 1.6;
            color: #dddddd;
            text-align: center;
            padding-bottom: 20px;
        }
    </style>
    <div class="title-text">🎨 Bulk Image Resizer & Compressor (JPEG ≤ 200KB)</div>
    <div class="desc-text">
        Resize, optionally crop, and compress your images to under <b>200KB</b> each.<br>
        Upload up to <b>20 images at a time</b> and download all processed images in a single ZIP.
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# File uploader (limit to 20)
# ---------------------------
uploaded_files = st.file_uploader(
    "Upload up to 20 images", accept_multiple_files=True,
    type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"]
)

if uploaded_files and len(uploaded_files) > 20:
    st.warning("⚠️ You can upload up to 20 images only.")
    uploaded_files = uploaded_files[:20]

# ---------------------------
# Aspect Ratio Section
# ---------------------------
st.subheader("🔢 Aspect Ratio")
preset_ratios = {
    "1:1 (Square)": (1, 1),
    "4:3 (Classic Monitor)": (4, 3),
    "5:4 (Photo Print)": (5, 4),
    "16:9 (Widescreen)": (16, 9),
    "Custom": None
}
preset = st.selectbox("Choose aspect ratio", list(preset_ratios.keys()), index=2)  # Default to 5:4
if preset != "Custom":
    aspect_w, aspect_h = preset_ratios[preset]
else:
    col1, col2 = st.columns(2)
    with col1:
        aspect_w = st.number_input("Aspect Ratio Width", value=5)
    with col2:
        aspect_h = st.number_input("Aspect Ratio Height", value=4)
target_ratio = aspect_w / aspect_h

# ---------------------------
# Crop and Resize Section
# ---------------------------
apply_crop = st.checkbox("✂️ Crop to Aspect Ratio", value=False)

st.subheader("📐 Resize Dimensions")
out_w = st.number_input("Final Width (px)", value=600)
out_h = st.number_input("Final Height (px)", value=480)
final_size = (int(out_w), int(out_h))

# ---------------------------
# Image Processing Section
# ---------------------------
max_file_size_kb = 200

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

                # Resize
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
