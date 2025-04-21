import os
import pytest
from pytest_html import extras
from datetime import datetime

# Create directory for screenshots if it doesn't exist
os.makedirs("reports/screenshots", exist_ok=True)

def pytest_configure(config):
    # Add markers
    config.addinivalue_line(
        "markers", "login: mark test as a login test"
    )
    config.addinivalue_line(
        "markers", "profile: mark test as a profile test"
    )
    
    # Configure retries for flaky tests
    config.addinivalue_line(
        "markers", "flaky: mark test as flaky, will be retried on failure"
    )
    
    # Logging configuration
    config.option.log_cli = True
    config.option.log_cli_level = "INFO"

def pytest_html_report_title(report):
    report.title = "W3Schools Automation Test Report"

def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(1, "<th>Time</th>")
    cells.insert(3, "<th>Screenshot</th>")
    cells.pop()

def pytest_html_results_table_row(report, cells):
    description = getattr(report, 'description', 'N/A')
    cells.insert(2, f"<td>{description}</td>")
    cells.insert(1, f"<td>{datetime.now().strftime('%H:%M:%S')}</td>")
    
    # Improved screenshot cell detection and display
    screenshot_cell = "<td>No screenshot</td>"
    screenshot_name = None
    
    # Check for screenshots in extras
    for extra in getattr(report, "extras", []):
        if extra.get("format_type") == "image":
            name = extra.get("name", "")
            if name and name.startswith("Screenshot_"):
                screenshot_name = name
                filename = name.replace("Screenshot_", "")
                screenshot_cell = f"<td>{filename}</td>"
                break
            else:
                screenshot_cell = "<td>Screenshot available</td>"
                break
    
    # If test failed but no screenshot in extras, check for files in the directory
    if report.failed and not screenshot_name:
        test_id = getattr(report, "nodeid", "").replace("::", "_").replace("/", "_").replace(".", "_")
        if test_id:
            import glob
            screenshot_files = glob.glob(f"reports/screenshots/*{test_id}*.png")
            if screenshot_files:
                newest_file = max(screenshot_files, key=os.path.getctime)
                filename = os.path.basename(newest_file)
                screenshot_cell = f"<td>{filename}</td>"
    
    cells.insert(3, screenshot_cell)
    cells.pop()

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        "<p><b>Project Name:</b> W3Schools Login & Profile Automation</p>",
        f"<p><b>Execution Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        "<p><b>Environment:</b> Test</p>",
        "<p><b>Browser:</b> Chrome</p>",
        "<p><b>Tester:</b> Thomas</p>",
        f"<p><b>Screenshots Path:</b> {os.path.abspath('reports/screenshots')}</p>",
        "<p><b>Note:</b> Screenshots are automatically captured for failed tests and named with test name and timestamp.</p>",
        "<p><b>Screenshot Format:</b> <code>testname_YYYYMMDD_HHMMSS.png</code></p>"
    ])

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    
    extras_list = getattr(report, "extras", []).copy()
    
    if report.when == "call":
        # Always try to access the driver
        try:
            driver = None
            
            # Try different ways to access the driver
            if hasattr(item, "_testcase") and hasattr(item._testcase, "driver"):
                driver = item._testcase.driver
            elif 'setup' in item.funcargs:
                driver = item.funcargs['setup']
            elif hasattr(item.function, "__self__") and hasattr(item.function.__self__, "driver"):
                driver = item.function.__self__.driver
            else:
                # Try to find a driver in the funcargs
                for arg_name, arg_value in item.funcargs.items():
                    if hasattr(arg_value, 'get_screenshot_as_base64'):
                        driver = arg_value
                        break
            
            if driver is None:
                # Try TestClass instance
                for fixture_name, fixture_value in item._fixtureinfo.name2fixturedefs.items():
                    if fixture_value and hasattr(fixture_value[0], 'cached_result') and fixture_value[0].cached_result:
                        result = fixture_value[0].cached_result[0]
                        if hasattr(result, 'driver'):
                            driver = result.driver
                            break
            
            # Add screenshot for failed tests
            if report.failed and driver is not None:
                # Create timestamp for unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name
                # Create a clean filename without special characters
                clean_test_name = ''.join(c if c.isalnum() else '_' for c in test_name)
                # Save screenshot to disk
                screenshot_path = f"reports/screenshots/{clean_test_name}_{timestamp}.png"
                
                try:
                    print(f"Attempting to save screenshot to: {screenshot_path}")
                    driver.save_screenshot(screenshot_path)
                    print(f"Screenshot saved successfully to: {screenshot_path}")
                    
                    # Add screenshot to report with meaningful name
                    screenshot = driver.get_screenshot_as_base64()
                    screenshot_name = f"{clean_test_name}_{timestamp}"
                    extras_list.append(extras.image(screenshot, screenshot_name))
                    
                    # Add additional debug information
                    try:
                        page_source = driver.page_source
                        extras_list.append(extras.text(page_source[:5000], "Page Source (truncated)"))
                    except:
                        print("Could not get page source")
                        
                except Exception as screenshot_error:
                    print(f"Error saving screenshot: {screenshot_error}")
                    extras_list.append(extras.text(f"Screenshot failed: {str(screenshot_error)}", "Screenshot Error"))
            
        except Exception as e:
            print(f"Failed to capture screenshot: {str(e)}")
            extras_list.append(extras.text(f"Screenshot capture failed: {str(e)}", "Error"))
        
        # Add test logs
        if hasattr(report, "wasxfail"):
            extras_list.append(extras.text("Test was expected to fail", "Expected Failure"))
        
        # Add test category
        if "login" in item.keywords:
            extras_list.append(extras.text("Login Test", "Test Category"))
        elif "profile" in item.keywords:
            extras_list.append(extras.text("Profile Test", "Test Category"))
    
    # Ensure this line is executed at the end of the function to correctly set report.extras
    report.extras = extras_list

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Report test summary when session finishes
    """
    print("\n" + "=" * 30 + " Test Summary " + "=" * 30)
    print(f"Total test count: {session.testscollected}")
    print(f"Passed tests: {session.testscollected - session.testsfailed}")
    print(f"Failed tests: {session.testsfailed}")
    
    # Print path to screenshots if any tests failed
    if session.testsfailed > 0:
        print(f"\nScreenshots available at: {os.path.abspath('reports/screenshots')}")
        
    print("=" * 73 + "\n")

    