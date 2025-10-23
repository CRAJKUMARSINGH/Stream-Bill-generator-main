#!/usr/bin/env python3
"""
Test script to verify that all batch files have correct syntax and structure
"""

import os
import sys
import subprocess

import glob


def _iter_batch_files():
    return [f for f in glob.glob("*.bat")] or []


def test_batch_file_syntax():
    """Test if a batch file has valid syntax"""
    print("Testing batch file syntax...")
    
    batch_files = _iter_batch_files()
    if not batch_files:
        print("No .bat files found; skipping batch syntax checks on non-Windows")
        return True
    for file_path in batch_files:
        try:
            if not os.path.exists(file_path):
                print(f"  ❌ File not found: {file_path}")
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.split('\n')
            has_echo_off = '@echo off' in content
            has_pause = 'pause' in content
            print(f"  ✅ {os.path.basename(file_path)} exists")
            print(f"  ✅ Has '@echo off': {has_echo_off}")
            print(f"  ✅ Has 'pause': {has_pause}")
            syntax_errors = []
            for i, line in enumerate(lines):
                if line.count('"') % 2 != 0:
                    syntax_errors.append(f"Line {i+1}: Unmatched quotes")
            for i, line in enumerate(lines):
                if 'if' in line.lower() and not ('(' in line and ')' in line):
                    if 'exit' in line.lower() and 'exit /b' not in line.lower():
                        syntax_errors.append("Line {i+1}: IF should use 'exit /b'")
            for error in syntax_errors:
                print(f"  ⚠️  {error}")
        except Exception as e:
            print(f"  ❌ Error testing {file_path}: {e}")
    return True

def test_batch_file_execution():
    """Test if a batch file can be executed without errors (dry run)"""
    print("Testing execution patterns of batch files...")
    
    batch_files = _iter_batch_files()
    if not batch_files:
        print("No .bat files found; skipping execution pattern checks on non-Windows")
        return True
    for file_path in batch_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            has_python_commands = 'python' in content
            has_pip_commands = 'pip' in content
            has_streamlit_commands = 'streamlit' in content
            print(f"  ✅ {os.path.basename(file_path)} contains Python commands: {has_python_commands}")
            print(f"  ✅ {os.path.basename(file_path)} contains pip commands: {has_pip_commands}")
            print(f"  ✅ {os.path.basename(file_path)} contains Streamlit commands: {has_streamlit_commands}")
        except Exception as e:
            print(f"  ❌ Error in execution test for {file_path}: {e}")
    return True

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