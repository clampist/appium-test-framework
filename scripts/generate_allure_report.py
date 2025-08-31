#!/usr/bin/env python3
"""
Allure Report Generator
Script to generate and open Allure reports
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


class AllureReportGenerator:
    """Allure report generator utility"""
    
    def __init__(self, results_dir="reports/allure-results", report_dir="reports/allure-report"):
        self.results_dir = Path(results_dir)
        self.report_dir = Path(report_dir)
    
    def check_allure_installed(self) -> bool:
        """Check if Allure command line tool is installed"""
        try:
            result = subprocess.run(["allure", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Allure version: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Allure command line tool is not installed")
            print("📦 Install Allure:")
            print("   macOS: brew install allure")
            print("   Linux: sudo apt-add-repository ppa:qameta/allure && sudo apt-get update && sudo apt-get install allure")
            print("   Windows: scoop install allure")
            return False
    
    def generate_report(self, clean: bool = True) -> bool:
        """Generate Allure report"""
        if not self.check_allure_installed():
            return False
        
        if not self.results_dir.exists():
            print(f"❌ Results directory not found: {self.results_dir}")
            return False
        
        # Clean existing report directory
        if clean and self.report_dir.exists():
            import shutil
            shutil.rmtree(self.report_dir)
            print(f"🗑️ Cleaned existing report directory: {self.report_dir}")
        
        # Create report directory
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Generate report
            print(f"📊 Generating Allure report...")
            print(f"   Results: {self.results_dir}")
            print(f"   Report: {self.report_dir}")
            
            # Check if results directory has content
            result_files = list(self.results_dir.glob("*.json"))
            if not result_files:
                print("⚠️ Warning: No result files found in results directory")
                return False
            
            print(f"   Found {len(result_files)} result files")
            
            result = subprocess.run([
                "allure", "generate", 
                str(self.results_dir), 
                "-o", str(self.report_dir),
                "--clean"
            ], capture_output=True, text=True, check=True)
            
            # Verify report was generated
            index_file = self.report_dir / "index.html"
            if not index_file.exists():
                print("❌ Report generation failed: index.html not found")
                return False
            
            # Check if data directory exists and has content
            data_dir = self.report_dir / "data"
            if not data_dir.exists():
                print("❌ Report generation failed: data directory not found")
                return False
            
            test_cases = list(data_dir.glob("test-cases/*.json"))
            if not test_cases:
                print("⚠️ Warning: No test cases found in generated report")
            
            print(f"✅ Allure report generated successfully")
            print(f"   Report location: {self.report_dir}")
            print(f"   Test cases: {len(test_cases)}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate Allure report: {e}")
            print(f"   Error: {e.stderr}")
            return False
    
    def open_report(self) -> bool:
        """Open Allure report in browser"""
        if not self.report_dir.exists():
            print(f"❌ Report directory not found: {self.report_dir}")
            return False
        
        index_file = self.report_dir / "index.html"
        if not index_file.exists():
            print(f"❌ Report index file not found: {index_file}")
            return False
        
        # Validate report before opening
        if not self.validate_report():
            print("⚠️ Report validation failed, but attempting to open anyway")
        
        try:
            # Get absolute path
            abs_path = index_file.absolute()
            
            if sys.platform == "darwin":  # macOS
                # Use file:// protocol for local files
                file_url = f"file://{abs_path}"
                subprocess.run(["open", file_url])
            elif sys.platform == "linux":  # Linux
                subprocess.run(["xdg-open", str(abs_path)])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", str(abs_path)], shell=True)
            else:
                print(f"📄 Report location: {abs_path}")
            
            print(f"🌐 Opened Allure report: {abs_path}")
            print(f"💡 If you see a loading screen, try:")
            print(f"   1. Refresh the page (F5)")
            print(f"   2. Clear browser cache")
            print(f"   3. Use --serve option instead: python scripts/generate_allure_report.py --serve")
            return True
            
        except Exception as e:
            print(f"❌ Failed to open report: {e}")
            print(f"📄 Manual open: {index_file.absolute()}")
            print(f"💡 Alternative: Use --serve option for better compatibility")
            return False
    
    def serve_report(self, host: str = "localhost", port: int = 8080) -> bool:
        """Serve Allure report on local server"""
        if not self.check_allure_installed():
            return False
        
        if not self.results_dir.exists():
            print(f"❌ Results directory not found: {self.results_dir}")
            return False
        
        try:
            print(f"🌐 Serving Allure report at http://{host}:{port}")
            print("   Press Ctrl+C to stop the server")
            
            subprocess.run([
                "allure", "serve", 
                str(self.results_dir),
                "-h", host,
                "-p", str(port)
            ], check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to serve Allure report: {e}")
            return False
        except KeyboardInterrupt:
            print("\n🛑 Allure server stopped")
            return True
    
    def list_results(self) -> None:
        """List available test results"""
        if not self.results_dir.exists():
            print(f"❌ Results directory not found: {self.results_dir}")
            return
        
        print(f"📋 Test results in: {self.results_dir}")
        
        # List result files
        result_files = list(self.results_dir.glob("*.json"))
        if result_files:
            print(f"   Found {len(result_files)} result files:")
            for file in sorted(result_files, key=lambda x: x.stat().st_mtime, reverse=True):
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                size = file.stat().st_size / 1024  # KB
                print(f"     📄 {file.name} ({size:.1f}KB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("   No result files found")
    
    def clean_results(self) -> bool:
        """Clean test results directory"""
        if self.results_dir.exists():
            import shutil
            shutil.rmtree(self.results_dir)
            print(f"🗑️ Cleaned results directory: {self.results_dir}")
            return True
        else:
            print(f"ℹ️ Results directory does not exist: {self.results_dir}")
            return False
    
    def validate_report(self) -> bool:
        """Validate generated report"""
        if not self.report_dir.exists():
            print(f"❌ Report directory not found: {self.report_dir}")
            return False
        
        index_file = self.report_dir / "index.html"
        if not index_file.exists():
            print(f"❌ Report index file not found: {index_file}")
            return False
        
        data_dir = self.report_dir / "data"
        if not data_dir.exists():
            print(f"❌ Report data directory not found: {data_dir}")
            return False
        
        test_cases = list(data_dir.glob("test-cases/*.json"))
        if not test_cases:
            print(f"⚠️ No test cases found in report")
            return False
        
        attachments = list(data_dir.glob("attachments/*"))
        if not attachments:
            print(f"⚠️ No attachments found in report")
        else:
            print(f"✅ Found {len(attachments)} attachments")
        
        print(f"✅ Report validation passed")
        print(f"   Test cases: {len(test_cases)}")
        print(f"   Attachments: {len(attachments)}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Allure Report Generator")
    parser.add_argument("--results-dir", default="reports/allure-results", 
                       help="Test results directory")
    parser.add_argument("--report-dir", default="reports/allure-report", 
                       help="Report output directory")
    parser.add_argument("--generate", action="store_true", 
                       help="Generate Allure report")
    parser.add_argument("--open", action="store_true", 
                       help="Open generated report in browser")
    parser.add_argument("--serve", action="store_true", 
                       help="Serve report on local server")
    parser.add_argument("--list", action="store_true", 
                       help="List available test results")
    parser.add_argument("--clean", action="store_true", 
                       help="Clean results directory")
    parser.add_argument("--validate", action="store_true", 
                       help="Validate generated report")
    parser.add_argument("--host", default="localhost", 
                       help="Host for serving report")
    parser.add_argument("--port", type=int, default=8080, 
                       help="Port for serving report")
    
    args = parser.parse_args()
    
    generator = AllureReportGenerator(args.results_dir, args.report_dir)
    
    if args.clean:
        generator.clean_results()
    
    if args.list:
        generator.list_results()
    
    if args.validate:
        generator.validate_report()
    
    if args.generate:
        if generator.generate_report():
            if args.open:
                generator.open_report()
    
    if args.serve:
        generator.serve_report(args.host, args.port)
    
    # Default: generate and open
    if not any([args.generate, args.open, args.serve, args.list, args.clean, args.validate]):
        if generator.generate_report():
            generator.open_report()


if __name__ == "__main__":
    main()
