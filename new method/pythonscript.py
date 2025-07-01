# %%
from PIL import Image
import os

# Input and output folders
input_folder = "Dishayein"
output_folder = "result"
os.makedirs(output_folder, exist_ok=True)

# Target aspect ratio (5:4) and final size (600x480)
target_ratio = 5 / 4
final_size = (600, 480)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp")):
        img_path = os.path.join(input_folder, filename)

        try:
            img = Image.open(img_path)
        except Exception as e:
            print(f"❌ Failed to open {filename}: {e}")
            continue

        width, height = img.size
        current_ratio = width / height

        # Crop to 5:4 aspect ratio
        if current_ratio > target_ratio:
            # Too wide: crop width
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            box = (left, 0, left + new_width, height)
        else:
            # Too tall: crop height
            new_height = int(width / target_ratio)
            top = (height - new_height) // 2
            box = (0, top, width, top + new_height)

        cropped_img = img.crop(box)

        # Resize to 600x480 using modern Pillow enum
        resized_img = cropped_img.resize(final_size, Image.Resampling.LANCZOS)

        # Save the result
        output_path = os.path.join(output_folder, filename)
        resized_img.save(output_path)

        print(f"✔️ Processed: {filename}")

print("✅ All images cropped to 5:4 and resized to 600x480 in 'result' folder.")



