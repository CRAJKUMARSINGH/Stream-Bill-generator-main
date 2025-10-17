"""
Minimal Streamlit App for Testing Streamlit Cloud Deployment
This version has minimal dependencies to ensure successful deployment
"""
import streamlit as st
import pandas as pd
import os

def main():
    st.set_page_config(
        page_title="Stream Bill Generator - Minimal Version",
        page_icon="📋",
        layout="wide"
    )
    
    st.title("📋 Stream Bill Generator - Minimal Version")
    st.markdown("""
    This is a minimal version of the Stream Bill Generator to test Streamlit Cloud deployment.
    """)
    
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
            st.success(f"✅ Successfully uploaded file with sheets: {', '.join(xl_file.sheet_names)}")
            
            # Show file info
            st.info(f"File name: {uploaded_file.name}")
            st.info(f"File size: {uploaded_file.size} bytes")
            
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
            
            3. The app will display information about your file
            """)

if __name__ == "__main__":
    main()