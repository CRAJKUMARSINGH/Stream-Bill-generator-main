#!/usr/bin/env python3
"""
Test script to verify that all modular fixes are working correctly
"""

import sys
import os

def test_file_structure():
    """Test that the new file structure is in place"""
    print("Testing file structure...")
    
    required_files = [
        "app/main.py",
        "core/computations/bill_processor.py",
        "exports/renderers.py",
        "templates/first_page.html",
        "templates/deviation_statement.html",
        "templates/extra_items.html",
        "templates/last_page.html",
        "templates/note_sheet.html"
    ]
    
    all_good = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_good = False
    
    return all_good

def test_module_imports():
    """Test that all modules can be imported"""
    print("\nTesting module imports...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Test app module
        from app.main import main
        print("  ✅ app/main.py")
        
        # Test core module
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        print("  ✅ core/computations/bill_processor.py")
        
        # Test exports module
        from exports.renderers import generate_pdf, create_word_doc
        print("  ✅ exports/renderers.py")
        
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_modular_entry_present():
    """Test that the modular entry app/main.py is present"""
    print("\nTesting for modular entry...")
    if os.path.exists("app/main.py"):
        print("  ✅ app/main.py found")
        return True
    print("  ❌ app/main.py missing")
    return False

def main():
    """Main test function"""
    print("Stream Bill Generator - Modular Fixes Verification")
    print("=" * 50)
    
    test1 = test_file_structure()
    test2 = test_module_imports()
    test3 = test_modular_entry_present()
    
    print("\n" + "=" * 50)
    if test1 and test2 and test3:
        print("✅ All tests passed! Modular fixes are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)