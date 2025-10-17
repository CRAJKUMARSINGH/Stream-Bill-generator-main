"""
Deployment Readiness Validation Script
This script validates that the application is ready for Streamlit Cloud deployment
"""
import os
import sys

def validate_deployment_readiness():
    """Validate that all requirements for Streamlit Cloud deployment are met"""
    print("🔍 Validating Streamlit Cloud Deployment Readiness...")
    print("=" * 60)
    
    # Test 1: Check requirements file
    print("1. Checking requirements.txt...")
    try:
        with open("requirements.txt", "r") as f:
            lines = f.readlines()
        
        if len(lines) >= 10:
            print("   ✅ requirements.txt exists and has sufficient packages")
            
            # Check for common problematic packages
            problematic_packages = ["weasyprint", "playwright", "cairo", "pango"]
            has_problematic = any(pkg in line.lower() for pkg in problematic_packages for line in lines)
            
            if has_problematic:
                print("   ⚠️  Warning: requirements.txt contains potentially problematic packages")
                print("      These may cause deployment issues on Streamlit Cloud")
            else:
                print("   ✅ requirements.txt does not contain known problematic packages")
        else:
            print("   ❌ requirements.txt is missing or incomplete")
            return False
    except Exception as e:
        print(f"   ❌ Error reading requirements.txt: {e}")
        return False
    
    # Test 2: Check minimal app file
    print("\n2. Checking minimal_app.py...")
    if os.path.exists("minimal_app.py"):
        print("   ✅ minimal_app.py exists")
    else:
        print("   ❌ minimal_app.py is missing")
        return False
    
    # Test 3: Check package initialization files
    print("\n3. Checking package initialization files...")
    required_init_files = [
        "__init__.py",
        "core/__init__.py",
        "core/computations/__init__.py",
        "exports/__init__.py",
        "app/__init__.py"
    ]
    
    missing_inits = []
    for init_file in required_init_files:
        if not os.path.exists(init_file):
            missing_inits.append(init_file)
    
    if missing_inits:
        print(f"   ⚠️  Missing __init__.py files: {missing_inits}")
        print("      These may not be required but are recommended for proper package structure")
    else:
        print("   ✅ All required __init__.py files present")
    
    # Test 4: Check Streamlit config
    print("\n4. Checking Streamlit configuration...")
    if os.path.exists(".streamlit/config.toml"):
        print("   ✅ .streamlit/config.toml exists")
    else:
        print("   ⚠️  .streamlit/config.toml is missing (not required but recommended)")
    
    # Test 5: Check documentation files
    print("\n5. Checking documentation files...")
    docs_files = [
        "DEPLOYMENT_TROUBLESHOOTING.md",
        "STREAMLIT_CLOUD_DEPLOYMENT_FIX.md"
    ]
    
    missing_docs = []
    for doc_file in docs_files:
        if not os.path.exists(doc_file):
            missing_docs.append(doc_file)
    
    if missing_docs:
        print(f"   ⚠️  Missing documentation files: {missing_docs}")
    else:
        print("   ✅ All documentation files present")
    
    print("\n" + "=" * 60)
    print("🎉 Deployment readiness validation completed!")
    
    print("\n📋 Recommended Deployment Steps:")
    print("1. First, try deploying minimal_app.py to test basic deployment")
    print("2. If that works, try streamlit_app.py for the full application")
    print("3. Monitor the build logs for any specific error messages")
    print("4. Refer to DEPLOYMENT_TROUBLESHOOTING.md if you encounter issues")
    
    return True

if __name__ == "__main__":
    success = validate_deployment_readiness()
    if success:
        print("\n✅ Your application is ready for Streamlit Cloud deployment!")
        print("\n🚀 Next steps:")
        print("1. Push all changes to your GitHub repository")
        print("2. Go to https://share.streamlit.io/")
        print("3. Create a new app")
        print("4. For testing: Set main file path to 'minimal_app.py'")
        print("5. For full app: Set main file path to 'streamlit_app.py'")
    else:
        print("\n❌ Deployment readiness validation failed!")
        print("Please fix the issues before deploying.")
        sys.exit(1)