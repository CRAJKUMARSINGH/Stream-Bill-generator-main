"""
Enhanced PDF Generator using multiple PDF generation libraries
"""
import os
import tempfile
from pathlib import Path
import asyncio

# Try to import optional packages
PDFKIT_AVAILABLE = False
XHTML2PDF_AVAILABLE = False
WEASYPRINT_AVAILABLE = False
PLAYWRIGHT_AVAILABLE = False
JINJA2_AVAILABLE = False

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    pdfkit = None

try:
    from xhtml2pdf import pisa
    XHTML2PDF_AVAILABLE = True
except ImportError:
    pisa = None

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    HTML = None
    CSS = None

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    async_playwright = None

try:
    from jinja2 import Environment, FileSystemLoader
    JINJA2_AVAILABLE = True
except ImportError:
    Environment = None
    FileSystemLoader = None

# Environment detection
IN_CLOUD_ENV = os.environ.get('STREAMLIT_CLOUD', '').lower() == 'true' or \
               os.environ.get('DEPLOYMENT_ENV', '').lower() == 'cloud' or \
               'streamlit' in os.environ.get('HOSTNAME', '').lower()

class EnhancedPDFGenerator:
    def __init__(self, template_dir=None):
        """Initialize the PDF generator with template directory"""
        if not JINJA2_AVAILABLE:
            raise Exception("Jinja2 is required but not available")
            
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        
        self.template_dir = template_dir
        # Only initialize environment if Jinja2 is available
        if JINJA2_AVAILABLE and Environment is not None and FileSystemLoader is not None:
            self.env = Environment(loader=FileSystemLoader(template_dir), cache_size=0)
        else:
            self.env = None
        
        # Define available engines in order of preference
        # In cloud environments, only use basic engines
        self.engines = []
        if not IN_CLOUD_ENV and WEASYPRINT_AVAILABLE:
            self.engines.append("weasyprint")
        if not IN_CLOUD_ENV and XHTML2PDF_AVAILABLE:
            self.engines.append("xhtml2pdf")
        if PDFKIT_AVAILABLE:
            self.engines.append("pdfkit")
        if not IN_CLOUD_ENV and PLAYWRIGHT_AVAILABLE:
            self.engines.append("playwright")
    
    def generate_pdf(self, template_name, data, output_path, engine=None, orientation="portrait"):
        """
        Generate PDF using the specified engine or the best available engine
        
        Args:
            template_name (str): Name of the template file (without .html extension)
            data (dict): Data to render in the template
            output_path (str): Path where PDF should be saved
            engine (str): Specific engine to use (weasyprint, xhtml2pdf, pdfkit, playwright)
            orientation (str): Page orientation (portrait or landscape)
        
        Returns:
            bool: True if successful, False otherwise
        """
        # In cloud environments, only allow pdfkit
        if IN_CLOUD_ENV:
            engine = "pdfkit"
            if not PDFKIT_AVAILABLE:
                raise Exception("pdfkit is required but not available in cloud environment")
        
        # Determine which engine to use
        if engine is None:
            if not self.engines:
                raise Exception("No PDF generation engines available. Please install one of: weasyprint, xhtml2pdf, pdfkit, playwright")
            engine = self.engines[0]  # Use the best available engine
        
        # Check if environment is available
        if self.env is None:
            raise Exception("Jinja2 environment not available")
            
        # Render HTML from template
        try:
            template = self.env.get_template(f"enhanced_{template_name}.html")
            html_content = template.render(data=data)
        except Exception as e:
            # Fallback to regular template if enhanced template not found
            try:
                template = self.env.get_template(f"{template_name}.html")
                html_content = template.render(data=data)
            except Exception as e2:
                raise Exception(f"Could not render template: {str(e2)}")
        
        # Generate PDF using selected engine
        if engine == "weasyprint" and WEASYPRINT_AVAILABLE:
            return self._generate_weasyprint(html_content, output_path, orientation)
        elif engine == "xhtml2pdf" and XHTML2PDF_AVAILABLE:
            return self._generate_xhtml2pdf(html_content, output_path)
        elif engine == "pdfkit" and PDFKIT_AVAILABLE:
            return self._generate_pdfkit(html_content, output_path, orientation)
        elif engine == "playwright" and PLAYWRIGHT_AVAILABLE:
            # For simplicity in this context, we'll run the async function in a separate event loop
            import asyncio
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self._generate_playwright(html_content, output_path, orientation))
                loop.close()
                return result
            except Exception as e:
                print(f"Playwright generation failed: {str(e)}")
                return False
        else:
            raise Exception(f"PDF engine {engine} not available or not supported")
    
    def _generate_weasyprint(self, html_content, output_path, orientation):
        """Generate PDF using WeasyPrint"""
        if not WEASYPRINT_AVAILABLE or HTML is None or CSS is None:
            return False
            
        try:
            # Add CSS for page orientation
            css_content = ""
            if orientation == "landscape":
                css_content = """
                @page {
                    size: A4 landscape;
                    margin: 15mm;
                }
                @media print {
                    body {
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }
                }
                """
            else:
                css_content = """
                @page {
                    size: A4 portrait;
                    margin: 15mm;
                }
                @media print {
                    body {
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }
                }
                """
            
            html = HTML(string=html_content)
            css = CSS(string=css_content)
            html.write_pdf(output_path, stylesheets=[css])
            return True
        except Exception as e:
            print(f"WeasyPrint generation failed: {str(e)}")
            return False
    
    def _generate_xhtml2pdf(self, html_content, output_path):
        """Generate PDF using xhtml2pdf"""
        if not XHTML2PDF_AVAILABLE or pisa is None:
            return False
            
        try:
            with open(output_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
                return not pisa_status.err
        except Exception as e:
            print(f"xhtml2pdf generation failed: {str(e)}")
            return False
    
    def _generate_pdfkit(self, html_content, output_path, orientation):
        """Generate PDF using pdfkit"""
        if not PDFKIT_AVAILABLE or pdfkit is None:
            return False
            
        try:
            options = {
                "page-size": "A4",
                "orientation": orientation,
                "margin-top": "15mm",
                "margin-bottom": "15mm",
                "margin-left": "15mm",
                "margin-right": "15mm",
                "encoding": "UTF-8",
                "no-outline": None,
                "enable-local-file-access": None
            }
            
            # Try to configure wkhtmltopdf path
            try:
                import platform
                if platform.system() == "Windows":
                    wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
                    if os.path.exists(wkhtmltopdf_path) and pdfkit is not None:
                        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
                        pdfkit.from_string(html_content, output_path, configuration=config, options=options)
                    else:
                        pdfkit.from_string(html_content, output_path, options=options)
                else:
                    pdfkit.from_string(html_content, output_path, options=options)
            except:
                pdfkit.from_string(html_content, output_path, options=options)
            
            return True
        except Exception as e:
            print(f"pdfkit generation failed: {str(e)}")
            return False
    
    async def _generate_playwright(self, html_content, output_path, orientation):
        """Generate PDF using Playwright"""
        if not PLAYWRIGHT_AVAILABLE or async_playwright is None:
            return False
            
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.set_content(html_content)
                
                pdf_options = {
                    "format": "A4",
                    "print_background": True,
                    "margin": {
                        "top": "15mm",
                        "bottom": "15mm",
                        "left": "15mm",
                        "right": "15mm"
                    }
                }
                
                if orientation == "landscape":
                    pdf_options["landscape"] = True
                
                await page.pdf(path=output_path, **pdf_options)
                await browser.close()
                return True
        except Exception as e:
            print(f"Playwright generation failed: {str(e)}")
            return False

# Convenience functions
def generate_pdf_with_fallback(template_name, data, output_path, orientation="portrait"):
    """
    Generate PDF using the best available engine with fallbacks
    
    Args:
        template_name (str): Name of the template file
        data (dict): Data to render in the template
        output_path (str): Path where PDF should be saved
        orientation (str): Page orientation
    
    Returns:
        str: Engine used to generate PDF
    """
    generator = EnhancedPDFGenerator()
    
    # Try engines in order of preference
    for engine in generator.engines:
        try:
            success = generator.generate_pdf(template_name, data, output_path, engine, orientation)
            if success:
                return engine
        except Exception as e:
            print(f"Failed to generate PDF with {engine}: {str(e)}")
            continue
    
    raise Exception("Failed to generate PDF with any available engine")

# Example usage
if __name__ == "__main__":
    # Example data
    sample_data = {
        "header": [["Agreement No.", "123/2024"]],
        "items": [
            {"unit": "M", "quantity": "100", "serial_no": "1", "description": "Sample Item", "rate": "50", "amount": "5000", "remark": "Test"}
        ],
        "totals": {
            "grand_total": "5000",
            "premium": {"percent": 0.05, "amount": "250"},
            "payable": "5250"
        }
    }
    
    # Generate sample PDF
    try:
        engine_used = generate_pdf_with_fallback("first_page", sample_data, "sample_output.pdf")
        print(f"PDF generated successfully using {engine_used}")
    except Exception as e:
        print(f"Failed to generate PDF: {str(e)}")