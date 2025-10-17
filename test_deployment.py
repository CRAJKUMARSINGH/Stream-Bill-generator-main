"""
Deployment Test Script
This script verifies that all components needed for Streamlit Cloud deployment work correctly
"""
import os
import sys

def test_deployment():
    """Test all components needed for Streamlit Cloud deployment"""
    print("Testing Streamlit Cloud Deployment Readiness...")
    print("=" * 50)
    
    # Test 1: Check Python path
    print("1. Checking Python path...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"   Current directory: {current_dir}")
    print(f"   Python path includes current directory: {current_dir in sys.path}")
    
    # Test 2: Test imports
    print("\n2. Testing module imports...")
    try:
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        print("   ✅ core.computations.bill_processor imports successful")
    except Exception as e:
        print(f"   ❌ core.computations.bill_processor import failed: {e}")
        return False
    
    try:
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        print("   ✅ exports.renderers imports successful")
    except Exception as e:
        print(f"   ❌ exports.renderers import failed: {e}")
        return False
    
    try:
        from core.streamlit_pdf_integration import StreamlitPDFManager
        print("   ✅ core.streamlit_pdf_integration imports successful")
    except Exception as e:
        print(f"   ❌ core.streamlit_pdf_integration import failed: {e}")
        return False
    
    # Test 3: Check requirements file
    print("\n3. Checking requirements file...")
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            required_packages = ["streamlit", "pandas", "openpyxl", "python-docx", "xhtml2pdf", "reportlab"]
            missing = [pkg for pkg in required_packages if pkg not in content]
            if missing:
                print(f"   ⚠️  Missing packages in requirements.txt: {missing}")
            else:
                print("   ✅ All required packages found in requirements.txt")
    except Exception as e:
        print(f"   ❌ Error reading requirements.txt: {e}")
        return False
    
    # Test 4: Check file structure
    print("\n4. Checking file structure...")
    required_files = [
        "streamlit_app.py",
        "core/computations/bill_processor.py",
        "exports/renderers.py",
        "core/streamlit_pdf_integration.py",
        ".streamlit/config.toml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"   ❌ Missing required files: {missing_files}")
        return False
    else:
        print("   ✅ All required files present")
    
    # Test 5: Check __init__.py files
    print("\n5. Checking package initialization files...")
    init_files = [
        "__init__.py",
        "core/__init__.py",
        "core/computations/__init__.py",
        "exports/__init__.py",
        "app/__init__.py"
    ]
    
    missing_inits = []
    for init_path in init_files:
        if not os.path.exists(init_path):
            missing_inits.append(init_path)
    
    if missing_inits:
        print(f"   ⚠️  Missing __init__.py files: {missing_inits}")
        print("       Note: These may not be required but are recommended for proper package structure")
    else:
        print("   ✅ All __init__.py files present")
    
    print("\n" + "=" * 50)
    print("🎉 Deployment readiness check completed!")
    print("All critical components are ready for Streamlit Cloud deployment.")
    return True

if __name__ == "__main__":
    success = test_deployment()
    if success:
        print("\n✅ Ready for Streamlit Cloud deployment!")
        print("\nNext steps:")
        print("1. Push all changes to your GitHub repository")
        print("2. Go to https://share.streamlit.io/")
        print("3. Create a new app with main file path: streamlit_app.py")
        print("4. Deploy and enjoy your application!")
    else:
        print("\n❌ Deployment readiness check failed!")
        print("Please fix the issues before deploying.")
        sys.exit(1)