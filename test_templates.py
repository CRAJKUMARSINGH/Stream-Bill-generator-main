"""
Test script to verify that the updated templates work correctly
"""
import os
from jinja2 import Environment, FileSystemLoader

def test_template_rendering():
    """Test rendering of all templates with sample data"""
    # Set up Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Sample data for testing
    sample_data = {
        "first_page": {
            "header": [
                ["Name of Contractor or supplier", "M/s Seema Electrical Udaipur"],
                ["Name of Work", "Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur"],
                ["Serial No. of this bill", "887"],
                ["No. and date of the last bill", "886 Dt. 15-12-2024"],
                ["Reference to work order or Agreement", "1179 Dt. 09-01-2025"],
                ["Agreement No", "1179"],
                ["Date of written order to commence work", "09-01-2025"],
                ["St. date of Start", "09-01-2025"],
                ["St. date of completion", "09-04-2025"],
                ["Date of actual completion of work", "08-04-2025"],
                ["Date of measurement", "08-04-2025"],
                ["WORK ORDER AMOUNT RS.", "200000"]
            ],
            "bill_items": [
                {
                    "unit": "Nos",
                    "quantity_since": 10.0,
                    "quantity_upto": 10.0,
                    "serial_no": "1",
                    "description": "Repair of Ceiling Fan",
                    "rate": 150.0,
                    "amount_upto": 1500.0,
                    "amount_since": 1500.0,
                    "remark": "Good"
                }
            ],
            "extra_items": [
                {
                    "unit": "Nos",
                    "quantity_since": 5.0,
                    "quantity_upto": 5.0,
                    "serial_no": "1",
                    "description": "Additional Light Fitting",
                    "rate": 200.0,
                    "amount_upto": 1000.0,
                    "amount_since": 1000.0,
                    "remark": "Extra"
                }
            ],
            "extra_items_base": 1000.0,
            "tender_premium_percent": 0.05,
            "extra_premium": 50.0,
            "extra_items_sum": 1050.0,
            "bill_total": 1500.0,
            "bill_premium": 75.0,
            "bill_grand_total": 1575.0,
            "last_bill_amount": 0.0,
            "net_payable": 2625.0
        },
        "deviation_statement": {
            "header": [
                ["Agreement No", "1179"],
                ["Name of Contractor or supplier", "M/s Seema Electrical Udaipur"],
                ["Name of Work", "Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur"]
            ],
            "deviation_items": [
                {
                    "serial_no": "1",
                    "description": "Repair of Ceiling Fan",
                    "unit": "Nos",
                    "qty_wo": 12.0,
                    "rate": 150.0,
                    "amt_wo": 1800.0,
                    "qty_bill": 10.0,
                    "amt_bill": 1500.0,
                    "excess_qty": 0.0,
                    "excess_amt": 0.0,
                    "saving_qty": 2.0,
                    "saving_amt": 300.0,
                    "remark": "Less quantity executed"
                }
            ],
            "deviation_summary": {
                "work_order_total": 1800.0,
                "executed_total": 1500.0,
                "overall_excess": 0.0,
                "overall_saving": 300.0,
                "tender_premium_f": 90.0,
                "tender_premium_h": 75.0,
                "tender_premium_j": 0.0,
                "tender_premium_l": 0.0,
                "grand_total_f": 1890.0,
                "grand_total_h": 1575.0,
                "grand_total_j": 0.0,
                "grand_total_l": 0.0,
                "net_difference": -300.0
            },
            "tender_premium_percent": 0.05
        },
        "extra_items": {
            "extra_items": [
                {
                    "serial_no": "1",
                    "reference": "BSR No. 123",
                    "description": "Additional Light Fitting",
                    "quantity": 5.0,
                    "unit": "Nos",
                    "rate": 200.0,
                    "amount": 1000.0,
                    "remark": "Extra"
                }
            ],
            "grand_total": 1000.0,
            "tender_premium_percent": 0.05,
            "tender_premium": 50.0,
            "total_executed": 1050.0
        },
        "note_sheet": {
            "agreement_no": "1179",
            "name_of_work": "Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur",
            "name_of_firm": "M/s Seema Electrical Udaipur",
            "date_commencement": "09-01-2025",
            "date_completion": "09-04-2025",
            "actual_completion": "08-04-2025",
            "delay_days": 0,
            "work_order_amount": 200000.0,
            "bill_grand_total": 1575.0,
            "extra_items_sum": 1050.0,
            "totals": {
                "sd_amount": 0.0,
                "it_amount": 0.0,
                "gst_amount": 0.0,
                "lc_amount": 0.0,
                "liquidated_damages": 0.0,
                "net_payable": 2625.0
            }
        },
        "last_page": {
            "name_of_work": "Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur",
            "name_of_firm": "M/s Seema Electrical Udaipur",
            "agreement_no": "1179",
            "work_order_amount": 200000.0,
            "bill_total": 1500.0,
            "bill_premium": 75.0,
            "bill_grand_total": 1575.0,
            "extra_items_base": 1000.0,
            "extra_premium": 50.0,
            "extra_items_sum": 1050.0,
            "last_bill_amount": 0.0,
            "net_payable": 2625.0,
            "amount_words": "Two Thousand Six Hundred Twenty Five Rupees Only"
        }
    }
    
    # Test rendering each template
    templates = [
        ("first_page.html", sample_data["first_page"]),
        ("deviation_statement.html", sample_data["deviation_statement"]),
        ("extra_items.html", sample_data["extra_items"]),
        ("note_sheet.html", sample_data["note_sheet"]),
        ("last_page.html", sample_data["last_page"])
    ]
    
    success = True
    for template_name, data in templates:
        try:
            template = env.get_template(template_name)
            rendered = template.render(data=data)
            print(f"✅ {template_name} rendered successfully ({len(rendered)} characters)")
        except Exception as e:
            print(f"❌ {template_name} rendering failed: {e}")
            success = False
    
    return success

if __name__ == "__main__":
    print("Testing Template Rendering...")
    print("=" * 40)
    
    success = test_template_rendering()
    
    if success:
        print("\n🎉 All templates rendered successfully!")
        exit(0)
    else:
        print("\n❌ Some templates failed to render!")
        exit(1)