"""
Test script to verify that the original templates work correctly
"""
import os
from jinja2 import Environment, FileSystemLoader

def test_original_template_rendering():
    """Test rendering of all original templates with sample data"""
    # Set up Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Sample data for testing (matching the original data structure)
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
            "items": [
                {
                    "unit": "Nos",
                    "quantity_since_last": "10.00",
                    "quantity_upto_date": "10.00",
                    "serial_no": "1",
                    "description": "Repair of Ceiling Fan",
                    "rate": "150.00",
                    "amount": "1500.00",
                    "amount_previous": "0.00",
                    "remark": "Good"
                }
            ],
            "totals": {
                "grand_total": "1500.00",
                "premium": {
                    "percent": 0.05,
                    "amount": "75.00"
                },
                "extra_items_sum": 0,
                "payable": "1575.00"
            }
        },
        "deviation_statement": {
            "items": [
                {
                    "serial_no": "1",
                    "description": "Repair of Ceiling Fan",
                    "unit": "Nos",
                    "qty_wo": "12.00",
                    "rate": "150.00",
                    "amt_wo": "1800.00",
                    "qty_bill": "10.00",
                    "amt_bill": "1500.00",
                    "excess_qty": "0.00",
                    "excess_amt": "0.00",
                    "saving_qty": "2.00",
                    "saving_amt": "300.00",
                    "remark": "Less quantity executed"
                }
            ],
            "summary": {
                "work_order_total": "1800.00",
                "executed_total": "1500.00",
                "overall_excess": "0.00",
                "overall_saving": "300.00",
                "premium": {
                    "percent": 0.05
                },
                "tender_premium_f": "90.00",
                "tender_premium_h": "75.00",
                "tender_premium_j": "0.00",
                "tender_premium_l": "0.00",
                "grand_total_f": "1890.00",
                "grand_total_h": "1575.00",
                "grand_total_j": "0.00",
                "grand_total_l": "0.00",
                "net_difference": "-300.00"
            }
        },
        "extra_items": {
            "items": [
                {
                    "serial_no": "1",
                    "remark": "Extra",
                    "description": "Additional Light Fitting",
                    "quantity": "5.00",
                    "unit": "Nos",
                    "rate": "200.00",
                    "amount": "1000.00"
                }
            ]
        },
        "last_page": {
            "header": [
                ["Agreement No", "1179"]
            ],
            "items": [
                {
                    "unit": "Nos",
                    "quantity": "10.00",
                    "serial_no": "1",
                    "description": "Repair of Ceiling Fan",
                    "rate": "150.00",
                    "amount": "1500.00",
                    "remark": "Good"
                }
            ],
            "totals": {
                "grand_total": "1500.00",
                "premium": {
                    "percent": 0.05,
                    "amount": "75.00"
                },
                "payable": "1575.00"
            }
        },
        "note_sheet": {
            "agreement_no": "1179",
            "name_of_work": "Electric Repair and MTC work at Govt. Ambedkar hostel Ambamata, Govardhanvilas, Udaipur",
            "name_of_firm": "M/s Seema Electrical Udaipur",
            "date_commencement": "09-01-2025",
            "date_completion": "09-04-2025",
            "actual_completion": "08-04-2025",
            "work_order_amount": "200000",
            "totals": {
                "payable": "1575"
            },
            "extra_item_amount": 0,
            "notes": [
                "1. The work has been completed 131.06% of the Work Order Amount.",
                "2. Requisite Deviation Statement is enclosed. The Overall Saving is 16.67% under 5%, approval of the same is to be granted by this office.",
                "3. Work was completed with delay of 18 days.",
                "5. Quality Control (QC) test reports attached.",
                "6. Please peruse above details for necessary decision-making."
            ]
        }
    }
    
    # Test rendering each template
    templates = [
        ("first_page.html", sample_data["first_page"]),
        ("deviation_statement.html", sample_data["deviation_statement"]),
        ("extra_items.html", sample_data["extra_items"]),
        ("last_page.html", sample_data["last_page"]),
        ("note_sheet.html", sample_data["note_sheet"])
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
    print("Testing Original Template Rendering...")
    print("=" * 40)
    
    success = test_original_template_rendering()
    
    if success:
        print("\n🎉 All original templates rendered successfully!")
        exit(0)
    else:
        print("\n❌ Some original templates failed to render!")
        exit(1)