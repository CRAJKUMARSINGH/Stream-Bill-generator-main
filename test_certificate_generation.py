import pandas as pd
import os
import sys
import tempfile
from exports.renderers import generate_html, create_word_doc

def test_certificate_generation():
    """Test Certificate II and III generation"""
    
    # Add the current directory to the path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Test data for certificates
    certificate_ii_data = {
        "measurement_officer": "Junior Engineer",
        "measurement_date": "01/03/2025",
        "measurement_book_page": "04-20",
        "measurement_book_no": "887",
        "officer_name": "Name of Officer",
        "officer_designation": "Assistant Engineer",
        "authorising_officer_name": "Name of Authorising Officer",
        "authorising_officer_designation": "Executive Engineer",
        "bill_date": "01/03/2025",
        "authorisation_date": "01/03/2025"
    }
    
    certificate_iii_data = {
        "totals": {
            "grand_total": 100000,
            "payable": 110000
        },
        "payable_words": "One Lakh Ten Thousand Only"
    }
    
    # Create temporary directory for outputs
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test HTML generation
        try:
            certificate_ii_html = generate_html("Certificate II", certificate_ii_data, os.path.join(current_dir, "templates"), temp_dir)
            print(f"✅ Certificate II HTML generated: {certificate_ii_html}")
        except Exception as e:
            print(f"❌ Certificate II HTML generation failed: {e}")
            return False
            
        try:
            certificate_iii_html = generate_html("Certificate III", certificate_iii_data, os.path.join(current_dir, "templates"), temp_dir)
            print(f"✅ Certificate III HTML generated: {certificate_iii_html}")
        except Exception as e:
            print(f"❌ Certificate III HTML generation failed: {e}")
            return False
            
        # Test Word document generation
        try:
            certificate_ii_doc = os.path.join(temp_dir, "certificate_ii.docx")
            create_word_doc("Certificate II", certificate_ii_data, certificate_ii_doc)
            print(f"✅ Certificate II Word document generated: {certificate_ii_doc}")
        except Exception as e:
            print(f"❌ Certificate II Word document generation failed: {e}")
            return False
            
        try:
            certificate_iii_doc = os.path.join(temp_dir, "certificate_iii.docx")
            create_word_doc("Certificate III", certificate_iii_data, certificate_iii_doc)
            print(f"✅ Certificate III Word document generated: {certificate_iii_doc}")
        except Exception as e:
            print(f"❌ Certificate III Word document generation failed: {e}")
            return False
            
    print("✅ All certificate generation tests passed!")
    return True

if __name__ == "__main__":
    test_certificate_generation()