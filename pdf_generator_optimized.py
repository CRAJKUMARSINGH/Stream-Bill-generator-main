"""
Optimized PDF Generator for Infrastructure Bills
Addresses: A4 page utilization, 10-15mm margins, landscape/portrait support
Elegant HTML to PDF conversion with statutory compliance
"""

import os
import io
import base64
from typing import Optional, Dict, Any, Literal
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    Professional PDF Generator with precise A4 layout control
    
    Features:
    - Exact 10-15mm margins for A4 pages
    - Landscape and portrait orientation support
    - Multiple PDF engine support with intelligent fallback
    - Cloud deployment compatible
    - Statutory format compliance
    """
    
    # A4 dimensions in mm
    A4_WIDTH_MM = 210
    A4_HEIGHT_MM = 297
    
    # Margin specifications (in mm)
    MARGIN_TOP = 12
    MARGIN_RIGHT = 12
    MARGIN_BOTTOM = 12
    MARGIN_LEFT = 12
    
    def __init__(self, 
                 orientation: Literal['portrait', 'landscape'] = 'portrait',
                 custom_margins: Optional[Dict[str, int]] = None):
        """
        Initialize PDF Generator
        
        Args:
            orientation: 'portrait' or 'landscape'
            custom_margins: Optional dict with keys: top, right, bottom, left (in mm)
        """
        self.orientation = orientation
        
        # Set margins
        if custom_margins:
            self.margin_top = custom_margins.get('top', self.MARGIN_TOP)
            self.margin_right = custom_margins.get('right', self.MARGIN_RIGHT)
            self.margin_bottom = custom_margins.get('bottom', self.MARGIN_BOTTOM)
            self.margin_left = custom_margins.get('left', self.MARGIN_LEFT)
        else:
            self.margin_top = self.MARGIN_TOP
            self.margin_right = self.MARGIN_RIGHT
            self.margin_bottom = self.MARGIN_BOTTOM
            self.margin_left = self.MARGIN_LEFT
        
        # Calculate content dimensions
        if orientation == 'landscape':
            self.page_width = self.A4_HEIGHT_MM
            self.page_height = self.A4_WIDTH_MM
        else:
            self.page_width = self.A4_WIDTH_MM
            self.page_height = self.A4_HEIGHT_MM
        
        self.content_width = self.page_width - self.margin_left - self.margin_right
        self.content_height = self.page_height - self.margin_top - self.margin_bottom
        
        # Detect available PDF engines
        self.available_engines = self._detect_engines()
        logger.info(f"Available PDF engines: {self.available_engines}")
    
    def _detect_engines(self) -> list:
        """Detect available PDF generation engines"""
        engines = []
        
        # Check for WeasyPrint
        try:
            import weasyprint
            engines.append('weasyprint')
        except ImportError:
            pass
        
        # Check for ReportLab
        try:
            from reportlab.pdfgen import canvas
            engines.append('reportlab')
        except ImportError:
            pass
        
        # Check for xhtml2pdf
        try:
            from xhtml2pdf import pisa
            engines.append('xhtml2pdf')
        except ImportError:
            pass
        
        # Check for pdfkit
        try:
            import pdfkit
            engines.append('pdfkit')
        except ImportError:
            pass
        
        return engines
    
    def get_base_css(self) -> str:
        """
        Generate base CSS with precise A4 page layout and margins
        Ensures proper page utilization with 10-15mm margins
        """
        css = f"""
        @page {{
            size: A4 {self.orientation};
            margin-top: {self.margin_top}mm;
            margin-right: {self.margin_right}mm;
            margin-bottom: {self.margin_bottom}mm;
            margin-left: {self.margin_left}mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #000;
            background: white;
        }}
        
        .page-container {{
            width: 100%;
            height: 100%;
            position: relative;
        }}
        
        /* Content area dimensions to maximize A4 page usage */
        .content-area {{
            width: {self.content_width}mm;
            min-height: {self.content_height}mm;
        }}
        
        /* Header styling */
        .document-header {{
            width: 100%;
            padding: 8px 0;
            border-bottom: 2px solid #333;
            margin-bottom: 10px;
        }}
        
        .document-title {{
            font-size: 16pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 5px;
            text-transform: uppercase;
        }}
        
        .document-subtitle {{
            font-size: 11pt;
            text-align: center;
            margin-bottom: 3px;
        }}
        
        /* Table styling for bills */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0;
            font-size: 9pt;
        }}
        
        table th {{
            background-color: #2c3e50;
            color: white;
            padding: 6px 4px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #000;
        }}
        
        table td {{
            padding: 5px 4px;
            border: 1px solid #333;
            vertical-align: top;
        }}
        
        table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        /* Numeric alignment */
        .numeric {{
            text-align: right;
            font-family: 'Courier New', monospace;
        }}
        
        /* Summary sections */
        .summary-section {{
            width: 100%;
            margin-top: 15px;
            page-break-inside: avoid;
        }}
        
        .summary-row {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid #ddd;
        }}
        
        .summary-label {{
            font-weight: bold;
            flex: 1;
        }}
        
        .summary-value {{
            flex: 1;
            text-align: right;
            font-family: 'Courier New', monospace;
        }}
        
        .grand-total {{
            background-color: #2c3e50;
            color: white;
            padding: 8px 10px;
            margin-top: 10px;
            font-weight: bold;
            font-size: 12pt;
        }}
        
        /* Signature section */
        .signature-section {{
            margin-top: 30px;
            page-break-inside: avoid;
        }}
        
        .signature-box {{
            display: inline-block;
            width: 45%;
            text-align: center;
            margin: 20px 2%;
        }}
        
        .signature-line {{
            border-top: 1px solid #000;
            margin-top: 40px;
            padding-top: 5px;
        }}
        
        /* Footer */
        .document-footer {{
            width: 100%;
            text-align: center;
            font-size: 8pt;
            color: #666;
            margin-top: 15px;
            padding-top: 8px;
            border-top: 1px solid #ccc;
        }}
        
        /* Page break utilities */
        .page-break {{
            page-break-after: always;
        }}
        
        .no-break {{
            page-break-inside: avoid;
        }}
        
        /* Print optimization */
        @media print {{
            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            .page-container {{
                page-break-after: always;
            }}
            
            .page-container:last-child {{
                page-break-after: auto;
            }}
        }}
        """
        return css
    
    def generate_html_template(self, 
                              title: str,
                              subtitle: str = "",
                              content: str = "",
                              footer: str = "",
                              custom_css: str = "") -> str:
        """
        Generate complete HTML with proper structure for PDF conversion
        
        Args:
            title: Document title
            subtitle: Optional subtitle
            content: Main content HTML
            footer: Footer text
            custom_css: Additional CSS styles
        
        Returns:
            Complete HTML string ready for PDF conversion
        """
        base_css = self.get_base_css()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {base_css}
        {custom_css}
    </style>
</head>
<body>
    <div class="page-container">
        <div class="content-area">
            <div class="document-header">
                <div class="document-title">{title}</div>
                {f'<div class="document-subtitle">{subtitle}</div>' if subtitle else ''}
            </div>
            
            <div class="document-content">
                {content}
            </div>
            
            {f'<div class="document-footer">{footer}</div>' if footer else ''}
        </div>
    </div>
</body>
</html>"""
        return html
    
    def html_to_pdf_weasyprint(self, html_content: str, output_path: str) -> bool:
        """Generate PDF using WeasyPrint (best quality)"""
        try:
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            font_config = FontConfiguration()
            
            # Create CSS with proper page setup
            css_string = f"""
            @page {{
                size: A4 {self.orientation};
                margin-top: {self.margin_top}mm;
                margin-right: {self.margin_right}mm;
                margin-bottom: {self.margin_bottom}mm;
                margin-left: {self.margin_left}mm;
            }}
            """
            
            html_doc = HTML(string=html_content)
            css_doc = CSS(string=css_string, font_config=font_config)
            
            html_doc.write_pdf(
                output_path,
                stylesheets=[css_doc],
                font_config=font_config
            )
            
            logger.info(f"PDF generated successfully using WeasyPrint: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"WeasyPrint generation failed: {e}")
            return False
    
    def html_to_pdf_reportlab(self, html_content: str, output_path: str) -> bool:
        """Generate PDF using ReportLab (fallback with HTML parsing)"""
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.units import mm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from bs4 import BeautifulSoup
            
            # Set page size
            pagesize = landscape(A4) if self.orientation == 'landscape' else A4
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=pagesize,
                leftMargin=self.margin_left * mm,
                rightMargin=self.margin_right * mm,
                topMargin=self.margin_top * mm,
                bottomMargin=self.margin_bottom * mm
            )
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Build story
            story = []
            styles = getSampleStyleSheet()
            
            # Extract title
            title_elem = soup.find(class_='document-title')
            if title_elem:
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    textColor=colors.black,
                    spaceAfter=12,
                    alignment=1  # Center
                )
                story.append(Paragraph(title_elem.get_text(), title_style))
            
            # Extract subtitle
            subtitle_elem = soup.find(class_='document-subtitle')
            if subtitle_elem:
                subtitle_style = ParagraphStyle(
                    'CustomSubtitle',
                    parent=styles['Normal'],
                    fontSize=11,
                    spaceAfter=8,
                    alignment=1
                )
                story.append(Paragraph(subtitle_elem.get_text(), subtitle_style))
            
            story.append(Spacer(1, 10))
            
            # Extract tables
            tables = soup.find_all('table')
            for table_elem in tables:
                data = []
                for row in table_elem.find_all('tr'):
                    cells = row.find_all(['th', 'td'])
                    data.append([cell.get_text(strip=True) for cell in cells])
                
                if data:
                    # Create table
                    t = Table(data)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF generated successfully using ReportLab: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"ReportLab generation failed: {e}")
            return False
    
    def html_to_pdf_xhtml2pdf(self, html_content: str, output_path: str) -> bool:
        """Generate PDF using xhtml2pdf"""
        try:
            from xhtml2pdf import pisa
            
            with open(output_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(
                    html_content,
                    dest=pdf_file
                )
            
            if pisa_status.err:
                logger.error("xhtml2pdf reported errors")
                return False
            
            logger.info(f"PDF generated successfully using xhtml2pdf: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"xhtml2pdf generation failed: {e}")
            return False
    
    def html_to_pdf_pdfkit(self, html_content: str, output_path: str) -> bool:
        """Generate PDF using pdfkit (wkhtmltopdf wrapper)"""
        try:
            import pdfkit
            
            options = {
                'page-size': 'A4',
                'orientation': self.orientation.capitalize(),
                'margin-top': f'{self.margin_top}mm',
                'margin-right': f'{self.margin_right}mm',
                'margin-bottom': f'{self.margin_bottom}mm',
                'margin-left': f'{self.margin_left}mm',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None,
                'print-media-type': None,
            }
            
            pdfkit.from_string(html_content, output_path, options=options)
            
            logger.info(f"PDF generated successfully using pdfkit: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"pdfkit generation failed: {e}")
            return False
    
    def generate_pdf(self, 
                    html_content: str, 
                    output_path: str,
                    preferred_engine: Optional[str] = None) -> bool:
        """
        Generate PDF with intelligent engine fallback
        
        Args:
            html_content: Complete HTML string
            output_path: Path to save PDF
            preferred_engine: Optional preferred engine name
        
        Returns:
            True if successful, False otherwise
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Define engine priority
        if preferred_engine and preferred_engine in self.available_engines:
            engine_order = [preferred_engine] + [e for e in self.available_engines if e != preferred_engine]
        else:
            engine_order = ['weasyprint', 'reportlab', 'xhtml2pdf', 'pdfkit']
            engine_order = [e for e in engine_order if e in self.available_engines]
        
        if not engine_order:
            logger.error("No PDF generation engines available!")
            return False
        
        # Try engines in order
        for engine in engine_order:
            logger.info(f"Attempting PDF generation with {engine}...")
            
            try:
                if engine == 'weasyprint':
                    if self.html_to_pdf_weasyprint(html_content, output_path):
                        return True
                elif engine == 'reportlab':
                    if self.html_to_pdf_reportlab(html_content, output_path):
                        return True
                elif engine == 'xhtml2pdf':
                    if self.html_to_pdf_xhtml2pdf(html_content, output_path):
                        return True
                elif engine == 'pdfkit':
                    if self.html_to_pdf_pdfkit(html_content, output_path):
                        return True
            except Exception as e:
                logger.error(f"Engine {engine} failed with exception: {e}")
                continue
        
        logger.error("All PDF generation engines failed!")
        return False
    
    def get_streamlit_download_link(self, pdf_path: str, link_text: str = "Download PDF") -> str:
        """
        Generate Streamlit download link for PDF
        
        Args:
            pdf_path: Path to PDF file
            link_text: Text for download button
        
        Returns:
            Base64 encoded download link
        """
        try:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="{os.path.basename(pdf_path)}">{link_text}</a>'
            return href
        except Exception as e:
            logger.error(f"Failed to generate download link: {e}")
            return ""


# Example usage and testing functions
def create_sample_bill_html(generator: PDFGenerator) -> str:
    """Create sample infrastructure bill HTML"""
    
    content = """
    <table>
        <thead>
            <tr>
                <th>S.No.</th>
                <th>Description of Work</th>
                <th>Unit</th>
                <th>Quantity</th>
                <th>Rate (₹)</th>
                <th>Amount (₹)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Earthwork in excavation by mechanical means</td>
                <td>Cum</td>
                <td class="numeric">1,250.00</td>
                <td class="numeric">185.50</td>
                <td class="numeric">2,31,875.00</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Providing and laying cement concrete 1:2:4</td>
                <td>Cum</td>
                <td class="numeric">850.00</td>
                <td class="numeric">4,250.00</td>
                <td class="numeric">36,12,500.00</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Providing and fixing M.S. reinforcement</td>
                <td>Kg</td>
                <td class="numeric">5,420.00</td>
                <td class="numeric">52.00</td>
                <td class="numeric">2,81,840.00</td>
            </tr>
            <tr>
                <td>4</td>
                <td>Brick work in foundation and plinth</td>
                <td>Sqm</td>
                <td class="numeric">2,150.00</td>
                <td class="numeric">425.00</td>
                <td class="numeric">9,13,750.00</td>
            </tr>
            <tr>
                <td>5</td>
                <td>12mm cement plaster (1:4)</td>
                <td>Sqm</td>
                <td class="numeric">3,200.00</td>
                <td class="numeric">125.00</td>
                <td class="numeric">4,00,000.00</td>
            </tr>
        </tbody>
    </table>
    
    <div class="summary-section">
        <div class="summary-row">
            <span class="summary-label">Sub Total:</span>
            <span class="summary-value">₹ 54,39,965.00</span>
        </div>
        <div class="summary-row">
            <span class="summary-label">Tender Premium (5%):</span>
            <span class="summary-value">₹ 2,71,998.25</span>
        </div>
        <div class="summary-row">
            <span class="summary-label">GST @ 18%:</span>
            <span class="summary-value">₹ 10,28,153.39</span>
        </div>
        <div class="grand-total">
            <div style="display: flex; justify-content: space-between;">
                <span>GRAND TOTAL:</span>
                <span>₹ 67,40,116.64</span>
            </div>
        </div>
    </div>
    
    <div class="signature-section">
        <div class="signature-box">
            <div class="signature-line">
                <strong>Contractor's Signature</strong><br>
                Date: ______________
            </div>
        </div>
        <div class="signature-box">
            <div class="signature-line">
                <strong>Engineer-in-Charge</strong><br>
                Date: ______________
            </div>
        </div>
    </div>
    """
    
    html = generator.generate_html_template(
        title="CONTRACTOR RUNNING BILL - JANUARY 2025",
        subtitle="Work Order No: WO/2024-25/1234 | Project: Highway Construction Package-A",
        content=content,
        footer="This is a computer-generated document | Page 1 of 1"
    )
    
    return html


if __name__ == "__main__":
    # Test both orientations
    print("=" * 70)
    print("Testing Optimized PDF Generator")
    print("=" * 70)
    
    # Test Portrait
    print("\n1. Testing Portrait orientation with 12mm margins...")
    portrait_gen = PDFGenerator(orientation='portrait')
    portrait_html = create_sample_bill_html(portrait_gen)
    portrait_success = portrait_gen.generate_pdf(
        portrait_html, 
        "/home/user/sample_bill_portrait.pdf"
    )
    print(f"   Portrait PDF: {'✓ Success' if portrait_success else '✗ Failed'}")
    
    # Test Landscape
    print("\n2. Testing Landscape orientation with 12mm margins...")
    landscape_gen = PDFGenerator(orientation='landscape')
    landscape_html = create_sample_bill_html(landscape_gen)
    landscape_success = landscape_gen.generate_pdf(
        landscape_html, 
        "/home/user/sample_bill_landscape.pdf"
    )
    print(f"   Landscape PDF: {'✓ Success' if landscape_success else '✗ Failed'}")
    
    # Test custom margins
    print("\n3. Testing custom 15mm margins...")
    custom_gen = PDFGenerator(
        orientation='portrait',
        custom_margins={'top': 15, 'right': 15, 'bottom': 15, 'left': 15}
    )
    custom_html = create_sample_bill_html(custom_gen)
    custom_success = custom_gen.generate_pdf(
        custom_html, 
        "/home/user/sample_bill_custom_margins.pdf"
    )
    print(f"   Custom margins PDF: {'✓ Success' if custom_success else '✗ Failed'}")
    
    print("\n" + "=" * 70)
    print("PDF Generation Testing Complete!")
    print("=" * 70)