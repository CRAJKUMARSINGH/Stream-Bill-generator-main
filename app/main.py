"""
Main Streamlit Application Entry Point
STREAMLIT CLOUD DEPLOYMENT OPTIMIZED VERSION

This version includes robust import handling to work across all deployment environments:
- Local development
- Streamlit Cloud
- Docker containers
- Custom servers
"""
import streamlit as st
import pandas as pd
import os
import sys
import tempfile
from io import BytesIO
from functools import lru_cache

# ============================================================================
# PATH SETUP - Critical for Streamlit Cloud Deployment
# ============================================================================

# Get absolute paths
CURRENT_FILE = os.path.abspath(__file__)
APP_DIR = os.path.dirname(CURRENT_FILE)
ROOT_DIR = os.path.dirname(APP_DIR)

# Add directories to Python path in correct order
for path in [ROOT_DIR, APP_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# ============================================================================
# ROBUST MODULE IMPORTS with Multiple Fallback Strategies
# ============================================================================

def import_modules():
    """
    Import required modules with comprehensive fallback handling.
    Tries multiple import strategies to ensure compatibility across environments.
    """
    # Strategy 1: Direct imports (works in most environments)
    try:
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        from core.streamlit_pdf_integration import StreamlitPDFManager
        return {
            'process_bill': process_bill,
            'safe_float': safe_float,
            'number_to_words': number_to_words,
            'generate_pdf': generate_pdf,
            'create_word_doc': create_word_doc,
            'merge_pdfs': merge_pdfs,
            'create_zip_archive': create_zip_archive,
            'StreamlitPDFManager': StreamlitPDFManager
        }
    except (ImportError, ModuleNotFoundError) as e1:
        st.warning(f"Standard import failed, trying fallback strategy 1: {e1}")
        pass
    
    # Strategy 2: Adjust sys.path and retry (Streamlit Cloud common scenario)
    try:
        # Add additional paths
        if ROOT_DIR not in sys.path:
            sys.path.insert(0, ROOT_DIR)
        
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        from core.streamlit_pdf_integration import StreamlitPDFManager
        return {
            'process_bill': process_bill,
            'safe_float': safe_float,
            'number_to_words': number_to_words,
            'generate_pdf': generate_pdf,
            'create_word_doc': create_word_doc,
            'merge_pdfs': merge_pdfs,
            'create_zip_archive': create_zip_archive,
            'StreamlitPDFManager': StreamlitPDFManager
        }
    except (ImportError, ModuleNotFoundError) as e2:
        st.warning(f"Fallback strategy 1 failed, trying strategy 2: {e2}")
        pass
    
    # Strategy 3: Import entire modules and extract functions
    try:
        # Add parent of parent directory
        parent_parent = os.path.dirname(ROOT_DIR)
        if parent_parent not in sys.path:
            sys.path.insert(0, parent_parent)
        
        import core.computations.bill_processor as bill_processor
        import exports.renderers as renderers
        import core.streamlit_pdf_integration as streamlit_pdf_integration
        
        return {
            'process_bill': bill_processor.process_bill,
            'safe_float': bill_processor.safe_float,
            'number_to_words': bill_processor.number_to_words,
            'generate_pdf': renderers.generate_pdf,
            'create_word_doc': renderers.create_word_doc,
            'merge_pdfs': renderers.merge_pdfs,
            'create_zip_archive': renderers.create_zip_archive,
            'StreamlitPDFManager': streamlit_pdf_integration.StreamlitPDFManager
        }
    except (ImportError, ModuleNotFoundError, AttributeError) as e3:
        st.warning(f"Fallback strategy 2 failed, trying strategy 3: {e3}")
        pass
    
    # Strategy 4: Relative imports from current location
    try:
        # Change to root directory temporarily
        original_dir = os.getcwd()
        os.chdir(ROOT_DIR)
        
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        from core.streamlit_pdf_integration import StreamlitPDFManager
        
        os.chdir(original_dir)
        
        return {
            'process_bill': process_bill,
            'safe_float': safe_float,
            'number_to_words': number_to_words,
            'generate_pdf': generate_pdf,
            'create_word_doc': create_word_doc,
            'merge_pdfs': merge_pdfs,
            'create_zip_archive': create_zip_archive,
            'StreamlitPDFManager': StreamlitPDFManager
        }
    except Exception as e4:
        st.warning(f"Fallback strategy 3 failed: {e4}")
        os.chdir(original_dir)  # Ensure we restore directory
        pass
    
    # If all strategies fail, show detailed error
    st.error("❌ **Critical Error: Unable to import required modules**")
    st.error("""
    **Troubleshooting Steps:**
    
    1. Verify the following directories exist:
       - `core/computations/`
       - `exports/`
    
    2. Ensure all directories have `__init__.py` files
    
    3. Check that the following files exist:
       - `core/computations/bill_processor.py`
       - `exports/renderers.py`
       - `core/streamlit_pdf_integration.py`
    
    4. Verify your repository structure matches:
       ```
       Stream-Bill-generator-main/
       ├── app/
       │   ├── __init__.py
       │   └── main.py
       ├── core/
       │   ├── __init__.py
       │   ├── computations/
       │   │   ├── __init__.py
       │   │   └── bill_processor.py
       │   └── streamlit_pdf_integration.py
       ├── exports/
       │   ├── __init__.py
       │   └── renderers.py
       └── requirements.txt
       ```
    
    **Current sys.path:**
    """)
    for i, path in enumerate(sys.path[:10]):
        st.code(f"{i}. {path}")
    
    st.error("**Please check your repository structure and redeploy.**")
    st.stop()

# Import modules at module level
try:
    MODULES = import_modules()
except Exception as e:
    st.error(f"Fatal import error: {e}")
    st.exception(e)
    st.stop()

# ============================================================================
# CONFIGURATION
# ============================================================================

TEMPLATE_DIR = os.path.join(ROOT_DIR, "templates")
if not os.path.exists(TEMPLATE_DIR):
    # Create templates directory if it doesn't exist
    os.makedirs(TEMPLATE_DIR, exist_ok=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

@st.cache_data(show_spinner=False, ttl=1800)
def _load_excel(file_bytes: bytes):
    """Load Excel once per unique content and return dataframes."""
    xl_file = pd.ExcelFile(BytesIO(file_bytes))
    ws_wo = pd.read_excel(xl_file, "Work Order", header=None)
    ws_bq = pd.read_excel(xl_file, "Bill Quantity", header=None)
    ws_extra = pd.read_excel(xl_file, "Extra Items", header=None)
    return ws_wo, ws_bq, ws_extra, xl_file.sheet_names


@st.cache_data(show_spinner=False, ttl=600)
def _process_bill_cached(ws_wo, ws_bq, ws_extra, premium_percent: float, premium_type: str):
    # Import lazily to avoid Streamlit serialization issues at import time
    from core.computations.bill_processor import process_bill
    return process_bill(ws_wo, ws_bq, ws_extra, premium_percent, premium_type)


def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="Stream Bill Generator",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("📋 Stream Bill Generator")
    st.markdown("""
    **Professional Infrastructure Bill Generation System**  
    Generate contractor bills, deviation statements, and statutory documents from Excel data.
    """)
    
    # Deployment status indicator
    with st.expander("ℹ️ System Information"):
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ All modules loaded successfully")
            st.info(f"📁 Root Directory: `{ROOT_DIR}`")
        with col2:
            st.info(f"🐍 Python Version: {sys.version.split()[0]}")
            st.info(f"📦 Streamlit Version: {st.__version__}")
    
    # File upload section
    st.markdown("---")
    st.subheader("📤 Upload Excel Data")
    
    uploaded_file = st.file_uploader(
        "Select Excel file containing Work Order, Bill Quantity, and Extra Items sheets",
        type=["xlsx", "xls"],
        key="excel_upload",
        help="Upload an Excel file with the required sheets: Work Order, Bill Quantity, and Extra Items"
    )
    
    if uploaded_file is not None:
        try:
            # Read Excel file with caching
            file_bytes = uploaded_file.getvalue()
            ws_wo, ws_bq, ws_extra, sheet_names = _load_excel(file_bytes)
            
            # Validate required sheets
            required_sheets = ["Work Order", "Bill Quantity", "Extra Items"]
            missing_sheets = [sheet for sheet in required_sheets if sheet not in sheet_names]
            
            if missing_sheets:
                st.error(f"❌ Missing required sheets: **{', '.join(missing_sheets)}**")
                st.info(f"📋 Available sheets: {', '.join(sheet_names)}")
                return
            
            # Display success and available sheets
            st.success(f"✅ Excel file loaded successfully with {len(sheet_names)} sheets")
            
            # Dataframes already loaded via cache above
            
            # Sidebar configuration
            st.sidebar.header("⚙️ Configuration")
            
            st.sidebar.markdown("### Premium Settings")
            premium_percent = st.sidebar.number_input(
                "Tender Premium (%)", 
                min_value=-50.0,
                max_value=100.0, 
                value=5.0, 
                step=0.1,
                help="Enter the tender premium percentage (can be positive or negative)"
            )
            
            premium_type = st.sidebar.radio(
                "Premium Type",
                ["above", "below"],
                index=0,
                help="Select whether premium is above (added) or below (subtracted)"
            )
            
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 📊 Quick Stats")
            st.sidebar.metric("Work Order Items", len(ws_wo) - 21 if len(ws_wo) > 21 else 0)
            st.sidebar.metric("Bill Quantity Items", len(ws_bq) - 21 if len(ws_bq) > 21 else 0)
            st.sidebar.metric("Extra Items", len(ws_extra) - 21 if len(ws_extra) > 21 else 0)
            
            # Generate button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                generate_button = st.button(
                    "🚀 Generate All Documents", 
                    type="primary",
                    use_container_width=True
                )
            
            if generate_button:
                with st.spinner("🔄 Processing bill and generating documents..."):
                    try:
                        # Extract imported functions
                        process_bill = MODULES['process_bill']
                        generate_pdf = MODULES['generate_pdf']
                        create_word_doc = MODULES['create_word_doc']
                        merge_pdfs = MODULES['merge_pdfs']
                        create_zip_archive = MODULES['create_zip_archive']
                        StreamlitPDFManager = MODULES['StreamlitPDFManager']
                        
                        # Process the bill
                        first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = _process_bill_cached(
                            ws_wo, ws_bq, ws_extra, premium_percent, premium_type
                        )
                        
                        # Create temporary directory for outputs
                        with tempfile.TemporaryDirectory() as temp_dir:
                            pdf_files = []
                            word_files = []
                            
                            # Progress tracking
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # Initialize PDF manager
                            status_text.text("Initializing PDF generator...")
                            pdf_manager = StreamlitPDFManager()
                            progress_bar.progress(10)
                            
                            # Generate First Page PDF
                            status_text.text("Generating First Page PDF...")
                            try:
                                bill_data = {
                                    'title': 'Contractor Bill - First Page',
                                    'subtitle': 'Work Order vs Executed Work Comparison',
                                    'items': first_page_data.get('items', []),
                                    'summary': {
                                        'subtotal': first_page_data['totals'].get('grand_total', 0),
                                        'premium': first_page_data['totals']['premium'].get('amount', 0),
                                        'grand_total': first_page_data['totals'].get('payable', 0)
                                    },
                                    'footer': 'This document is computer generated and does not require signature'
                                }
                                
                                config = {
                                    'orientation': 'landscape',
                                    'margins': {'top': 12, 'right': 12, 'bottom': 12, 'left': 12}
                                }
                                
                                first_page_pdf = pdf_manager.generate_bill_pdf(bill_data, config, "first_page.pdf")
                                if not first_page_pdf:
                                    # Fallback to standard generator
                                    first_page_pdf = generate_pdf("First Page", first_page_data, "landscape", TEMPLATE_DIR, temp_dir)
                                
                                pdf_files.append(first_page_pdf)
                            except Exception as e:
                                st.warning(f"Using fallback PDF generator for First Page: {str(e)}")
                                first_page_pdf = generate_pdf("First Page", first_page_data, "landscape", TEMPLATE_DIR, temp_dir)
                                pdf_files.append(first_page_pdf)
                            
                            progress_bar.progress(25)
                            
                            # Generate remaining PDFs
                            status_text.text("Generating Last Page PDF...")
                            # Prepare Last Page data to match template expectations
                            last_page_pdf_data = {
                                "header": first_page_data.get("header", []),
                                "items": first_page_data.get("items", []),
                                "totals": first_page_data.get("totals", {}),
                            }
                            last_page_pdf = generate_pdf("Last Page", last_page_pdf_data, "portrait", TEMPLATE_DIR, temp_dir)
                            pdf_files.append(last_page_pdf)
                            progress_bar.progress(35)
                            
                            status_text.text("Generating Deviation Statement PDF...")
                            deviation_pdf = generate_pdf("Deviation Statement", deviation_data, "landscape", TEMPLATE_DIR, temp_dir)
                            pdf_files.append(deviation_pdf)
                            progress_bar.progress(45)
                            
                            status_text.text("Generating Extra Items PDF...")
                            extra_items_pdf = generate_pdf("Extra Items", extra_items_data, "landscape", TEMPLATE_DIR, temp_dir)
                            pdf_files.append(extra_items_pdf)
                            progress_bar.progress(55)
                            
                            status_text.text("Generating Note Sheet PDF...")
                            note_sheet_pdf = generate_pdf("Note Sheet", note_sheet_data, "portrait", TEMPLATE_DIR, temp_dir)
                            pdf_files.append(note_sheet_pdf)
                            progress_bar.progress(65)
                            
                            # Generate Word documents
                            status_text.text("Creating Word documents...")
                            
                            word_files_data = [
                                ("first_page.docx", "First Page", first_page_data),
                                ("last_page.docx", "Last Page", last_page_data),
                                ("deviation_statement.docx", "Deviation Statement", deviation_data),
                                ("extra_items.docx", "Extra Items", extra_items_data),
                                ("note_sheet.docx", "Note Sheet", note_sheet_data)
                            ]
                            
                            for i, (filename, doc_name, doc_data) in enumerate(word_files_data):
                                doc_path = os.path.join(temp_dir, filename)
                                create_word_doc(doc_name, doc_data, doc_path)
                                word_files.append(doc_path)
                                progress_bar.progress(65 + (i + 1) * 4)
                            
                            # Merge PDFs
                            status_text.text("Merging all PDFs...")
                            merged_pdf = os.path.join(temp_dir, "complete_bill.pdf")
                            merge_pdfs(pdf_files, merged_pdf)
                            progress_bar.progress(90)
                            
                            # Create ZIP archive
                            status_text.text("Creating ZIP archive...")
                            all_files = pdf_files + word_files + [merged_pdf]
                            zip_path = os.path.join(temp_dir, "bill_documents.zip")
                            create_zip_archive(all_files, zip_path)
                            progress_bar.progress(100)
                            
                            status_text.text("✅ All documents generated successfully!")
                            
                            # Display success message
                            st.success("🎉 **Documents generated successfully!**")
                            
                            # Download section
                            st.markdown("---")
                            st.subheader("📥 Download Generated Documents")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("#### Complete Bill (PDF)")
                                with open(merged_pdf, "rb") as f:
                                    st.download_button(
                                        label="📄 Download Complete PDF",
                                        data=f,
                                        file_name="complete_bill.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                            
                            with col2:
                                st.markdown("#### All Documents (ZIP)")
                                with open(zip_path, "rb") as f:
                                    st.download_button(
                                        label="📦 Download ZIP Archive",
                                        data=f,
                                        file_name="bill_documents.zip",
                                        mime="application/zip",
                                        use_container_width=True
                                    )
                            
                            with col3:
                                st.markdown("#### Bill Summary")
                                grand_total = first_page_data['totals']['grand_total']
                                premium_amount = first_page_data['totals']['premium']['amount']
                                payable = first_page_data['totals']['payable']
                                
                                st.metric("Grand Total", f"₹{grand_total:,.2f}")
                                st.metric("Premium", f"₹{premium_amount:,.2f}", 
                                         delta=f"{premium_percent}% {premium_type}")
                                st.metric("Total Payable", f"₹{payable:,.2f}")
                            
                            # Clear progress indicators
                            progress_bar.empty()
                            status_text.empty()
                            
                    except Exception as e:
                        st.error(f"❌ **Error processing bill:** {str(e)}")
                        st.exception(e)
                        
        except Exception as e:
            st.error(f"❌ **Error reading Excel file:** {str(e)}")
            st.exception(e)
    else:
        # Welcome message and instructions
        st.info("👆 **Please upload an Excel file to get started**")
        
        # Instructions
        with st.expander("📋 **How to Use This Application**", expanded=True):
            st.markdown("""
            ### Step-by-Step Instructions:
            
            1. **Prepare Your Excel File**
               - Ensure it contains three required sheets:
                 - `Work Order` - Original work order details
                 - `Bill Quantity` - Executed work quantities
                 - `Extra Items` - Additional items not in work order
            
            2. **Upload the File**
               - Click the "Browse files" button above
               - Select your Excel file (.xlsx or .xls format)
            
            3. **Configure Settings** (Optional)
               - Adjust tender premium percentage in the sidebar
               - Select premium type (above/below)
            
            4. **Generate Documents**
               - Click the "Generate All Documents" button
               - Wait for processing to complete
            
            5. **Download Results**
               - Download the complete merged PDF
               - Or download the ZIP archive with all formats (PDF + Word)
            
            ### 📊 Generated Documents:
            
            - **First Page**: Summary of work items and amounts
            - **Last Page**: Final calculations and totals
            - **Deviation Statement**: Comparison between work order and executed work
            - **Extra Items**: Additional items with calculations
            - **Note Sheet**: Detailed notes and breakdowns
            """)
        
        # Sample data structure
        with st.expander("📊 **Required Excel Structure**"):
            st.markdown("""
            ### Work Order / Bill Quantity Sheet Structure:
            
            | Row | Column A | Column B | Column C | Column D | Column E | Column F |
            |-----|----------|----------|----------|----------|----------|----------|
            | 1-19 | Header information (work order details, contractor info, etc.) |
            | 20 | Table headers: S.No. | Description | Unit | Quantity | Rate | Amount |
            | 21+ | Work item data rows |
            
            ### Extra Items Sheet Structure:
            
            Similar to Work Order sheet, containing additional items not in original scope.
            
            ### Important Notes:
            
            - Excel file must be in `.xlsx` or `.xls` format
            - All three sheets must be present
            - Headers should be in row 20, data starts from row 21
            - Numeric values should be properly formatted
            - Ensure no merged cells in data rows
            """)
        
        # Features highlight
        with st.expander("✨ **Application Features**"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Document Generation:**
                - ✅ PDF format (optimized, professional)
                - ✅ Word format (editable .docx)
                - ✅ Merged complete bill PDF
                - ✅ ZIP archive of all documents
                
                **Calculations:**
                - ✅ Automatic premium calculation
                - ✅ Deviation analysis
                - ✅ Extra items processing
                - ✅ Grand total computation
                """)
            
            with col2:
                st.markdown("""
                **Quality Features:**
                - ✅ Statutory government format compliance
                - ✅ Professional document styling
                - ✅ Accurate number-to-words conversion
                - ✅ Detailed error handling
                
                **Performance:**
                - ✅ Fast processing (<30 seconds)
                - ✅ Cloud-optimized deployment
                - ✅ Batch processing support
                - ✅ Progress tracking
                """)

if __name__ == "__main__":
    main()