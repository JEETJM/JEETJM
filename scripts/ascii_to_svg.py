from PIL import (
    Image,
    ImageOps,
    ImageEnhance,
    ImageFilter
)

import os

# =====================================================
# CONFIG
# =====================================================

WIDTH = 180

FONT_SIZE = 5.5

LINE_HEIGHT = 5.8

ASCII_CHARS = (
    "@@@@@@@%%%%%%#####******++++++======------::::::......      "
)

# =====================================================
# IMAGE LOADER
# =====================================================


def load_image(path):

    image = Image.open(path)

    image = image.convert("RGB")

    return image


# =====================================================
# AUTO CONTRAST
# =====================================================

def enhance(image):

    image = ImageOps.autocontrast(image)

    image = ImageEnhance.Contrast(image).enhance(2.4)

    image = ImageEnhance.Sharpness(image).enhance(2.3)

    image = ImageEnhance.Brightness(image).enhance(1.05)

    return image


# =====================================================
# RESIZE
# =====================================================

def resize(image):

    w, h = image.size

    ratio = h / w

    new_height = int(WIDTH * ratio * 0.43)

    image = image.resize(
        (WIDTH, new_height),
        Image.Resampling.LANCZOS
    )

    return image


# =====================================================
# GRAYSCALE
# =====================================================

def gray(image):

    return ImageOps.grayscale(image)


# =====================================================
# EDGE BOOST
# =====================================================

def edge(image):

    edge_img = image.filter(ImageFilter.FIND_EDGES)

    edge_img = ImageEnhance.Contrast(edge_img).enhance(2)

    return edge_img


# =====================================================
# MIX EDGE + ORIGINAL
# =====================================================

def mix(gray_img):

    edge_img = edge(gray_img)

    mixed = Image.blend(
        gray_img,
        edge_img,
        0.18
    )

    return mixed


# =====================================================
# PIXEL → ASCII
# =====================================================

def pixel_to_char(pixel):

    scale = len(ASCII_CHARS) - 1

    index = int(pixel / 255 * scale)

    return ASCII_CHARS[index]
# =====================================================
# FLOYD–STEINBERG DITHERING
# =====================================================


def floyd_dither(image):

    image = image.copy().convert("L")

    pixels = image.load()

    w, h = image.size

    for y in range(h - 1):

        for x in range(1, w - 1):

            old = pixels[x, y]

            new = round(old / 255) * 255

            pixels[x, y] = new

            error = old - new

            pixels[x + 1, y] = max(
                0,
                min(255, pixels[x + 1, y] + error * 7 // 16)
            )

            pixels[x - 1, y + 1] = max(
                0,
                min(255, pixels[x - 1, y + 1] + error * 3 // 16)
            )

            pixels[x, y + 1] = max(
                0,
                min(255, pixels[x, y + 1] + error * 5 // 16)
            )

            pixels[x + 1, y + 1] = max(
                0,
                min(255, pixels[x + 1, y + 1] + error * 1 // 16)
            )

    return image


# =====================================================
# PIXELS -> ASCII STRING
# =====================================================

def pixels_to_ascii(image):

    pixels = list(image.getdata())

    chars = []

    scale = len(ASCII_CHARS) - 1

    for pixel in pixels:

        index = pixel * scale // 255

        chars.append(ASCII_CHARS[index])

    return "".join(chars)


# =====================================================
# BUILD ASCII IMAGE
# =====================================================

def make_ascii(path):

    image = load_image(path)

    image = enhance(image)

    image = resize(image)

    image = gray(image)

    image = mix(image)

    image = floyd_dither(image)

    ascii_string = pixels_to_ascii(image)

    ascii_lines = []

    for i in range(0, len(ascii_string), WIDTH):

        ascii_lines.append(
            ascii_string[i:i + WIDTH]
        )

    return "\n".join(ascii_lines)


# =====================================================
# SAVE TXT
# =====================================================

def save_ascii(text, output):

    with open(output, "w", encoding="utf8") as f:

        f.write(text)

    print("ASCII saved ->", output)
    # =====================================================
# ASCII -> PREMIUM SVG
# =====================================================


def ascii_to_svg(ascii_text, output_svg):

    lines = ascii_text.splitlines()

    svg_width = WIDTH * 6
    svg_height = max(560, len(lines) * LINE_HEIGHT + 40)

    svg = []

    svg.append('<?xml version="1.0" encoding="UTF-8"?>')

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">'''
    )

    svg.append("""

<defs>

<linearGradient id="asciiGradient"
x1="0%"
y1="0%"
x2="100%"
y2="100%">

<stop offset="0%" stop-color="#7C3AED">
<animate attributeName="stop-color"
values="#7C3AED;#22D3EE;#10B981;#7C3AED"
dur="8s"
repeatCount="indefinite"/>
</stop>

<stop offset="100%" stop-color="#22D3EE"/>

</linearGradient>

<filter id="glow">
<feGaussianBlur stdDeviation="0.8"/>
</filter>

</defs>

<rect
width="100%"
height="100%"
fill="#0B1120"/>

""")

    # Scanlines
    for y in range(0, int(svg_height), 4):

        svg.append(
            f'<line x1="0" y1="{y}" x2="{svg_width}" y2="{y}" stroke="#FFFFFF" opacity="0.02"/>'
        )

    y = 20

    for line in lines:

        safe = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        svg.append(

            f'''<text
x="8"
y="{y}"
font-family="JetBrains Mono, monospace"
font-size="{FONT_SIZE}"
fill="url(#asciiGradient)"
filter="url(#glow)"
xml:space="preserve">{safe}</text>'''

        )

        y += LINE_HEIGHT

    svg.append("</svg>")

    with open(output_svg, "w", encoding="utf8") as f:

        f.write("\n".join(svg))

    print("SVG saved ->", output_svg)


# =====================================================
# MAIN
# =====================================================

def main():

    image_path = "../assets/profile.png"

    txt_output = "../assets/avatar.txt"

    svg_output = "../assets/avatar.svg"

    if not os.path.exists(image_path):

        print("profile.png not found!")

        return

    ascii_art = make_ascii(image_path)

    save_ascii(ascii_art, txt_output)

    ascii_to_svg(ascii_art, svg_output)

    print()

    print("="*45)

    print(" Premium ASCII Generated Successfully ")

    print("="*45)

    print()

    print("TXT :", txt_output)

    print("SVG :", svg_output)


if __name__ == "__main__":

    main()
