#!/usr/bin/env python
"""
Verify Test Environment Setup
----------------------------
Checks if all required packages are installed and properly configured.
"""

import importlib.util
import sys
import os

def check_package(package_name, friendly_name=None):
    """Check if a package is installed and print the result"""
    friendly_name = friendly_name or package_name
    is_installed = importlib.util.find_spec(package_name) is not None
    
    if is_installed:
        print(f"✅ {friendly_name} is installed")
    else:
        print(f"❌ {friendly_name} is NOT installed")
    
    return is_installed

def main():
    print("\n=== Verifying Test Environment Setup ===\n")
    
    # Check required packages
    all_packages_installed = True
    
    # Core dependencies
    all_packages_installed &= check_package("selenium", "Selenium")
    all_packages_installed &= check_package("webdriver_manager", "WebDriver Manager")
    
    # Testing framework
    all_packages_installed &= check_package("pytest", "pytest")
    all_packages_installed &= check_package("pytest_html", "pytest-html")
    all_packages_installed &= check_package("pytest_metadata", "pytest-metadata")
    all_packages_installed &= check_package("pytest_rerunfailures", "pytest-rerunfailures")
    
    # Utilities
    all_packages_installed &= check_package("requests", "Requests")
    
    # Check directories exist
    print("\n=== Checking Project Structure ===\n")
    
    directories_to_check = [
        "pages",
        "test_data",
        "tests",
        "reports",
        "reports/screenshots"
    ]
    
    all_directories_exist = True
    
    for directory in directories_to_check:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Directory missing: {directory}")
            all_directories_exist = False
            # Create missing directory
            os.makedirs(directory, exist_ok=True)
            print(f"  ➡️ Created directory: {directory}")
    
    # Summary
    print("\n=== Setup Verification Summary ===\n")
    
    if all_packages_installed:
        print("✅ All required packages are installed")
    else:
        print("❌ Some packages are missing. Run the following command to install all requirements:")
        print("  pip install -r requirements.txt")
    
    if all_directories_exist:
        print("✅ All required directories exist")
    else:
        print("✅ Missing directories have been created")
    
    return 0 if all_packages_installed and all_directories_exist else 1

if __name__ == "__main__":
    sys.exit(main()) 