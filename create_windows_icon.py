#!/usr/bin/env python3
"""
Script to create a Windows .ico file from the source image.
"""
import os
from PIL import Image

# Source image path (same as before)
source_image = "/Users/tamerelwakeel/.gemini/antigravity/brain/50a00449-1076-46d2-85a5-43860a17ab21/uploaded_image_1766857539813.jpg"
output_path = "/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/Calculator.ico"

try:
    if os.path.exists(source_image):
        img = Image.open(source_image)
        # Windows ICO files usually contain multiple sizes
        # 16, 32, 48, 64, 128, 256
        img.save(output_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print(f"✅ Success! Windows icon created at: {output_path}")
    else:
        print(f"❌ Source image not found at: {source_image}")
        print("Using a placeholder block if running without source.")
        # Create a basic placeholder if source is missing to prevent failure
        img = Image.new('RGBA', (256, 256), color='green')
        img.save(output_path, format='ICO', sizes=[(256,256)])
        print(f"Created placeholder icon at: {output_path}")

except Exception as e:
    print(f"❌ Error creating icon: {e}")
