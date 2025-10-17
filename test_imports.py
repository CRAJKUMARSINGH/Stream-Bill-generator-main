#!/usr/bin/env python3
"""
Test script to verify that all imports work correctly
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    # Add the parent directory to the path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Test core module imports
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        print("✓ Core computation module imports successful")
        
        # Test exports module imports
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        print("✓ Exports module imports successful")
        
        # Test app module imports
        import app.main
        print("✓ App module imports successful")
        
        # Test data module imports
        from data.cache_utils import get_cache
        print("✓ Data module imports successful")
        
        # Test config module imports
        from config.settings import get_settings
        print("✓ Config module imports successful")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing module imports...")
    print("=" * 50)
    
    success = test_imports()
    
    print("=" * 50)
    if success:
        print("✓ All tests passed! Module imports are working correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Check the output above.")
        sys.exit(1)