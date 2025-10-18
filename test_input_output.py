#!/usr/bin/env python3
"""
Test script to verify that different inputs produce different outputs
"""

import os
import sys
import tempfile
import pandas as pd
from io import BytesIO

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def create_test_excel_data(work_order_value=100, bill_quantity_value=100, extra_items_value=50):
    """Create test Excel data with specified values"""
    
    # Create Work Order sheet
    work_order_data = []
    # Add header rows (A1:G19)
    for i in range(19):
        work_order_data.append([f"Header{i}", f"Value{i}", "", "", "", "", ""])
    
    # Add data rows (starting from row 22, which is index 21)
    for i in range(21, 30):
        work_order_data.append([
            f"Item{i-20}",  # Serial No
            f"Description for item {i-20}",  # Description
            "Unit",  # Unit
            work_order_value,  # Quantity
            10.0,  # Rate
            work_order_value * 10.0,  # Amount
            f"Remark {i-20}"  # Remark
        ])
    
    work_order_df = pd.DataFrame(work_order_data)
    
    # Create Bill Quantity sheet (similar structure)
    bill_quantity_data = []
    # Add header rows (A1:G19)
    for i in range(19):
        bill_quantity_data.append([f"Header{i}", f"Value{i}", "", "", "", "", ""])
    
    # Add data rows (starting from row 22, which is index 21)
    for i in range(21, 30):
        bill_quantity_data.append([
            f"Item{i-20}",  # Serial No
            f"Description for item {i-20}",  # Description
            "Unit",  # Unit
            bill_quantity_value,  # Quantity
            10.0,  # Rate
            bill_quantity_value * 10.0,  # Amount
            f"Remark {i-20}"  # Remark
        ])
    
    bill_quantity_df = pd.DataFrame(bill_quantity_data)
    
    # Create Extra Items sheet
    extra_items_data = []
    # Add header rows (A1:G5)
    for i in range(5):
        extra_items_data.append([f"Header{i}", f"Value{i}", "", "", "", "", ""])
    
    # Add data rows (starting from row 7, which is index 6)
    for i in range(6, 10):
        extra_items_data.append([
            f"Extra{i-5}",  # Serial No
            f"Extra remark {i-5}",  # Remark
            f"Extra description {i-5}",  # Description
            extra_items_value,  # Quantity
            "Unit",  # Unit
            15.0,  # Rate
            extra_items_value * 15.0  # Amount
        ])
    
    extra_items_df = pd.DataFrame(extra_items_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        work_order_df.to_excel(writer, sheet_name='Work Order', index=False, header=False)
        bill_quantity_df.to_excel(writer, sheet_name='Bill Quantity', index=False, header=False)
        extra_items_df.to_excel(writer, sheet_name='Extra Items', index=False, header=False)
    
    output.seek(0)
    return output

def test_different_inputs():
    """Test that different inputs produce different outputs"""
    
    try:
        from core.computations.bill_processor import process_bill
        from exports.renderers import generate_html
        
        # Test with first set of values
        print("Testing with first set of values...")
        excel_data_1 = create_test_excel_data(100, 100, 50)
        xl_file_1 = pd.ExcelFile(excel_data_1)
        ws_wo_1 = pd.read_excel(xl_file_1, "Work Order", header=None)
        ws_bq_1 = pd.read_excel(xl_file_1, "Bill Quantity", header=None)
        ws_extra_1 = pd.read_excel(xl_file_1, "Extra Items", header=None)
        
        first_page_data_1, last_page_data_1, deviation_data_1, extra_items_data_1, note_sheet_data_1 = process_bill(
            ws_wo_1, ws_bq_1, ws_extra_1, 5.0, "above"
        )
        
        # Test with second set of values
        print("Testing with second set of values...")
        excel_data_2 = create_test_excel_data(200, 150, 75)
        xl_file_2 = pd.ExcelFile(excel_data_2)
        ws_wo_2 = pd.read_excel(xl_file_2, "Work Order", header=None)
        ws_bq_2 = pd.read_excel(xl_file_2, "Bill Quantity", header=None)
        ws_extra_2 = pd.read_excel(xl_file_2, "Extra Items", header=None)
        
        first_page_data_2, last_page_data_2, deviation_data_2, extra_items_data_2, note_sheet_data_2 = process_bill(
            ws_wo_2, ws_bq_2, ws_extra_2, 5.0, "above"
        )
        
        # Compare the data
        print("\nComparing results...")
        print(f"First Page Data 1 Grand Total: {first_page_data_1['totals'].get('grand_total', 0)}")
        print(f"First Page Data 2 Grand Total: {first_page_data_2['totals'].get('grand_total', 0)}")
        
        # Check if the totals are different
        if first_page_data_1['totals'].get('grand_total', 0) != first_page_data_2['totals'].get('grand_total', 0):
            print("✅ Different inputs produce different outputs - this is correct behavior")
            return True
        else:
            print("❌ Different inputs produce the same outputs - this is incorrect behavior")
            return False
            
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

if __name__ == "__main__":
    test_different_inputs()