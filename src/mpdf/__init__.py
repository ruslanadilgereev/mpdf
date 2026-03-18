"""
MPDF — Media PDF: Open document format with animated GIF support.

Usage:
    from mpdf import MPDFDocument

    doc = MPDFDocument("My Paper", author="Author Name")
    page = doc.add_page()
    page.add_heading("Title", level=1)
    page.add_text("Hello world.")
    page.add_gif("animation.gif", caption="Figure 1")
    doc.save("output.mpdf")
"""

__version__ = "1.0.0"

import base64
from datetime import date

from .stylesheet import MPDF_CSS


def _escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


class MPDFPage:
    """Represents a single page in an MPDF document."""

    def __init__(self):
        self.elements = []

    def add_heading(self, text, level=1):
        if level not in (1, 2, 3):
            raise ValueError("Heading level must be 1, 2, or 3")
        self.elements.append(('heading', level, text))
        return self

    def add_text(self, text):
        self.elements.append(('text', text))
        return self

    def add_gif(self, gif_path=None, gif_bytes=None, gif_b64=None,
                alt="Animated GIF", caption=""):
        if gif_path:
            with open(gif_path, 'rb') as f:
                gif_b64 = base64.b64encode(f.read()).decode('ascii')
        elif gif_bytes:
            gif_b64 = base64.b64encode(gif_bytes).decode('ascii')
        elif gif_b64 is None:
            raise ValueError("Provide gif_path, gif_bytes, or gif_b64")
        self.elements.append(('gif', gif_b64, alt, caption))
        return self

    def add_image(self, image_path=None, image_bytes=None, image_b64=None,
                  mime="image/png", alt="Image", caption=""):
        if image_path:
            with open(image_path, 'rb') as f:
                image_b64 = base64.b64encode(f.read()).decode('ascii')
        elif image_bytes:
            image_b64 = base64.b64encode(image_bytes).decode('ascii')
        elif image_b64 is None:
            raise ValueError("Provide image_path, image_bytes, or image_b64")
        self.elements.append(('image', image_b64, mime, alt, caption))
        return self

    def add_separator(self):
        self.elements.append(('separator',))
        return self

    def _render(self, page_num):
        parts = []
        for el in self.elements:
            if el[0] == 'heading':
                lvl, text = el[1], el[2]
                parts.append(f'<h{lvl} class="mpdf-heading">{_escape(text)}</h{lvl}>')
            elif el[0] == 'text':
                parts.append(f'<p class="mpdf-text">{_escape(el[1])}</p>')
            elif el[0] == 'gif':
                _, b64, alt, caption = el
                cap = f'\n<figcaption>{_escape(caption)}</figcaption>' if caption else ''
                parts.append(
                    f'<figure class="mpdf-gif">\n'
                    f'<img src="data:image/gif;base64,{b64}" alt="{_escape(alt)}">'
                    f'{cap}\n</figure>'
                )
            elif el[0] == 'image':
                _, b64, mime, alt, caption = el
                cap = f'\n<figcaption>{_escape(caption)}</figcaption>' if caption else ''
                parts.append(
                    f'<figure class="mpdf-image">\n'
                    f'<img src="data:{mime};base64,{b64}" alt="{_escape(alt)}">'
                    f'{cap}\n</figure>'
                )
            elif el[0] == 'separator':
                parts.append('<hr class="mpdf-separator">')
        content = '\n'.join(parts)
        return f'<section class="mpdf-page" data-page="{page_num}">\n{content}\n</section>'


class MPDFDocument:
    """Create MPDF documents programmatically."""

    def __init__(self, title, author="", subject="", keywords=""):
        self.title = title
        self.author = author
        self.subject = subject
        self.keywords = keywords
        self.pages = []

    def add_page(self):
        page = MPDFPage()
        self.pages.append(page)
        return page

    def render(self):
        meta = [
            '<meta charset="utf-8">',
            f'<meta name="mpdf:title" content="{_escape(self.title)}">',
        ]
        if self.author:
            meta.append(f'<meta name="mpdf:author" content="{_escape(self.author)}">')
        if self.subject:
            meta.append(f'<meta name="mpdf:subject" content="{_escape(self.subject)}">')
        if self.keywords:
            meta.append(f'<meta name="mpdf:keywords" content="{_escape(self.keywords)}">')
        meta.append(f'<meta name="mpdf:created" content="{date.today().isoformat()}">')
        meta.append('<meta name="mpdf:generator" content="mpdf-python/1.0">')
        meta.append(f'<title>{_escape(self.title)}</title>')
        meta.append(f'<style>{MPDF_CSS}</style>')

        page_html = '\n'.join(p._render(i) for i, p in enumerate(self.pages, 1))

        return (
            f'<!DOCTYPE mpdf>\n'
            f'<html data-mpdf-version="1.0">\n'
            f'<head>\n' + '\n'.join(meta) + '\n</head>\n'
            f'<body>\n'
            f'<article class="mpdf-document">\n{page_html}\n</article>\n'
            f'</body>\n</html>'
        )

    def save(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.render())
