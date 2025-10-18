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
        from exports.renderers import generate_pdf, create_word_doc, merge_pdfs, create_zip_archive, setup_pdfkit_config, generate_html
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
            
            # Debug information
            st.write("Debug: File information")
            st.write(f"File name: {uploaded_file.name}")
            st.write(f"File size: {uploaded_file.size}")
            st.write(f"Work Order sheet shape: {ws_wo.shape}")
            st.write(f"Bill Quantity sheet shape: {ws_bq.shape}")
            st.write(f"Extra Items sheet shape: {ws_extra.shape}")
            
            # Show first few rows of each sheet for debugging
            st.write("Work Order sheet (first 5 rows):")
            st.dataframe(ws_wo.head())
            st.write("Bill Quantity sheet (first 5 rows):")
            st.dataframe(ws_bq.head())
            st.write("Extra Items sheet (first 5 rows):")
            st.dataframe(ws_extra.head())
            
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
                        # Setup pdfkit configuration
                        config = setup_pdfkit_config()
                        
                        # Process the bill using our core computation logic
                        first_page_data, last_page_data, deviation_data, extra_items_data, note_sheet_data = process_bill(
                            ws_wo, ws_bq, ws_extra, premium_percent, premium_type
                        )
                        
                        # Create temporary directory for outputs
                        with tempfile.TemporaryDirectory() as temp_dir:
                            pdf_files = []
                            word_files = []
                            html_files = []  # Add this line to store HTML files
                            
                            # Generate note sheet data like the original
                            try:
                                work_order_amount = sum(
                                    float(ws_wo.iloc[i, 3]) * float(ws_wo.iloc[i, 4])
                                    for i in range(21, ws_wo.shape[0])
                                    if pd.notnull(ws_wo.iloc[i, 3]) and pd.notnull(ws_wo.iloc[i, 4])
                                )
                            except Exception as e:
                                st.error(f"Error calculating work_order_amount: {e}")
                                work_order_amount = 854678  # Fallback value

                            extra_item_amount = first_page_data["totals"].get("extra_items_sum", 0)
                            payable_amount = first_page_data["totals"].get("payable", 0)
                            
                            # Prepare last_page_data with all required fields from first_page_data
                            last_page_data["header"] = first_page_data.get("header", [])
                            last_page_data["items"] = first_page_data.get("items", [])
                            last_page_data["totals"] = first_page_data.get("totals", {})
                            
                            # Generate note sheet using original logic
                            from datetime import datetime
                            
                            # Define work_order_data from ws_wo
                            work_order_data = {
                                'agreement_no': ws_wo.iloc[0, 1] if pd.notnull(ws_wo.iloc[0, 1]) else '48/2024-25',
                                'name_of_work': ws_wo.iloc[1, 1] if pd.notnull(ws_wo.iloc[1, 1]) else 'Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur',
                                'name_of_firm': ws_wo.iloc[2, 1] if pd.notnull(ws_wo.iloc[2, 1]) else 'M/s Seema Electrical Udaipur',
                                'date_commencement': ws_wo.iloc[3, 1] if pd.notnull(ws_wo.iloc[3, 1]) else '18/01/2025',
                                'date_completion': ws_wo.iloc[4, 1] if pd.notnull(ws_wo.iloc[4, 1]) else '17/04/2025',
                                'actual_completion': ws_wo.iloc[5, 1] if pd.notnull(ws_wo.iloc[5, 1]) else '01/03/2025',
                                'work_order_amount': str(work_order_amount)
                            }

                            # Prepare note_sheet_data with VBA-style notes
                            percentage_work_done = (float(payable_amount) / float(work_order_amount) * 100) if work_order_amount > 0 else 0
                            notes = [
                                f"1. The work has been completed {percentage_work_done:.2f}% of the Work Order Amount."
                            ]
                            if percentage_work_done < 90:
                                notes.append("2. The execution of work at final stage is less than 90% of the Work Order Amount, the Requisite Deviation Statement is enclosed to observe check on unuseful expenditure. Approval of the Deviation is having jurisdiction under this office.")
                            elif 100 < percentage_work_done <= 105:
                                notes.append("2. Requisite Deviation Statement is enclosed. The Overall Excess is less than or equal to 5% and is having approval jurisdiction under this office.")
                            elif percentage_work_done > 105:
                                notes.append("2. Requisite Deviation Statement is enclosed. The Overall Excess is more than 5% and Approval of the Deviation Case is required from the Superintending Engineer, PWD Electrical Circle, Udaipur.")
                            
                            try:
                                delay_days = (datetime.strptime(work_order_data['actual_completion'], '%d/%m/%Y') - datetime.strptime(work_order_data['date_completion'], '%d/%m/%Y')).days
                                if delay_days > 0:
                                    time_allowed = (datetime.strptime(work_order_data['date_completion'], '%d/%m/%Y') - datetime.strptime(work_order_data['date_commencement'], '%d/%m/%Y')).days
                                    notes.append(f"3. Time allowed for completion of the work was {time_allowed} days. The Work was delayed by {delay_days} days.")
                                    if delay_days > 0.5 * time_allowed:
                                        notes.append("4. Approval of the Time Extension Case is required from the Superintending Engineer, PWD Electrical Circle, Udaipur.")
                                    else:
                                        notes.append("4. Approval of the Time Extension Case is to be done by this office.")
                                else:
                                    notes.append("3. Work was completed in time.")
                            except:
                                notes.append("3. Work was completed in time.")
                                
                            if extra_item_amount > 0:
                                extra_item_percentage = (extra_item_amount / float(work_order_amount) * 100) if work_order_amount > 0 else 0
                                if extra_item_percentage > 5:
                                    notes.append(f"4. The amount of Extra items is Rs. {extra_item_amount} which is {extra_item_percentage:.2f}% of the Work Order Amount; exceed 5%, require approval from the Superintending Engineer, PWD Electrical Circle, Udaipur.")
                                else:
                                    notes.append(f"4. The amount of Extra items is Rs. {extra_item_amount} which is {extra_item_percentage:.2f}% of the Work Order Amount; under 5%, approval of the same is to be granted by this office.")
                            notes.extend([
                                "5. Quality Control (QC) test reports attached.",
                                "6. Please peruse above details for necessary decision-making.",
                                "",
                                "                                Premlata Jain",
                                "                               AAO- As Auditor"
                            ])

                            note_sheet_data = {
                                'agreement_no': work_order_data.get('agreement_no', '48/2024-25'),
                                'name_of_work': work_order_data.get('name_of_work', 'Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur'),
                                'name_of_firm': work_order_data.get('name_of_firm', 'M/s Seema Electrical Udaipur'),
                                'date_commencement': work_order_data.get('date_commencement', '18/01/2025'),
                                'date_completion': work_order_data.get('date_completion', '17/04/2025'),
                                'actual_completion': work_order_data.get('actual_completion', '01/03/2025'),
                                'work_order_amount': work_order_data.get('work_order_amount', '854678'),
                                'extra_item_amount': extra_item_amount,
                                'notes': notes,
                                'totals': first_page_data.get('totals', {'payable': str(payable_amount)})
                            }
                            
                            # Prepare Certificate II data
                            certificate_ii_data = {
                                'measurement_officer': 'Junior Engineer',
                                'measurement_date': work_order_data.get('actual_completion', '01/03/2025'),
                                'measurement_book_page': '04-20',
                                'measurement_book_no': '887',
                                'officer_name': 'Name of Officer',
                                'officer_designation': 'Assistant Engineer',
                                'bill_date': work_order_data.get('actual_completion', '01/03/2025'),
                                'authorising_officer_name': 'Name of Authorising Officer',
                                'authorising_officer_designation': 'Executive Engineer',
                                'authorisation_date': work_order_data.get('actual_completion', '01/03/2025')
                            }
                            
                            # Prepare Certificate III data
                            certificate_iii_data = {
                                'totals': first_page_data.get('totals', {}),
                                'payable_words': number_to_words(first_page_data['totals'].get('payable', 0))
                            }
                            
                            # Generate HTML files for all document types
                            html_files.append(generate_html("First Page", first_page_data, os.path.join(current_dir, "templates"), temp_dir))
                            html_files.append(generate_html("Certificate II", certificate_ii_data, os.path.join(current_dir, "templates"), temp_dir))
                            html_files.append(generate_html("Certificate III", certificate_iii_data, os.path.join(current_dir, "templates"), temp_dir))
                            html_files.append(generate_html("Deviation Statement", deviation_data, os.path.join(current_dir, "templates"), temp_dir))
                            html_files.append(generate_html("Note Sheet", note_sheet_data, os.path.join(current_dir, "templates"), temp_dir))
                            html_files.append(generate_html("Last Page", last_page_data, os.path.join(current_dir, "templates"), temp_dir))
                            html_files.append(generate_html("Extra Items", extra_items_data, os.path.join(current_dir, "templates"), temp_dir))
                            
                            # Generate PDFs using original approach
                            for sheet_name, data, orientation in [
                                ("First Page", first_page_data, "portrait"),
                                ("Certificate II", certificate_ii_data, "portrait"),
                                ("Certificate III", certificate_iii_data, "portrait"),
                                ("Deviation Statement", deviation_data, "landscape"),
                                ("Note Sheet", note_sheet_data, "portrait"),
                                ("Extra Items", extra_items_data, "portrait"),
                            ]:
                                pdf_path = generate_pdf(
                                    sheet_name, 
                                    data, 
                                    orientation, 
                                    os.path.join(current_dir, "templates"), 
                                    temp_dir,
                                    config
                                )
                                pdf_files.append(pdf_path)
                            
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
                            
                            # Create ZIP archive with PDFs, Word docs, and HTML files
                            all_files = pdf_files + word_files + html_files + [merged_pdf]
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