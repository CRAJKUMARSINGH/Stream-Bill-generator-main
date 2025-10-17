"""
Test basic functionality of the bill generator
"""
import os
import sys

def test_imports():
    """Test if we can import the main modules"""
    print("Testing imports...")
    
    try:
        import streamlit_app
        print("✓ streamlit_app imported successfully")
    except Exception as e:
        print(f"✗ Failed to import streamlit_app: {e}")
        return False
    
    try:
        import enhanced_batch_tester
        print("✓ enhanced_batch_tester imported successfully")
    except Exception as e:
        print(f"✗ Failed to import enhanced_batch_tester: {e}")
        return False
        
    try:
        import validate_and_process_tests
        print("✓ validate_and_process_tests imported successfully")
    except Exception as e:
        print(f"✗ Failed to import validate_and_process_tests: {e}")
        return False
    
    return True

def test_function_imports():
    """Test if we can import specific functions"""
    print("\nTesting function imports...")
    
    try:
        from streamlit_app import process_bill
        print("✓ process_bill function imported successfully")
    except Exception as e:
        print(f"✗ Failed to import process_bill: {e}")
        return False
    
    try:
        from enhanced_batch_tester import process_single_excel_file
        print("✓ process_single_excel_file function imported successfully")
    except Exception as e:
        print(f"✗ Failed to import process_single_excel_file: {e}")
        return False
    
    return True

def check_test_files():
    """Check if we have test files to work with"""
    print("\nChecking test files...")
    
    test_dir = "Test_Files"
    if not os.path.exists(test_dir):
        print(f"✗ {test_dir} directory not found")
        return False
    
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.xlsx')]
    print(f"✓ Found {len(test_files)} Excel files in {test_dir}")
    
    if test_files:
        print(f"  First file: {test_files[0]}")
        return True
    else:
        print("⚠ No Excel files found in Test_Files directory")
        return False

def main():
    """Main test function"""
    print("Stream Bill Generator - Basic Functionality Test")
    print("=" * 50)
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return
    
    # Test function imports
    if not test_function_imports():
        print("\n❌ Function import tests failed")
        return
    
    # Check test files
    if not check_test_files():
        print("\n❌ Test file check failed")
        return
    
    print("\n✅ All basic functionality tests passed!")
    print("\nYou should now be able to run the batch tests successfully.")

if __name__ == "__main__":
    main()