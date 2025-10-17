"""
Main Streamlit application entry point
This module provides the UI layer that interacts with the core computation and export modules.
"""
import sys
import os

# Add the parent directory to the path so we can import the original streamlit app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# For now, we'll just import and run the existing streamlit app
# This maintains backward compatibility while we transition to the modular structure
import streamlit_app

if __name__ == "__main__":
    # The streamlit_app.py already has the Streamlit code at the module level
    # so we don't need to call anything here - Streamlit will run it automatically
    pass
