#!/usr/bin/env python3
"""
Deployment validation script for Stream Bill Generator
This script checks if all dependencies are available for deployment.
"""

import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is sufficient"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        return False, f"Python 3.7+ required, found {version.major}.{version.minor}"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def check_module(module_name, required=True):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        return True, f"{module_name} - OK"
    except ImportError as e:
        if required:
            return False, f"{module_name} - MISSING ({str(e)})"
        else:
            return True, f"{module_name} - Optional (not installed)"

def check_file(file_path):
    """Check if a file exists"""
    if os.path.exists(file_path):
        return True, f"{file_path} - Found"
    return False, f"{file_path} - Missing"

def validate_deployment():
    """Validate deployment requirements"""
    print("Stream Bill Generator - Deployment Validation")
    print("=" * 50)
    
    # Check Python version
    version_ok, version_msg = check_python_version()
    print(f"Python Version: {version_msg}")
    if not version_ok:
        return False
    
    # Check required modules
    required_modules = [
        "streamlit",
        "pandas",
        "openpyxl",
        "pdfkit",
        "docx",
        "num2words",
        "jinja2",
        "pypdf"
    ]
    
    print("\nRequired Modules:")
    modules_ok = True
    for module in required_modules:
        module_ok, module_msg = check_module(module)
        print(f"  {module_msg}")
        if not module_ok:
            modules_ok = False
    
    # Check optional modules
    print("\nOptional Modules:")
    optional_modules = [
        "xhtml2pdf",
        "weasyprint",
        "playwright",
        "redis"
    ]
    
    for module in optional_modules:
        module_ok, module_msg = check_module(module, required=False)
        print(f"  {module_msg}")
    
    # Check required files
    print("\nRequired Files:")
    required_files = [
        "core/computations/bill_processor.py",
        "exports/renderers.py",
        "app/main.py",
        "templates/first_page.html",
        "templates/deviation_statement.html",
        "templates/extra_items.html",
        "templates/last_page.html",
        "templates/note_sheet.html"
    ]
    
    files_ok = True
    for file_path in required_files:
        file_ok, file_msg = check_file(file_path)
        print(f"  {file_msg}")
        if not file_ok:
            files_ok = False
    
    # Overall result
    print("\n" + "=" * 50)
    if modules_ok and files_ok:
        print("✅ Deployment validation PASSED")
        print("All required dependencies and files are available.")
        return True
    else:
        print("❌ Deployment validation FAILED")
        if not modules_ok:
            print("  - Missing required modules")
        if not files_ok:
            print("  - Missing required files")
        return False

if __name__ == "__main__":
    success = validate_deployment()
    sys.exit(0 if success else 1)