from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_store_assets():
    # Colors
    bg_color = (10, 10, 10) # Almost black
    gold_main = (255, 215, 0)   # Gold
    gold_light = (249, 226, 125) # Light Gold
    gold_metallic = (212, 175, 55)  # Metallic Gold
    gold_dark = (184, 134, 11)  # Dark Gold

    # Font Search
    font_path = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
    if not os.path.exists(font_path):
        font_path = "Arial" # System font fallback

    def get_gradient(size_w, size_h):
        grad = Image.new('RGB', (size_w, size_h), (0,0,0))
        draw = ImageDraw.Draw(grad)
        for i in range(size_h):
            ratio = i / size_h
            if ratio < 0.33:
                r = gold_light[0] + (gold_main[0]-gold_light[0]) * (ratio/0.33)
                g = gold_light[1] + (gold_main[1]-gold_light[1]) * (ratio/0.33)
                b = gold_light[2] + (gold_main[2]-gold_light[2]) * (ratio/0.33)
            elif ratio < 0.66:
                r = gold_main[0] + (gold_metallic[0]-gold_main[0]) * ((ratio-0.33)/0.33)
                g = gold_main[1] + (gold_metallic[1]-gold_main[1]) * ((ratio-0.33)/0.33)
                b = gold_main[2] + (gold_metallic[2]-gold_main[2]) * ((ratio-0.33)/0.33)
            else:
                r = gold_metallic[0] + (gold_dark[0]-gold_metallic[0]) * ((ratio-0.66)/0.34)
                g = gold_metallic[1] + (gold_dark[1]-gold_metallic[1]) * ((ratio-0.66)/0.34)
                b = gold_metallic[2] + (gold_dark[2]-gold_metallic[2]) * ((ratio-0.66)/0.34)
            draw.line([(0, i), (size_w, i)], fill=(int(r), int(g), int(b)))
        return grad

    # 1. Generate App Icon (512x512)
    size = 512
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, int(size * 0.7))
    except:
        font = ImageFont.load_default()
    
    text = "S"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x, y = (size-text_w)//2, (size-text_h)//2 - int(size*0.05)

    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).text((x, y), text, font=font, fill=255)
    
    grad = get_gradient(size, size)
    icon = Image.composite(grad, img, mask)
    
    # Add Glow
    glow_mask = mask.filter(ImageFilter.GaussianBlur(15))
    glow_layer = Image.new('RGB', (size, size), gold_metallic)
    icon = Image.composite(glow_layer, icon, glow_mask)
    icon = Image.composite(grad, icon, mask)
    
    icon.save("saghalive_mobile/google_play_icon.png")

    # 2. Generate Feature Graphic (1024x500)
    w, h = 1024, 500
    feat = Image.new('RGB', (w, h), bg_color)
    draw_feat = ImageDraw.Draw(feat)
    
    # Background "S" large and faded
    try:
        font_bg = ImageFont.truetype(font_path, int(h * 1.2))
    except:
        font_bg = ImageFont.load_default()
    
    bbox_s = draw_feat.textbbox((0,0), "S", font=font_bg)
    sw, sh = bbox_s[2]-bbox_s[0], bbox_s[3]-bbox_s[1]
    draw_feat.text((w-sw+100, (h-sh)//2), "S", font=font_bg, fill=(20, 20, 20))

    # Title Text
    try:
        font_title = ImageFont.truetype(font_path, 80)
        font_sub = ImageFont.truetype(font_path, 30)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_feat.text((60, 160), "SaghaLive", font=font_title, fill=gold_main)
    draw_feat.text((60, 260), "Egyptian Gold & Silver Portal", font=font_sub, fill=gold_metallic)
    draw_feat.text((60, 300), "Live Rates • Calculator • Smart Planner", font=font_sub, fill=(150, 150, 150))

    feat.save("saghalive_mobile/google_play_feature.png")
    
    print("Assets generated: ")
    print("- saghalive_mobile/google_play_icon.png (512x512)")
    print("- saghalive_mobile/google_play_feature.png (1024x500)")

if __name__ == "__main__":
    create_store_assets()
