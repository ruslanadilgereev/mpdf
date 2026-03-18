# MPDF — Media PDF

**An open document format like PDF, but with animated GIF support.**

Send someone an `.mpdf` file, they open it in their browser — boom, a paper with animated GIFs. No viewer to install, no tools, nothing.

## How it works

1. Create an `.mpdf` document (with the reference tool or by hand)
2. Send the file to anyone
3. They open it in their browser
4. Done — paper layout with animated GIFs

## Quick Start

**Create a demo document:**

```bash
python create_demo.py
```

This generates `test.mpdf` — open it in your browser to see it in action.

**Create your own document:**

```bash
python mpdf-create.py --title "My Paper" --author "Your Name" -o paper.mpdf \
    h1 "My Research Paper" \
    text "Introduction paragraph..." \
    gif figure1.gif "Figure 1: Results" \
    text "As shown in Figure 1..."
```

**First-time setup (Windows):**

Double-click `register-mpdf.reg` to associate `.mpdf` files with your browser. After that, you can open `.mpdf` files with a double-click.

## Format

MPDF is a self-rendering, self-contained document format. Every `.mpdf` file includes its own stylesheet and all media (GIFs) embedded as base64 — one file, no dependencies.

What makes it a standard (not just HTML):

- `<!DOCTYPE mpdf>` — own doctype
- `data-mpdf-version` — versioned format
- `mpdf:` meta tags — standardized metadata
- `mpdf-*` CSS classes — defined document structure
- Standard stylesheet — deterministic rendering everywhere

See the full [Format Specification](mpdf-spec.md).

## Project Structure

```
mpdf-spec.md        Format specification v1.0
mpdf-create.py      Reference tool for creating .mpdf files
create_demo.py      Generates test.mpdf with a demo animated GIF
register-mpdf.reg   Windows file type registration (one-time setup)
```

## License

MIT
