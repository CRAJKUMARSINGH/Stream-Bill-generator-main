"""
Comprehensive Streamlit Deployment Test Script
"""
import subprocess
import sys
import os
import time
import threading
import requests

def check_python_environment():
    """Check if Python environment is properly set up"""
    print("1. Checking Python Environment")
    print("-" * 30)
    
    # Check Python version
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, timeout=10)
        print(f"  ✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"  ❌ Python check failed: {e}")
        return False
    
    # Check if in correct directory
    if not os.path.exists("streamlit_app.py"):
        print("  ❌ streamlit_app.py not found in current directory")
        return False
    print("  ✅ streamlit_app.py found")
    
    # Check templates directory
    if not os.path.exists("templates"):
        print("  ❌ templates directory not found")
        return False
    print("  ✅ templates directory found")
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n2. Checking Dependencies")
    print("-" * 20)
    
    required_packages = [
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("pdfkit", "pdfkit"),
        ("python-docx", "docx"),
        ("num2words", "num2words"),
        ("jinja2", "jinja2"),
        ("pypdf", "pypdf"),
        ("numpy", "numpy")
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} (missing)")
            missing_packages.append(package_name)
        except Exception as e:
            print(f"  ⚠️  {package_name} (error: {e})")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n  Missing packages: {', '.join(missing_packages)}")
        return False
    
    return True

def check_template_files():
    """Check if all required template files exist"""
    print("\n3. Checking Template Files")
    print("-" * 22)
    
    required_templates = [
        "first_page.html",
        "deviation_statement.html",
        "extra_items.html",
        "last_page.html",
        "note_sheet.html"
    ]
    
    missing_templates = []
    for template in required_templates:
        template_path = os.path.join("templates", template)
        if os.path.exists(template_path):
            print(f"  ✅ {template}")
        else:
            print(f"  ❌ {template} (missing)")
            missing_templates.append(template)
    
    if missing_templates:
        print(f"\n  Missing templates: {', '.join(missing_templates)}")
        return False
    
    return True

def check_wkhtmltopdf():
    """Check if wkhtmltopdf is properly installed"""
    print("\n4. Checking wkhtmltopdf")
    print("-" * 22)
    
    # Check common paths
    common_paths = [
        r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
        r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
    ]
    
    wkhtmltopdf_found = False
    for path in common_paths:
        if os.path.exists(path):
            print(f"  ✅ wkhtmltopdf found at: {path}")
            wkhtmltopdf_found = True
            break
    
    if not wkhtmltopdf_found:
        # Try to check if it's in PATH
        try:
            result = subprocess.run(["wkhtmltopdf", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"  ✅ wkhtmltopdf found in PATH: {result.stdout.strip()}")
                wkhtmltopdf_found = True
            else:
                print("  ❌ wkhtmltopdf not found in PATH")
        except FileNotFoundError:
            print("  ❌ wkhtmltopdf not found in PATH")
        except Exception as e:
            print(f"  ⚠️  Error checking wkhtmltopdf: {e}")
    
    return wkhtmltopdf_found

def test_import_streamlit_app():
    """Test if streamlit_app.py can be imported without errors"""
    print("\n5. Testing Streamlit App Import")
    print("-" * 30)
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        # Try to import the app
        import streamlit_app
        print("  ✅ streamlit_app.py imported successfully")
        
        # Try to access key functions
        if hasattr(streamlit_app, 'process_bill'):
            print("  ✅ process_bill function available")
        else:
            print("  ⚠️  process_bill function not found")
            
        if hasattr(streamlit_app, 'generate_pdf'):
            print("  ✅ generate_pdf function available")
        else:
            print("  ⚠️  generate_pdf function not found")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error importing streamlit_app.py: {e}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
        return False

def run_streamlit_syntax_check():
    """Run Python syntax check on streamlit_app.py"""
    print("\n6. Checking Python Syntax")
    print("-" * 24)
    
    try:
        result = subprocess.run([sys.executable, "-m", "py_compile", "streamlit_app.py"],
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("  ✅ streamlit_app.py syntax is correct")
            return True
        else:
            print("  ❌ streamlit_app.py has syntax errors:")
            print(f"    {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Syntax check failed: {e}")
        return False

def test_jinja2_templates():
    """Test if Jinja2 templates can be loaded"""
    print("\n7. Testing Jinja2 Templates")
    print("-" * 25)
    
    try:
        from jinja2 import Environment, FileSystemLoader
        import os
        
        # Set up Jinja2 environment
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(template_dir), cache_size=0)
        
        # Test loading each template
        templates = ["first_page.html", "deviation_statement.html", "extra_items.html", 
                    "last_page.html", "note_sheet.html"]
        
        for template_name in templates:
            try:
                template = env.get_template(template_name)
                print(f"  ✅ {template_name} loaded successfully")
            except Exception as e:
                print(f"  ❌ Error loading {template_name}: {e}")
                return False
        
        print("  ✅ All templates loaded successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ Jinja2 template test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide a comprehensive report"""
    print("STREAMLIT APP DEPLOYABILITY TEST")
    print("=" * 35)
    print()
    
    # Run all tests
    tests = [
        ("Python Environment", check_python_environment),
        ("Dependencies", check_dependencies),
        ("Template Files", check_template_files),
        ("wkhtmltopdf", check_wkhtmltopdf),
        ("App Import", test_import_streamlit_app),
        ("Syntax Check", run_streamlit_syntax_check),
        ("Jinja2 Templates", test_jinja2_templates)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 35)
    print("DEPLOYABILITY TEST SUMMARY")
    print("=" * 35)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your Streamlit app is ready for deployment!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Issues found that need to be addressed:")
        for test_name, result in results:
            if not result:
                print(f"  - {test_name}")
        return False

def main():
    """Main function"""
    success = run_comprehensive_test()
    
    if success:
        print("\n✅ You can now run your Streamlit app with:")
        print("   streamlit run streamlit_app.py --server.port 8503")
    else:
        print("\n❌ Please fix the issues above before deploying.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)