#!/usr/bin/env python3
"""
mpdf-create — Reference tool for creating MPDF documents.

Usage:
  python mpdf-create.py --title "My Paper" -o output.mpdf \\
      text "Introduction paragraph..." \\
      gif  diagram.gif "Figure 1: Animation" \\
      text "More content here..."

Part of the MPDF Open Standard.
"""

import argparse
import base64
import sys
from datetime import date

MPDF_STYLESHEET = (
    '*{margin:0;padding:0;box-sizing:border-box}'
    "body{background:#f0f0f0;font-family:Georgia,'Times New Roman',Times,serif;"
    'font-size:16px;line-height:1.8;color:#1a1a1a;padding:40px 20px}'
    '.mpdf-document{max-width:800px;margin:0 auto}'
    '.mpdf-page{background:#fff;padding:60px 70px;margin-bottom:30px;'
    'box-shadow:0 2px 8px rgba(0,0,0,0.12);position:relative;'
    'min-height:900px;page-break-after:always}'
    ".mpdf-heading{font-family:Georgia,'Times New Roman',Times,serif;"
    'margin-bottom:0.6em;line-height:1.3}'
    'h1.mpdf-heading{font-size:28px;text-align:center;margin-bottom:0.8em}'
    'h2.mpdf-heading{font-size:22px;margin-top:1.2em}'
    'h3.mpdf-heading{font-size:18px;margin-top:1em}'
    '.mpdf-text{margin-bottom:1em;text-align:justify;hyphens:auto}'
    '.mpdf-gif,.mpdf-image{margin:1.5em auto;text-align:center}'
    '.mpdf-gif img,.mpdf-image img{max-width:100%;height:auto;'
    'border:1px solid #ddd;border-radius:3px}'
    '.mpdf-gif figcaption,.mpdf-image figcaption{font-size:13px;'
    "color:#666;margin-top:8px;font-style:italic}"
    '.mpdf-separator{border:none;border-top:1px solid #ccc;margin:2em 0}'
    '@media(max-width:600px){.mpdf-page{padding:30px 25px}'
    'h1.mpdf-heading{font-size:22px}body{padding:10px}}'
    '@media print{body{background:#fff;padding:0}'
    '.mpdf-page{box-shadow:none;padding:40px 50px;margin:0}'
    '.mpdf-gif img{max-height:400px}}'
    '@media(prefers-color-scheme:dark){body{background:#1e1e1e}'
    '.mpdf-page{background:#2d2d2d;color:#e0e0e0;'
    'box-shadow:0 2px 8px rgba(0,0,0,0.4)}'
    '.mpdf-gif img,.mpdf-image img{border-color:#444}'
    '.mpdf-gif figcaption,.mpdf-image figcaption{color:#999}'
    '.mpdf-separator{border-color:#444}}'
)


def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def build_mpdf(title, author, pages):
    """Build an MPDF document string.

    Args:
        title: Document title
        author: Author name (can be empty)
        pages: List of pages. Each page is a list of element dicts:
               {"type": "h1"|"h2"|"h3"|"text", "content": "..."}
               {"type": "gif", "data_b64": "...", "alt": "...", "caption": "..."}
    """
    meta = [
        '<meta charset="utf-8">',
        f'<meta name="mpdf:title" content="{escape_html(title)}">',
    ]
    if author:
        meta.append(f'<meta name="mpdf:author" content="{escape_html(author)}">')
    meta.append(f'<meta name="mpdf:created" content="{date.today().isoformat()}">')
    meta.append('<meta name="mpdf:generator" content="mpdf-create/1.0">')
    meta.append(f'<title>{escape_html(title)}</title>')
    meta.append(f'<style>{MPDF_STYLESHEET}</style>')

    head = '\n'.join(meta)

    page_sections = []
    for i, page in enumerate(pages, 1):
        elements = []
        for el in page:
            t = el['type']
            if t in ('h1', 'h2', 'h3'):
                elements.append(f'<{t} class="mpdf-heading">{escape_html(el["content"])}</{t}>')
            elif t == 'text':
                elements.append(f'<p class="mpdf-text">{escape_html(el["content"])}</p>')
            elif t == 'gif':
                cap = ''
                if el.get('caption'):
                    cap = f'\n<figcaption>{escape_html(el["caption"])}</figcaption>'
                alt = escape_html(el.get('alt', 'Animated GIF'))
                elements.append(
                    f'<figure class="mpdf-gif">\n'
                    f'<img src="data:image/gif;base64,{el["data_b64"]}" alt="{alt}">'
                    f'{cap}\n</figure>'
                )
            elif t == 'separator':
                elements.append('<hr class="mpdf-separator">')

        content = '\n'.join(elements)
        page_sections.append(f'<section class="mpdf-page" data-page="{i}">\n{content}\n</section>')

    body = '\n'.join(page_sections)

    return (
        f'<!DOCTYPE mpdf>\n'
        f'<html data-mpdf-version="1.0">\n'
        f'<head>\n{head}\n</head>\n'
        f'<body>\n'
        f'<article class="mpdf-document">\n{body}\n</article>\n'
        f'</body>\n</html>'
    )


def gif_file_to_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')


def main():
    parser = argparse.ArgumentParser(
        description='Create MPDF documents — the open standard for documents with animated GIFs.',
        epilog='Elements are added to the current page in order. Use "page" to start a new page.',
    )
    parser.add_argument('--title', '-t', required=True, help='Document title')
    parser.add_argument('--author', '-a', default='', help='Author name')
    parser.add_argument('-o', '--output', required=True, help='Output .mpdf file path')
    parser.add_argument(
        'elements', nargs='+',
        help='Sequence of: text "..." | gif <file> ["caption"] | h1/h2/h3 "..." | sep | page'
    )

    args = parser.parse_args()

    pages = [[]]
    els = iter(args.elements)
    for token in els:
        if token == 'page':
            pages.append([])
        elif token == 'sep':
            pages[-1].append({'type': 'separator'})
        elif token in ('h1', 'h2', 'h3'):
            content = next(els, '')
            pages[-1].append({'type': token, 'content': content})
        elif token == 'text':
            content = next(els, '')
            pages[-1].append({'type': 'text', 'content': content})
        elif token == 'gif':
            path = next(els, '')
            caption = ''
            try:
                maybe_caption = next(els)
                if maybe_caption in ('text', 'gif', 'h1', 'h2', 'h3', 'sep', 'page'):
                    pages[-1].append({
                        'type': 'gif',
                        'data_b64': gif_file_to_b64(path),
                        'alt': path,
                        'caption': '',
                    })
                    if maybe_caption == 'page':
                        pages.append([])
                    elif maybe_caption == 'sep':
                        pages[-1].append({'type': 'separator'})
                    elif maybe_caption in ('h1', 'h2', 'h3'):
                        c = next(els, '')
                        pages[-1].append({'type': maybe_caption, 'content': c})
                    elif maybe_caption == 'text':
                        c = next(els, '')
                        pages[-1].append({'type': 'text', 'content': c})
                    elif maybe_caption == 'gif':
                        p = next(els, '')
                        cap2 = ''
                        try:
                            cap2 = next(els)
                        except StopIteration:
                            pass
                        pages[-1].append({
                            'type': 'gif',
                            'data_b64': gif_file_to_b64(p),
                            'alt': p,
                            'caption': cap2,
                        })
                    continue
                else:
                    caption = maybe_caption
            except StopIteration:
                pass
            pages[-1].append({
                'type': 'gif',
                'data_b64': gif_file_to_b64(path),
                'alt': path,
                'caption': caption,
            })
        else:
            print(f'Warning: unknown element type "{token}", treating as text', file=sys.stderr)
            pages[-1].append({'type': 'text', 'content': token})

    doc = build_mpdf(args.title, args.author, pages)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(doc)

    print(f'Created: {args.output}')


if __name__ == '__main__':
    main()
