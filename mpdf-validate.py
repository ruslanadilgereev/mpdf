#!/usr/bin/env python3
"""
mpdf-validate — Validates .mpdf files against the MPDF v1.0 specification.

Usage:
  python mpdf-validate.py test.mpdf
  python mpdf-validate.py file1.mpdf file2.mpdf ...

Exit codes:
  0 — all files valid
  1 — one or more files invalid
"""

import re
import sys


def validate_mpdf(filepath):
    """Validate an MPDF file. Returns a list of error strings (empty = valid)."""
    errors = []

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return [f"File is not valid UTF-8"]
    except FileNotFoundError:
        return [f"File not found: {filepath}"]
    except OSError as e:
        return [f"Cannot read file: {e}"]

    lines = content.strip().split('\n')

    # 1. DOCTYPE check
    if not lines or not lines[0].strip().startswith('<!DOCTYPE mpdf>'):
        errors.append("Missing or incorrect DOCTYPE — must begin with <!DOCTYPE mpdf>")

    # 2. Version attribute
    if 'data-mpdf-version=' not in content:
        errors.append("Missing data-mpdf-version attribute on <html> element")
    else:
        match = re.search(r'data-mpdf-version="([^"]*)"', content)
        if not match:
            errors.append("data-mpdf-version attribute has no value")

    # 3. Required meta tags
    if '<meta charset="utf-8">' not in content and "<meta charset='utf-8'>" not in content:
        errors.append("Missing <meta charset=\"utf-8\">")

    if 'name="mpdf:title"' not in content and "name='mpdf:title'" not in content:
        errors.append("Missing required <meta name=\"mpdf:title\"> tag")

    # 4. Title element
    if '<title>' not in content:
        errors.append("Missing <title> element")

    # 5. Style element with stylesheet
    if '<style>' not in content and '<style ' not in content:
        errors.append("Missing <style> element — must include the MPDF Standard Stylesheet")
    else:
        if '.mpdf-document' not in content or '.mpdf-page' not in content:
            errors.append("Standard Stylesheet appears incomplete — missing .mpdf-document or .mpdf-page rules")

    # 6. Document structure
    if 'class="mpdf-document"' not in content:
        errors.append("Missing <article class=\"mpdf-document\"> element")

    if 'class="mpdf-page"' not in content:
        errors.append("Missing <section class=\"mpdf-page\"> elements — document has no pages")

    # 7. Page numbering
    page_numbers = [int(m) for m in re.findall(r'data-page="(\d+)"', content)]
    if page_numbers:
        expected = list(range(1, len(page_numbers) + 1))
        if page_numbers != expected:
            errors.append(f"Page numbering is not sequential — found {page_numbers}, expected {expected}")
    elif 'class="mpdf-page"' in content:
        errors.append("Pages are missing data-page attributes")

    # 8. No script tags
    if re.search(r'<script[\s>]', content, re.IGNORECASE):
        errors.append("Contains <script> elements — not allowed in MPDF (static document format)")

    # 9. No external resources
    external_refs = re.findall(r'(?:src|href)=["\']https?://[^"\']+["\']', content)
    if external_refs:
        errors.append(f"Contains external resource references — all resources must be inline: {external_refs[:3]}")

    # 10. No external stylesheets or link tags
    if re.search(r'<link\s+[^>]*rel=["\']stylesheet["\']', content, re.IGNORECASE):
        errors.append("Contains external <link> stylesheet — not allowed")

    # 11. GIF images must be data URIs
    img_srcs = re.findall(r'<img\s+[^>]*src="([^"]*)"', content)
    for src in img_srcs:
        if not src.startswith('data:'):
            errors.append(f"Image src is not a data URI: {src[:80]}...")

    # 12. GIF figures must have alt text
    gif_imgs = re.findall(r'class="mpdf-gif">\s*<img\s+([^>]*?)>', content, re.DOTALL)
    for img_attrs in gif_imgs:
        if 'alt=' not in img_attrs:
            errors.append("GIF image missing alt attribute (required for accessibility)")

    # 13. Content element classes
    headings_without_class = re.findall(r'<h[123]\s*>', content)
    if headings_without_class:
        errors.append(f"Found {len(headings_without_class)} heading(s) without mpdf-heading class")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python mpdf-validate.py <file.mpdf> [file2.mpdf ...]")
        sys.exit(1)

    all_valid = True

    for filepath in sys.argv[1:]:
        errors = validate_mpdf(filepath)

        if errors:
            all_valid = False
            print(f"INVALID  {filepath}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"VALID    {filepath}")

    sys.exit(0 if all_valid else 1)


if __name__ == '__main__':
    main()
