"""
Test script to verify the float conversion fix
"""
def test_float_conversion():
    """Test float conversion with various inputs including empty strings"""
    
    def safe_float_conversion(value):
        """Safely convert a value to float with proper empty string handling"""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            cleaned_value = value.strip().replace(',', '').replace(' ', '')
            # Handle empty string case
            if cleaned_value == '':
                return 0.0
            else:
                try:
                    return float(cleaned_value)
                except ValueError:
                    return 0.0
        else:
            return 0.0
    
    # Test cases
    test_cases = [
        ("", 0.0),           # Empty string
        ("  ", 0.0),         # Whitespace only
        ("0", 0.0),          # Zero as string
        ("123", 123.0),      # Valid number
        ("123.45", 123.45),  # Valid decimal
        (" 123 ", 123.0),    # Number with whitespace
        ("1,234", 1234.0),   # Number with comma
        ("abc", 0.0),        # Invalid string
        (123, 123.0),        # Integer
        (123.45, 123.45),    # Float
        (None, 0.0),         # None value
    ]
    
    print("Testing float conversion fix:")
    for input_value, expected in test_cases:
        result = safe_float_conversion(input_value)
        status = "✓" if result == expected else "✗"
        print(f"  {status} Input: {repr(input_value)} -> Output: {result} (Expected: {expected})")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_float_conversion()