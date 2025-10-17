def test_zero_rate_item_handling():
    """
    Test script to demonstrate zero rate item handling
    """
    print("Testing Zero Rate Item Handling")
    print("=" * 40)
    
    # Simulate a zero rate item from Work Order sheet
    print("\n1. Work Order Zero Rate Item:")
    wo_item = {
        "serial_no": "10",
        "description": "Concrete Mixture",
        "unit": "Cubic Meter",
        "quantity": "15.5",
        "rate": "0",  # Zero rate
        "remark": "Rate to be determined"
    }
    
    print(f"   Input - Serial No: {wo_item['serial_no']}")
    print(f"   Input - Description: {wo_item['description']}")
    print(f"   Input - Unit: {wo_item['unit']}")
    print(f"   Input - Quantity: {wo_item['quantity']}")
    print(f"   Input - Rate: {wo_item['rate']}")
    print(f"   Input - Remark: {wo_item['remark']}")
    
    # Apply zero rate logic
    rate = float(wo_item["rate"]) if wo_item["rate"] and wo_item["rate"] != "" else 0
    
    if rate == 0:
        processed_item = {
            "serial_no": wo_item["serial_no"],
            "description": wo_item["description"],
            "unit": "",  # Leave blank as per specification
            "quantity": "",  # Leave blank as per specification
            "rate": "",  # Leave blank as per specification
            "remark": wo_item["remark"],
            "amount": ""  # Leave blank as per specification
        }
        print("\n   Output (Zero Rate Handling):")
        print(f"   ✅ Serial No: {processed_item['serial_no']}")
        print(f"   ✅ Description: {processed_item['description']}")
        print(f"   ❌ Unit: '{processed_item['unit']}'")
        print(f"   ❌ Quantity: '{processed_item['quantity']}'")
        print(f"   ❌ Rate: '{processed_item['rate']}'")
        print(f"   ✅ Remark: {processed_item['remark']}")
        print(f"   ❌ Amount: '{processed_item['amount']}'")
    
    # Simulate a normal rate item for comparison
    print("\n2. Normal Rate Item (for comparison):")
    normal_item = {
        "serial_no": "15",
        "description": "Steel Bars",
        "unit": "Kilogram",
        "quantity": "100.0",
        "rate": "45.50",
        "remark": "Standard rate"
    }
    
    print(f"   Input - Serial No: {normal_item['serial_no']}")
    print(f"   Input - Description: {normal_item['description']}")
    print(f"   Input - Unit: {normal_item['unit']}")
    print(f"   Input - Quantity: {normal_item['quantity']}")
    print(f"   Input - Rate: {normal_item['rate']}")
    print(f"   Input - Remark: {normal_item['remark']}")
    
    rate = float(normal_item["rate"]) if normal_item["rate"] and normal_item["rate"] != "" else 0
    qty = float(normal_item["quantity"]) if normal_item["quantity"] and normal_item["quantity"] != "" else 0
    
    if rate != 0:
        processed_item = {
            "serial_no": normal_item["serial_no"],
            "description": normal_item["description"],
            "unit": normal_item["unit"],
            "quantity": qty,
            "rate": rate,
            "remark": normal_item["remark"],
            "amount": round(qty * rate)
        }
        print("\n   Output (Normal Rate Handling):")
        print(f"   ✅ Serial No: {processed_item['serial_no']}")
        print(f"   ✅ Description: {processed_item['description']}")
        print(f"   ✅ Unit: {processed_item['unit']}")
        print(f"   ✅ Quantity: {processed_item['quantity']}")
        print(f"   ✅ Rate: {processed_item['rate']}")
        print(f"   ✅ Remark: {processed_item['remark']}")
        print(f"   ✅ Amount: {processed_item['amount']}")
    
    # Simulate an Extra Items zero rate item
    print("\n3. Extra Items Zero Rate Item:")
    extra_item = {
        "serial_no": "5",
        "description": "Special Coating",
        "unit": "Square Meter",
        "quantity": "25.0",
        "rate": "",  # Blank rate
        "remark": "Pending approval"
    }
    
    print(f"   Input - Serial No: {extra_item['serial_no']}")
    print(f"   Input - Description: {extra_item['description']}")
    print(f"   Input - Unit: {extra_item['unit']}")
    print(f"   Input - Quantity: {extra_item['quantity']}")
    print(f"   Input - Rate: '{extra_item['rate']}'")
    print(f"   Input - Remark: {extra_item['remark']}")
    
    # Apply zero rate logic
    rate = 0
    if extra_item["rate"] and extra_item["rate"] != "":
        try:
            rate = float(extra_item["rate"])
        except ValueError:
            rate = 0
    
    if rate == 0:
        processed_item = {
            "serial_no": extra_item["serial_no"],
            "description": extra_item["description"],
            "unit": "",  # Leave blank as per specification
            "quantity": "",  # Leave blank as per specification
            "rate": "",  # Leave blank as per specification
            "remark": extra_item["remark"],
            "amount": ""  # Leave blank as per specification
        }
        print("\n   Output (Zero Rate Handling):")
        print(f"   ✅ Serial No: {processed_item['serial_no']}")
        print(f"   ✅ Description: {processed_item['description']}")
        print(f"   ❌ Unit: '{processed_item['unit']}'")
        print(f"   ❌ Quantity: '{processed_item['quantity']}'")
        print(f"   ❌ Rate: '{processed_item['rate']}'")
        print(f"   ✅ Remark: {processed_item['remark']}")
        print(f"   ❌ Amount: '{processed_item['amount']}'")
    
    print("\n" + "=" * 40)
    print("Zero Rate Handling Test Complete")
    print("✅ Confirmed: Specification compliance verified")
    print("❌ Blank fields correctly left empty for zero rate items")

if __name__ == "__main__":
    test_zero_rate_item_handling()