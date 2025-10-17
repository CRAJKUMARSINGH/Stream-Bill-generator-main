# Streamlit Cloud Deployment Troubleshooting Guide

This guide helps resolve common issues when deploying the Stream Bill Generator to Streamlit Cloud.

## Common Deployment Errors and Solutions

### 1. Requirements Installation Error

**Error Message**: "Error installing requirements"

**Causes and Solutions**:

1. **Incompatible Package Versions**
   - Some packages may have version conflicts in the Streamlit Cloud environment
   - Solution: Use more flexible version specifications in requirements.txt

2. **System Dependencies**
   - Some packages require system-level dependencies not available in Streamlit Cloud
   - Solution: Remove or replace packages that require system dependencies

3. **Hidden Characters or Encoding Issues**
   - requirements.txt may contain hidden characters or incorrect encoding
   - Solution: Create a clean requirements.txt file with UTF-8 encoding

### 2. Import Errors

**Error Message**: "ModuleNotFoundError: No module named 'core.computations.bill_processor'"

**Causes and Solutions**:

1. **Incorrect File Structure**
   - Missing or improperly configured `__init__.py` files
   - Solution: Ensure all directories have proper `__init__.py` files

2. **Python Path Issues**
   - Streamlit Cloud has different Python path handling
   - Solution: Use relative imports or explicit path configuration

### 3. Memory or Performance Issues

**Error Message**: "Application exceeded memory limits" or "Timeout during deployment"

**Causes and Solutions**:

1. **Large Dependencies**
   - Some packages are too large for Streamlit Cloud's free tier
   - Solution: Use minimal dependencies or upgrade to a paid plan

2. **Complex Initialization**
   - Heavy initialization code can cause timeouts
   - Solution: Move heavy operations inside functions, not at module level

## Testing Deployment Locally

Before deploying to Streamlit Cloud, test locally:

```bash
# Create a virtual environment
python -m venv streamlit_env
source streamlit_env/bin/activate  # On Windows: streamlit_env\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the app
streamlit run minimal_app.py
```

## Streamlit Cloud Specific Recommendations

### 1. Use Minimal Dependencies
Start with the minimal_app.py and requirements.txt to ensure basic deployment works.

### 2. Check Build Logs
Always check the build logs in the Streamlit Cloud dashboard for specific error messages.

### 3. Use Correct File Paths
Ensure all file paths are relative and work in the Streamlit Cloud environment.

### 4. Handle Imports Carefully
Use try/except blocks for imports that might fail in different environments.

## Step-by-Step Deployment Process

### Step 1: Test with Minimal Version
1. Deploy minimal_app.py first to verify the basic setup works
2. Use the minimal requirements.txt file

### Step 2: Gradually Add Features
1. Once minimal deployment works, gradually add more features
2. Add packages one by one to identify problematic dependencies

### Step 3: Monitor Resource Usage
1. Keep an eye on memory usage
2. Optimize code to reduce resource consumption

## Alternative Deployment Options

If Streamlit Cloud continues to have issues:

1. **Heroku**: Supports more dependencies but requires more setup
2. **Railway**: Similar to Heroku with a simpler interface
3. **Google Cloud Run**: More complex but very flexible
4. **Docker Deployment**: Package the app in a container for maximum compatibility

## Contact Support

If you continue to experience issues:
1. Check the Streamlit Community Forums: https://discuss.streamlit.io/
2. File an issue on the GitHub repository
3. Contact Streamlit support through their website

## Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Python Package Compatibility Checker](https://libraries.io/)
- [Streamlit Components Gallery](https://streamlit.io/components)