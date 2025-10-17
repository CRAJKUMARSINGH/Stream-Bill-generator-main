"""
Direct test of enhanced batch tester to see what error occurs
"""
import sys
import traceback

def test_enhanced_batch_tester():
    """Test the enhanced batch tester directly"""
    print("Testing enhanced batch tester directly...")
    
    try:
        # Import the function
        from enhanced_batch_tester import batch_process_all_test_files
        print("✓ Imported batch_process_all_test_files successfully")
        
        # Try to run it
        print("Running batch_process_all_test_files...")
        batch_process_all_test_files()
        print("✓ batch_process_all_test_files completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error running batch_process_all_test_files: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("Direct Test of Enhanced Batch Tester")
    print("=" * 40)
    print()
    
    success = test_enhanced_batch_tester()
    
    print()
    if success:
        print("✅ Enhanced batch tester test passed!")
    else:
        print("❌ Enhanced batch tester test failed!")
        print("Check the error above to diagnose the issue.")

if __name__ == "__main__":
    main()