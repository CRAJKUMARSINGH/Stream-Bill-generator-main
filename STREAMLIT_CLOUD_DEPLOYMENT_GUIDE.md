# Streamlit Cloud Deployment Guide

This guide provides step-by-step instructions for deploying the Stream Bill Generator to Streamlit Cloud.

## Prerequisites

1. A GitHub account
2. A fork or clone of the repository: https://github.com/CRAJKUMARSINGH/Stream-Bill-generator-main
3. All the fixes in this repository have been applied

## Deployment Steps

### 1. Repository Preparation

Ensure your repository contains all the necessary files:
- `app/main.py` (main application file)
- `core/` directory with all computation modules
- `exports/` directory with rendering modules
- `requirements.txt` with all dependencies
- `.streamlit/config.toml` for configuration
- All necessary `__init__.py` files

### 2. Streamlit Cloud Deployment

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the following configuration:
   - **Branch**: `main`
   - **Main file path**: `app/main.py`
   - **App URL**: Choose your preferred URL slug
6. Click "Deploy"

### 3. Configuration Settings

The application uses the following configuration in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
enableCORS = false
enableXsrfProtection = false

[client]
showErrorDetails = true

[runner]
magicEnabled = true
fastReruns = true
```

### 4. Environment Variables

If you need to set environment variables, you can do so in the Streamlit Cloud dashboard:
1. Go to your app settings
2. Navigate to "Secrets"
3. Add your variables in the `.streamlit/secrets.toml` format

### 5. Requirements

The application requires the following dependencies (from `requirements.txt`):

```
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
numpy>=1.24.0
python-docx>=0.8.11
jinja2>=3.1.2
xhtml2pdf>=0.2.11
reportlab>=4.0.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
num2words>=0.5.12
Pillow>=10.0.0
```

## Troubleshooting Common Issues

### Import Errors

If you encounter import errors like:
```
ModuleNotFoundError: No module named 'core.computations.bill_processor'
```

**Solution**: 
1. Ensure all `__init__.py` files are present
2. Verify the main file path is set to `app/main.py`
3. Check that the repository structure matches the expected layout

### Missing Dependencies

If modules are not found, ensure `requirements.txt` is properly formatted and contains all necessary packages.

### File Path Issues

The application is designed to work with relative paths. All file operations use paths relative to the application directory.

## Verification

After deployment, verify that:

1. ✅ The app loads without errors
2. ✅ All modules import correctly
3. ✅ File upload functionality works
4. ✅ Document generation completes successfully
5. ✅ Download buttons function properly

## Updating the Deployment

To update your deployed app:

1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically redeploy
3. Monitor the build logs for any issues

## Support

For additional help with deployment:

1. Check the build logs in the Streamlit Cloud dashboard
2. Verify all files are in the correct locations
3. Ensure `requirements.txt` contains all necessary dependencies
4. Confirm the main file path is set to `app/main.py`

## Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Components Documentation](https://docs.streamlit.io/library/components)
- [Python Package Management](https://packaging.python.org/tutorials/managing-dependencies/)