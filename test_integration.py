"""
Integration Testing Script
Tests PDF generation with various scenarios to ensure quality
"""

import os
import sys
from datetime import datetime
from pdf_generator_optimized import PDFGenerator
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class PDFTester:
    """Comprehensive PDF testing"""
    
    def __init__(self):
        self.test_results = []
        self.output_dir = "test_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.test_results.append({
            'test': test_name,
            'status': status,
            'passed': passed,
            'message': message
        })
        print(f"{status}: {test_name}")
        if message:
            print(f"   → {message}")
    
    def test_portrait_12mm_margins(self):
        """Test portrait orientation with 12mm margins"""
        try:
            generator = PDFGenerator(orientation='portrait')
            
            html = generator.generate_html_template(
                title="TEST: Portrait 12mm Margins",
                subtitle="A4 Portrait - 12mm margins all around",
                content="<p>This is a test of portrait orientation with 12mm margins.</p>",
                footer="Test document"
            )
            
            output_path = os.path.join(self.output_dir, "test_portrait_12mm.pdf")
            success = generator.generate_pdf(html, output_path)
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                self.log_result(
                    "Portrait 12mm Margins",
                    True,
                    f"Generated {file_size} bytes"
                )
            else:
                self.log_result("Portrait 12mm Margins", False, "PDF not generated")
                
        except Exception as e:
            self.log_result("Portrait 12mm Margins", False, str(e))
    
    def test_landscape_15mm_margins(self):
        """Test landscape orientation with 15mm margins"""
        try:
            generator = PDFGenerator(
                orientation='landscape',
                custom_margins={'top': 15, 'right': 15, 'bottom': 15, 'left': 15}
            )
            
            html = generator.generate_html_template(
                title="TEST: Landscape 15mm Margins",
                subtitle="A4 Landscape - 15mm margins all around",
                content="<p>This is a test of landscape orientation with 15mm margins.</p>",
                footer="Test document"
            )
            
            output_path = os.path.join(self.output_dir, "test_landscape_15mm.pdf")
            success = generator.generate_pdf(html, output_path)
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                self.log_result(
                    "Landscape 15mm Margins",
                    True,
                    f"Generated {file_size} bytes"
                )
            else:
                self.log_result("Landscape 15mm Margins", False, "PDF not generated")
                
        except Exception as e:
            self.log_result("Landscape 15mm Margins", False, str(e))
    
    def test_complex_bill(self):
        """Test complex infrastructure bill with tables"""
        try:
            generator = PDFGenerator(orientation='portrait')
            
            # Create complex bill content
            content = """
            <table>
                <thead>
                    <tr>
                        <th style="width: 5%;">S.No.</th>
                        <th style="width: 45%;">Description of Work</th>
                        <th style="width: 10%;">Unit</th>
                        <th style="width: 12%;">Quantity</th>
                        <th style="width: 13%;">Rate (₹)</th>
                        <th style="width: 15%;">Amount (₹)</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            # Add 20 rows to test pagination
            for i in range(1, 21):
                content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>Test work item number {i} - Earthwork excavation and filling</td>
                        <td>Cum</td>
                        <td class="numeric">{100 + i * 50:,.2f}</td>
                        <td class="numeric">{150.50 + i * 10:,.2f}</td>
                        <td class="numeric">{(100 + i * 50) * (150.50 + i * 10):,.2f}</td>
                    </tr>
                """
            
            content += """
                </tbody>
            </table>
            
            <div class="summary-section">
                <div class="summary-row">
                    <span class="summary-label">Sub Total:</span>
                    <span class="summary-value">₹ 12,45,678.90</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Tender Premium (8%):</span>
                    <span class="summary-value">₹ 99,654.31</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">GST @ 18%:</span>
                    <span class="summary-value">₹ 2,42,159.98</span>
                </div>
                <div class="grand-total">
                    <div style="display: flex; justify-content: space-between;">
                        <span>GRAND TOTAL:</span>
                        <span>₹ 14,87,493.19</span>
                    </div>
                </div>
            </div>
            
            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-line">
                        <strong>Contractor's Signature</strong><br>
                        Date: ______________
                    </div>
                </div>
                <div class="signature-box">
                    <div class="signature-line">
                        <strong>Engineer-in-Charge</strong><br>
                        Date: ______________
                    </div>
                </div>
            </div>
            """
            
            html = generator.generate_html_template(
                title="INFRASTRUCTURE BILL - COMPLEX TEST",
                subtitle="Work Order No: WO/TEST/2025 | Project: Highway Construction Phase II",
                content=content,
                footer=f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Page 1 of 1"
            )
            
            output_path = os.path.join(self.output_dir, "test_complex_bill.pdf")
            success = generator.generate_pdf(html, output_path)
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024  # KB
                self.log_result(
                    "Complex Bill with 20 Rows",
                    True,
                    f"Generated {file_size:.2f} KB"
                )
            else:
                self.log_result("Complex Bill with 20 Rows", False, "PDF not generated")
                
        except Exception as e:
            self.log_result("Complex Bill with 20 Rows", False, str(e))
    
    def test_minimum_margins(self):
        """Test minimum margins (10mm)"""
        try:
            generator = PDFGenerator(
                orientation='portrait',
                custom_margins={'top': 10, 'right': 10, 'bottom': 10, 'left': 10}
            )
            
            # Calculate expected content area
            expected_width = 210 - 10 - 10  # 190mm
            expected_height = 297 - 10 - 10  # 277mm
            
            html = generator.generate_html_template(
                title="TEST: Minimum Margins (10mm)",
                subtitle=f"Expected content area: {expected_width}mm × {expected_height}mm",
                content="<p>Testing minimum margins for maximum page utilization.</p>",
                footer="Minimum margin test"
            )
            
            output_path = os.path.join(self.output_dir, "test_min_margins.pdf")
            success = generator.generate_pdf(html, output_path)
            
            if success:
                utilization = (expected_width * expected_height) / (210 * 297) * 100
                self.log_result(
                    "Minimum Margins (10mm)",
                    True,
                    f"Page utilization: {utilization:.1f}%"
                )
            else:
                self.log_result("Minimum Margins (10mm)", False)
                
        except Exception as e:
            self.log_result("Minimum Margins (10mm)", False, str(e))
    
    def test_maximum_margins(self):
        """Test maximum practical margins (15mm)"""
        try:
            generator = PDFGenerator(
                orientation='portrait',
                custom_margins={'top': 15, 'right': 15, 'bottom': 15, 'left': 15}
            )
            
            # Calculate expected content area
            expected_width = 210 - 15 - 15  # 180mm
            expected_height = 297 - 15 - 15  # 267mm
            
            html = generator.generate_html_template(
                title="TEST: Maximum Margins (15mm)",
                subtitle=f"Expected content area: {expected_width}mm × {expected_height}mm",
                content="<p>Testing maximum practical margins while maintaining good readability.</p>",
                footer="Maximum margin test"
            )
            
            output_path = os.path.join(self.output_dir, "test_max_margins.pdf")
            success = generator.generate_pdf(html, output_path)
            
            if success:
                utilization = (expected_width * expected_height) / (210 * 297) * 100
                self.log_result(
                    "Maximum Margins (15mm)",
                    True,
                    f"Page utilization: {utilization:.1f}%"
                )
            else:
                self.log_result("Maximum Margins (15mm)", False)
                
        except Exception as e:
            self.log_result("Maximum Margins (15mm)", False, str(e))
    
    def test_all_engines(self):
        """Test all available PDF engines"""
        generator = PDFGenerator(orientation='portrait')
        
        for engine in generator.available_engines:
            try:
                html = generator.generate_html_template(
                    title=f"TEST: {engine.upper()} Engine",
                    subtitle=f"Testing PDF generation with {engine}",
                    content=f"<p>This PDF was generated using the {engine} engine.</p>",
                    footer=f"Generated with {engine}"
                )
                
                output_path = os.path.join(self.output_dir, f"test_engine_{engine}.pdf")
                success = generator.html_to_pdf_weasyprint(html, output_path) if engine == 'weasyprint' \
                    else generator.html_to_pdf_reportlab(html, output_path) if engine == 'reportlab' \
                    else generator.html_to_pdf_xhtml2pdf(html, output_path) if engine == 'xhtml2pdf' \
                    else generator.html_to_pdf_pdfkit(html, output_path) if engine == 'pdfkit' \
                    else False
                
                if success:
                    self.log_result(f"Engine Test: {engine}", True)
                else:
                    self.log_result(f"Engine Test: {engine}", False)
                    
            except Exception as e:
                self.log_result(f"Engine Test: {engine}", False, str(e))
    
    def test_unicode_support(self):
        """Test Unicode support including Indian Rupee symbol"""
        try:
            generator = PDFGenerator(orientation='portrait')
            
            content = """
            <p>Testing Unicode support:</p>
            <ul>
                <li>Indian Rupee symbol: ₹</li>
                <li>Copyright symbol: ©</li>
                <li>Registered trademark: ®</li>
                <li>Degree symbol: °</li>
                <li>Mathematical symbols: ∑ ∫ ∞</li>
            </ul>
            """
            
            html = generator.generate_html_template(
                title="TEST: Unicode Support",
                subtitle="Testing special characters and symbols",
                content=content,
                footer="Unicode test document"
            )
            
            output_path = os.path.join(self.output_dir, "test_unicode.pdf")
            success = generator.generate_pdf(html, output_path)
            
            if success:
                self.log_result("Unicode Support", True)
            else:
                self.log_result("Unicode Support", False)
                
        except Exception as e:
            self.log_result("Unicode Support", False, str(e))
    
    def run_all_tests(self):
        """Run all tests and display results"""
        print("🧪 Running PDF Integration Tests...\n")
        
        # Run all tests
        self.test_portrait_12mm_margins()
        self.test_landscape_15mm_margins()
        self.test_complex_bill()
        self.test_minimum_margins()
        self.test_maximum_margins()
        self.test_all_engines()
        self.test_unicode_support()
        
        # Display summary
        print("\n" + "="*50)
        print("📊 TEST RESULTS SUMMARY")
        print("="*50)
        
        passed = sum(1 for result in self.test_results if result['passed'])
        total = len(self.test_results)
        
        for result in self.test_results:
            print(f"{result['status']}: {result['test']}")
            if result['message']:
                print(f"   → {result['message']}")
        
        print("\n" + "="*50)
        print(f"📈 RESULTS: {passed}/{total} tests passed")
        print("="*50)
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
            return True
        else:
            print(f"❌ {total - passed} tests failed")
            return False


if __name__ == "__main__":
    tester = PDFTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)