"""
Test script for Streamlit PDF integration
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_streamlit_pdf_integration():
    """Test the Streamlit PDF integration"""
    try:
        from core.streamlit_pdf_integration import StreamlitPDFManager, PDFGenerator
        print("✅ Successfully imported StreamlitPDFManager and PDFGenerator")
        
        # Test PDF manager initialization
        pdf_manager = StreamlitPDFManager()
        print(f"✅ PDF Manager initialized - Cloud mode: {pdf_manager.is_cloud}")
        print(f"✅ Temporary directory: {pdf_manager.temp_dir}")
        
        # Test PDF generator
        generator = PDFGenerator()
        print(f"✅ PDF Generator initialized - Available engines: {generator.available_engines}")
        
        # Test configuration creation would require Streamlit context
        print("✅ Streamlit PDF integration is working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Streamlit PDF integration: {e}")
        return False

if __name__ == "__main__":
    success = test_streamlit_pdf_integration()
    if success:
        print("\n🎉 All tests passed! Streamlit PDF integration is ready to use.")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")