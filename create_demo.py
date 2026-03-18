#!/usr/bin/env python3
"""
Creates test.mpdf — a demo MPDF document with a programmatically generated animated GIF.
No external dependencies required.
"""

import base64
import struct
from datetime import date

# ─── GIF Generation (raw GIF89a binary, no Pillow needed) ────────────────────

def lzw_encode(pixels, min_code_size):
    """LZW-compress pixel data for GIF image."""
    clear_code = 1 << min_code_size
    eoi_code = clear_code + 1

    code_table = {}
    for i in range(clear_code):
        code_table[(i,)] = i
    next_code = eoi_code + 1
    code_size = min_code_size + 1
    max_code = 1 << code_size

    output = bytearray()
    bit_buffer = 0
    bits_in_buffer = 0

    def emit(code):
        nonlocal bit_buffer, bits_in_buffer, code_size, max_code, next_code
        bit_buffer |= code << bits_in_buffer
        bits_in_buffer += code_size
        while bits_in_buffer >= 8:
            output.append(bit_buffer & 0xFF)
            bit_buffer >>= 8
            bits_in_buffer -= 8

    emit(clear_code)

    buffer = (pixels[0],)
    for pixel in pixels[1:]:
        buffer_plus = buffer + (pixel,)
        if buffer_plus in code_table:
            buffer = buffer_plus
        else:
            emit(code_table[buffer])
            if next_code < 4096:
                code_table[buffer_plus] = next_code
                next_code += 1
                if next_code > max_code and code_size < 12:
                    code_size += 1
                    max_code = 1 << code_size
            else:
                emit(clear_code)
                code_table = {}
                for i in range(clear_code):
                    code_table[(i,)] = i
                next_code = eoi_code + 1
                code_size = min_code_size + 1
                max_code = 1 << code_size
            buffer = (pixel,)

    emit(code_table[buffer])
    emit(eoi_code)

    if bits_in_buffer > 0:
        output.append(bit_buffer & 0xFF)

    return bytes(output)


def create_animated_gif():
    """Create a 120x120 animated GIF with a moving colored gradient bar."""
    W, H = 120, 120
    num_frames = 8
    delay = 15  # centiseconds (150ms per frame)

    palette = [
        (41, 98, 255),    # 0: blue
        (0, 200, 83),     # 1: green
        (255, 61, 0),     # 2: red/orange
        (255, 214, 0),    # 3: yellow
        (156, 39, 176),   # 4: purple
        (0, 172, 193),    # 5: teal
        (255, 255, 255),  # 6: white (background)
        (30, 30, 30),     # 7: dark gray
    ]

    gif = bytearray()

    # Header
    gif.extend(b'GIF89a')

    # Logical Screen Descriptor
    gif.extend(struct.pack('<HH', W, H))
    gif.append(0b10000010)  # GCT flag=1, color res=0, sort=0, GCT size=2 (8 colors)
    gif.append(6)  # background color index (white)
    gif.append(0)  # pixel aspect ratio

    # Global Color Table
    for r, g, b in palette:
        gif.extend(bytes([r, g, b]))

    # Netscape Application Extension (loop forever)
    gif.extend(bytes([0x21, 0xFF, 0x0B]))
    gif.extend(b'NETSCAPE2.0')
    gif.extend(bytes([0x03, 0x01, 0x00, 0x00, 0x00]))

    for frame_idx in range(num_frames):
        # Graphic Control Extension
        gif.extend(bytes([0x21, 0xF9, 0x04]))
        gif.append(0x08)  # disposal: restore to background
        gif.extend(struct.pack('<H', delay))
        gif.append(0x00)
        gif.append(0x00)

        # Image Descriptor
        gif.append(0x2C)
        gif.extend(struct.pack('<HH', 0, 0))
        gif.extend(struct.pack('<HH', W, H))
        gif.append(0x00)

        # Pixel data: colored bar moving down
        pixels = []
        bar_height = 20
        bar_y = (frame_idx * (H - bar_height)) // (num_frames - 1)
        color = frame_idx % 6

        for y in range(H):
            for x in range(W):
                if bar_y <= y < bar_y + bar_height:
                    if (x // 10 + frame_idx) % 2 == 0:
                        pixels.append(color)
                    else:
                        pixels.append((color + 1) % 6)
                else:
                    pixels.append(6)  # white

        # LZW encode
        min_code_size = 3
        gif.append(min_code_size)
        compressed = lzw_encode(pixels, min_code_size)

        i = 0
        while i < len(compressed):
            block_size = min(255, len(compressed) - i)
            gif.append(block_size)
            gif.extend(compressed[i:i + block_size])
            i += block_size
        gif.append(0x00)

    gif.append(0x3B)
    return bytes(gif)


# ─── MPDF Document Generation ────────────────────────────────────────────────

MPDF_CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f0f0;font-family:Georgia,'Times New Roman',Times,serif;font-size:16px;line-height:1.8;color:#1a1a1a;padding:40px 20px}
.mpdf-document{max-width:800px;margin:0 auto}
.mpdf-page{background:#fff;padding:60px 70px;margin-bottom:30px;box-shadow:0 2px 8px rgba(0,0,0,0.12);position:relative;min-height:900px;page-break-after:always}
.mpdf-heading{font-family:Georgia,'Times New Roman',Times,serif;margin-bottom:0.6em;line-height:1.3}
h1.mpdf-heading{font-size:28px;text-align:center;margin-bottom:0.8em}
h2.mpdf-heading{font-size:22px;margin-top:1.2em}
h3.mpdf-heading{font-size:18px;margin-top:1em}
.mpdf-text{margin-bottom:1em;text-align:justify;hyphens:auto}
.mpdf-gif,.mpdf-image{margin:1.5em auto;text-align:center}
.mpdf-gif img,.mpdf-image img{max-width:100%;height:auto;border:1px solid #ddd;border-radius:3px}
.mpdf-gif figcaption,.mpdf-image figcaption{font-size:13px;color:#666;margin-top:8px;font-style:italic}
.mpdf-separator{border:none;border-top:1px solid #ccc;margin:2em 0}
@media(max-width:600px){.mpdf-page{padding:30px 25px}h1.mpdf-heading{font-size:22px}body{padding:10px}}
@media print{body{background:#fff;padding:0}.mpdf-page{box-shadow:none;padding:40px 50px;margin:0}.mpdf-gif img{max-height:400px}}
@media(prefers-color-scheme:dark){body{background:#1e1e1e}.mpdf-page{background:#2d2d2d;color:#e0e0e0;box-shadow:0 2px 8px rgba(0,0,0,0.4)}.mpdf-gif img,.mpdf-image img{border-color:#444}.mpdf-gif figcaption,.mpdf-image figcaption{color:#999}.mpdf-separator{border-color:#444}}"""


def create_demo():
    print("Generating animated GIF...")
    gif_data = create_animated_gif()
    gif_b64 = base64.b64encode(gif_data).decode('ascii')
    print(f"  GIF size: {len(gif_data)} bytes")

    today = date.today().isoformat()

    doc = f"""<!DOCTYPE mpdf>
<html data-mpdf-version="1.0">
<head>
<meta charset="utf-8">
<meta name="mpdf:title" content="MPDF Format Demonstration">
<meta name="mpdf:author" content="MPDF Reference Implementation">
<meta name="mpdf:created" content="{today}">
<meta name="mpdf:generator" content="create_demo/1.0">
<title>MPDF Format Demonstration</title>
<style>{MPDF_CSS}</style>
</head>
<body>
<article class="mpdf-document">
<section class="mpdf-page" data-page="1">
<h1 class="mpdf-heading">MPDF: Media PDF<br>Documents with Animated GIFs</h1>
<h2 class="mpdf-heading">Abstract</h2>
<p class="mpdf-text">This document demonstrates the MPDF file format — an open standard for creating portable documents that support embedded animated GIF images. Unlike traditional PDF files, which can only display static images, MPDF enables authors to include animations directly within their documents while maintaining the familiar paper-like reading experience.</p>
<h2 class="mpdf-heading">1. Introduction</h2>
<p class="mpdf-text">The Portable Document Format (PDF) has been the standard for document exchange for over three decades. However, as digital communication evolves, the need for richer media in documents becomes apparent. MPDF addresses this by extending the document paradigm with animated GIF support.</p>
<p class="mpdf-text">Below is an animated figure demonstrating the format's capability to embed and display animated GIF images inline with text content:</p>
<figure class="mpdf-gif">
<img src="data:image/gif;base64,{gif_b64}" alt="Animated demonstration showing a moving colored gradient bar">
<figcaption>Figure 1: An animated gradient bar demonstrating embedded GIF support in the MPDF format.</figcaption>
</figure>
<h2 class="mpdf-heading">2. Format Design</h2>
<p class="mpdf-text">MPDF is designed around three core principles: zero-install viewing (any browser can open it), self-containment (all resources are embedded inline), and deterministic rendering (a standardized stylesheet ensures consistent appearance across platforms).</p>
<p class="mpdf-text">The format is intentionally simple — a single self-contained file that can be shared via email, messaging, or any file transfer mechanism. Recipients need nothing more than a web browser to view the document, including its animated content.</p>
<h2 class="mpdf-heading">3. Conclusion</h2>
<p class="mpdf-text">MPDF proves that document formats can evolve to include richer media without sacrificing simplicity or portability. This very document is a valid .mpdf file — if you are reading it in a browser, you are experiencing the format firsthand.</p>
<hr class="mpdf-separator">
<p class="mpdf-text">MPDF v1.0 — Open Standard — {today}</p>
</section>
</article>
</body>
</html>"""

    output_path = 'test.mpdf'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(doc)

    print(f"  Created: {output_path}")
    print(f"  File size: {len(doc.encode('utf-8'))} bytes")
    print(f"\nOpen in browser: {output_path}")


if __name__ == '__main__':
    create_demo()
