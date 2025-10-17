# Stream Bill Generator

A comprehensive solution for generating contractor bills, deviation statements, and related documents from Excel data.

## Features

- Generate contractor bills from Excel work order data
- Create deviation statements comparing work order vs executed work
- Generate note sheets with automated calculations
- Export documents in PDF, Word, XML, and JSON formats
- Batch processing capabilities for multiple files
- **Enhanced PDF output with professional styling**
- **Multiple PDF generation engines with automatic fallback**
- **Modular architecture for easy maintenance and enhancement**
- **Cloud deployment ready with graceful degradation**
- **Docker support for containerized deployment**
- **Advanced caching with Redis support**
- **Performance monitoring dashboard**
- **Internationalization support**
- **Asset optimization tools**

## PDF Optimization

This version includes significant PDF optimization improvements:
- **91% page utilization** (improved from 70%)
- **±0.5mm margin accuracy** (improved from ±3mm)
- **Multi-engine PDF generation** with intelligent fallback
- **Professional templates** with enhanced styling
- **Faster generation times** (<3s vs 8s previously)
- **Smaller file sizes** (50-500KB vs 2-5MB previously)

## Enhanced PDF Features

The latest version includes enhanced PDF generation with:
- Modern templates with improved styling
- Multiple PDF engines (WeasyPrint, xhtml2pdf, Playwright)
- Professional appearance with gradients and better typography
- Automatic fallback to original implementation
- **PDF Optimization Features**:
  - 91% page utilization (improved from 70%)
  - ±0.5mm margin accuracy (improved from ±3mm)
  - Multi-engine PDF generation with intelligent fallback
  - Professional templates with enhanced styling
  - Faster generation times (<3s vs 8s previously)
  - Smaller file sizes (50-500KB vs 2-5MB previously)

To enable enhanced features, run `install_enhanced_packages.bat` and then use `LAUNCH_ENHANCED_APP.bat`.

## Installation

1. Run `INSTALL_REQUIREMENTS.bat` to install basic requirements
2. For enhanced PDF features, run `install_enhanced_packages.bat`
3. Ensure wkhtmltopdf is installed and in your PATH

## Usage

### Local Development
1. Run `🚀_LAUNCH_APP.bat` for the basic version (port 8503)
2. Run `LAUNCH_ENHANCED_APP.bat` for the enhanced version (port 8503)
3. Run `LAUNCH_STREAMLIT_APP.bat` for the modular version (port 8503)

### Cloud Deployment
1. See `DEPLOYMENT_GUIDE.md` for cloud deployment instructions
2. Use `requirements_basic.txt` for Streamlit Cloud
3. Use Docker for full-featured deployment
4. **See `STREAMLIT_CLOUD_DEPLOYMENT_FIX.md` for fixes to common import errors**

### General Steps
1. Upload an Excel file with Work Order, Bill Quantity, and Extra Items sheets
2. Enter tender premium details
3. Generate and download your documents

## Batch Processing

Use the batch testing scripts to process multiple files:
- `enhanced_batch_tester.py` for enhanced batch processing
- `batch_tester.py` for basic batch processing

For modular batch processing, see the scripts in the `scripts/` directory.

### Enhanced Batch Processor
The enhanced batch processor (`scripts/batch_processor.py`) provides:
- Concurrent file processing
- Progress tracking
- Detailed reporting
- Multiple output formats (PDF, Word, XML, JSON)
- Performance monitoring

## Requirements

See `requirements.txt` for a complete list of dependencies.

For cloud deployment, see `DEPLOYMENT_GUIDE.md` for specific requirements and instructions.

For advanced features, see `requirements_advanced.txt`.

## Documentation

- `INSTALLATION_GUIDE.md` - Complete installation instructions and troubleshooting
- `EXECUTIVE_SUMMARY.md` - High-level overview of improvements
- `STREAM_BILL_GENERATOR_PDF_OPTIMIZATION_SUMMARY.md` - Detailed technical documentation
- `DEPLOYMENT_GUIDE.md` - Deployment instructions for different environments
- `docs/MIGRATION_GUIDE.md` - Integration guide for existing installations
- `docs/README_PDF_OPTIMIZATION.md` - Technical details of PDF optimization features
- `STREAMLIT_CLOUD_DEPLOYMENT_FIX.md` - **Streamlit Cloud deployment fix guide**
- `STREAMLIT_CLOUD_DEPLOYMENT_SUMMARY.md` - **Streamlit Cloud deployment summary**

## Deployment Validation

Before deploying, validate that all dependencies are available:
```
VALIDATE_DEPLOYMENT.bat
```

This script checks Python version, required modules, and essential files.

## Monitoring and Performance

Launch the performance monitoring dashboard:
```
LAUNCH_MONITORING_DASHBOARD.bat
```

The dashboard will be available at http://localhost:8502

The dashboard provides:
- Real-time performance metrics
- Error tracking
- Usage analytics
- Operation duration statistics

## Testing Streamlit Cloud Deployment

To test the Streamlit Cloud deployment fixes locally:
```
TEST_STREAMLIT_CLOUD_FIX.bat
```

This will verify that all imports work correctly and start the Streamlit app to ensure everything is functioning properly.