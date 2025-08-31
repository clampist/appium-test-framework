#!/usr/bin/env python3
"""
Test Runner Script
Test runner script
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime
from core.utils.logger import Log
from core.utils.file_utils import FileUtils


def run_command(command, description):
    """Run command"""
    Log.info(f"Running: {description}")
    Log.info(f"Command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        Log.info(f"Command completed successfully: {description}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        Log.error(f"Command failed: {description}")
        Log.error(f"Error: {e.stderr}")
        return None


def setup_environment():
    """Setup test environment"""
    Log.info("Setting up test environment...")
    
    # Create necessary directories
    directories = [
        "logs",
        "reports", 
        "screenshots",
        "uploads",
        "backups"
    ]
    
    for directory in directories:
        FileUtils.ensure_dir(directory)
        Log.info(f"Created directory: {directory}")


def run_tests(test_path=None, markers=None, parallel=None, html_report=True):
    """Run tests"""
    Log.info("Starting test execution...")
    
    # Build pytest command
    cmd_parts = ["python", "-m", "pytest"]
    
    # Add test path
    if test_path:
        cmd_parts.append(test_path)
    else:
        cmd_parts.append("tests/")
    
    # Add markers
    if markers:
        for marker in markers:
            cmd_parts.extend(["-m", marker])
    
    # Add parallel execution
    if parallel:
        cmd_parts.extend(["-n", str(parallel)])
    
    # Add HTML report
    if html_report:
        cmd_parts.extend([
            "--html=reports/report.html",
            "--self-contained-html"
        ])
    
    # Add JUnit XML report
    cmd_parts.extend(["--junitxml=reports/junit.xml"])
    
    # Add verbose output
    cmd_parts.extend(["-v", "--tb=short"])
    
    command = " ".join(cmd_parts)
    
    # Run tests
    result = run_command(command, "Test execution")
    
    if result:
        Log.info("Test execution completed successfully")
        return True
    else:
        Log.error("Test execution failed")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="ATF Test Runner")
    
    parser.add_argument(
        "--test-path",
        help="Test path (e.g., tests/com.honda.roadsync.duo/)"
    )
    
    parser.add_argument(
        "--markers",
        nargs="+",
        help="Test markers (e.g., smoke regression)"
    )
    
    parser.add_argument(
        "--parallel",
        type=int,
        help="Number of parallel executions"
    )
    
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Do not generate HTML report"
    )
    
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="Setup environment only"
    )
    
    args = parser.parse_args()
    
    # Initialize logging
    Log.info("ATF Test Runner started")
    Log.info(f"Python version: {sys.version}")
    Log.info(f"Working directory: {os.getcwd()}")
    
    # Setup environment
    setup_environment()
    
    if args.setup_only:
        Log.info("Environment setup completed")
        return
    
    # Run tests
    success = run_tests(
        test_path=args.test_path,
        markers=args.markers,
        parallel=args.parallel,
        html_report=not args.no_html
    )
    
    if success:
        Log.info("All tests completed successfully")
        sys.exit(0)
    else:
        Log.error("Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
