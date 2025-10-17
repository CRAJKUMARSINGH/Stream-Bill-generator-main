# Deployment Guide

This guide explains how to deploy the Stream Bill Generator application in different environments.

## Streamlit Cloud Deployment

For deployment to Streamlit Cloud, use the basic requirements to avoid system dependency issues:

1. Use `requirements_basic.txt` instead of `requirements.txt`
2. The application will automatically fall back to basic pdfkit for PDF generation
3. All core functionality remains available

### Streamlit Cloud Configuration

In your Streamlit Cloud app settings, set these requirements:

```
streamlit
pandas
openpyxl
pdfkit
python-docx
num2words
jinja2
pypdf
numpy
```

Note: Enhanced PDF features (WeasyPrint, xhtml2pdf, Playwright) are not available in Streamlit Cloud due to system dependency restrictions.

## Local Development Deployment

For local development with enhanced features:

1. Install basic requirements:
   ```
   pip install -r requirements.txt
   ```

2. Install enhanced packages:
   ```
   install_enhanced_packages.bat
   ```

3. Run the enhanced application:
   ```
   LAUNCH_ENHANCED_APP.bat
   ```

## Docker Deployment (Recommended for Production)

For production deployment with full features, use Docker:

1. Build the Docker image:
   ```
   docker build -t stream-bill-generator .
   ```

2. Run the container:
   ```
   docker run -p 8501:8501 stream-bill-generator
   ```

## Environment Detection

The application automatically detects the deployment environment:

- In cloud environments (Streamlit Cloud), only basic PDF generation is used
- In local environments, enhanced PDF generation is enabled if packages are available
- You can force cloud mode by setting `STREAMLIT_CLOUD=true` environment variable

## PDF Generation Engines

The application supports multiple PDF generation engines with automatic fallback:

1. **WeasyPrint** (best quality, requires system dependencies)
2. **xhtml2pdf** (good compatibility, requires system dependencies)
3. **Playwright** (browser-based, requires system dependencies)
4. **pdfkit** (basic but reliable, works in cloud environments)

In cloud environments, only pdfkit is used regardless of what's installed.