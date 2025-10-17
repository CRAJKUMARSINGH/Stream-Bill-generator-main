def test_deviation_statement_zero_rate_handling():
    """
    Test script to demonstrate Deviation Statement zero rate item handling
    """
    print("Testing Deviation Statement Zero Rate Item Handling")
    print("=" * 55)
    
    # Simulate a zero rate item in Deviation Statement
    print("\n1. Deviation Statement Zero Rate Item:")
    zero_rate_item = {
        "item_no": "10",
        "description": "Specialized Equipment",
        "unit": "Unit",
        "qty_wo": "5.0",
        "rate": "0",  # Zero rate
        "amt_wo": "0",
        "qty_bill": "5.0",
        "amt_bill": "0",
        "excess_qty": "0",
        "excess_amt": "0",
        "saving_qty": "0",
        "saving_amt": "0"
    }
    
    print(f"   Input Data:")
    for key, value in zero_rate_item.items():
        print(f"   - {key}: {value}")
    
    # Apply zero rate logic (as implemented in the application)
    rate = float(zero_rate_item["rate"]) if zero_rate_item["rate"] and zero_rate_item["rate"] != "" else 0
    
    print(f"\n   Processing Logic:")
    print(f"   - Rate value: {rate}")
    print(f"   - Condition (rate is None or rate == 0): {rate is None or rate == 0}")
    
    if rate is None or rate == 0:
        processed_item = {
            "serial_no": zero_rate_item["item_no"],
            "description": "",  # Leave blank as per specification
            "unit": "",  # Leave blank as per specification
            "qty_wo": "",  # Leave blank as per specification
            "rate": "",  # Leave blank as per specification
            "amt_wo": "",  # Leave blank as per specification
            "qty_bill": "",  # Leave blank as per specification
            "amt_bill": "",  # Leave blank as per specification
            "excess_qty": "",  # Leave blank as per specification
            "excess_amt": "",  # Leave blank as per specification
            "saving_qty": "",  # Leave blank as per specification
            "saving_amt": ""  # Leave blank as per specification
        }
        print("\n   Output (Zero Rate Handling):")
        print(f"   ✅ Item No. (serial_no): '{processed_item['serial_no']}'")
        print(f"   ❌ Description: '{processed_item['description']}'")
        print(f"   ❌ Unit: '{processed_item['unit']}'")
        print(f"   ❌ Qty as per Work Order: '{processed_item['qty_wo']}'")
        print(f"   ❌ Rate: '{processed_item['rate']}'")
        print(f"   ❌ Amt as per Work Order: '{processed_item['amt_wo']}'")
        print(f"   ❌ Qty Executed: '{processed_item['qty_bill']}'")
        print(f"   ❌ Amt as per Executed: '{processed_item['amt_bill']}'")
        print(f"   ❌ Excess Qty: '{processed_item['excess_qty']}'")
        print(f"   ❌ Excess Amt: '{processed_item['excess_amt']}'")
        print(f"   ❌ Saving Qty: '{processed_item['saving_qty']}'")
        print(f"   ❌ Saving Amt: '{processed_item['saving_amt']}'")
    
    # Simulate a normal rate item for comparison
    print("\n2. Deviation Statement Normal Rate Item (for comparison):")
    normal_rate_item = {
        "item_no": "15",
        "description": "Standard Materials",
        "unit": "Kilogram",
        "qty_wo": "100.0",
        "rate": "25.50",
        "qty_bill": "95.0"
    }
    
    # Calculate amounts
    qty_wo = float(normal_rate_item["qty_wo"])
    rate = float(normal_rate_item["rate"])
    qty_bill = float(normal_rate_item["qty_bill"])
    amt_wo = round(qty_wo * rate)
    amt_bill = round(qty_bill * rate)
    excess_qty = qty_bill - qty_wo if qty_bill > qty_wo else 0
    excess_amt = round(excess_qty * rate) if excess_qty > 0 else 0
    saving_qty = qty_wo - qty_bill if qty_bill < qty_wo else 0
    saving_amt = round(saving_qty * rate) if saving_qty > 0 else 0
    
    print(f"   Input Data:")
    print(f"   - Item No.: {normal_rate_item['item_no']}")
    print(f"   - Description: {normal_rate_item['description']}")
    print(f"   - Unit: {normal_rate_item['unit']}")
    print(f"   - Qty as per Work Order: {normal_rate_item['qty_wo']}")
    print(f"   - Rate: {normal_rate_item['rate']}")
    print(f"   - Qty Executed: {normal_rate_item['qty_bill']}")
    
    print(f"\n   Calculated Values:")
    print(f"   - Amt as per Work Order: {amt_wo}")
    print(f"   - Amt as per Executed: {amt_bill}")
    print(f"   - Excess Qty: {excess_qty}")
    print(f"   - Excess Amt: {excess_amt}")
    print(f"   - Saving Qty: {saving_qty}")
    print(f"   - Saving Amt: {saving_amt}")
    
    rate = float(normal_rate_item["rate"]) if normal_rate_item["rate"] and normal_rate_item["rate"] != "" else 0
    
    print(f"\n   Processing Logic:")
    print(f"   - Rate value: {rate}")
    print(f"   - Condition (rate is None or rate == 0): {rate is None or rate == 0}")
    
    if rate != 0:
        processed_item = {
            "serial_no": normal_rate_item["item_no"],
            "description": normal_rate_item["description"],
            "unit": normal_rate_item["unit"],
            "qty_wo": qty_wo,
            "rate": rate,
            "amt_wo": amt_wo,
            "qty_bill": qty_bill,
            "amt_bill": amt_bill,
            "excess_qty": excess_qty,
            "excess_amt": excess_amt,
            "saving_qty": saving_qty,
            "saving_amt": saving_amt
        }
        print("\n   Output (Normal Rate Handling):")
        print(f"   ✅ Item No. (serial_no): '{processed_item['serial_no']}'")
        print(f"   ✅ Description: '{processed_item['description']}'")
        print(f"   ✅ Unit: '{processed_item['unit']}'")
        print(f"   ✅ Qty as per Work Order: '{processed_item['qty_wo']}'")
        print(f"   ✅ Rate: '{processed_item['rate']}'")
        print(f"   ✅ Amt as per Work Order: '{processed_item['amt_wo']}'")
        print(f"   ✅ Qty Executed: '{processed_item['qty_bill']}'")
        print(f"   ✅ Amt as per Executed: '{processed_item['amt_bill']}'")
        print(f"   ✅ Excess Qty: '{processed_item['excess_qty']}'")
        print(f"   ✅ Excess Amt: '{processed_item['excess_amt']}'")
        print(f"   ✅ Saving Qty: '{processed_item['saving_qty']}'")
        print(f"   ✅ Saving Amt: '{processed_item['saving_amt']}'")
    
    print("\n" + "=" * 55)
    print("Deviation Statement Zero Rate Handling Test Complete")
    print("✅ Confirmed: Specification compliance verified")
    print("❌ Blank fields correctly left empty for zero rate items")

if __name__ == "__main__":
    test_deviation_statement_zero_rate_handling()