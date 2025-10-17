#!/usr/bin/env python3
"""
Simple test script to check if Python execution is working
"""
import sys
import os

print("Simple Test Script Execution")
print("=" * 30)
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")

# Check if streamlit_app.py exists
if os.path.exists("streamlit_app.py"):
    print("✅ streamlit_app.py found")
else:
    print("❌ streamlit_app.py not found")

# Check if templates directory exists
if os.path.exists("templates"):
    print("✅ templates directory found")
else:
    print("❌ templates directory not found")

print("\nTest completed successfully!")