"""
Test script for Streamlit Cloud requirements
"""
import sys
import importlib

def test_requirements():
    """Test that all required packages can be imported"""
    required_packages = [
        'streamlit',
        'pandas',
        'openpyxl',
        'numpy',
        'docx',
        'jinja2',
        'xhtml2pdf',
        'reportlab',
        'bs4',  # beautifulsoup4
        'lxml',
        'num2words',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - OK")
        except ImportError as e:
            print(f"❌ {package} - MISSING ({e})")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        return False
    else:
        print("\n🎉 All required packages are available!")
        return True

if __name__ == "__main__":
    success = test_requirements()
    if success:
        print("\n✅ Requirements test passed!")
    else:
        print("\n❌ Requirements test failed!")
        sys.exit(1)