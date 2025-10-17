"""
Test script for enhanced PDF generation
"""
import os
import sys

def test_enhanced_pdf_generation():
    """Test enhanced PDF generation capabilities"""
    print("Testing Enhanced PDF Generation...")
    print("=" * 40)
    
    # Try to import enhanced PDF generator
    try:
        from enhanced_pdf_generator import EnhancedPDFGenerator, generate_pdf_with_fallback
        print("✅ Enhanced PDF Generator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Enhanced PDF Generator: {e}")
        return False
    
    # Test data
    test_data = {
        "header": [["Agreement No.", "TEST/2024/001"]],
        "items": [
            {
                "unit": "M", 
                "quantity": "100.00", 
                "serial_no": "1", 
                "description": "Test Item Description", 
                "rate": "50.00", 
                "amount": "5000.00", 
                "remark": "Test Remark"
            }
        ],
        "totals": {
            "grand_total": "5000.00",
            "premium": {"percent": 0.05, "amount": "250.00"},
            "payable": "5250.00"
        }
    }
    
    # Test generator initialization
    try:
        generator = EnhancedPDFGenerator()
        print("✅ EnhancedPDFGenerator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize EnhancedPDFGenerator: {e}")
        return False
    
    # Test available engines
    print(f"Available engines: {generator.engines}")
    
    # Test PDF generation with fallback
    output_file = "test_enhanced_output.pdf"
    try:
        engine_used = generate_pdf_with_fallback("first_page", test_data, output_file)
        print(f"✅ PDF generated successfully using {engine_used}")
        
        # Check if file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ Output file created: {output_file} ({file_size} bytes)")
            # Clean up test file
            os.remove(output_file)
            print("✅ Test file cleaned up")
        else:
            print("❌ Output file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Failed to generate PDF: {e}")
        return False
    
    print("\n🎉 All tests passed! Enhanced PDF generation is working correctly.")
    return True

if __name__ == "__main__":
    success = test_enhanced_pdf_generation()
    sys.exit(0 if success else 1)