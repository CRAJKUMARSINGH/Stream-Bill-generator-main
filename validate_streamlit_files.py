"""
Validation script for Streamlit Cloud deployment files
This script checks that requirements.txt and packages.txt are properly formatted
"""
import os

def validate_requirements_file():
    """Validate that requirements.txt is properly formatted"""
    print("Checking requirements.txt...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
    
    # Check for comments or empty lines
    clean_lines = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    
    if len(clean_lines) == 0:
        print("❌ requirements.txt is empty or contains only comments")
        return False
    
    print(f"✅ requirements.txt has {len(clean_lines)} packages")
    
    # Check for common issues
    for line in clean_lines:
        if " " in line and not any(op in line for op in [">", "<", "==", ">=", "<="]):
            print(f"⚠️  Warning: Line '{line}' might have formatting issues")
    
    return True

def validate_packages_file():
    """Validate that packages.txt is properly formatted"""
    print("Checking packages.txt...")
    
    if not os.path.exists("packages.txt"):
        print("⚠️  packages.txt not found (not required for all deployments)")
        return True
    
    with open("packages.txt", "r") as f:
        lines = f.readlines()
    
    # Check for comments or empty lines
    clean_lines = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    
    if len(clean_lines) == 0:
        print("⚠️  packages.txt is empty or contains only comments")
        return True  # This is not necessarily an error
    
    print(f"✅ packages.txt has {len(clean_lines)} system packages")
    
    # Check for common issues
    for line in clean_lines:
        if " " in line:
            print(f"⚠️  Warning: Line '{line}' contains spaces")
        if line.startswith("#"):
            print(f"❌ Error: Line '{line}' is a comment (comments not allowed in packages.txt)")
            return False
    
    return True

def validate_deployment_files():
    """Validate all deployment files"""
    print("🔍 Validating Streamlit Cloud deployment files...")
    print("=" * 50)
    
    results = []
    results.append(validate_requirements_file())
    results.append(validate_packages_file())
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("🎉 All deployment files are properly formatted!")
        print("\n📋 Next steps:")
        print("1. Push changes to your GitHub repository")
        print("2. Deploy to Streamlit Cloud")
        print("3. Monitor the build logs for any issues")
        return True
    else:
        print("❌ Some deployment files have issues!")
        print("Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = validate_deployment_files()
    exit(0 if success else 1)