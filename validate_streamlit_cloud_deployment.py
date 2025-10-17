"""
Validation script for Streamlit Cloud deployment
This script checks if all requirements for Streamlit Cloud deployment are met
"""
import os
import sys
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version compatible: {}.{}.{}".format(version.major, version.minor, version.micro))
        return True
    else:
        print("❌ Python version not compatible: {}.{}.{} (requires 3.8+)".format(version.major, version.minor, version.micro))
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "app/main.py",
        "core/computations/bill_processor.py",
        "exports/renderers.py",
        "core/streamlit_pdf_integration.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_imports():
    """Check if all required imports work"""
    # Add current directory to path
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    required_imports = [
        ("core.computations.bill_processor", ["process_bill", "safe_float", "number_to_words"]),
        ("exports.renderers", ["generate_pdf", "create_word_doc", "merge_pdfs", "create_zip_archive"]),
        ("core.streamlit_pdf_integration", ["StreamlitPDFManager"])
    ]
    
    failed_imports = []
    
    for module_name, functions in required_imports:
        try:
            module = importlib.import_module(module_name)
            for function_name in functions:
                if not hasattr(module, function_name):
                    failed_imports.append(f"{module_name}.{function_name}")
            print(f"✅ {module_name} imported successfully")
        except Exception as e:
            failed_imports.append(f"{module_name}: {str(e)}")
            print(f"❌ {module_name} import failed: {str(e)}")
    
    if failed_imports:
        print("❌ Failed imports:")
        for imp in failed_imports:
            print(f"   - {imp}")
        return False
    else:
        print("✅ All imports successful")
        return True

def check_requirements():
    """Check if requirements file is properly formatted"""
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        required_packages = [
            "streamlit",
            "pandas",
            "openpyxl",
            "python-docx",
            "xhtml2pdf",
            "reportlab"
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            print("⚠️  Missing packages in requirements.txt:")
            for package in missing_packages:
                print(f"   - {package}")
        else:
            print("✅ All required packages found in requirements.txt")
        
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {str(e)}")
        return False

def main():
    """Main validation function"""
    print("=" * 60)
    print("Streamlit Cloud Deployment Validation")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Module Imports", check_imports),
        ("Requirements File", check_requirements)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\nChecking {check_name}...")
        result = check_func()
        results.append((check_name, result))
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:<20} {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 All validations passed! Ready for Streamlit Cloud deployment.")
        print("\nNext steps:")
        print("1. Push all changes to your GitHub repository")
        print("2. Go to https://share.streamlit.io/")
        print("3. Click 'New app' and connect to your GitHub repository")
        print("4. Set the main file path to 'app/main.py'")
        print("5. Deploy the app")
    else:
        print("❌ Some validations failed. Please fix the issues before deploying.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)