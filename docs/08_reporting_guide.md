# ATF Framework Reporting Guide

## Overview

This guide covers all aspects of test reporting in the ATF Framework, including HTML reports, JUnit XML reports, Allure reports, and custom reporting solutions.

## Report Types

### 1. HTML Reports

HTML reports provide a comprehensive, interactive view of test results that can be viewed in any web browser.

#### Basic HTML Report

```bash
# Generate basic HTML report
pytest tests/ --html=reports/report.html

# Generate self-contained HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Generate HTML report with screenshots
pytest tests/ --html=reports/report.html --capture=no
```

#### HTML Report Configuration

```python
# pytest.ini configuration for HTML reports
[tool:pytest]
addopts = 
    --html=reports/report.html
    --self-contained-html
    --capture=no
    --metadata Platform Android
    --metadata App com.example.app
    --metadata Version 1.0.0
```

#### Custom HTML Report

```python
# scripts/generate_custom_html_report.py
import json
from datetime import datetime
from core.utils.file_utils import FileUtils

class CustomHTMLReport:
    def __init__(self, output_file="reports/custom_report.html"):
        self.output_file = output_file
        self.test_results = []
    
    def add_test_result(self, test_name, status, duration, error=None):
        """Add test result to report"""
        self.test_results.append({
            "name": test_name,
            "status": status,
            "duration": duration,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self):
        """Generate HTML report"""
        html_content = self._generate_html_content()
        FileUtils.write_file(self.output_file, html_content)
        print(f"Custom HTML report generated: {self.output_file}")
    
    def _generate_html_content(self):
        """Generate HTML content"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ATF Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; }}
                .test-result {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
                .passed {{ background-color: #d4edda; }}
                .failed {{ background-color: #f8d7da; }}
                .skipped {{ background-color: #fff3cd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>ATF Test Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            {self._generate_test_results_html()}
        </body>
        </html>
        """
    
    def _generate_test_results_html(self):
        """Generate test results HTML"""
        html = ""
        for result in self.test_results:
            status_class = result["status"].lower()
            html += f"""
            <div class="test-result {status_class}">
                <h3>{result['name']}</h3>
                <p>Status: {result['status']}</p>
                <p>Duration: {result['duration']:.2f}s</p>
                {f'<p>Error: {result["error"]}</p>' if result['error'] else ''}
            </div>
            """
        return html
```

### 2. JUnit XML Reports

JUnit XML reports are compatible with CI/CD systems and provide structured test results.

#### Basic JUnit Report

```bash
# Generate JUnit XML report
pytest tests/ --junitxml=reports/junit.xml

# Generate JUnit XML with test class names
pytest tests/ --junitxml=reports/junit.xml --junit-prefix=atf

# Generate JUnit XML with custom attributes
pytest tests/ --junitxml=reports/junit.xml --junit-family=xunit2
```

#### JUnit Report Configuration

```python
# pytest.ini configuration for JUnit reports
[tool:pytest]
addopts = 
    --junitxml=reports/junit.xml
    --junit-prefix=atf
    --junit-family=xunit2
```

#### Custom JUnit Report

```python
# scripts/generate_custom_junit_report.py
import xml.etree.ElementTree as ET
from datetime import datetime

class CustomJUnitReport:
    def __init__(self, output_file="reports/custom_junit.xml"):
        self.output_file = output_file
        self.testsuites = ET.Element("testsuites")
    
    def add_testsuite(self, name, tests, failures, errors, skipped, time):
        """Add test suite to report"""
        testsuite = ET.SubElement(self.testsuites, "testsuite")
        testsuite.set("name", name)
        testsuite.set("tests", str(tests))
        testsuite.set("failures", str(failures))
        testsuite.set("errors", str(errors))
        testsuite.set("skipped", str(skipped))
        testsuite.set("time", str(time))
        testsuite.set("timestamp", datetime.now().isoformat())
        return testsuite
    
    def add_testcase(self, testsuite, name, classname, time, failure=None):
        """Add test case to test suite"""
        testcase = ET.SubElement(testsuite, "testcase")
        testcase.set("name", name)
        testcase.set("classname", classname)
        testcase.set("time", str(time))
        
        if failure:
            failure_elem = ET.SubElement(testcase, "failure")
            failure_elem.set("message", failure.get("message", ""))
            failure_elem.text = failure.get("details", "")
        
        return testcase
    
    def generate_report(self):
        """Generate JUnit XML report"""
        tree = ET.ElementTree(self.testsuites)
        tree.write(self.output_file, encoding="utf-8", xml_declaration=True)
        print(f"Custom JUnit report generated: {self.output_file}")
```

### 3. Allure Reports

Allure reports provide rich, interactive test reports with detailed analytics and visualizations.

#### Allure Installation

```bash
# Install Allure command-line tool
# macOS
brew install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Windows
scoop install allure
# or
choco install allure
```

#### Basic Allure Report

```bash
# Generate Allure results
pytest tests/ --alluredir=reports/allure-results

# Serve Allure report
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results --clean

# Open Allure report
allure open reports/allure-results
```

#### Allure Configuration

```python
# pytest.ini configuration for Allure
[tool:pytest]
addopts = 
    --alluredir=reports/allure-results
    --clean-alluredir
```

#### Allure Annotations

```python
import allure
import pytest

@allure.epic("ATF Framework")
@allure.feature("Login Functionality")
class TestLogin:
    
    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        """Test successful login flow"""
        with allure.step("Navigate to login page"):
            # Test step implementation
            pass
        
        with allure.step("Enter credentials"):
            # Test step implementation
            pass
        
        with allure.step("Click login button"):
            # Test step implementation
            pass
        
        with allure.step("Verify login success"):
            # Test step implementation
            pass
    
    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_login(self, driver):
        """Test failed login flow"""
        with allure.step("Enter invalid credentials"):
            # Test step implementation
            pass
        
        with allure.step("Verify error message"):
            # Test step implementation
            pass
```

#### Allure Attachments

```python
import allure
from core.utils.screenshot_utils import ScreenshotUtils

def test_with_attachments(self, driver):
    """Test with Allure attachments"""
    
    # Attach screenshot
    screenshot_path = ScreenshotUtils.save_screenshot(driver, "com.example.app", "test", "01")
    allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)
    
    # Attach page source
    page_source = driver.page_source
    allure.attach(page_source, name="Page Source", attachment_type=allure.attachment_type.XML)
    
    # Attach log file
    with open("logs/test.log", "r") as f:
        log_content = f.read()
    allure.attach(log_content, name="Test Log", attachment_type=allure.attachment_type.TEXT)
    
    # Attach JSON data
    test_data = {"status": "success", "duration": 1.5}
    allure.attach(str(test_data), name="Test Data", attachment_type=allure.attachment_type.JSON)
```

### 4. Custom Reports

#### Test Summary Report

```python
# scripts/generate_test_summary.py
import json
from datetime import datetime
from core.utils.file_utils import FileUtils

class TestSummaryReport:
    def __init__(self, output_file="reports/test_summary.txt"):
        self.output_file = output_file
        self.summary = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "duration": 0.0,
            "test_details": []
        }
    
    def add_test_result(self, test_name, status, duration, error=None):
        """Add test result to summary"""
        self.summary["total_tests"] += 1
        self.summary["duration"] += duration
        
        if status == "PASSED":
            self.summary["passed"] += 1
        elif status == "FAILED":
            self.summary["failed"] += 1
        elif status == "SKIPPED":
            self.summary["skipped"] += 1
        
        self.summary["test_details"].append({
            "name": test_name,
            "status": status,
            "duration": duration,
            "error": error
        })
    
    def generate_report(self):
        """Generate test summary report"""
        content = self._generate_summary_content()
        FileUtils.write_file(self.output_file, content)
        print(f"Test summary report generated: {self.output_file}")
    
    def _generate_summary_content(self):
        """Generate summary content"""
        return f"""
ATF Test Summary Report
=======================

Generated: {self.summary['timestamp']}

Test Results:
- Total Tests: {self.summary['total_tests']}
- Passed: {self.summary['passed']}
- Failed: {self.summary['failed']}
- Skipped: {self.summary['skipped']}
- Success Rate: {(self.summary['passed'] / self.summary['total_tests'] * 100):.2f}%
- Total Duration: {self.summary['duration']:.2f}s

Test Details:
{self._generate_test_details()}
        """
    
    def _generate_test_details(self):
        """Generate test details"""
        details = ""
        for test in self.summary["test_details"]:
            status_icon = "✅" if test["status"] == "PASSED" else "❌" if test["status"] == "FAILED" else "⏭️"
            details += f"{status_icon} {test['name']} ({test['duration']:.2f}s)\n"
            if test["error"]:
                details += f"    Error: {test['error']}\n"
        return details
```

#### Performance Report

```python
# scripts/generate_performance_report.py
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class PerformanceReport:
    def __init__(self, output_file="reports/performance_report.html"):
        self.output_file = output_file
        self.performance_data = []
    
    def add_performance_data(self, test_name, duration, memory_usage, cpu_usage):
        """Add performance data"""
        self.performance_data.append({
            "test_name": test_name,
            "duration": duration,
            "memory_usage": memory_usage,
            "cpu_usage": cpu_usage,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self):
        """Generate performance report"""
        df = pd.DataFrame(self.performance_data)
        
        # Create performance charts
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Duration chart
        axes[0, 0].bar(df['test_name'], df['duration'])
        axes[0, 0].set_title('Test Duration')
        axes[0, 0].set_ylabel('Duration (seconds)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Memory usage chart
        axes[0, 1].bar(df['test_name'], df['memory_usage'])
        axes[0, 1].set_title('Memory Usage')
        axes[0, 1].set_ylabel('Memory (MB)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # CPU usage chart
        axes[1, 0].bar(df['test_name'], df['cpu_usage'])
        axes[1, 0].set_title('CPU Usage')
        axes[1, 0].set_ylabel('CPU (%)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Performance summary
        axes[1, 1].text(0.1, 0.8, f"Total Tests: {len(df)}", fontsize=12)
        axes[1, 1].text(0.1, 0.6, f"Average Duration: {df['duration'].mean():.2f}s", fontsize=12)
        axes[1, 1].text(0.1, 0.4, f"Average Memory: {df['memory_usage'].mean():.2f}MB", fontsize=12)
        axes[1, 1].text(0.1, 0.2, f"Average CPU: {df['cpu_usage'].mean():.2f}%", fontsize=12)
        axes[1, 1].set_title('Performance Summary')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig('reports/performance_charts.png', dpi=300, bbox_inches='tight')
        
        # Generate HTML report
        html_content = self._generate_html_content(df)
        with open(self.output_file, 'w') as f:
            f.write(html_content)
        
        print(f"Performance report generated: {self.output_file}")
    
    def _generate_html_content(self, df):
        """Generate HTML content for performance report"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ATF Performance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; }}
                .chart {{ text-align: center; margin: 20px 0; }}
                .summary {{ background-color: #e8f4f8; padding: 15px; margin: 20px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>ATF Performance Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>Performance Summary</h2>
                <p>Total Tests: {len(df)}</p>
                <p>Average Duration: {df['duration'].mean():.2f}s</p>
                <p>Average Memory Usage: {df['memory_usage'].mean():.2f}MB</p>
                <p>Average CPU Usage: {df['cpu_usage'].mean():.2f}%</p>
            </div>
            
            <div class="chart">
                <h2>Performance Charts</h2>
                <img src="performance_charts.png" alt="Performance Charts" style="max-width: 100%;">
            </div>
            
            <h2>Detailed Performance Data</h2>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Duration (s)</th>
                    <th>Memory (MB)</th>
                    <th>CPU (%)</th>
                </tr>
                {self._generate_table_rows(df)}
            </table>
        </body>
        </html>
        """
    
    def _generate_table_rows(self, df):
        """Generate table rows for performance data"""
        rows = ""
        for _, row in df.iterrows():
            rows += f"""
                <tr>
                    <td>{row['test_name']}</td>
                    <td>{row['duration']:.2f}</td>
                    <td>{row['memory_usage']:.2f}</td>
                    <td>{row['cpu_usage']:.2f}</td>
                </tr>
            """
        return rows
```

## Report Integration

### 1. CI/CD Integration

#### GitHub Actions Integration

```yaml
# .github/workflows/ci-tests.yml
name: ATF Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests with reports
      run: |
        pytest tests/ --html=reports/report.html --junitxml=reports/junit.xml --alluredir=reports/allure-results
    
    - name: Generate Allure report
      run: |
        allure generate reports/allure-results --clean
    
    - name: Upload HTML report
      uses: actions/upload-artifact@v3
      with:
        name: html-report
        path: reports/report.html
    
    - name: Upload JUnit report
      uses: actions/upload-artifact@v3
      with:
        name: junit-report
        path: reports/junit.xml
    
    - name: Upload Allure report
      uses: actions/upload-artifact@v3
      with:
        name: allure-report
        path: reports/allure-report
```

#### Jenkins Integration

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                sh '''
                    pyenv activate atf
                    pytest tests/ --html=reports/report.html --junitxml=reports/junit.xml --alluredir=reports/allure-results
                '''
            }
        }
        
        stage('Generate Reports') {
            steps {
                sh '''
                    allure generate reports/allure-results --clean
                '''
            }
        }
    }
    
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'ATF HTML Report'
            ])
            
            publishTestResults([
                testResultsPattern: 'reports/junit.xml'
            ])
            
            publishAllure([
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/allure-results']]
            ])
        }
    }
}
```

### 2. Report Aggregation

#### Multi-Project Report Aggregation

```python
# scripts/aggregate_reports.py
import json
import os
from datetime import datetime
from core.utils.file_utils import FileUtils

class ReportAggregator:
    def __init__(self, output_file="reports/aggregated_report.json"):
        self.output_file = output_file
        self.aggregated_data = {
            "timestamp": datetime.now().isoformat(),
            "projects": {},
            "summary": {
                "total_tests": 0,
                "total_passed": 0,
                "total_failed": 0,
                "total_skipped": 0
            }
        }
    
    def add_project_report(self, project_name, report_file):
        """Add project report to aggregation"""
        if os.path.exists(report_file):
            report_data = FileUtils.read_json(report_file)
            self.aggregated_data["projects"][project_name] = report_data
            
            # Update summary
            self.aggregated_data["summary"]["total_tests"] += report_data.get("total_tests", 0)
            self.aggregated_data["summary"]["total_passed"] += report_data.get("passed", 0)
            self.aggregated_data["summary"]["total_failed"] += report_data.get("failed", 0)
            self.aggregated_data["summary"]["total_skipped"] += report_data.get("skipped", 0)
    
    def generate_aggregated_report(self):
        """Generate aggregated report"""
        FileUtils.write_json(self.output_file, self.aggregated_data)
        print(f"Aggregated report generated: {self.output_file}")
        
        # Generate summary
        summary = self.aggregated_data["summary"]
        success_rate = (summary["total_passed"] / summary["total_tests"] * 100) if summary["total_tests"] > 0 else 0
        
        print(f"""
Aggregated Test Results:
- Total Tests: {summary['total_tests']}
- Passed: {summary['total_passed']}
- Failed: {summary['total_failed']}
- Skipped: {summary['total_skipped']}
- Success Rate: {success_rate:.2f}%
        """)
```

## Report Customization

### 1. Custom Report Templates

#### HTML Template Customization

```python
# scripts/custom_html_template.py
class CustomHTMLTemplate:
    def __init__(self, template_file="templates/custom_report.html"):
        self.template_file = template_file
    
    def generate_report(self, test_results, output_file="reports/custom_report.html"):
        """Generate custom HTML report"""
        template_content = FileUtils.read_file(self.template_file)
        
        # Replace placeholders with actual data
        report_content = template_content.replace("{{timestamp}}", datetime.now().isoformat())
        report_content = report_content.replace("{{test_results}}", self._format_test_results(test_results))
        
        FileUtils.write_file(output_file, report_content)
        print(f"Custom HTML report generated: {output_file}")
    
    def _format_test_results(self, test_results):
        """Format test results for HTML"""
        html = ""
        for result in test_results:
            status_class = result["status"].lower()
            html += f"""
            <div class="test-result {status_class}">
                <h3>{result['name']}</h3>
                <p>Status: {result['status']}</p>
                <p>Duration: {result['duration']:.2f}s</p>
                {f'<p>Error: {result["error"]}</p>' if result['error'] else ''}
            </div>
            """
        return html
```

### 2. Report Styling

#### CSS Customization

```css
/* styles/custom_report.css */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.test-result {
    background: white;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #ddd;
}

.test-result.passed {
    border-left-color: #28a745;
}

.test-result.failed {
    border-left-color: #dc3545;
}

.test-result.skipped {
    border-left-color: #ffc107;
}

.summary-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-number {
    font-size: 2em;
    font-weight: bold;
    color: #667eea;
}
```

## Report Automation

### 1. Automated Report Generation

```python
# scripts/auto_report_generator.py
import schedule
import time
from datetime import datetime
from core.utils.logger import Log

class AutoReportGenerator:
    def __init__(self):
        self.report_types = ["html", "junit", "allure", "summary"]
    
    def generate_all_reports(self):
        """Generate all types of reports"""
        Log.info("Starting automated report generation")
        
        try:
            # Run tests and generate reports
            self._run_tests_with_reports()
            
            # Generate additional reports
            self._generate_performance_report()
            self._generate_summary_report()
            
            # Clean up old reports
            self._cleanup_old_reports()
            
            Log.success("Automated report generation completed")
        except Exception as e:
            Log.error(f"Automated report generation failed: {e}")
    
    def _run_tests_with_reports(self):
        """Run tests with all report types"""
        import subprocess
        
        cmd = [
            "pytest", "tests/",
            "--html=reports/report.html",
            "--junitxml=reports/junit.xml",
            "--alluredir=reports/allure-results"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            Log.warning("Some tests failed, but reports will still be generated")
    
    def _generate_performance_report(self):
        """Generate performance report"""
        from scripts.generate_performance_report import PerformanceReport
        
        report = PerformanceReport()
        # Add performance data collection logic here
        report.generate_report()
    
    def _generate_summary_report(self):
        """Generate summary report"""
        from scripts.generate_test_summary import TestSummaryReport
        
        report = TestSummaryReport()
        # Add test result collection logic here
        report.generate_report()
    
    def _cleanup_old_reports(self):
        """Clean up old report files"""
        import os
        import glob
        
        # Keep only last 10 reports
        report_files = glob.glob("reports/*.html") + glob.glob("reports/*.xml")
        report_files.sort(key=os.path.getmtime, reverse=True)
        
        for old_file in report_files[10:]:
            os.remove(old_file)
            Log.info(f"Removed old report: {old_file}")
    
    def schedule_reports(self, schedule_time="18:00"):
        """Schedule daily report generation"""
        schedule.every().day.at(schedule_time).do(self.generate_all_reports)
        
        Log.info(f"Report generation scheduled for {schedule_time} daily")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
```

### 2. Report Notifications

```python
# scripts/report_notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from core.utils.logger import Log

class ReportNotifier:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send_report_email(self, recipients, subject, body, attachments=None):
        """Send report via email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_path.split("/")[-1]}'
                    )
                    msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            Log.success(f"Report email sent to {recipients}")
        except Exception as e:
            Log.error(f"Failed to send report email: {e}")
    
    def generate_email_body(self, test_results):
        """Generate email body from test results"""
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r["status"] == "PASSED")
        failed_tests = sum(1 for r in test_results if r["status"] == "FAILED")
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return f"""
        <html>
        <body>
            <h2>ATF Test Report</h2>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h3>Summary</h3>
            <ul>
                <li>Total Tests: {total_tests}</li>
                <li>Passed: {passed_tests}</li>
                <li>Failed: {failed_tests}</li>
                <li>Success Rate: {success_rate:.2f}%</li>
            </ul>
            
            <h3>Test Results</h3>
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration</th>
                </tr>
                {self._generate_email_table_rows(test_results)}
            </table>
        </body>
        </html>
        """
    
    def _generate_email_table_rows(self, test_results):
        """Generate table rows for email"""
        rows = ""
        for result in test_results:
            status_color = "green" if result["status"] == "PASSED" else "red"
            rows += f"""
                <tr>
                    <td>{result['name']}</td>
                    <td style="color: {status_color};">{result['status']}</td>
                    <td>{result['duration']:.2f}s</td>
                </tr>
            """
        return rows
```

## Best Practices

### 1. Report Organization

1. **Consistent Naming**: Use consistent naming conventions for report files
2. **Directory Structure**: Organize reports in logical directory structure
3. **Version Control**: Include report generation scripts in version control
4. **Backup Strategy**: Implement backup strategy for important reports

### 2. Report Performance

1. **Efficient Generation**: Optimize report generation for large test suites
2. **Incremental Updates**: Support incremental report updates
3. **Caching**: Implement caching for frequently accessed report data
4. **Compression**: Compress large report files

### 3. Report Security

1. **Access Control**: Implement access control for sensitive reports
2. **Data Sanitization**: Sanitize sensitive data in reports
3. **Secure Storage**: Store reports in secure locations
4. **Audit Trail**: Maintain audit trail for report access

### 4. Report Maintenance

1. **Regular Cleanup**: Implement regular cleanup of old reports
2. **Archive Strategy**: Archive important reports for long-term storage
3. **Monitoring**: Monitor report generation and access
4. **Updates**: Keep report templates and tools updated

## Conclusion

This reporting guide covers comprehensive test reporting capabilities in the ATF Framework. By implementing these reporting solutions, you can:

- Generate detailed, interactive test reports
- Integrate reports with CI/CD systems
- Customize reports to meet specific needs
- Automate report generation and distribution
- Maintain comprehensive test result documentation

Remember to:
- Choose appropriate report types for your needs
- Implement proper report organization and maintenance
- Ensure report security and access control
- Keep reports updated and relevant
- Monitor report performance and usage
