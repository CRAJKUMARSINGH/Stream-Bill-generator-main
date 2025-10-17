"""
Test script to verify Streamlit Cloud imports work correctly
"""
import os
import sys

def test_imports():
    """Test that all required imports work correctly"""
    print("Testing Streamlit Cloud imports...")
    
    # Add paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"Current sys.path: {sys.path}")
    print(f"Current directory: {current_dir}")
    print(f"Parent directory: {parent_dir}")
    
    try:
        # Test core imports
        print("Testing core.computations.bill_processor import...")
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        print("✓ core.computations.bill_processor imports successful")
        
        # Test exports imports
        print("Testing exports.renderers import...")
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        print("✓ exports.renderers imports successful")
        
        # Test streamlit PDF integration
        print("Testing core.streamlit_pdf_integration import...")
        from core.streamlit_pdf_integration import StreamlitPDFManager
        print("✓ core.streamlit_pdf_integration imports successful")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if not success:
        sys.exit(1)