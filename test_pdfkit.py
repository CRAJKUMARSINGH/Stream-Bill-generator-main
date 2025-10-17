"""
Test if pdfkit is working with wkhtmltopdf
"""
import pdfkit
import platform
import os

def test_pdfkit():
    """Test if pdfkit can generate a simple PDF"""
    print("Testing pdfkit with wkhtmltopdf...")
    
    # Configure wkhtmltopdf
    if platform.system() == "Windows":
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if os.path.exists(wkhtmltopdf_path):
            print(f"✓ Found wkhtmltopdf at: {wkhtmltopdf_path}")
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        else:
            print(f"✗ wkhtmltopdf not found at: {wkhtmltopdf_path}")
            return False
    else:
        config = pdfkit.configuration()
    
    # Test HTML content
    html_content = """
    <html>
    <head>
        <title>Test PDF</title>
    </head>
    <body>
        <h1>PDF Generation Test</h1>
        <p>This is a test to see if pdfkit is working correctly.</p>
    </body>
    </html>
    """
    
    # Try to generate a PDF
    try:
        output_path = "test_output.pdf"
        pdfkit.from_string(html_content, output_path, configuration=config)
        print("✓ PDF generated successfully!")
        
        # Check if file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✓ Output file created: {output_path} ({file_size} bytes)")
            # Clean up
            os.remove(output_path)
            print("✓ Test file cleaned up")
            return True
        else:
            print("✗ Output file was not created")
            return False
            
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("PDFKit and wkhtmltopdf Test")
    print("=" * 30)
    print()
    
    success = test_pdfkit()
    
    print()
    if success:
        print("✅ PDFKit test passed!")
        print("The issue is likely not with PDF generation.")
    else:
        print("❌ PDFKit test failed!")
        print("There may be an issue with wkhtmltopdf installation or configuration.")

if __name__ == "__main__":
    main()