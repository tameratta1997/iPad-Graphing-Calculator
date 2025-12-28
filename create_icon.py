#!/usr/bin/env python3
"""
Script to convert a PNG image to macOS .icns format
"""
import os
import shutil
from PIL import Image

# Source image path
source_image = "/Users/tamerelwakeel/.gemini/antigravity/brain/50a00449-1076-46d2-85a5-43860a17ab21/uploaded_image_1766857539813.jpg"
output_dir = "/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma"
iconset_path = os.path.join(output_dir, "Calculator.iconset")
icns_path = os.path.join(output_dir, "Calculator.icns")

# Create iconset directory
if os.path.exists(iconset_path):
    shutil.rmtree(iconset_path)
os.makedirs(iconset_path)

# Open source image
img = Image.open(source_image)

# macOS icon sizes (standard sizes for .icns)
sizes = [
    (16, "16x16"),
    (32, "16x16@2x"),
    (32, "32x32"),
    (64, "32x32@2x"),
    (128, "128x128"),
    (256, "128x128@2x"),
    (256, "256x256"),
    (512, "256x256@2x"),
    (512, "512x512"),
    (1024, "512x512@2x"),
]

print("Creating icon sizes...")
for size, name in sizes:
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    icon_path = os.path.join(iconset_path, f"icon_{name}.png")
    resized.save(icon_path, "PNG")
    print(f"  Created: icon_{name}.png ({size}x{size})")

print(f"\nIconset created at: {iconset_path}")
print("Converting to .icns format using macOS iconutil...")

# Use macOS iconutil to convert iconset to icns
os.system(f"iconutil -c icns '{iconset_path}' -o '{icns_path}'")

if os.path.exists(icns_path):
    print(f"\n✅ Success! Icon created at: {icns_path}")
    # Clean up iconset directory
    shutil.rmtree(iconset_path)
    print(f"Cleaned up temporary iconset directory")
else:
    print("\n❌ Failed to create .icns file")
