"""
Export renderers for generating PDF, Word, and other document formats
This module handles the output generation while preserving the core computation logic.
"""
import os
import tempfile
from jinja2 import Environment, FileSystemLoader
import platform
from docx import Document
from pypdf import PdfReader, PdfWriter
import zipfile

# Try to import pdfkit, but handle gracefully if not available
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    pdfkit = None
    PDFKIT_AVAILABLE = False

def setup_jinja_environment(template_dir):
    """Set up Jinja2 environment with the specified template directory"""
    return Environment(loader=FileSystemLoader(template_dir), cache_size=0)

def setup_pdfkit_config():
    """Configure wkhtmltopdf path"""
    if not PDFKIT_AVAILABLE or pdfkit is None:
        return None
        
    if platform.system() == "Windows":
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if os.path.exists(wkhtmltopdf_path):
            return pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    return pdfkit.configuration()

def generate_pdf(sheet_name, data, orientation, template_dir, temp_dir, config=None):
    """
    Generate PDF using the enhanced PDF generator if available, otherwise fallback to pdfkit
    
    Args:
        sheet_name (str): Name of the sheet to generate
        data (dict): Data to render in the template
        orientation (str): Page orientation ("portrait" or "landscape")
        template_dir (str): Directory containing templates
        temp_dir (str): Directory for temporary files
        config: PDFKit configuration
    
    Returns:
        str: Path to generated PDF file
    """
    # Try to use enhanced PDF generator if available
    try:
        from enhanced_pdf_generator import generate_pdf_with_fallback
        pdf_path = os.path.join(temp_dir, f"{sheet_name.replace(' ', '_')}.pdf")
        try:
            engine_used = generate_pdf_with_fallback(
                sheet_name.lower().replace(' ', '_'), 
                data, 
                pdf_path, 
                "landscape" if orientation == "landscape" else "portrait"
            )
            return pdf_path
        except Exception as e:
            # If enhanced generation fails, fall back to original implementation
            print(f"Enhanced PDF generation failed: {str(e)}. Using fallback.")
            pass
    except ImportError:
        # Enhanced PDF generator not available, use original implementation
        pass
    
    # Check if pdfkit is available
    if not PDFKIT_AVAILABLE or pdfkit is None:
        # If pdfkit is not available, we need to provide an alternative
        # For now, we'll raise an exception but in a real implementation,
        # we might want to use another PDF generation method
        raise ImportError("pdfkit is not available. Please install pdfkit and wkhtmltopdf.")
    
    # Original pdfkit implementation
    env = setup_jinja_environment(template_dir)
    template = env.get_template(f"{sheet_name.lower().replace(' ', '_')}.html")
    html_content = template.render(data=data)
    options = {
        "page-size": "A4",
        "orientation": orientation,
        "margin-top": "15mm",
        "margin-bottom": "15mm",
        "margin-left": "10mm",
        "margin-right": "10mm"
    }
    pdf_path = os.path.join(temp_dir, f"{sheet_name.replace(' ', '_')}.pdf")
    
    # Only call pdfkit if it's available
    if pdfkit and PDFKIT_AVAILABLE:
        pdfkit.from_string(
            html_content,
            pdf_path,
            configuration=config,
            options=options
        )
    else:
        raise ImportError("pdfkit is not available. Please install pdfkit and wkhtmltopdf.")
    
    return pdf_path

def create_word_doc(sheet_name, data, doc_path):
    """
    Create Word document from data
    
    Args:
        sheet_name (str): Name of the sheet
        data (dict): Data to include in the document
        doc_path (str): Path where to save the document
    """
    doc = Document()
    if sheet_name == "First Page":
        table = doc.add_table(rows=len(data["items"]) + 3, cols=9)
        table.style = "Table Grid"
        for i, item in enumerate(data["items"]):
            row = table.rows[i]
            row.cells[0].text = str(item.get("unit", ""))
            row.cells[2].text = str(item.get("quantity", ""))
            row.cells[3].text = str(item.get("serial_no", ""))
            row.cells[4].text = str(item.get("description", ""))
            row.cells[5].text = str(item.get("rate", ""))
            row.cells[6].text = str(item.get("amount", ""))
            row.cells[8].text = str(item.get("remark", ""))
        row = table.rows[-3]
        row.cells[4].text = "Grand Total"
        row.cells[6].text = str(data["totals"].get("grand_total", ""))
        row = table.rows[-2]
        premium_percent_value = data['totals']['premium'].get('percent', 0)
        if isinstance(premium_percent_value, str):
            try:
                premium_percent_value = float(premium_percent_value)
            except (ValueError, TypeError):
                premium_percent_value = 0
        row.cells[4].text = f"Tender Premium @ {premium_percent_value:.2%}"
        row.cells[6].text = str(data["totals"]["premium"].get("amount", ""))
        row = table.rows[-1]
        row.cells[4].text = "Payable Amount"
        row.cells[6].text = str(data["totals"].get("payable", ""))
    elif sheet_name == "Last Page":
        doc.add_paragraph(f"Payable Amount: {data.get('payable_amount', '')}")
        doc.add_paragraph(f"Total in Words: {data.get('amount_words', '')}")
    elif sheet_name == "Extra Items":
        table = doc.add_table(rows=len(data["items"]) + 1, cols=7)
        table.style = "Table Grid"
        headers = ["Serial No.", "Remark", "Description", "Quantity", "Unit", "Rate", "Amount"]
        for j, header in enumerate(headers):
            table.rows[0].cells[j].text = header
        for i, item in enumerate(data["items"]):
            row = table.rows[i + 1]
            row.cells[0].text = str(item.get("serial_no", ""))
            row.cells[1].text = str(item.get("remark", ""))
            row.cells[2].text = str(item.get("description", ""))
            row.cells[3].text = str(item.get("quantity", ""))
            row.cells[4].text = str(item.get("unit", ""))
            row.cells[5].text = str(item.get("rate", ""))
            row.cells[6].text = str(item.get("amount", ""))
    elif sheet_name == "Deviation Statement":
        table = doc.add_table(rows=len(data["items"]) + 5, cols=12)
        table.style = "Table Grid"
        headers = ["Serial No.", "Description", "Unit", "Qty WO", "Rate", "Amt WO", "Qty Bill", "Amt Bill", "Excess Qty", "Excess Amt", "Saving Qty", "Saving Amt"]
        for j, header in enumerate(headers):
            table.rows[0].cells[j].text = header
        for i, item in enumerate(data["items"]):
            row = table.rows[i + 1]
            row.cells[0].text = str(item.get("serial_no", ""))
            row.cells[1].text = str(item.get("description", ""))
            row.cells[2].text = str(item.get("unit", ""))
            row.cells[3].text = str(item.get("qty_wo", ""))
            row.cells[4].text = str(item.get("rate", ""))
            row.cells[5].text = str(item.get("amt_wo", ""))
            row.cells[6].text = str(item.get("qty_bill", ""))
            row.cells[7].text = str(item.get("amt_bill", ""))
            row.cells[8].text = str(item.get("excess_qty", ""))
            row.cells[9].text = str(item.get("excess_amt", ""))
            row.cells[10].text = str(item.get("saving_qty", ""))
            row.cells[11].text = str(item.get("saving_amt", ""))
        row = table.rows[-4]
        row.cells[1].text = "Grand Total"
        row.cells[5].text = str(data["summary"].get("work_order_total", ""))
        row.cells[7].text = str(data["summary"].get("executed_total", ""))
        row.cells[9].text = str(data["summary"].get("overall_excess", ""))
        row.cells[11].text = str(data["summary"].get("overall_saving", ""))
        row = table.rows[-3]
        premium_percent_value = data['summary']['premium'].get('percent', 0)
        if isinstance(premium_percent_value, str):
            try:
                premium_percent_value = float(premium_percent_value)
            except (ValueError, TypeError):
                premium_percent_value = 0
        row.cells[1].text = f"Add Tender Premium ({premium_percent_value:.2%})"
        row.cells[5].text = str(data["summary"].get("tender_premium_f", ""))
        row.cells[7].text = str(data["summary"].get("tender_premium_h", ""))
        row.cells[9].text = str(data["summary"].get("tender_premium_j", ""))
        row.cells[11].text = str(data["summary"].get("tender_premium_l", ""))
        row = table.rows[-2]
        row.cells[1].text = "Grand Total including Tender Premium"
        row.cells[5].text = str(data["summary"].get("grand_total_f", ""))
        row.cells[7].text = str(data["summary"].get("grand_total_h", ""))
        row.cells[9].text = str(data["summary"].get("grand_total_j", ""))
        row.cells[11].text = str(data["summary"].get("grand_total_l", ""))
        row = table.rows[-1]
        net_difference = data["summary"].get("net_difference", 0)
        row.cells[1].text = "Overall Excess" if net_difference > 0 else "Overall Saving"
        row.cells[7].text = str(abs(round(net_difference)))
    elif sheet_name == "Note Sheet":
        for note in data.get("notes", []):
            doc.add_paragraph(str(note))
    doc.save(doc_path)

def merge_pdfs(pdf_files, output_path):
    """
    Merge multiple PDF files into a single PDF
    
    Args:
        pdf_files (list): List of paths to PDF files to merge
        output_path (str): Path where to save the merged PDF
    """
    writer = PdfWriter()
    
    for pdf in pdf_files:
        if os.path.exists(pdf):
            reader = PdfReader(pdf)
            for page in reader.pages:
                writer.add_page(page)
    
    with open(output_path, "wb") as out_file:
        writer.write(out_file)

def create_zip_archive(files, zip_path):
    """
    Create a ZIP archive containing the specified files
    
    Args:
        files (list): List of file paths to include in the ZIP
        zip_path (str): Path where to save the ZIP archive
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files:
            if os.path.exists(file_path):
                zipf.write(file_path, os.path.basename(file_path))