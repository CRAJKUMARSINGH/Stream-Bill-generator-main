#!/usr/bin/env python3
"""
Comprehensive Streamlit App Deployability Test
This script tests if the Streamlit app is actually deployable.
"""

import sys
import os
import subprocess
import time
import threading

def test_python_environment():
    """Test if Python environment is properly set up"""
    print("1. Testing Python Environment")
    print("-" * 30)
    
    # Check Python version
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, timeout=10)
        print(f"  ✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"  ❌ Python check failed: {e}")
        return False
    
    return True

def test_required_dependencies():
    """Test if all required dependencies are available"""
    print("\n2. Testing Required Dependencies")
    print("-" * 32)
    
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

def test_module_imports():
    """Test if all application modules can be imported"""
    print("\n3. Testing Application Module Imports")
    print("-" * 38)
    
    # Add current directory to path
    sys.path.insert(0, os.getcwd())
    
    modules_to_test = [
        ("app.main", "main function"),
        ("core.computations.bill_processor", "bill processor module"),
        ("exports.renderers", "export renderers"),
        ("data.cache_utils", "cache utilities"),
        ("config.settings", "configuration settings")
    ]
    
    failed_imports = []
    for module_name, description in modules_to_test:
        try:
            # Split module and attribute
            if "." in module_name:
                parts = module_name.split(".")
                module_import = ".".join(parts[:-1])
                attr_name = parts[-1]
                module = __import__(module_import, fromlist=[attr_name])
                getattr(module, attr_name)
            else:
                __import__(module_name)
            print(f"  ✅ {description}")
        except ImportError as e:
            print(f"  ❌ {description}: {e}")
            failed_imports.append(module_name)
        except Exception as e:
            print(f"  ⚠️  {description}: {e}")
            failed_imports.append(module_name)
    
    if failed_imports:
        print(f"\n  Failed imports: {', '.join(failed_imports)}")
        return False
    
    return True

def test_template_files():
    """Test if all required template files exist and are readable"""
    print("\n4. Testing Template Files")
    print("-" * 24)
    
    required_templates = [
        "first_page.html",
        "deviation_statement.html",
        "extra_items.html",
        "last_page.html",
        "note_sheet.html"
    ]
    
    template_dir = "templates"
    if not os.path.exists(template_dir):
        print(f"  ❌ Template directory '{template_dir}' not found")
        return False
    
    missing_templates = []
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    f.read(100)  # Read first 100 chars to test readability
                print(f"  ✅ {template}")
            except Exception as e:
                print(f"  ❌ {template} (unreadable: {e})")
                missing_templates.append(template)
        else:
            print(f"  ❌ {template} (missing)")
            missing_templates.append(template)
    
    if missing_templates:
        print(f"\n  Missing/broken templates: {', '.join(missing_templates)}")
        return False
    
    return True

def test_streamlit_syntax():
    """Test if the main Streamlit app has valid Python syntax"""
    print("\n5. Testing Streamlit App Syntax")
    print("-" * 30)
    
    app_file = "app/main.py"
    if not os.path.exists(app_file):
        print(f"  ❌ {app_file} not found")
        return False
    
    try:
        result = subprocess.run([sys.executable, "-m", "py_compile", app_file],
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✅ {app_file} syntax is correct")
            return True
        else:
            print(f"  ❌ {app_file} has syntax errors:")
            print(f"    {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Syntax check failed: {e}")
        return False

def test_actual_streamlit_import():
    """Test if the Streamlit app can actually be imported without errors"""
    print("\n6. Testing Actual Streamlit App Import")
    print("-" * 38)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Try to import the main function
        from app.main import main
        print("  ✅ app/main.py imported successfully")
        
        # Try to call main function (it should not crash)
        # We'll just test if it can be called without immediate errors
        import inspect
        if inspect.isfunction(main):
            print("  ✅ main function is properly defined")
        else:
            print("  ⚠️  main is not a function")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error importing app/main.py: {e}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
        return False

def run_comprehensive_test():
    """Run all deployability tests"""
    print("Streamlit App Deployability Test")
    print("=" * 35)
    
    tests = [
        test_python_environment,
        test_required_dependencies,
        test_module_imports,
        test_template_files,
        test_streamlit_syntax,
        test_actual_streamlit_import
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
        time.sleep(0.1)  # Small delay between tests
    
    print("\n" + "=" * 35)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The Streamlit app appears to be deployable")
        print("✅ All dependencies are available")
        print("✅ All modules can be imported")
        print("✅ All templates are accessible")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print("❌ The Streamlit app may not be deployable")
        print("❌ Please check the errors above")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)