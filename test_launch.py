#!/usr/bin/env python3
"""
Test script to verify that the app can be launched correctly
"""

import sys
import os
import subprocess
import time

def test_app_launch():
    """Test that the app can be launched without errors"""
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Test that the main module can be imported
        sys.path.insert(0, project_dir)
        
        # Try to import the main module
        import app.main
        print("✓ App module can be imported successfully")
        
        # Try to import core modules
        from core.computations.bill_processor import process_bill
        print("✓ Core computation module can be imported successfully")
        
        # Try to import export modules
        from exports.renderers import generate_pdf
        print("✓ Export module can be imported successfully")
        
        # Check that template files exist
        template_files = [
            "templates/first_page.html",
            "templates/deviation_statement.html",
            "templates/extra_items.html",
            "templates/last_page.html",
            "templates/note_sheet.html"
        ]
        
        for template_file in template_files:
            if os.path.exists(template_file):
                print(f"✓ {template_file} exists")
            else:
                print(f"✗ {template_file} is missing")
                return False
        
        print("\n✅ All tests passed! The app should launch successfully.")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing app launch readiness...")
    print("=" * 50)
    
    success = test_app_launch()
    
    print("=" * 50)
    if success:
        print("✅ App is ready to launch!")
        sys.exit(0)
    else:
        print("❌ App has issues that need to be resolved.")
        sys.exit(1)