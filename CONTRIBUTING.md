# Contributing to MPDF

Thanks for your interest in MPDF! Here's how you can help.

## Ways to Contribute

### Report Issues
Found a bug or have a feature request? [Open an issue](https://github.com/ruslanadilgereev/mpdf/issues).

### Improve the Specification
The MPDF spec is in `mpdf-spec.md`. Propose changes via pull request. For major changes, open an issue first to discuss.

### Build Tools
The reference implementation is in Python, but MPDF is language-agnostic. We welcome implementations in any language:
- JavaScript/TypeScript (browser-based creator)
- Rust/Go/C (CLI tools)
- Browser extensions (auto-render .mpdf files)

### Add Examples
Create interesting .mpdf documents and add them to `examples/`.

## Development Setup

```bash
# Clone
git clone https://github.com/ruslanadilgereev/mpdf.git
cd mpdf

# Install in development mode
pip install -e .

# Run validator
mpdf validate test.mpdf

# Create a demo
python create_demo.py
```

## Pull Request Guidelines

1. Run the validator against your changes: `python mpdf-validate.py examples/*.mpdf`
2. Keep changes focused — one feature/fix per PR
3. Update `CHANGELOG.md` if applicable
4. Follow existing code style

## Specification Changes

Changes to `mpdf-spec.md` require:
1. Discussion in an issue first
2. Backwards compatibility (or a version bump)
3. Updated validator to match
4. At least one example demonstrating the change
