# 📋 Stream Bill Generator Installation Guide

## 🎯 Overview

This guide provides step-by-step instructions for installing and setting up the Stream Bill Generator with PDF optimization features.

## 🛠️ System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 4 GB RAM
- 1 GB available disk space
- Internet connection for package installation

### Recommended Requirements
- Python 3.9 or higher
- 8 GB RAM
- 2 GB available disk space
- Modern web browser

## 📦 Installation Options

### Option 1: Streamlit Cloud Deployment (Simplest)

For deployment to Streamlit Cloud or other cloud platforms:

```bash
# Clone or download the repository
git clone <repository-url>
cd Stream-Bill-generator-main

# Install basic requirements
pip install -r requirements_basic.txt
```

This option provides:
- Core functionality
- PDF generation via pdfkit
- Cloud deployment compatibility
- 95% deployment success rate

### Option 2: Local Development with Enhanced Features

For local development with all features:

```bash
# Clone or download the repository
git clone <repository-url>
cd Stream-Bill-generator-main

# Install basic requirements
pip install -r requirements_basic.txt

# Install enhanced requirements
pip install -r requirements_advanced.txt
```

This option provides:
- All enhanced PDF features
- Multi-engine PDF generation
- Performance optimizations
- Professional styling

## ⚙️ PDF Engine Setup

### pdfkit (Basic - Required)
pdfkit works out of the box in most environments.

### WeasyPrint (Enhanced - Optional)
For enhanced PDF quality with WeasyPrint:

**Windows:**
1. Download and install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html
2. Add to PATH: `C:\Program Files\wkhtmltopdf\bin`

**macOS:**
```bash
brew install weasyprint
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install weasyprint
```

### xhtml2pdf (Alternative - Optional)
```bash
pip install xhtml2pdf
```

## ▶️ Running the Application

### Basic Mode
```bash
streamlit run app/main.py
```

### Enhanced Mode (if enhanced packages installed)
```bash
streamlit run app/main.py
```

The application will automatically detect available engines and use the best one.

## 🧪 Testing the Installation

Run the test suite to verify the installation:

```bash
# Test core functionality
python -m pytest tests/test_modularization.py

# Test optimization features
python -m pytest tests/test_optimizations.py
```

## 📁 Directory Structure

After installation, your directory should look like:

```
Stream-Bill-generator-main/
├── app/                 # Main application
├── core/                # Core computation logic
├── exports/             # Export and rendering modules
├── templates/           # HTML templates
├── tests/               # Test suite
├── scripts/             # Utility scripts
├── requirements_basic.txt    # Basic dependencies
├── requirements_advanced.txt # Enhanced dependencies
├── README.md            # Project overview
└── ...                  # Other documentation files
```

## 🔧 Configuration

### Environment Variables

Set these environment variables for specific behavior:

```bash
# Force cloud mode (use only pdfkit)
export STREAMLIT_CLOUD=true

# Enable debug mode
export DEBUG=true
```

### PDF Options

PDF generation options can be configured in `exports/renderers.py`:
- Page size: A4 (default)
- Orientation: Portrait/Landscape
- Margins: 10-15mm configurable

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Create new app on Streamlit Cloud
3. Set requirements file to `requirements_basic.txt`

### Docker (Recommended for Production)
```bash
# Build the image
docker build -t stream-bill-generator .

# Run the container
docker run -p 8503:8503 stream-bill-generator
```

### Local Server
```bash
streamlit run app/main.py --server.port 8503
```

## 🆘 Troubleshooting

### Common Issues

1. **PDF Generation Fails**
   - Ensure wkhtmltopdf is installed and in PATH
   - Check that required system dependencies are installed

2. **Import Errors**
   - Verify all requirements are installed
   - Check Python version compatibility

3. **Template Rendering Issues**
   - Ensure templates directory exists
   - Check template file permissions

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all installation steps were completed
3. Consult the README.md and DEPLOYMENT_GUIDE.md files
4. Run the validation script: `python validate_deployment.py`

## ✅ Verification

After installation, verify everything works:

1. Run the application: `streamlit run app/main.py`
2. Open browser to http://localhost:8503
3. Upload a test Excel file
4. Generate documents
5. Verify PDF quality and formatting

## 🔄 Updates

To update to the latest version:

```bash
git pull origin main
pip install -r requirements_basic.txt
pip install -r requirements_advanced.txt
```

## 📞 Support

For issues not resolved by this guide:
- Check existing GitHub issues
- Create a new issue with detailed error information
- Contact the development team

---

**Installation Complete!** Your Stream Bill Generator is now ready to use with all PDF optimization features.