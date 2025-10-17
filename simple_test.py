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

# Check if app/main.py exists (new modular structure)
if os.path.exists("app/main.py"):
    print("✅ app/main.py found (new modular structure)")
else:
    print("❌ app/main.py not found")

# Check if core/computations/bill_processor.py exists
if os.path.exists("core/computations/bill_processor.py"):
    print("✅ core/computations/bill_processor.py found")
else:
    print("❌ core/computations/bill_processor.py not found")

# Check if exports/renderers.py exists
if os.path.exists("exports/renderers.py"):
    print("✅ exports/renderers.py found")
else:
    print("❌ exports/renderers.py not found")

# Check if templates directory exists
if os.path.exists("templates"):
    print("✅ templates directory found")
else:
    print("❌ templates directory not found")

print("\nTest completed successfully!")