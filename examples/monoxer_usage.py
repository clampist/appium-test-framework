"""
Simple standalone test for Monoxer App
"""

import time
import os
import shutil
import sys
import argparse
from datetime import datetime
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageChops
import hashlib

APP_PACKAGE = "com.monoxer"
APP_ACTIVITY = "com.monoxer.view.main.MainActivity"
WAIT_TIME = 15

def clear_screenshot_directory():
    """Clear screenshot directory before test run"""
    screenshot_dir = f"screenshots/{APP_PACKAGE}/cur"
    if os.path.exists(screenshot_dir):
        try:
            shutil.rmtree(screenshot_dir)
            print(f"🗑️ Cleared screenshot directory: {screenshot_dir}")
        except Exception as e:
            print(f"⚠️ Failed to clear screenshot directory: {str(e)}")
    else:
        print(f"ℹ️ Screenshot directory does not exist: {screenshot_dir}")
        # Create the directory if it doesn't exist
        os.makedirs(screenshot_dir, exist_ok=True)
        print(f"📁 Created screenshot directory: {screenshot_dir}")

def compare_screenshots():
    """Compare screenshots between base and cur directories"""
    base_dir = f"screenshots/{APP_PACKAGE}/base"
    cur_dir = f"screenshots/{APP_PACKAGE}/cur"
    
    if not os.path.exists(base_dir):
        print(f"ℹ️ Base directory does not exist: {base_dir}")
        return False
    
    if not os.path.exists(cur_dir):
        print(f"ℹ️ Current directory does not exist: {cur_dir}")
        return False
    
    base_files = set(os.listdir(base_dir))
    cur_files = set(os.listdir(cur_dir))
    
    # Find common files (same step numbers)
    common_files = base_files.intersection(cur_files)
    
    if not common_files:
        print("ℹ️ No common screenshot files found for comparison")
        return False
    
    print(f"🔍 Comparing {len(common_files)} screenshot files...")
    
    differences = []
    identical = []
    
    for filename in sorted(common_files):
        if not filename.endswith('.png'):
            continue
            
        base_path = os.path.join(base_dir, filename)
        cur_path = os.path.join(cur_dir, filename)
        
        try:
            # Load images
            base_img = Image.open(base_path)
            cur_img = Image.open(cur_path)
            
            # Compare images
            if base_img.size != cur_img.size:
                differences.append(f"Size mismatch: {filename}")
                continue
            
            # Convert to same mode if needed
            if base_img.mode != cur_img.mode:
                base_img = base_img.convert(cur_img.mode)
            
            # Calculate difference
            diff = ImageChops.difference(base_img, cur_img)
            
            if diff.getbbox() is None:
                identical.append(filename)
                print(f"✅ {filename} - Identical")
            else:
                differences.append(filename)
                print(f"❌ {filename} - Different")
                
        except Exception as e:
            differences.append(f"Error comparing {filename}: {str(e)}")
            print(f"⚠️ Error comparing {filename}: {str(e)}")
    
    print(f"\n📊 Comparison Summary:")
    print(f"   Identical: {len(identical)}")
    print(f"   Different: {len(differences)}")
    
    if differences:
        print(f"\n❌ Differences found in:")
        for diff in differences:
            print(f"   - {diff}")
        return False
    else:
        print(f"\n✅ All screenshots are identical!")
        return True

def set_base_screenshots():
    """Set current screenshots as base screenshots"""
    base_dir = f"screenshots/{APP_PACKAGE}/base"
    cur_dir = f"screenshots/{APP_PACKAGE}/cur"
    
    # Check if base directory is empty
    if os.path.exists(base_dir) and os.listdir(base_dir):
        print(f"❌ Base directory is not empty: {base_dir}")
        print("   Cannot auto-set base screenshots. Please clear base directory first.")
        return False
    
    if not os.path.exists(cur_dir):
        print(f"❌ Current directory does not exist: {cur_dir}")
        return False
    
    cur_files = os.listdir(cur_dir)
    if not cur_files:
        print(f"❌ Current directory is empty: {cur_dir}")
        return False
    
    try:
        # Create base directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
        # Copy all files from cur to base
        for filename in cur_files:
            src = os.path.join(cur_dir, filename)
            dst = os.path.join(base_dir, filename)
            shutil.copy2(src, dst)
        
        print(f"✅ Set {len(cur_files)} screenshots as base screenshots")
        return True
        
    except Exception as e:
        print(f"❌ Failed to set base screenshots: {str(e)}")
        return False

def auto_set_base_if_successful():
    """Auto set base screenshots if all tests are successful and base is empty"""
    base_dir = f"screenshots/{APP_PACKAGE}/base"
    cur_dir = f"screenshots/{APP_PACKAGE}/cur"
    
    # Check if base directory is empty
    if os.path.exists(base_dir) and os.listdir(base_dir):
        print(f"ℹ️ Base directory is not empty, skipping auto-set")
        return False
    
    # Check if current directory has screenshots
    if not os.path.exists(cur_dir) or not os.listdir(cur_dir):
        print(f"ℹ️ Current directory is empty, skipping auto-set")
        return False
    
    print(f"🔄 Auto-setting base screenshots...")
    return set_base_screenshots()

def click_home_tab(driver, wait):
    """Click home tab to return to main page"""
    try:
        home_tab = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ID, "com.monoxer:id/bottom_navigation_home_for_individuals")
        ))
        home_tab.click()
        print("✅ Clicked home tab")
        time.sleep(2)  # Wait for home page to load
        return True
    except Exception as e:
        print(f"⚠️ Failed to click home tab: {str(e)}")
        return False

def create_driver():
    """Create Appium driver with Monoxer app configuration"""
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:platformVersion": "13",
        "appium:deviceName": "emulator-5554",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": APP_PACKAGE,
        "appium:appActivity": APP_ACTIVITY,
        "appium:noReset": "true",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True
    })
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)    
    return driver

def open_sidebar(driver, wait):
    """Open the left sidebar by clicking the header selector"""
    try:
        # Click the header selector to open sidebar
        header_selector = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ID, "com.monoxer:id/iOS_like_header_org_selector")
        ))
        header_selector.click()
        print("✅ Sidebar opened successfully")
        time.sleep(2)  # Wait for sidebar animation
        return True
    except Exception as e:
        print(f"❌ Failed to open sidebar: {str(e)}")
        return False

def test_invitation_code(driver, wait):
    """Test invitation code feature"""
    print("🔑 Testing invitation code feature...")
    
    # Ensure we start from home page
    click_home_tab(driver, wait)
    
    try:
        # Open sidebar first
        if not open_sidebar(driver, wait):
            print("❌ Failed to open sidebar")
            return False
        
        save_screenshot(driver, "sidebar_opened", "02")
        
        # Click "Enter invitation code" text
        invitation_code_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter invitation code")')
        ))
        invitation_code_btn.click()
        print("✅ Clicked 'Enter invitation code'")
        
        # Wait for page to load
        time.sleep(1)
        
        # Take screenshot after clicking invitation code button
        save_screenshot(driver, "invitation_code_page", "03a")
        
        # Click "Navigate up" to return to home
        navigate_up_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ACCESSIBILITY_ID, "Navigate up")
        ))
        navigate_up_btn.click()
        print("✅ Clicked 'Navigate up' to return home")
        
        # Ensure we're back to home page
        click_home_tab(driver, wait)
        
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Failed to test invitation code: {str(e)}")
        # Try to return to home page even if test fails
        click_home_tab(driver, wait)
        return False

def test_sync_feature(driver, wait):
    """Test sync feature"""
    print("🔄 Testing sync feature...")
    
    # Ensure we start from home page
    click_home_tab(driver, wait)
    
    try:
        # Open sidebar first
        if not open_sidebar(driver, wait):
            print("❌ Failed to open sidebar")
            return False
        
        save_screenshot(driver, "sidebar_opened", "05")
        
        # Click "Sync" text
        sync_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sync")')
        ))
        sync_btn.click()
        print("✅ Clicked 'Sync' button")
        
        # Wait for sync operation to complete
        print("⏳ Waiting for sync operation...")
        time.sleep(1)
        
        # Take screenshot after clicking sync button
        save_screenshot(driver, "sync_button_clicked", "05a")        
        
        # Check for "Synced" toast message
        try:
            # Look for toast message (may appear briefly)
            synced_toast = driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'Synced')]")
            if synced_toast.is_displayed():
                print("✅ 'Synced' toast message detected")
            else:
                print("ℹ️ Sync operation completed (toast may have disappeared)")
        except:
            print("ℹ️ Sync operation completed")
        
        # Click linear_layout to return to main page
        try:
            linear_layout_btn = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, "com.monoxer:id/linear_layout")
            ))
            linear_layout_btn.click()
            print("✅ Clicked linear_layout to return to main page")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Failed to click linear_layout: {str(e)}")
        
        # Ensure we're back to home page
        click_home_tab(driver, wait)
        
        return True
    except Exception as e:
        print(f"❌ Failed to test sync feature: {str(e)}")
        # Try to return to home page even if test fails
        click_home_tab(driver, wait)
        return False

def test_search_feature(driver, wait):
    """Test search feature"""
    print("🔍 Testing search feature...")
    
    # Ensure we start from home page
    click_home_tab(driver, wait)
    
    try:
        # Click search tab in bottom navigation
        search_tab = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ID, "com.monoxer:id/bottom_navigation_search")
        ))
        search_tab.click()
        print("✅ Clicked search tab")
        
        # Wait for search page to load
        time.sleep(2)
        save_screenshot(driver, "search_page_opened", "07")
        
        # Try to find and interact with search input field
        try:
            # Try multiple approaches to find search input
            search_input = None
            
            # Method 1: Try with search_src_text ID
            try:
                search_input = wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ID, "com.monoxer:id/search_src_text")
                ))
                print("✅ Found search input with search_src_text ID")
            except:
                # Method 2: Try with search_view ID
                try:
                    search_input = wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, "com.monoxer:id/search_view")
                    ))
                    print("✅ Found search input with search_view ID")
                except:
                    # Method 3: Try with AutoCompleteTextView class
                    try:
                        search_input = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.AutoCompleteTextView")
                        print("✅ Found search input with AutoCompleteTextView class")
                    except:
                        # Method 4: Try with any clickable element that might be search
                        try:
                            search_input = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                                'new UiSelector().className("android.widget.AutoCompleteTextView")')
                            print("✅ Found search input with UiAutomator")
                        except:
                            print("❌ Could not find search input field")
                            save_screenshot(driver, "search_input_not_found", "08")
                            return False
            
            if search_input:
                # Click and type in search field
                search_input.click()
                print("✅ Clicked search input field")
                
                # Re-find the element to avoid stale element reference
                try:
                    search_input = wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, "com.monoxer:id/search_src_text")
                    ))
                    # Clear and type search query
                    search_input.clear()
                    search_input.send_keys("日本の祝日")
                    print("✅ Typed search query: 日本の祝日")
                except:
                    # Try alternative method if the first one fails
                    try:
                        search_input = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.AutoCompleteTextView")
                        search_input.clear()
                        search_input.send_keys("日本の祝日")
                        print("✅ Typed search query: 日本の祝日 (alternative method)")
                    except Exception as e:
                        print(f"❌ Failed to type in search field: {str(e)}")
                        return False
                
                # Wait for search results
                print("⏳ Waiting for search results...")
                time.sleep(3)
                save_screenshot(driver, "search_results", "08")
                
                # Try to click first search result
                try:
                    first_result = wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, "com.monoxer:id/card_view")
                    ))
                    first_result.click()
                    print("✅ Clicked first search result")
                    
                    # Wait for detail page to load
                    time.sleep(2)
                    save_screenshot(driver, "search_result_detail", "09")
                    
                    # Try to click contents button
                    try:
                        contents_btn = wait.until(EC.element_to_be_clickable(
                            (AppiumBy.ID, "com.monoxer:id/contents")
                        ))
                        contents_btn.click()
                        print("✅ Clicked contents button")
                        
                        # Wait for contents page to load
                        time.sleep(2)
                        save_screenshot(driver, "contents_page", "10")
                        
                        # Click back button 4 times to return to tabs view
                        for i in range(4):
                            try:
                                back_btn = wait.until(EC.element_to_be_clickable(
                                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Navigate up")')
                                ))
                                back_btn.click()
                                print(f"✅ Clicked back button ({i+1}/4)")
                                time.sleep(1)  # Wait between back clicks
                            except Exception as e:
                                print(f"⚠️ Failed to click back button ({i+1}/4): {str(e)}")
                                break
                        
                        # Click home tab to return to main page
                        click_home_tab(driver, wait)
                        
                    except Exception as e:
                        print(f"⚠️ Contents button not found: {str(e)}")
                        save_screenshot(driver, "contents_button_not_found", "10")
                        # Try to return to home page
                        click_home_tab(driver, wait)
                    
                except Exception as e:
                    print(f"⚠️ Search result not found: {str(e)}")
                    save_screenshot(driver, "search_result_not_found", "09")
                    # Try to return to home page
                    click_home_tab(driver, wait)
            
        except Exception as e:
            print(f"❌ Error in search input interaction: {str(e)}")
            save_screenshot(driver, "search_input_error", "08")
            # Try to return to home page
            click_home_tab(driver, wait)
            return False
        
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Failed to test search feature: {str(e)}")
        # Try to return to home page even if test fails
        click_home_tab(driver, wait)
        return False

def test_study_mode(driver, wait, step_prefix="17"):
    """Test STUDY mode - can be called from different entry points"""
    print("📖 Testing STUDY mode...")
    
    try:
        # Try multiple approaches to find start_test button
        start_test_btn = None
        
        try:
            # Method 1: Try with exact ID
            start_test_btn = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ID, "com.monoxer:id/start_test")
            ))
            print("✅ Found start_test button with ID")
        except:
            try:
                # Method 2: Try with class name
                start_test_btn = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.Button")
                print("✅ Found start_test button with class name")
            except:
                try:
                    # Method 3: Try with UiAutomator
                    start_test_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                        'new UiSelector().resourceId("com.monoxer:id/start_test")')
                    print("✅ Found start_test button with UiAutomator")
                except:
                    try:
                        # Method 4: Try with XPath
                        start_test_btn = driver.find_element(AppiumBy.XPATH, 
                            '//android.widget.Button[@resource-id="com.monoxer:id/start_test"]')
                        print("✅ Found start_test button with XPath")
                    except:
                        try:
                            # Method 5: Try with text content
                            start_test_btn = driver.find_element(AppiumBy.XPATH, "//*[@text='STUDY']")
                            print("✅ Found start_test button with text 'STUDY'")
                        except:
                            print("❌ Could not find start_test button")
                            save_screenshot(driver, "start_test_not_found", f"{step_prefix}")
                            return False
        
        if start_test_btn:
            start_test_btn.click()
            print("✅ Clicked 'Start Test' button")
            
            # Wait for STUDY page to load
            time.sleep(3)
            save_screenshot(driver, "study_page_opened", f"{step_prefix}")
            
            # Answer first question - try choice or fill-in-the-blank
            try:
                # Try to find choice1_text first (multiple choice question)
                try:
                    choice1 = wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, "com.monoxer:id/choice1_text")
                    ))
                    choice1.click()
                    print("✅ Clicked first choice for question 1 (multiple choice)")
                    
                    # Wait and take screenshot
                    time.sleep(0.001)
                    save_screenshot(driver, "question1_answered", f"{int(step_prefix)+1}")
                    
                except Exception as choice_error:
                    print("ℹ️ No multiple choice found, trying fill-in-the-blank...")
                    
                    # Try to click Done button on virtual keyboard (fill-in-the-blank question)
                    try:
                        done_btn = wait.until(EC.element_to_be_clickable(
                            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Done")')
                        ))
                        done_btn.click()
                        print("✅ Clicked 'Done' button for question 1 (fill-in-the-blank)")
                        
                    except Exception as done_error:
                        try:
                            # Alternative XPath for Done button
                            done_btn = driver.find_element(AppiumBy.XPATH, 
                                '//android.widget.TextView[@resource-id="com.monoxer:id/label" and @text="Done"]')
                            done_btn.click()
                            print("✅ Clicked 'Done' button for question 1 (fill-in-the-blank) - XPath")
                            
                        except Exception as xpath_error:
                            print(f"❌ Could not find Done button: {str(xpath_error)}")
                            save_screenshot(driver, "done_button_not_found", f"{int(step_prefix)+1}")
                            raise xpath_error
                    
                    # Wait and take screenshot
                    time.sleep(0.001)
                    save_screenshot(driver, "question1_answered", f"{int(step_prefix)+1}")
                
                # Wait 5 seconds as requested
                print("⏳ Waiting 5 seconds...")
                time.sleep(5)
                
                # Answer second question - try choice or fill-in-the-blank again
                try:
                    # Try to find choice1_text first (multiple choice question)
                    try:
                        choice1_2 = wait.until(EC.element_to_be_clickable(
                            (AppiumBy.ID, "com.monoxer:id/choice1_text")
                        ))
                        choice1_2.click()
                        print("✅ Clicked first choice for question 2 (multiple choice)")
                        
                    except Exception as choice_error2:
                        print("ℹ️ No multiple choice found for question 2, trying fill-in-the-blank...")
                        
                        # Try to click Done button on virtual keyboard (fill-in-the-blank question)
                        try:
                            done_btn2 = wait.until(EC.element_to_be_clickable(
                                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Done")')
                            ))
                            done_btn2.click()
                            print("✅ Clicked 'Done' button for question 2 (fill-in-the-blank)")
                            
                        except Exception as done_error2:
                            try:
                                # Alternative XPath for Done button
                                done_btn2 = driver.find_element(AppiumBy.XPATH, 
                                    '//android.widget.TextView[@resource-id="com.monoxer:id/label" and @text="Done"]')
                                done_btn2.click()
                                print("✅ Clicked 'Done' button for question 2 (fill-in-the-blank) - XPath")
                                
                            except Exception as xpath_error2:
                                print(f"❌ Could not find Done button for question 2: {str(xpath_error2)}")
                                save_screenshot(driver, "done_button_not_found_q2", f"{int(step_prefix)+2}")
                                raise xpath_error2
                    
                    # Wait and take screenshot
                    time.sleep(0.001)
                    save_screenshot(driver, "question2_answered", f"{int(step_prefix)+2}")
                    
                except Exception as e:
                    print(f"⚠️ Failed to answer second question: {str(e)}")
                    save_screenshot(driver, "question2_failed", f"{int(step_prefix)+2}")
                
            except Exception as e:
                print(f"⚠️ Failed to answer first question: {str(e)}")
                save_screenshot(driver, "question1_failed", f"{int(step_prefix)+1}")
            
            # Click back button to return from STUDY mode
            try:
                back_btn = wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Navigate up")
                ))
                back_btn.click()
                print("✅ Clicked back button from STUDY mode")
                
                # Wait for return to deck page
                time.sleep(2)
                save_screenshot(driver, "returned_from_study", f"{int(step_prefix)+3}")
                
            except Exception as e:
                print(f"⚠️ Failed to click back button from STUDY: {str(e)}")
                save_screenshot(driver, "study_back_failed", f"{int(step_prefix)+3}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test STUDY mode: {str(e)}")
        return False

def test_library_feature(driver, wait):
    """Test library feature"""
    print("📚 Testing library feature...")
    
    # Ensure we start from home page
    click_home_tab(driver, wait)
    
    try:
        # Click library tab in bottom navigation
        library_tab = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ID, "com.monoxer:id/bottom_navigation_library")
        ))
        library_tab.click()
        print("✅ Clicked library tab")
        
        # Wait for library page to load
        time.sleep(2)
        save_screenshot(driver, "library_page_opened", "12")
        
        # Click "My Books" tab
        try:
            my_books_tab = wait.until(EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "My Books")
            ))
            my_books_tab.click()
            print("✅ Clicked 'My Books' tab")
            
            # Wait for My Books content to load
            time.sleep(2)
            save_screenshot(driver, "my_books_tab_selected", "13")
            
            # Try to find and click open_deck button
            try:
                # First, try to find open_deck button directly
                open_deck_btn = driver.find_element(AppiumBy.ID, "com.monoxer:id/open_deck")
                open_deck_btn.click()
                print("✅ Clicked 'Open Deck' button directly")
                
            except Exception as e:
                print("ℹ️ Open deck button not found directly, trying to click auto_test title first...")
                
                # If open_deck not found, try to click auto_test title first
                try:
                    auto_test_title = wait.until(EC.element_to_be_clickable(
                        (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='com.monoxer:id/word_books_book_title' and @text='auto_test']")
                    ))
                    auto_test_title.click()
                    print("✅ Clicked 'auto_test' title")
                    
                    # Wait for page to load
                    time.sleep(2)
                    save_screenshot(driver, "auto_test_selected", "14a")
                    
                    # Now try to click open_deck button
                    open_deck_btn = wait.until(EC.element_to_be_clickable(
                        (AppiumBy.ID, "com.monoxer:id/open_deck")
                    ))
                    open_deck_btn.click()
                    print("✅ Clicked 'Open Deck' button after selecting auto_test")
                    
                except Exception as e2:
                    print(f"❌ Failed to click auto_test title or open_deck: {str(e2)}")
                    save_screenshot(driver, "auto_test_or_open_deck_failed", "14a")
                    return False
            
            # Wait for deck to open
            time.sleep(2)
            save_screenshot(driver, "deck_opened", "14")
            
            # Click back button
            try:
                back_btn = wait.until(EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Navigate up")
                ))
                back_btn.click()
                print("✅ Clicked back button")
                
                # Wait for return to library
                time.sleep(2)
                save_screenshot(driver, "returned_to_library", "15")
                
            except Exception as e:
                print(f"⚠️ Failed to click back button: {str(e)}")
                save_screenshot(driver, "back_button_failed", "15")
            
            # Test STUDY mode using the independent function
            test_study_mode(driver, wait, "17")
            
        except Exception as e:
            print(f"⚠️ My Books tab not found: {str(e)}")
            save_screenshot(driver, "my_books_tab_not_found", "13")
        
        # Ensure we're back to home page
        click_home_tab(driver, wait)
        
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Failed to test library feature: {str(e)}")
        # Try to return to home page even if test fails
        click_home_tab(driver, wait)
        return False

def save_screenshot(driver, name="monoxer", step_num="01"):
    """Save screenshot with timestamp and step number"""
    import os
    
    # Create directory structure: screenshots/com.monoxer/cur/
    screenshot_dir = f"screenshots/{APP_PACKAGE}/cur"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"{screenshot_dir}/{now}_{step_num}_{name}.png"
    driver.save_screenshot(screenshot_path)
    print(f"✅ Screenshot saved: {screenshot_path}")

def run_single_test(driver, wait, test_name):
    """Run a single test based on test name"""
    print(f"\n" + "="*50)
    print(f"🧪 TESTING FEATURE: {test_name.upper()}")
    print("="*50)
    
    test_success = False
    
    if test_name == "invitation":
        if test_invitation_code(driver, wait):
            save_screenshot(driver, "invitation_code_completed", "04")
            test_success = True
        else:
            save_screenshot(driver, "invitation_code_failed", "04")
    elif test_name == "sync":
        if test_sync_feature(driver, wait):
            save_screenshot(driver, "sync_completed", "06")
            test_success = True
        else:
            save_screenshot(driver, "sync_failed", "06")
    elif test_name == "search":
        if test_search_feature(driver, wait):
            save_screenshot(driver, "search_completed", "11")
            test_success = True
        else:
            save_screenshot(driver, "search_failed", "11")
    elif test_name == "library":
        if test_library_feature(driver, wait):
            save_screenshot(driver, "library_completed", "16")
            test_success = True
        else:
            save_screenshot(driver, "library_failed", "16")
    else:
        print(f"❌ Unknown test name: {test_name}")
        print("Available tests: invitation, sync, search, library")
        return False
    
    return test_success

def run_all_tests(driver, wait):
    """Run all tests in sequence"""
    print("🚀 Running all tests...")
    
    all_tests_success = True
    
    # Test Feature 1: Invitation Code
    print("\n" + "="*50)
    print("🧪 TESTING FEATURE 1: INVITATION CODE")
    print("="*50)
    
    # Test invitation code feature (independent)
    if test_invitation_code(driver, wait):
        save_screenshot(driver, "invitation_code_completed", "04")
    else:
        save_screenshot(driver, "invitation_code_failed", "04")
        all_tests_success = False
    
    # Test Feature 2: Sync
    print("\n" + "="*50)
    print("🧪 TESTING FEATURE 2: SYNC")
    print("="*50)
    
    # Test sync feature (independent)
    if test_sync_feature(driver, wait):
        save_screenshot(driver, "sync_completed", "06")
    else:
        save_screenshot(driver, "sync_failed", "06")
        all_tests_success = False
    
    # Test Feature 3: Search
    print("\n" + "="*50)
    print("🧪 TESTING FEATURE 3: SEARCH")
    print("="*50)
    
    # Test search feature (independent)
    if test_search_feature(driver, wait):
        save_screenshot(driver, "search_completed", "11")
    else:
        save_screenshot(driver, "search_failed", "11")
        all_tests_success = False
    
    # Test Feature 4: Library
    print("\n" + "="*50)
    print("🧪 TESTING FEATURE 4: LIBRARY")
    print("="*50)
    
    # Test library feature (independent)
    if test_library_feature(driver, wait):
        save_screenshot(driver, "library_completed", "16")
    else:
        save_screenshot(driver, "library_failed", "16")
        all_tests_success = False
    
    return all_tests_success

def main():
    """Main function to test Monoxer app"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Monoxer App Test Suite')
    parser.add_argument('--test', '-t', 
                       choices=['invitation', 'sync', 'search', 'library', 'all'],
                       default='all',
                       help='Test to run: invitation, sync, search, library, or all (default)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List available tests')
    parser.add_argument('--compare', '-c', action='store_true',
                       help='Compare screenshots between base and cur directories')
    parser.add_argument('--set-base', '-s', action='store_true',
                       help='Set current screenshots as base screenshots')
    parser.add_argument('--clear-base', action='store_true',
                       help='Clear base screenshots directory')
    
    args = parser.parse_args()
    
    # Handle screenshot management commands
    if args.compare:
        print("🔍 Comparing screenshots...")
        compare_screenshots()
        return
    
    if args.set_base:
        print("📸 Setting base screenshots...")
        set_base_screenshots()
        return
    
    if args.clear_base:
        base_dir = f"screenshots/{APP_PACKAGE}/base"
        if os.path.exists(base_dir):
            try:
                shutil.rmtree(base_dir)
                print(f"🗑️ Cleared base screenshots directory: {base_dir}")
            except Exception as e:
                print(f"❌ Failed to clear base directory: {str(e)}")
        else:
            print(f"ℹ️ Base directory does not exist: {base_dir}")
        return
    
    # List available tests if requested
    if args.list:
        print("📋 Available tests:")
        print("  invitation  - Test invitation code feature")
        print("  sync        - Test sync feature")
        print("  search      - Test search feature")
        print("  library     - Test library feature")
        print("  all         - Run all tests (default)")
        print("\n📸 Screenshot management:")
        print("  --compare   - Compare screenshots between base and cur")
        print("  --set-base  - Set current screenshots as base")
        print("  --clear-base - Clear base screenshots directory")
        return
    
    print("🚀 Starting Monoxer app test...")
    print(f"🎯 Test mode: {args.test}")
    
    # Clear screenshot directory before test run
    clear_screenshot_directory()
    
    driver = create_driver()
    print("📱 Driver created successfully")
    
    try:
        # Activate the app
        driver.activate_app(APP_PACKAGE)
        print("📱 App activated")
        
        # Wait for app to load
        wait = WebDriverWait(driver, WAIT_TIME)
        print(f"⏳ Waiting {WAIT_TIME} seconds for app to load...")
        time.sleep(5)  # Give app time to start
        
        # Click home tab to ensure we're on the main page
        click_home_tab(driver, wait)
        
        # Take initial screenshot
        save_screenshot(driver, "initial", "01")
        
        # Run tests based on argument
        test_success = True
        if args.test == 'all':
            test_success = run_all_tests(driver, wait)
        else:
            test_success = run_single_test(driver, wait, args.test)
        
        # Terminate the app
        driver.terminate_app(APP_PACKAGE)
        print("📱 App terminated")
        
        # Compare screenshots if base exists
        print("\n" + "="*50)
        print("🔍 SCREENSHOT COMPARISON")
        print("="*50)
        compare_screenshots()
        
        # Auto set base screenshots if all tests successful and base is empty
        if test_success:
            print("\n" + "="*50)
            print("🔄 AUTO-SET BASE SCREENSHOTS")
            print("="*50)
            auto_set_base_if_successful()
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        # Take screenshot even if there's an error
        try:
            save_screenshot(driver, "error", "99")
        except:
            pass
    finally:
        driver.quit()
        print("🔚 Test completed")

if __name__ == "__main__":
    main()
