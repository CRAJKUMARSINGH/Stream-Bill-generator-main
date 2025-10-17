"""
Diagnostic script to check what's happening with batch tests
"""
import os
import sys
import traceback

def diagnose_environment():
    """Diagnose the Python environment"""
    print("=== Environment Diagnosis ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    print()

def check_files():
    """Check if required files exist"""
    print("=== File Check ===")
    required_files = [
        "streamlit_app.py",
        "enhanced_batch_tester.py",
        "validate_and_process_tests.py",
        "requirements.txt"
    ]
    
    for file in required_files:
        exists = os.path.exists(file)
        print(f"{'✓' if exists else '✗'} {file}: {'Found' if exists else 'Missing'}")
    
    print()

def check_test_files():
    """Check test files"""
    print("=== Test Files Check ===")
    test_dir = "Test_Files"
    if os.path.exists(test_dir):
        files = os.listdir(test_dir)
        print(f"Found {len(files)} files in {test_dir}:")
        for file in files[:5]:  # Show first 5 files
            print(f"  - {file}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more files")
    else:
        print(f"✗ {test_dir} directory not found")
    print()

def check_dependencies():
    """Check if dependencies can be imported"""
    print("=== Dependency Check ===")
    dependencies = [
        "streamlit",
        "pandas",
        "numpy",
        "jinja2",
        "pdfkit",
        "docx",
        "num2words",
        "pypdf"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep}: Available")
        except ImportError as e:
            print(f"✗ {dep}: Not available - {e}")
        except Exception as e:
            print(f"✗ {dep}: Error - {e}")
    print()

def test_simple_function():
    """Test a simple function from one of our modules"""
    print("=== Function Test ===")
    try:
        from validate_and_process_tests import validate_excel_file
        print("✓ validate_excel_file function imported successfully")
    except Exception as e:
        print(f"✗ Failed to import validate_excel_file: {e}")
        traceback.print_exc()
    print()

def main():
    """Main diagnostic function"""
    print("Stream Bill Generator - Diagnostic Tool")
    print("=" * 40)
    print()
    
    diagnose_environment()
    check_files()
    check_test_files()
    check_dependencies()
    test_simple_function()
    
    print("=== Diagnostic Complete ===")
    print("If all checks passed, try running the batch test again.")

if __name__ == "__main__":
    main()