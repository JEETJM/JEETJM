from PIL import Image
import os

ASCII_CHARS = "@%#*+=-:. "

WIDTH = 95


def resize(image):
    w, h = image.size

    ratio = h / w

    new_height = int(WIDTH * ratio * 0.55)

    return image.resize((WIDTH, new_height))


def gray(image):
    return image.convert("L")


def pixels_to_ascii(image):

    pixels = image.getdata()

    text = ""

    for pixel in pixels:

        index = pixel * (len(ASCII_CHARS) - 1) // 255

        text += ASCII_CHARS[index]

    return text


def make_ascii(path):

    image = Image.open(path)

    image = resize(image)

    image = gray(image)

    ascii_data = pixels_to_ascii(image)

    pixels = len(ascii_data)

    width = image.width

    ascii_image = ""

    for i in range(0, pixels, width):

        ascii_image += ascii_data[i:i + width] + "\n"

    return ascii_image


def save_ascii(text, output_file):

    with open(output_file, "w", encoding="utf-8") as file:

        file.write(text)

    print(f"\nASCII saved to: {output_file}")


def main():

    image_path = "../assets/profile.png"

    output_path = "../assets/avatar.txt"

    if not os.path.exists(image_path):

        print("Error: profile.png not found!")

        print("Put your image inside assets/profile.png")

        return

    ascii_art = make_ascii(image_path)

    save_ascii(ascii_art, output_path)


def ascii_to_svg(ascii_text, output_svg):

    lines = ascii_text.splitlines()

    font_size = 8
    line_height = 9

    width = 390
    height = max(560, len(lines) * line_height + 40)

    svg = []

    svg.append('<?xml version="1.0" encoding="UTF-8"?>')

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )

    svg.append("""
<defs>

<linearGradient id="asciiGradient">

<stop offset="0%" stop-color="#7C3AED">
<animate attributeName="stop-color"
values="#7C3AED;#22D3EE;#10B981;#7C3AED"
dur="8s"
repeatCount="indefinite"/>
</stop>

<stop offset="100%" stop-color="#22D3EE"/>

</linearGradient>

<filter id="glow">
<feGaussianBlur stdDeviation="2"/>
</filter>

</defs>
""")

    y = 20

    for line in lines:

        safe = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        svg.append(
            f'<text x="10" y="{y}" '
            f'font-family="JetBrains Mono, monospace" '
            f'font-size="{font_size}" '
            f'fill="url(#asciiGradient)" '
            f'filter="url(#glow)">{safe}</text>'
        )

        y += line_height

    svg.append("</svg>")

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print("SVG Avatar Created:", output_svg)

def main():

    image_path = "../assets/profile.png"

    ascii_output = "../assets/avatar.txt"

    svg_output = "../assets/avatar.svg"

    if not os.path.exists(image_path):

        print("Error: profile.png not found!")

        return

    ascii_art = make_ascii(image_path)

    save_ascii(ascii_art, ascii_output)

    ascii_to_svg(ascii_art, svg_output)

    print("\n✅ All files generated successfully!")


if __name__ == "__main__":

    main()