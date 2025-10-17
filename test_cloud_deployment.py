#!/usr/bin/env python3
"""
Test script to verify cloud deployment configuration
"""

import os
import sys
import tempfile

def test_basic_requirements():
    """Test that basic requirements can be imported"""
    required_packages = [
        'streamlit',
        'pandas',
        'openpyxl',
        'pdfkit',
        'docx',
        'num2words',
        'jinja2',
        'pypdf',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'docx':
                import docx
            elif package == 'pypdf':
                from pypdf import PdfReader
            else:
                __import__(package)
            print(f"✓ {package} - OK")
        except ImportError as e:
            print(f"✗ {package} - MISSING ({str(e)})")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def test_environment_detection():
    """Test environment detection"""
    # Simulate cloud environment
    os.environ['STREAMLIT_CLOUD'] = 'true'
    
    try:
        from enhanced_pdf_generator import EnhancedPDFGenerator, IN_CLOUD_ENV
        print(f"Cloud environment detection: {IN_CLOUD_ENV}")
        
        if IN_CLOUD_ENV:
            print("✓ Cloud environment correctly detected")
            return True
        else:
            print("✗ Cloud environment not detected")
            return False
    except Exception as e:
        print(f"✗ Failed to import enhanced_pdf_generator: {str(e)}")
        return False

def test_pdf_generation():
    """Test basic PDF generation"""
    try:
        # Test data
        sample_data = {
            "header": [["Agreement No.", "123/2024"]],
            "items": [
                {"unit": "M", "quantity": "100", "serial_no": "1", "description": "Sample Item", "rate": "50", "amount": "5000", "remark": "Test"}
            ],
            "totals": {
                "grand_total": "5000",
                "premium": {"percent": 0.05, "amount": "250"},
                "payable": "5250"
            }
        }
        
        # Test with cloud environment
        os.environ['STREAMLIT_CLOUD'] = 'true'
        
        from enhanced_pdf_generator import generate_pdf_with_fallback
        
        tmp_path = tempfile.mktemp(suffix='.pdf')
        
        try:
            engine_used = generate_pdf_with_fallback("first_page", sample_data, tmp_path)
            print(f"✓ PDF generation successful using {engine_used}")
            os.unlink(tmp_path)
            return True
        except Exception as e:
            print(f"✗ PDF generation failed: {str(e)}")
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            return False
            
    except Exception as e:
        print(f"✗ PDF generation test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing cloud deployment configuration...")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing basic requirements:")
    if not test_basic_requirements():
        success = False
    
    print("\n2. Testing environment detection:")
    if not test_environment_detection():
        success = False
    
    print("\n3. Testing PDF generation:")
    if not test_pdf_generation():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! Ready for cloud deployment.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Check the output above.")
        sys.exit(1)