import os
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random
import io

THUMBNAILS_DIR = "thumbnails"
os.makedirs(THUMBNAILS_DIR, exist_ok=True)

BACKGROUNDS = [
    {"colors": ["#667eea", "#764ba2"]},
    {"colors": ["#f093fb", "#f5576c"]},
    {"colors": ["#4facfe", "#00f2fe"]},
    {"colors": ["#43e97b", "#38f9d7"]},
    {"colors": ["#fa709a", "#fee140"]},
    {"colors": ["#a8edea", "#fed6e3"]},
    {"colors": ["#ff9a9e", "#fecfef"]},
    {"colors": ["#ffecd2", "#fcb69f"]},
    {"colors": ["#6a11cb", "#2575fc"]},
    {"colors": ["#232526", "#414345"]},
]

def create_gradient(width, height, colors):
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    color1 = tuple(int(colors[0][i:i+2], 16) for i in (1, 3, 5))
    color2 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def circle_image(img, size):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size - 1, size - 1], fill=255)
    
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    resized = img.resize((size, size), Image.LANCZOS)
    output.paste(resized, (0, 0), mask)
    return output

def add_glow_circle(size, color, glow_size=20):
    output = Image.new("RGBA", (size + glow_size * 2, size + glow_size * 2), (0, 0, 0, 0))
    for i in range(glow_size, 0, -1):
        alpha = int(80 * (1 - i / glow_size))
        glow_color = (*color[:3], alpha)
        draw = ImageDraw.Draw(output)
        offset = glow_size - i
        draw.ellipse(
            [offset, offset, size + offset, size + offset],
            fill=glow_color
        )
    return output

def get_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    
    return ImageFont.load_default()

async def create_playing_thumbnail(title, duration, artist, thumbnail_url=None, bg_index=None):
    try:
        width, height = 640, 640
        
        if bg_index is None:
            bg_index = random.randint(0, len(BACKGROUNDS) - 1)
        
        bg = create_gradient(width, height, BACKGROUNDS[bg_index]["colors"])
        bg = bg.filter(ImageFilter.GaussianBlur(radius=2))
        
        overlay = Image.new("RGB", (width, height), (0, 0, 0))
        overlay.paste(bg, (0, 0))
        bg = overlay
        draw = ImageDraw.Draw(bg)
        
        circle_size = 220
        center_x = width // 2
        center_y = 180
        
        shadow = Image.new("RGBA", (circle_size + 50, circle_size + 50), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        for i in range(25, 0, -1):
            alpha = int(60 * (1 - i / 25))
            shadow_draw.ellipse(
                [25 - i, 25 - i, circle_size + 25 - 1 + i, circle_size + 25 - 1 + i],
                fill=(0, 0, 0, alpha)
            )
        
        circle_img = Image.new("RGBA", (circle_size + 50, circle_size + 50), (0, 0, 0, 0))
        
        border_color = (255, 255, 255)
        border_width = 5
        
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url, timeout=10)
                if response.status_code == 200:
                    thumb_img = Image.open(io.BytesIO(response.content))
                    thumb_img = thumb_img.convert("RGBA")
                    thumb_circle = circle_image(thumb_img, circle_size)
                    
                    border = Image.new("RGBA", (circle_size + border_width * 2, circle_size + border_width * 2), border_color + (255,))
                    border_circle = circle_image(border, circle_size)
                    
                    circle_img.paste(thumb_circle, (25, 25), thumb_circle)
                    circle_img.paste(border_circle, (0, 0), border_circle)
            except Exception as e:
                print(f"Thumbnail load error: {e}")
                music_icon = Image.new("RGBA", (circle_size, circle_size), (255, 255, 255, 255))
                circle_img.paste(circle_image(music_icon, circle_size), (25, 25), circle_image(music_icon, circle_size))
        else:
            music_icon = Image.new("RGBA", (circle_size, circle_size), (255, 255, 255, 255))
            circle_img.paste(circle_image(music_icon, circle_size), (25, 25), circle_image(music_icon, circle_size))
        
        bg.paste(shadow, (center_x - (circle_size + 50) // 2, center_y - (circle_size + 50) // 2), shadow)
        bg.paste(circle_img, (center_x - (circle_size + 50) // 2, center_y - (circle_size + 50) // 2), circle_img)
        
        draw = ImageDraw.Draw(bg)
        note_font = get_font(100)
        note_text = "♪"
        note_bbox = draw.textbbox((0, 0), note_text, font=note_font)
        note_width = note_bbox[2] - note_bbox[0]
        note_height = note_bbox[3] - note_bbox[1]
        draw.text(
            (center_x - note_width // 2, center_y - note_height // 2 - 10),
            note_text,
            font=note_font,
            fill=(50, 50, 50, 180)
        )
        
        header_text = "▶ NOW PLAYING"
        header_font = get_font(26)
        header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
        header_width = header_bbox[2] - header_bbox[0]
        header_x = (width - header_width) // 2
        draw.text((header_x, 360), header_text, font=header_font, fill=(255, 255, 255))
        
        title_short = title[:30] + "..." if len(title) > 30 else title
        title_font = get_font(30)
        title_bbox = draw.textbbox((0, 0), title_short, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        draw.text((title_x, 410), title_short, font=title_font, fill=(255, 255, 255))
        
        info_text = f"⏱ {duration} • {artist[:15]}"
        info_font = get_font(22)
        info_bbox = draw.textbbox((0, 0), info_text, font=info_font)
        info_width = info_bbox[2] - info_bbox[0]
        info_x = (width - info_width) // 2
        draw.text((info_x, 465), info_text, font=info_font, fill=(220, 220, 255))
        
        for i in range(5):
            size = 10 if i == 2 else 7
            alpha = 255 if i == 2 else 150
            x = center_x - 50 + i * 25
            y = 530
            draw.ellipse([x - size, y - size, x + size, y + size], fill=(255, 255, 255, alpha))
        
        file_hash = hash(title) % 1000000
        file_path = os.path.join(THUMBNAILS_DIR, f"playing_{file_hash}.png")
        
        bg_rgb = bg.convert("RGB")
        bg_rgb.save(file_path, "PNG")
        
        return file_path
        
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        import traceback
        traceback.print_exc()
        return None

async def get_thumbnail(video_id, title):
    try:
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return await create_playing_thumbnail(title, "N/A", "Loading...", thumbnail_url)
    except Exception as e:
        print(f"Thumbnail error: {e}")
        return None
