#!/usr/bin/env python
"""
Test Runner Script for W3Schools Automation Project
---------------------------------------------------
Usage:
    python run_tests.py [options]

Options:
    --login      Run only login tests
    --profile    Run only profile tests
    --all        Run all tests (default)
    --rerun      Enable rerun of failed tests
    --report     Generate HTML report
"""

import os
import sys
import subprocess
import argparse
import importlib.util
from datetime import datetime

def is_package_installed(package_name):
    """Check if a Python package is installed"""
    return importlib.util.find_spec(package_name) is not None

def parse_args():
    parser = argparse.ArgumentParser(description='Run W3Schools Automation Tests')
    parser.add_argument('--login', action='store_true', help='Run only login tests')
    parser.add_argument('--profile', action='store_true', help='Run only profile tests')
    parser.add_argument('--all', action='store_true', help='Run all tests (default)')
    parser.add_argument('--rerun', action='store_true', help='Enable rerun of failed tests')
    parser.add_argument('--report', action='store_true', help='Generate HTML report')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Check for required packages
    missing_packages = []
    
    if args.rerun and not is_package_installed('pytest_rerunfailures'):
        print("Warning: pytest-rerunfailures is not installed. Retry functionality will be disabled.")
        print("Install with: pip install pytest-rerunfailures")
        args.rerun = False
    
    if args.report and not is_package_installed('pytest_html'):
        print("Warning: pytest-html is not installed. HTML reports will be disabled.")
        print("Install with: pip install pytest-html")
        args.report = False
    
    # Create reports and screenshots directories if they don't exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test selection
    if args.login:
        cmd.append("-m")
        cmd.append("login")
    elif args.profile:
        cmd.append("-m")
        cmd.append("profile")
    elif not args.all:
        # Default to all tests if no specific selection is made
        pass
    
    # Add rerun option
    if args.rerun:
        cmd.append("--reruns")
        cmd.append("2")
        cmd.append("--reruns-delay")
        cmd.append("1")
    
    # Add HTML report option
    if args.report:
        # Use more specific report name based on test type
        if args.login:
            report_path = "reports/login_report.html"
        elif args.profile:
            report_path = "reports/profile_report.html"
        else:
            # Use timestamp for generic reports
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"reports/report_{timestamp}.html"
            
        cmd.append(f"--html={report_path}")
        cmd.append("--self-contained-html")
        print(f"Report will be generated at: {report_path}")
    
    # Add verbose output
    cmd.append("-v")
    
    # Print the command being run
    print("Running command: " + " ".join(cmd))
    print("\nTest Configuration:")
    print("-------------------")
    print(f"- Test Type: {'Login Tests' if args.login else 'Profile Tests' if args.profile else 'All Tests'}")
    print(f"- Retry Failed Tests: {'Enabled' if args.rerun else 'Disabled'}")
    print(f"- HTML Report: {'Enabled' if args.report else 'Disabled'}")
    print(f"- Screenshots: Automatically captured for failed tests")
    print(f"- Screenshots Location: {os.path.abspath('reports/screenshots')}")
    if args.report:
        print(f"- Report Location: {os.path.abspath(report_path)}")
    print("-------------------")
    
    print("\nNote: If you see strange Chrome device log messages (e.g. USB errors with garbled text),")
    print("      these are normal internal Chrome logs and can be ignored. We've added settings to")
    print("      minimize these messages, but some may still appear.")
    print("\nStarting tests...\n")
    
    # Run the tests
    result = subprocess.run(cmd)
    
    # Return the exit code
    return result.returncode

if __name__ == "__main__":
    sys.exit(main()) 