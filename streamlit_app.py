"""
Streamlit Cloud Optimized Version of Stream Bill Generator
This version is specifically designed for Streamlit Cloud deployment with proper import handling
"""
import streamlit as st
import pandas as pd
import os
import sys
import tempfile
from io import BytesIO

# Add the current directory to the path for Streamlit Cloud
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    st.set_page_config(
        page_title="Stream Bill Generator",
        page_icon="📋",
        layout="wide"
    )
    
    st.title("📋 Stream Bill Generator")
    st.markdown("""
    Generate contractor bills, deviation statements, and related documents from Excel data.
    """)
    
    # Try to import the core modules with robust error handling
    try:
        from core.computations.bill_processor import process_bill, safe_float, number_to_words
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive
        from core.streamlit_pdf_integration import StreamlitPDFManager
        st.success("✅ All modules imported successfully!")
    except Exception as e:
        st.error(f"❌ Module import failed: {str(e)}")
        st.info("This app requires specific dependencies. Please check requirements.txt")
        return
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Excel file with Work Order, Bill Quantity, and Extra Items sheets",
        type=["xlsx", "xls"],
        key="excel_upload"
    )
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            xl_file = pd.ExcelFile(uploaded_file)
            sheet_names = xl_file.sheet_names
            
            # Check required sheets
            required_sheets = ["Work Order", "Bill Quantity", "Extra Items"]
            missing_sheets = [sheet for sheet in required_sheets if sheet not in sheet_names]
            
            if missing_sheets:
                st.error(f"Missing required sheets: {', '.join(missing_sheets)}")
                return
            
            # Read sheets
            ws_wo = pd.read_excel(xl_file, "Work Order", header=None)
            ws_bq = pd.read_excel(xl_file, "Bill Quantity", header=None)
            ws_extra = pd.read_excel(xl_file, "Extra Items", header=None)
            
            # Premium settings
            st.sidebar.header("Premium Settings")
            premium_percent = st.sidebar.number_input(
                "Tender Premium (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=5.0, 
                step=0.1
            )
            
            premium_type = st.sidebar.radio(
                "Premium Type",
                ["above", "below"],
                index=0
            )
            
            # Process bill
            if st.button("Generate Documents", type="primary"):
                with st.spinner("Processing bill and generating documents..."):
                    try:
                        # Process the bill using our core computation logic
                        first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
                            ws_wo, ws_bq, ws_extra, premium_percent, premium_type
                        )
                        
                        # Create temporary directory for outputs
                        with tempfile.TemporaryDirectory() as temp_dir:
                            pdf_files = []
                            word_files = []
                            
                            # Initialize PDF manager
                            pdf_manager = StreamlitPDFManager()
                            
                            # Prepare bill data for PDF generation
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
                            
                            # PDF configuration
                            config = {
                                'orientation': 'landscape',
                                'margins': {
                                    'top': 12,
                                    'right': 12,
                                    'bottom': 12,
                                    'left': 12
                                }
                            }
                            
                            # Generate First Page using optimized PDF generator
                            try:
                                first_page_pdf = pdf_manager.generate_bill_pdf(
                                    bill_data, 
                                    config, 
                                    "first_page.pdf"
                                )
                                if first_page_pdf:
                                    pdf_files.append(first_page_pdf)
                                else:
                                    # Fallback to original implementation
                                    st.warning("Optimized PDF generation failed for First Page, using fallback")
                                    first_page_pdf = generate_pdf(
                                        "First Page", 
                                        first_page_data, 
                                        "landscape", 
                                        os.path.join(current_dir, "templates"), 
                                        temp_dir
                                    )
                                    pdf_files.append(first_page_pdf)
                            except Exception as e:
                                # Fallback to original implementation
                                st.warning(f"Optimized PDF generation failed for First Page, using fallback: {e}")
                                first_page_pdf = generate_pdf(
                                    "First Page", 
                                    first_page_data, 
                                    "landscape", 
                                    os.path.join(current_dir, "templates"), 
                                    temp_dir
                                )
                                pdf_files.append(first_page_pdf)
                            
                            # Create Word documents
                            first_page_doc = os.path.join(temp_dir, "first_page.docx")
                            create_word_doc("First Page", first_page_data, first_page_doc)
                            word_files.append(first_page_doc)
                            
                            last_page_doc = os.path.join(temp_dir, "last_page.docx")
                            create_word_doc("Last Page", last_page_data, last_page_doc)
                            word_files.append(last_page_doc)
                            
                            deviation_doc = os.path.join(temp_dir, "deviation_statement.docx")
                            create_word_doc("Deviation Statement", deviation_data, deviation_doc)
                            word_files.append(deviation_doc)
                            
                            extra_items_doc = os.path.join(temp_dir, "extra_items.docx")
                            create_word_doc("Extra Items", extra_items_data, extra_items_doc)
                            word_files.append(extra_items_doc)
                            
                            note_sheet_doc = os.path.join(temp_dir, "note_sheet.docx")
                            create_word_doc("Note Sheet", note_sheet_data, note_sheet_doc)
                            word_files.append(note_sheet_doc)
                            
                            # Merge all PDFs
                            merged_pdf = os.path.join(temp_dir, "complete_bill.pdf")
                            merge_pdfs(pdf_files, merged_pdf)
                            
                            # Create ZIP archive
                            all_files = pdf_files + word_files + [merged_pdf]
                            zip_path = os.path.join(temp_dir, "bill_documents.zip")
                            create_zip_archive(all_files, zip_path)
                            
                            # Display results
                            st.success("Documents generated successfully!")
                            
                            # Provide download buttons
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                with open(merged_pdf, "rb") as f:
                                    st.download_button(
                                        label="📥 Download Complete PDF",
                                        data=f,
                                        file_name="complete_bill.pdf",
                                        mime="application/pdf"
                                    )
                            
                            with col2:
                                with open(zip_path, "rb") as f:
                                    st.download_button(
                                        label="📦 Download All Documents (ZIP)",
                                        data=f,
                                        file_name="bill_documents.zip",
                                        mime="application/zip"
                                    )
                            
                            with col3:
                                # Show summary
                                st.subheader("Bill Summary")
                                st.metric("Grand Total", f"₹{first_page_data['totals']['grand_total']:,}")
                                st.metric("Tender Premium", f"₹{first_page_data['totals']['premium']['amount']:,}")
                                st.metric("Payable Amount", f"₹{first_page_data['totals']['payable']:,}")
                                
                    except Exception as e:
                        st.error(f"Error processing bill: {str(e)}")
                        st.exception(e)
                        
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
            st.exception(e)
    else:
        st.info("👆 Please upload an Excel file to get started")
        
        # Show instructions
        with st.expander("📋 Instructions"):
            st.markdown("""
            ### How to use this application:
            
            1. Prepare an Excel file with the following sheets:
               - **Work Order**: Contains work order details
               - **Bill Quantity**: Contains executed work quantities
               - **Extra Items**: Contains additional items
               
            2. Upload the Excel file using the file uploader above
            
            3. Adjust the tender premium settings in the sidebar if needed
               - Default premium: 5%
               - Premium type: Above (added to total)
               
            4. Click "Generate Documents" to create all required documents
            
            5. Download the generated documents:
               - Complete PDF (all pages merged)
               - ZIP archive with all formats (PDF and Word)
            """)
            
        # Show sample data structure
        with st.expander("📊 Sample Data Structure"):
            st.markdown("""
            The Excel file should have the following structure:
            
            **Work Order Sheet:**
            - Columns: Serial No., Description, Unit, Quantity, Rate, Amount, Remark
            - Rows 1-19: Header information
            - Row 21 onwards: Work items
            
            **Bill Quantity Sheet:**
            - Same structure as Work Order
            - Contains actual executed quantities
            
            **Extra Items Sheet:**
            - Contains additional items not in the original work order
            """)

if __name__ == "__main__":
    main()