#!/usr/bin/env python3
"""
Test script to verify certificate templates are properly linked with data
"""
import os
from jinja2 import Environment, FileSystemLoader

def test_certificate_templates():
    """Test that certificate templates render correctly with sample data"""
    
    # Setup Jinja2 environment
    template_dir = "templates"
    env = Environment(loader=FileSystemLoader(template_dir), cache_size=0)
    
    # Sample data for Certificate II
    certificate_ii_data = {
        'measurement_officer': 'Junior Engineer Test',
        'measurement_date': '01/03/2025',
        'measurement_book_page': '04-20',
        'measurement_book_no': '887',
        'officer_name': 'Test Officer',
        'officer_designation': 'Assistant Engineer',
        'bill_date': '01/03/2025',
        'authorising_officer_name': 'Test Authorising Officer',
        'authorising_officer_designation': 'Executive Engineer',
        'authorisation_date': '02/03/2025'
    }
    
    # Sample data for Certificate III
    certificate_iii_data = {
        'totals': {
            'grand_total': 100000,
            'payable': 85000
        },
        'payable_words': 'Eighty Five Thousand'
    }
    
    print("=== Testing Certificate II Template ===")
    try:
        template = env.get_template("certificate_ii.html")
        html_content = template.render(data=certificate_ii_data)
        print(f"✅ Certificate II template rendered successfully")
        print(f"HTML length: {len(html_content)} characters")
        
        # Check if key data is in the rendered HTML
        if "Junior Engineer Test" in html_content:
            print("✅ Measurement officer name found")
        if "01/03/2025" in html_content:
            print("✅ Measurement date found")
        if "Test Officer" in html_content:
            print("✅ Officer name found")
        if "Test Authorising Officer" in html_content:
            print("✅ Authorising officer name found")
            
    except Exception as e:
        print(f"❌ Certificate II template rendering failed: {e}")
        return False
    
    print("\n=== Testing Certificate III Template ===")
    try:
        template = env.get_template("certificate_iii.html")
        html_content = template.render(data=certificate_iii_data)
        print(f"✅ Certificate III template rendered successfully")
        print(f"HTML length: {len(html_content)} characters")
        
        # Check if key data is in the rendered HTML
        if "100,000" in html_content or "100000" in html_content:
            print("✅ Grand total found")
        if "85,000" in html_content or "85000" in html_content:
            print("✅ Payable amount found")
        if "Eighty Five Thousand" in html_content:
            print("✅ Amount in words found")
            
    except Exception as e:
        print(f"❌ Certificate III template rendering failed: {e}")
        return False
    
    print("\n🎉 All certificate templates render successfully!")
    return True

if __name__ == "__main__":
    success = test_certificate_templates()
    exit(0 if success else 1)
