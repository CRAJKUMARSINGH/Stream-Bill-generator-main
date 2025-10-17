"""
Verification script for Streamlit Cloud deployment setup
"""
import os
import sys

def verify_files():
    """Verify that required files exist"""
    required_files = [
        'requirements_streamlit_cloud.txt',
        'packages.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - FOUND")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def verify_requirements_content():
    """Verify requirements file content"""
    try:
        with open('requirements_streamlit_cloud.txt', 'r') as f:
            content = f.read()
        
        # Check that WeasyPrint is commented out
        if '# weasyprint>=60.0' in content:
            print("✅ WeasyPrint is commented out for Streamlit Cloud compatibility")
        else:
            print("⚠️  Check if WeasyPrint is properly commented out for Streamlit Cloud")
        
        # Check for required packages
        required_packages = [
            'streamlit>=1.28.0',
            'pandas>=2.0.0',
            'reportlab>=4.0.0',
            'xhtml2pdf>=0.2.11'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package in content:
                print(f"✅ {package} - FOUND")
            else:
                print(f"❌ {package} - MISSING")
                missing_packages.append(package)
        
        return len(missing_packages) == 0
    except Exception as e:
        print(f"❌ Error reading requirements file: {e}")
        return False

def verify_packages_content():
    """Verify packages file content"""
    try:
        with open('packages.txt', 'r') as f:
            content = f.read()
        
        # Check for required system packages
        required_packages = [
            'libpango-1.0-0',
            'libcairo2',
            'libffi-dev',
            'fontconfig'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package in content:
                print(f"✅ {package} - FOUND")
            else:
                print(f"❌ {package} - MISSING")
                missing_packages.append(package)
        
        return len(missing_packages) == 0
    except Exception as e:
        print(f"❌ Error reading packages file: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 Verifying Streamlit Cloud deployment setup...\n")
    
    # Verify files exist
    print("📁 Checking required files:")
    files_ok = verify_files()
    print()
    
    # Verify requirements content
    print("📋 Checking requirements file content:")
    requirements_ok = verify_requirements_content()
    print()
    
    # Verify packages content
    print("📦 Checking packages file content:")
    packages_ok = verify_packages_content()
    print()
    
    # Final result
    if files_ok and requirements_ok and packages_ok:
        print("🎉 All checks passed! Ready for Streamlit Cloud deployment.")
        return True
    else:
        print("❌ Some checks failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)