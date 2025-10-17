"""
Root package initialization for Stream Bill Generator
Required for proper module imports in Streamlit Cloud and other environments
"""
import os
import sys

# Ensure the current directory is in the Python path for relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Make core modules easily accessible
__all__ = ['core', 'exports', 'app']