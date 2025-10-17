"""
Comprehensive Streamlit Deployment Test Script (Updated for Modular Structure)
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
    if not os.path.exists("app/main.py"):
        print("  ❌ app/main.py not found in current directory")
        print("  Looking for new modular structure...")
        return False
    print("  ✅ app/main.py found (new modular structure)")
    
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

def test_import_modular_app():
    """Test if the new modular app can be imported without errors"""
    print("\n5. Testing Modular App Import")
    print("-" * 30)
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        # Try to import the app modules
        from app.main import main
        print("  ✅ app/main.py imported successfully")
        
        # Try to import core modules
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        print("  ✅ core/computations/bill_processor.py imported successfully")
        
        # Try to import export modules
        from exports.renderers import generate_pdf, create_word_doc
        print("  ✅ exports/renderers.py imported successfully")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error importing modular app: {e}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
        return False

def run_modular_syntax_check():
    """Run Python syntax check on modular app files"""
    print("\n6. Checking Python Syntax")
    print("-" * 24)
    
    files_to_check = [
        "app/main.py",
        "core/computations/bill_processor.py",
        "exports/renderers.py"
    ]
    
    all_passed = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                result = subprocess.run([sys.executable, "-m", "py_compile", file_path],
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"  ✅ {file_path} syntax is correct")
                else:
                    print(f"  ❌ {file_path} has syntax errors:")
                    print(f"    {result.stderr}")
                    all_passed = False
            except Exception as e:
                print(f"  ❌ Syntax check for {file_path} failed: {e}")
                all_passed = False
        else:
            print(f"  ❌ {file_path} not found")
            all_passed = False
    
    return all_passed

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
                print(f"  ❌ {template_name} failed to load: {e}")
                return False
                
        return True
    except Exception as e:
        print(f"  ❌ Jinja2 template test failed: {e}")
        return False

def print_deployment_instructions():
    """Print deployment instructions"""
    print("\n8. Deployment Instructions")
    print("-" * 25)
    print("To run the Streamlit app:")
    print("  streamlit run app/main.py --server.port 8503")
    print("\nOr use the provided launch scripts:")
    print("  🚀_LAUNCH_APP.bat          (Basic version)")
    print("  LAUNCH_ENHANCED_APP.bat    (Enhanced version)")
    print("  LAUNCH_STREAMLIT_APP.bat   (Modular version)")
    print("\nThe app will be available at: http://localhost:8503")

def run_all_tests():
    """Run all deployment tests"""
    print("Streamlit Deployment Test Suite (Modular Version)")
    print("=" * 50)
    
    tests = [
        check_python_environment,
        check_dependencies,
        check_template_files,
        check_wkhtmltopdf,
        test_import_modular_app,
        run_modular_syntax_check,
        test_jinja2_templates
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed! The app is ready for deployment.")
        print_deployment_instructions()
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)