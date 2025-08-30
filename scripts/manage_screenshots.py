#!/usr/bin/env python3
"""
Screenshot Management Script
"""

import argparse
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.utils.screenshot_utils import ScreenshotUtils
from core.utils.logger import Log


def main():
    """Main function for screenshot management"""
    parser = argparse.ArgumentParser(description='Screenshot Management Tool')
    parser.add_argument('--app-package', '-a', required=True,
                       help='Application package name (e.g., com.monoxer)')
    parser.add_argument('--compare', '-c', action='store_true',
                       help='Compare screenshots between base and cur directories')
    parser.add_argument('--set-base', '-s', action='store_true',
                       help='Set current screenshots as base screenshots')
    parser.add_argument('--clear-base', action='store_true',
                       help='Clear base screenshots directory')
    parser.add_argument('--clear-cur', action='store_true',
                       help='Clear current screenshots directory')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List available commands')
    
    args = parser.parse_args()
    
    # List available commands if requested
    if args.list:
        print("📋 Available screenshot management commands:")
        print("  --compare     - Compare screenshots between base and cur")
        print("  --set-base    - Set current screenshots as base")
        print("  --clear-base  - Clear base screenshots directory")
        print("  --clear-cur   - Clear current screenshots directory")
        print("\n📝 Usage examples:")
        print("  python scripts/manage_screenshots.py -a com.monoxer --compare")
        print("  python scripts/manage_screenshots.py -a com.monoxer --set-base")
        print("  python scripts/manage_screenshots.py -a com.monoxer --clear-base")
        return
    
    app_package = args.app_package
    
    # Handle screenshot management commands
    if args.compare:
        print(f"🔍 Comparing screenshots for {app_package}...")
        ScreenshotUtils.compare_screenshots(app_package)
    
    elif args.set_base:
        print(f"📸 Setting base screenshots for {app_package}...")
        ScreenshotUtils.set_base_screenshots(app_package)
    
    elif args.clear_base:
        print(f"🗑️ Clearing base screenshots for {app_package}...")
        ScreenshotUtils.clear_base_screenshots(app_package)
    
    elif args.clear_cur:
        print(f"🗑️ Clearing current screenshots for {app_package}...")
        ScreenshotUtils.clear_screenshot_directory(app_package)
    
    else:
        print("❌ No action specified. Use --help for usage information.")
        print("   Use --list to see available commands.")


if __name__ == "__main__":
    main()
