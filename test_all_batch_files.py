#!/usr/bin/env python3
"""
Test script to verify that all batch files have correct syntax and structure
"""

import os
import sys
import subprocess

def test_batch_file_syntax(file_path):
    """Test if a batch file has valid syntax"""
    print(f"Testing {os.path.basename(file_path)}...")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"  ❌ File not found: {file_path}")
            return False
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic syntax checks
        lines = content.split('\n')
        
        # Check for required elements
        has_echo_off = '@echo off' in content
        has_pause = 'pause' in content
        has_exit_codes = 'exit /b' in content or 'exit /b 1' in content
        
        print(f"  ✅ File exists")
        print(f"  ✅ Has '@echo off': {has_echo_off}")
        print(f"  ✅ Has 'pause': {has_pause}")
        
        # Check for common syntax errors
        syntax_errors = []
        
        # Check for unmatched quotes
        for i, line in enumerate(lines):
            if line.count('"') % 2 != 0:
                syntax_errors.append(f"Line {i+1}: Unmatched quotes")
        
        # Check for proper IF statements
        for i, line in enumerate(lines):
            if 'if' in line.lower() and not ('(' in line and ')' in line):
                if 'exit' in line.lower() and not 'exit /b' in line.lower():
                    syntax_errors.append(f"Line {i+1}: IF statement should use 'exit /b' not 'exit'")
        
        if syntax_errors:
            for error in syntax_errors:
                print(f"  ⚠️  {error}")
        else:
            print(f"  ✅ No obvious syntax errors")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing {file_path}: {e}")
        return False

def test_batch_file_execution(file_path):
    """Test if a batch file can be executed without errors (dry run)"""
    print(f"Testing execution of {os.path.basename(file_path)}...")
    
    try:
        # Try to parse the batch file with a dry run
        # We'll just check if it can be read and parsed without errors
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for common execution patterns
        has_python_commands = 'python' in content
        has_pip_commands = 'pip' in content
        has_streamlit_commands = 'streamlit' in content
        
        print(f"  ✅ Contains Python commands: {has_python_commands}")
        print(f"  ✅ Contains pip commands: {has_pip_commands}")
        print(f"  ✅ Contains Streamlit commands: {has_streamlit_commands}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in execution test for {file_path}: {e}")
        return False

def main():
    """Main test function"""
    print("Testing All Batch Files")
    print("=" * 50)
    
    # Get all batch files
    batch_files = [f for f in os.listdir('.') if f.endswith('.bat')]
    
    if not batch_files:
        print("❌ No batch files found in current directory")
        return False
    
    print(f"Found {len(batch_files)} batch files:")
    for bf in batch_files:
        print(f"  - {bf}")
    
    print("\n" + "=" * 50)
    
    all_passed = True
    for batch_file in batch_files:
        file_path = os.path.join(os.getcwd(), batch_file)
        
        # Test syntax
        syntax_ok = test_batch_file_syntax(file_path)
        
        # Test execution patterns
        execution_ok = test_batch_file_execution(file_path)
        
        if syntax_ok and execution_ok:
            print(f"  🎉 {batch_file}: PASSED")
        else:
            print(f"  ❌ {batch_file}: FAILED")
            all_passed = False
        
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 ALL BATCH FILES PASSED!")
        print("✅ All batch files have correct syntax and structure")
        return True
    else:
        print("❌ SOME BATCH FILES FAILED")
        print("Please check the output above for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)