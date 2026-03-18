#!/usr/bin/env python3
"""MPDF command-line interface."""

import argparse
import base64
import os
import sys
import tempfile
import webbrowser

from . import MPDFDocument


def cmd_create(args):
    """Create an MPDF document from command-line arguments."""
    doc = MPDFDocument(args.title, author=args.author)
    page = doc.add_page()

    els = iter(args.elements)
    for token in els:
        if token == 'page':
            page = doc.add_page()
        elif token == 'sep':
            page.add_separator()
        elif token in ('h1', 'h2', 'h3'):
            text = next(els, '')
            page.add_heading(text, level=int(token[1]))
        elif token == 'text':
            text = next(els, '')
            page.add_text(text)
        elif token == 'gif':
            path = next(els, '')
            caption = ''
            try:
                maybe = next(els)
                if maybe in ('text', 'gif', 'h1', 'h2', 'h3', 'sep', 'page'):
                    page.add_gif(gif_path=path)
                    # Process the consumed token
                    if maybe == 'page':
                        page = doc.add_page()
                    elif maybe == 'sep':
                        page.add_separator()
                    elif maybe in ('h1', 'h2', 'h3'):
                        page.add_heading(next(els, ''), level=int(maybe[1]))
                    elif maybe == 'text':
                        page.add_text(next(els, ''))
                    elif maybe == 'gif':
                        p2 = next(els, '')
                        try:
                            c2 = next(els)
                        except StopIteration:
                            c2 = ''
                        page.add_gif(gif_path=p2, caption=c2)
                    continue
                else:
                    caption = maybe
            except StopIteration:
                pass
            page.add_gif(gif_path=path, caption=caption)
        else:
            page.add_text(token)

    doc.save(args.output)
    print(f"Created: {args.output}")


def cmd_validate(args):
    """Validate MPDF files."""
    # Import validate function inline to avoid circular dependency
    validate_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                  'mpdf-validate.py')

    # Use inline validation logic
    import re

    all_valid = True
    for filepath in args.files:
        errors = _validate(filepath)
        if errors:
            all_valid = False
            print(f"INVALID  {filepath}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"VALID    {filepath}")

    sys.exit(0 if all_valid else 1)


def _validate(filepath):
    """Validate an MPDF file. Returns list of errors."""
    import re

    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return ["File is not valid UTF-8"]
    except FileNotFoundError:
        return [f"File not found: {filepath}"]

    lines = content.strip().split('\n')

    if not lines or not lines[0].strip().startswith('<!DOCTYPE mpdf>'):
        errors.append("Missing <!DOCTYPE mpdf>")
    if 'data-mpdf-version=' not in content:
        errors.append("Missing data-mpdf-version")
    if 'name="mpdf:title"' not in content:
        errors.append("Missing mpdf:title meta tag")
    if '<title>' not in content:
        errors.append("Missing <title>")
    if '.mpdf-document' not in content or '.mpdf-page' not in content:
        errors.append("Stylesheet incomplete")
    if 'class="mpdf-document"' not in content:
        errors.append("Missing mpdf-document element")
    if 'class="mpdf-page"' not in content:
        errors.append("No pages found")
    if re.search(r'<script[\s>]', content, re.IGNORECASE):
        errors.append("Contains <script> — not allowed")
    if re.findall(r'(?:src|href)=["\']https?://', content):
        errors.append("Contains external resources")

    return errors


def cmd_view(args):
    """Open an MPDF file in the default browser."""
    filepath = os.path.abspath(args.file)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    # Create a temp .html copy so the browser renders it
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    tmp = tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8')
    tmp.write(content)
    tmp.close()

    webbrowser.open(f'file://{tmp.name}')
    print(f"Opened in browser: {filepath}")


def main():
    parser = argparse.ArgumentParser(prog='mpdf', description='MPDF — Media PDF toolkit')
    sub = parser.add_subparsers(dest='command')

    # create
    p_create = sub.add_parser('create', help='Create an MPDF document')
    p_create.add_argument('--title', '-t', required=True)
    p_create.add_argument('--author', '-a', default='')
    p_create.add_argument('-o', '--output', required=True)
    p_create.add_argument('elements', nargs='+')

    # validate
    p_validate = sub.add_parser('validate', help='Validate MPDF files')
    p_validate.add_argument('files', nargs='+')

    # view
    p_view = sub.add_parser('view', help='Open an MPDF file in the browser')
    p_view.add_argument('file')

    args = parser.parse_args()

    if args.command == 'create':
        cmd_create(args)
    elif args.command == 'validate':
        cmd_validate(args)
    elif args.command == 'view':
        cmd_view(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
