"""
Compatibility shim that re-exports the core PDF generator implementation.

This keeps imports like `from pdf_generator_optimized import PDFGenerator`
working while ensuring a single source of truth in `core/pdf_generator_optimized.py`.
"""

try:
    # Preferred path
    from core.pdf_generator_optimized import PDFGenerator  # type: ignore F401
except Exception as _e:
    # As a last resort, attempt relative import (for unusual execution contexts)
    from importlib import import_module as _import_module
    PDFGenerator = _import_module('core.pdf_generator_optimized').PDFGenerator  # type: ignore

__all__ = ["PDFGenerator"]