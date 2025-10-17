#!/usr/bin/env python3
"""
Test script to verify the modular app structure
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    try:
        # Add the parent directory to the path
        sys.path.append(os.path.join(os.path.dirname(__file__)))
        
        # Test core module imports
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        print("✓ Core computation module imports successful")
        
        # Test exports module imports
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        print("✓ Exports module imports successful")
        
        # Test app module imports
        from app.main import main
        print("✓ App module imports successful")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {str(e)}")
        return False

def test_module_structure():
    """Test that the module structure is correct"""
    expected_files = [
        "core/computations/bill_processor.py",
        "exports/renderers.py",
        "app/main.py",
        "config/settings.py",
        "data/cache_utils.py"
    ]
    
    missing_files = []
    for file_path in expected_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
            print(f"✗ Missing file: {file_path}")
        else:
            print(f"✓ Found file: {file_path}")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    print("Testing modular app structure...")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing module imports:")
    if not test_imports():
        success = False
    
    print("\n2. Testing module structure:")
    if not test_module_structure():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! Modular app structure is correct.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Check the output above.")
        sys.exit(1)