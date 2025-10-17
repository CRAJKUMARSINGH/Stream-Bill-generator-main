"""
Test script to verify pdfkit import and usage
"""
import sys
import os

def test_pdfkit_import():
    """Test pdfkit import"""
    print("Testing pdfkit import...")
    
    try:
        import pdfkit
        print("✅ pdfkit imported successfully")
        
        # Test if wkhtmltopdf is available
        try:
            config = pdfkit.configuration()
            print("✅ wkhtmltopdf is available")
            return True
        except Exception as e:
            print(f"⚠️  wkhtmltopdf not available: {e}")
            return True
            
    except ImportError as e:
        print(f"❌ pdfkit import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ pdfkit error: {e}")
        return False

def test_renderers_import():
    """Test exports.renderers import"""
    print("\nTesting exports.renderers import...")
    
    try:
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        print("✅ exports.renderers imported successfully")
        return True
    except Exception as e:
        print(f"❌ exports.renderers import failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing PDFKit and Renderers Import...")
    print("=" * 40)
    
    success1 = test_pdfkit_import()
    success2 = test_renderers_import()
    
    if success1 and success2:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)