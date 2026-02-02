from PIL import Image, ImageDraw, ImageFont
import os

# 設定
SIZE = 200  # 画像サイズ
CIRCLE_RATIO = 0.95  # 円のサイズ比率（画像に対して）
TEXT_RATIO = 0.80  # 文字のサイズ比率（円に対して）

# IMEIndicatorClockの実際のデフォルト色（RGB 0.0-1.0 → 0-255に変換）
# englishColor: (0.0, 0.0, 1.0) = 青
# japaneseColor: (1.0, 0.0, 0.0) = 赤
# chineseSimplifiedColor: (0.0, 0.7, 0.0) = 明るい緑
# chineseTraditionalColor: (0.0, 0.5, 0.0) = 暗めの緑
# koreanColor: (0.6, 0.0, 0.6) = 紫

def rgb_to_hex(r, g, b):
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

icons = [
    ("ime_ja.png", rgb_to_hex(1.0, 0.0, 0.0), "あ"),      # 日本語 - 赤
    ("ime_ko.png", rgb_to_hex(0.6, 0.0, 0.6), "한"),      # 韓国語 - 紫
    ("ime_zh_hant.png", rgb_to_hex(0.0, 0.5, 0.0), "繁"), # 繁体字 - 暗めの緑
    ("ime_zh_hans.png", rgb_to_hex(0.0, 0.7, 0.0), "简"), # 簡体字 - 明るい緑
    ("ime_en.png", rgb_to_hex(0.0, 0.0, 1.0), "A"),       # 英語 - 青
]

print("Colors:")
for name, color, text in icons:
    print(f"  {name}: {color} ({text})")

# フォント（各言語用）
def get_font_for_text(text, size):
    # 韓国語用
    if text == "한":
        korean_fonts = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/Library/Fonts/NanumGothic.ttf",
        ]
        for path in korean_fonts:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
    # 日本語用
    elif text == "あ":
        jp_fonts = [
            "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        ]
        for path in jp_fonts:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
    # 中国語用
    elif text in ["繁", "简"]:
        cn_fonts = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
        ]
        for path in cn_fonts:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
    # 英語・その他
    default_fonts = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in default_fonts:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

output_dir = "/Users/obote/Documents/_Programing/IMEIndicatorClock_宣伝素材/ime_icons"

for filename, color, text in icons:
    # 透明背景の画像を作成
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 円を描画
    circle_size = int(SIZE * CIRCLE_RATIO)
    margin = (SIZE - circle_size) // 2
    draw.ellipse(
        [margin, margin, SIZE - margin, SIZE - margin],
        fill=color
    )
    
    # 文字サイズを計算（円に対して80%）
    font_size = int(circle_size * TEXT_RATIO)
    font = get_font_for_text(text, font_size)
    
    # 文字の位置を計算（中央揃え）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (SIZE - text_width) // 2
    y = (SIZE - text_height) // 2 - bbox[1]  # ベースライン調整
    
    # 白い文字を描画
    draw.text((x, y), text, fill="white", font=font)
    
    # 保存
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, "PNG")
    print(f"Created: {filepath}")

print("Done!")
