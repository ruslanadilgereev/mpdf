# MPDF Format Specification v1.0

**Media PDF — Portable Document Format with Animated GIF Support**

## 1. Overview

MPDF is an open document format designed for sharing rich documents that include animated GIF images. An MPDF file is a self-contained, self-rendering document that can be displayed in any modern web browser without additional software.

**MIME Type:** `application/mpdf`
**File Extension:** `.mpdf`

## 2. Design Principles

1. **Zero-install viewing** — Any recipient can open an .mpdf file in their browser
2. **Self-contained** — All resources (text, images, styles) are embedded inline
3. **Deterministic rendering** — The stylesheet is part of the spec; documents look the same everywhere
4. **Simple authoring** — The format is human-readable and can be created by any tool or by hand

## 3. File Structure

An MPDF file is a UTF-8 encoded text file with the following structure:

### 3.1 Document Declaration

```html
<!DOCTYPE mpdf>
```

The document MUST begin with `<!DOCTYPE mpdf>`. This identifies the file as an MPDF document.

### 3.2 Root Element

```html
<html data-mpdf-version="1.0">
```

The `data-mpdf-version` attribute is REQUIRED and specifies the format version.

### 3.3 Head Section

The `<head>` section MUST contain:

| Element | Required | Description |
|---------|----------|-------------|
| `<meta charset="utf-8">` | YES | Character encoding |
| `<meta name="mpdf:title" content="...">` | YES | Document title |
| `<meta name="mpdf:author" content="...">` | NO | Author name |
| `<meta name="mpdf:created" content="YYYY-MM-DD">` | NO | Creation date (ISO 8601) |
| `<meta name="mpdf:generator" content="...">` | NO | Tool that created the file |
| `<meta name="mpdf:subject" content="...">` | NO | Document subject/topic |
| `<meta name="mpdf:keywords" content="...">` | NO | Comma-separated keywords |
| `<title>` | YES | Document title (for browser tab) |
| `<style>` | YES | The MPDF Standard Stylesheet (see Section 5) |

### 3.4 Body Section

```html
<body>
  <article class="mpdf-document">
    <section class="mpdf-page" data-page="1">
      <!-- page content -->
    </section>
  </article>
</body>
```

- The `<body>` MUST contain exactly one `<article class="mpdf-document">`
- The article contains one or more `<section class="mpdf-page">` elements
- Each page MUST have a `data-page` attribute with its 1-based page number

## 4. Content Elements

### 4.1 Heading

```html
<h1 class="mpdf-heading">Title</h1>
<h2 class="mpdf-heading">Subtitle</h2>
<h3 class="mpdf-heading">Section Heading</h3>
```

Heading levels 1–3 are supported. The `mpdf-heading` class is REQUIRED.

### 4.2 Paragraph

```html
<p class="mpdf-text">Body text goes here.</p>
```

The `mpdf-text` class is REQUIRED.

### 4.3 Animated GIF

```html
<figure class="mpdf-gif">
  <img src="data:image/gif;base64,..." alt="Description">
  <figcaption>Optional caption</figcaption>
</figure>
```

- The `mpdf-gif` class is REQUIRED
- The `src` attribute MUST be a `data:image/gif;base64,...` data URI
- The `alt` attribute is REQUIRED for accessibility
- The `<figcaption>` element is OPTIONAL

### 4.4 Static Image (Optional)

```html
<figure class="mpdf-image">
  <img src="data:image/png;base64,..." alt="Description">
  <figcaption>Optional caption</figcaption>
</figure>
```

Supports PNG and JPEG via data URIs. The `mpdf-image` class is REQUIRED.

### 4.5 Horizontal Rule

```html
<hr class="mpdf-separator">
```

## 5. Standard Stylesheet

The following stylesheet is part of the MPDF specification. Conforming documents MUST include it verbatim in their `<style>` element to ensure consistent rendering.

```css
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f0f0;font-family:Georgia,'Times New Roman',Times,serif;
  font-size:16px;line-height:1.8;color:#1a1a1a;padding:40px 20px}
.mpdf-document{max-width:800px;margin:0 auto}
.mpdf-page{background:#fff;padding:60px 70px;margin-bottom:30px;
  box-shadow:0 2px 8px rgba(0,0,0,0.12);position:relative;
  min-height:900px;page-break-after:always}
.mpdf-heading{font-family:Georgia,'Times New Roman',Times,serif;
  margin-bottom:0.6em;line-height:1.3}
h1.mpdf-heading{font-size:28px;text-align:center;margin-bottom:0.8em}
h2.mpdf-heading{font-size:22px;margin-top:1.2em}
h3.mpdf-heading{font-size:18px;margin-top:1em}
.mpdf-text{margin-bottom:1em;text-align:justify;hyphens:auto}
.mpdf-gif,.mpdf-image{margin:1.5em auto;text-align:center}
.mpdf-gif img,.mpdf-image img{max-width:100%;height:auto;
  border:1px solid #ddd;border-radius:3px}
.mpdf-gif figcaption,.mpdf-image figcaption{font-size:13px;
  color:#666;margin-top:8px;font-style:italic}
.mpdf-separator{border:none;border-top:1px solid #ccc;margin:2em 0}
@media(max-width:600px){.mpdf-page{padding:30px 25px}
  h1.mpdf-heading{font-size:22px}body{padding:10px}}
@media print{body{background:#fff;padding:0}
  .mpdf-page{box-shadow:none;padding:40px 50px;margin:0}
  .mpdf-gif img{max-height:400px}}
@media(prefers-color-scheme:dark){body{background:#1e1e1e}
  .mpdf-page{background:#2d2d2d;color:#e0e0e0;
    box-shadow:0 2px 8px rgba(0,0,0,0.4)}
  .mpdf-gif img,.mpdf-image img{border-color:#444}
  .mpdf-gif figcaption,.mpdf-image figcaption{color:#999}
  .mpdf-separator{border-color:#444}}
```

## 6. Conformance Rules

1. An MPDF file MUST begin with `<!DOCTYPE mpdf>`
2. All media MUST be embedded as base64 data URIs — no external references
3. The Standard Stylesheet MUST be included verbatim
4. No `<script>` elements are allowed — MPDF is a static document format
5. No `<link>` or external `<style>` references are allowed
6. The file MUST be valid UTF-8
7. Page numbers in `data-page` MUST be sequential starting from 1

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-18 | Initial specification |
