"""
Test script to verify essential packages can be imported
"""
import sys

def test_essential_packages():
    """Test if essential packages can be imported"""
    print("Testing Essential Package Imports")
    print("=" * 35)
    
    # List of essential packages
    packages = [
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("openpyxl", "openpyxl"),
        ("pdfkit", "pdfkit"),
        ("python-docx", "docx"),
        ("num2words", "num2words"),
        ("jinja2", "jinja2"),
        ("pypdf", "pypdf"),
        ("numpy", "numpy")
    ]
    
    success_count = 0
    failed_packages = []
    
    for package_name, import_name in packages:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ {package_name} - {e}")
            failed_packages.append(package_name)
        except Exception as e:
            print(f"  ⚠️  {package_name} - {e}")
            failed_packages.append(package_name)
    
    print()
    print(f"Results: {success_count}/{len(packages)} packages imported successfully")
    
    if failed_packages:
        print(f"Failed packages: {', '.join(failed_packages)}")
        print("\nTroubleshooting tips:")
        print("1. Try installing with: pip install --user " + " ".join(failed_packages))
        print("2. For Cairo-related issues, run: python resolve_cairo_issue.py")
        print("3. Check if you have the latest pip: python -m pip install --upgrade pip")
        return False
    else:
        print("🎉 All essential packages imported successfully!")
        return True

def main():
    """Main test function"""
    print("Stream Bill Generator - Essential Package Test")
    print("=" * 45)
    print()
    
    success = test_essential_packages()
    
    if success:
        print("\n✅ Your environment is ready for Stream Bill Generator!")
        print("You can now run the application.")
    else:
        print("\n❌ Some packages are missing.")
        print("Please install the missing packages and try again.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)