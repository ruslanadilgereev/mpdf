#!/usr/bin/env python3
"""Generate example .mpdf files for the MPDF project."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from mpdf import MPDFDocument
from mpdf.stylesheet import MPDF_CSS

# We need the GIF generator from create_demo.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from create_demo import create_animated_gif

import base64


def create_minimal():
    """Smallest valid MPDF document."""
    doc = MPDFDocument("Minimal MPDF")
    page = doc.add_page()
    page.add_heading("Hello, MPDF!", level=1)
    page.add_text("This is the smallest valid MPDF document.")
    doc.save(os.path.join(os.path.dirname(__file__), 'minimal.mpdf'))
    print("  Created: examples/minimal.mpdf")


def create_academic_paper():
    """Academic paper with sections and a GIF figure."""
    gif_data = create_animated_gif()

    doc = MPDFDocument(
        "On the Feasibility of Animated Figures in Academic Publishing",
        author="MPDF Research Group",
        subject="Document Formats",
        keywords="MPDF, GIF, academic publishing, animated figures"
    )
    page = doc.add_page()

    page.add_heading("On the Feasibility of Animated Figures\nin Academic Publishing", level=1)

    page.add_heading("Abstract", level=2)
    page.add_text(
        "Traditional academic publishing relies on static figures to convey dynamic processes. "
        "This paper demonstrates how the MPDF format enables authors to embed animated GIF images "
        "directly into portable documents, improving the communication of temporal and sequential data "
        "without requiring external video players or internet connectivity."
    )

    page.add_heading("1. Introduction", level=2)
    page.add_text(
        "The limitations of static figures in academic papers have long been recognized. "
        "Processes such as algorithm visualizations, fluid dynamics simulations, and user interface "
        "demonstrations lose significant information when reduced to a single frame. While supplementary "
        "video materials can be provided, they require separate hosting and are often lost over time."
    )
    page.add_text(
        "MPDF addresses this gap by enabling animated GIF images to be embedded directly within "
        "the document file. The format is self-contained, requiring no external resources or "
        "specialized viewing software beyond a standard web browser."
    )

    page.add_heading("2. Methodology", level=2)
    page.add_text(
        "We designed the MPDF format around three constraints: (1) zero-install viewing, "
        "(2) complete self-containment, and (3) deterministic rendering across platforms. "
        "The format specification defines a strict document structure with a standardized stylesheet "
        "to ensure consistent visual presentation."
    )

    page.add_heading("3. Results", level=2)
    page.add_text(
        "Figure 1 demonstrates an embedded animated GIF within this MPDF document. "
        "The animation renders natively in any modern web browser without plugins or external dependencies."
    )

    page.add_gif(
        gif_bytes=gif_data,
        alt="Animated gradient bar demonstrating MPDF capabilities",
        caption="Figure 1: Animated gradient bar rendered inline within the MPDF document."
    )

    page.add_heading("4. Conclusion", level=2)
    page.add_text(
        "MPDF provides a practical solution for including animated figures in portable documents. "
        "The format's simplicity and browser-based rendering make it immediately accessible "
        "without requiring adoption of new software."
    )

    page.add_separator()
    page.add_text("MPDF v1.0 — Open Standard")

    doc.save(os.path.join(os.path.dirname(__file__), 'academic-paper.mpdf'))
    print("  Created: examples/academic-paper.mpdf")


def create_tutorial():
    """Step-by-step tutorial document."""
    gif_data = create_animated_gif()

    doc = MPDFDocument("Getting Started with MPDF", author="MPDF Project")
    page = doc.add_page()

    page.add_heading("Getting Started with MPDF", level=1)

    page.add_heading("What is MPDF?", level=2)
    page.add_text(
        "MPDF (Media PDF) is an open document format that works like PDF but supports "
        "animated GIF images. You're reading an MPDF document right now!"
    )

    page.add_heading("Step 1: Install the Tools", level=2)
    page.add_text("Install the MPDF toolkit via pip:")
    page.add_text("pip install mpdf")

    page.add_heading("Step 2: Create Your First Document", level=2)
    page.add_text("Use the command-line tool to create a document:")
    page.add_text(
        'mpdf create --title "My Document" -o my-doc.mpdf '
        'h1 "Hello World" text "This is my first MPDF document."'
    )

    page.add_heading("Step 3: Add Animated GIFs", level=2)
    page.add_text(
        "The real power of MPDF is embedding animated GIFs. Here's one right in this tutorial:"
    )

    page.add_gif(
        gif_bytes=gif_data,
        alt="Example animated GIF in tutorial",
        caption="An animated GIF embedded directly in this tutorial document."
    )

    page.add_heading("Step 4: Share Your Document", level=2)
    page.add_text(
        "Just send the .mpdf file to anyone. They open it in their browser and see "
        "your document with animated GIFs. No special software needed."
    )

    page.add_heading("Step 5: Validate", level=2)
    page.add_text(
        "Check that your document follows the MPDF specification:"
    )
    page.add_text("mpdf validate my-doc.mpdf")

    page.add_separator()
    page.add_text("Learn more at github.com/ruslanadilgereev/mpdf")

    doc.save(os.path.join(os.path.dirname(__file__), 'tutorial.mpdf'))
    print("  Created: examples/tutorial.mpdf")


if __name__ == '__main__':
    print("Generating examples...")
    create_minimal()
    create_academic_paper()
    create_tutorial()
    print("Done!")
