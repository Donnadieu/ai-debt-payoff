#!/usr/bin/env python3
"""Simple test runner to verify test suite functionality."""

import sys
import os
import subprocess
from pathlib import Path

def run_tests():
    """Run tests with proper Python path setup."""
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    
    # Add backend directory to Python path
    env = os.environ.copy()
    pythonpath = str(backend_dir)
    if 'PYTHONPATH' in env:
        pythonpath = f"{pythonpath}:{env['PYTHONPATH']}"
    env['PYTHONPATH'] = pythonpath
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "-x"  # Stop on first failure
    ]
    
    print("Running test suite...")
    print(f"Command: {' '.join(cmd)}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PYTHONPATH: {env.get('PYTHONPATH', 'Not set')}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Exit code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def check_test_files():
    """Check that all test files exist."""
    test_files = [
        "tests/conftest.py",
        "tests/test_planner.py", 
        "tests/test_api.py",
        "tests/test_analytics_api.py",
        "tests/test_middleware.py",
        "tests/test_integration.py",
        "tests/test_event_service.py",
        "tests/test_nudge_service.py",
        "tests/test_llm_validation.py",
        "tests/test_workers.py"
    ]
    
    missing_files = []
    for test_file in test_files:
        if not Path(test_file).exists():
            missing_files.append(test_file)
    
    if missing_files:
        print("Missing test files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print(f"All {len(test_files)} test files found.")
    return True

def count_test_functions():
    """Count test functions across all test files."""
    test_count = 0
    test_files = Path("tests").glob("test_*.py")
    
    for test_file in test_files:
        with open(test_file, 'r') as f:
            content = f.read()
            # Count functions that start with "test_"
            test_count += content.count("def test_")
    
    print(f"Total test functions: {test_count}")
    return test_count

if __name__ == "__main__":
    print("=== Test Suite Verification ===")
    print()
    
    # Check test files exist
    if not check_test_files():
        sys.exit(1)
    
    # Count tests
    test_count = count_test_functions()
    
    # Run tests
    success = run_tests()
    
    print("\n=== Summary ===")
    print(f"Test files: ✓")
    print(f"Test functions: {test_count}")
    print(f"Test execution: {'✓' if success else '✗'}")
    
    sys.exit(0 if success else 1)
