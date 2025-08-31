#!/usr/bin/env python3
"""
Configuration Validation Script for Monoxer Tests
Validates the new configuration system
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from configs.config_manager import config_manager, get_appium_config, get_server_config


def validate_configuration():
    """Validate the configuration system"""
    print("🔧 Validating Monoxer Configuration System")
    print("=" * 50)
    
    try:
        # 1. Validate configuration file
        print("1. Validating configuration file...")
        config_manager.validate_config()
        print("   ✅ Configuration file is valid")
        
        # 2. List available languages
        print("\n2. Available languages:")
        languages = config_manager.list_available_languages()
        for lang in languages:
            print(f"   - {lang}")
        
        # 3. Test configuration loading for each language
        print("\n3. Testing configuration loading:")
        for language in languages:
            try:
                config = get_appium_config(language)
                device_name = config.get('deviceName', 'Unknown')
                platform_version = config.get('platformVersion', 'Unknown')
                print(f"   ✅ {language}: {device_name} (Android {platform_version})")
            except Exception as e:
                print(f"   ❌ {language}: {e}")
        
        # 4. Test server configuration
        print("\n4. Server configuration:")
        server_config = get_server_config()
        host = server_config.get('host', 'Unknown')
        port = server_config.get('port', 'Unknown')
        print(f"   ✅ Server: {host}:{port}")
        
        # 5. Test timeout configuration
        print("\n5. Timeout configuration:")
        timeout_config = config_manager.get_timeout_config()
        explicit_wait = timeout_config.get('explicit_wait', 'Unknown')
        print(f"   ✅ Explicit wait: {explicit_wait}s")
        
        # 6. Test screenshot configuration
        print("\n6. Screenshot configuration:")
        screenshot_config = config_manager.get_screenshot_config()
        enabled = screenshot_config.get('enabled', False)
        format_type = screenshot_config.get('format', 'Unknown')
        print(f"   ✅ Screenshots: {'enabled' if enabled else 'disabled'} ({format_type})")
        
        print("\n🎉 All configurations validated successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Configuration validation failed: {e}")
        return False


def show_configuration_details():
    """Show detailed configuration information"""
    print("\n📋 Configuration Details")
    print("=" * 30)
    
    # Show English configuration
    print("\n🇺🇸 English Configuration:")
    en_config = get_appium_config("en")
    for key, value in en_config.items():
        print(f"   {key}: {value}")
    
    # Show Japanese configuration
    print("\n🇯🇵 Japanese Configuration:")
    ja_config = get_appium_config("ja")
    for key, value in ja_config.items():
        print(f"   {key}: {value}")
    
    # Show server configuration
    print("\n🌐 Server Configuration:")
    server_config = get_server_config()
    for key, value in server_config.items():
        print(f"   {key}: {value}")


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--details":
        show_configuration_details()
    else:
        success = validate_configuration()
        if success:
            print("\n💡 Use --details flag to see full configuration")
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
