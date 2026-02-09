from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

def create_premium_assets():
    # Colors
    bg_color = (15, 23, 42) # Deep Slate/Dark Blue common in premium apps
    gold_main = (212, 175, 55)   # Metallic Gold
    gold_highlight = (255, 240, 150) # Very Light Gold
    gold_shadow = (120, 90, 20)  # Dark Bronze
    accent_color = (255, 215, 0) # Bright Gold

    # Font Search
    font_path = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
    if not os.path.exists(font_path):
        font_path = "Arial"

    def draw_beveled_text(draw_obj, text, pos, font, fill_main, highlight, shadow):
        x, y = pos
        # Draw shadow
        draw_obj.text((x + 6, y + 6), text, font=font, fill=shadow)
        # Draw main
        draw_obj.text((x, y), text, font=font, fill=fill_main)
        # Draw highlight (very subtle offset)
        draw_obj.text((x - 2, y - 2), text, font=font, fill=highlight)

    # 1. PREMIUM ICON (512x512)
    size = 512
    icon = Image.new('RGB', (size, size), bg_color)
    draw_icon = ImageDraw.Draw(icon)

    # Rounded Square Base for the logo center
    padding = 60
    draw_icon.rounded_rectangle([padding, padding, size-padding, size-padding], radius=100, fill=(20, 30, 50), outline=gold_main, width=4)

    try:
        font_large = ImageFont.truetype(font_path, int(size * 0.5))
    except:
        font_large = ImageFont.load_default()

    text = "S"
    bbox = draw_icon.textbbox((0, 0), text, font=font_large)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    tx, ty = (size-tw)//2, (size-th)//2 - 20

    # Draw Glow
    glow_mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(glow_mask).text((tx, ty), text, font=font_large, fill=255)
    glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(25))
    glow_layer = Image.new('RGB', (size, size), gold_main)
    icon = Image.composite(glow_layer, icon, glow_mask)

    # Draw Beveled S
    draw_icon = ImageDraw.Draw(icon)
    draw_beveled_text(draw_icon, text, (tx, ty), font_large, gold_main, gold_highlight, shadow=(10, 10, 10))

    icon.save("saghalive_mobile/google_play_icon_premium.png")

    # 2. PREMIUM FEATURE GRAPHIC (1024x500)
    w, h = 1024, 500
    feat = Image.new('RGB', (w, h), bg_color)
    draw_feat = ImageDraw.Draw(feat)

    # Add subtle gradient/vignette background
    for i in range(h):
        alpha = int(255 * (1 - (i/h) * 0.3))
        draw_feat.line([(0, i), (w, i)], fill=(10, 20, 40))

    # Decorative large "S" in background
    try:
        font_huge = ImageFont.truetype(font_path, 600)
        draw_feat.text((w-400, -100), "S", font=font_huge, fill=(20, 32, 55))
    except:
        pass

    # Title & Subtitle
    try:
        f_title = ImageFont.truetype(font_path, 90)
        f_sub = ImageFont.truetype(font_path, 35)
        f_tag = ImageFont.truetype(font_path, 20)
    except:
        f_title = f_sub = f_tag = ImageFont.load_default()

    # SaghaLive Title
    draw_feat.text((80, 120), "SaghaLive", font=f_title, fill=gold_main)
    
    # Line Separator
    draw_feat.line([(80, 230), (400, 230)], fill=gold_main, width=5)

    # Subtitle
    draw_feat.text((80, 255), "Premium Gold & Silver Tracker", font=f_sub, fill=(240, 240, 240))
    
    # Feature Pills
    features = [
        "✓ Real-time Market Rates",
        "✓ Smart Investment Planner",
        "✓ Advanced Fee Calculator",
        "✓ Multi-Currency Support"
    ]
    
    y_off = 320
    for f in features:
        draw_feat.text((80, y_off), f, font=f_tag, fill=gold_highlight)
        y_off += 30

    # Add a "Glass" Card effect on the right side
    card_x, card_y = 600, 100
    card_w, card_h = 350, 300
    draw_feat.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], radius=30, fill=(30, 41, 59), outline=gold_main, width=2)
    
    # Fake Chart inside card
    chart_pts = [(card_x+50, card_y+250), (card_x+100, card_y+200), (card_x+150, card_y+220), (card_x+200, card_y+150), (card_x+250, card_y+100), (card_x+300, card_y+50)]
    draw_feat.line(chart_pts, fill=gold_main, width=3, joint='curve')
    for pt in chart_pts:
        draw_feat.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill=accent_color)
    
    draw_feat.text((card_x+40, card_y+20), "MARKET SENSORS", font=f_tag, fill=gold_main)

    feat.save("saghalive_mobile/google_play_feature_premium.png")
    
    print("Premium assets generated successfully:")
    print("- saghalive_mobile/google_play_icon_premium.png")
    print("- saghalive_mobile/google_play_feature_premium.png")

if __name__ == "__main__":
    create_premium_assets()
