"""
Stream Bill Generator - Root Package Initialization
This file ensures proper module imports across all deployment environments
"""
import os
import sys

# Get the absolute path to the root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure the root directory is in Python path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Version information
__version__ = "2.0.0"
__author__ = "CRAJKUMARSINGH"
__description__ = "Infrastructure Bill Generator for Government Statutory Formats"

# Make core modules easily accessible
__all__ = ['core', 'exports', 'app']