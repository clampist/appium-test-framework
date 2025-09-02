#!/bin/bash

# TikTok App Test Runner Script
# Run automated tests for TikTok App

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_DIR="tests/com.ss.android.ugc.trill"
REPORT_DIR="reports"
ALLURE_RESULTS_DIR="$REPORT_DIR/allure-results"
HTML_REPORT_DIR="$REPORT_DIR/html"
JUNIT_REPORT_DIR="$REPORT_DIR/junit"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed or not in PATH"
        exit 1
    fi
    
    # Check if pytest is available
    if ! python3 -c "import pytest" &> /dev/null; then
        print_error "pytest is not installed. Please install it first."
        exit 1
    fi
    
    # Check if test directory exists
    if [ ! -d "$TEST_DIR" ]; then
        print_error "Test directory $TEST_DIR does not exist"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to create report directories
create_report_dirs() {
    print_info "Creating report directories..."
    
    mkdir -p "$ALLURE_RESULTS_DIR"
    mkdir -p "$HTML_REPORT_DIR"
    mkdir -p "$JUNIT_REPORT_DIR"
    
    print_success "Report directories created"
}

# Function to run tests
run_tests() {
    local language=${1:-"en"}
    local test_type=${2:-"all"}
    
    print_info "Running TikTok tests (Language: $language, Type: $test_type)"
    
    # Base pytest command
    local pytest_cmd="pytest $TEST_DIR"
    
    # Add language parameter
    pytest_cmd="$pytest_cmd --language=$language"
    
    # Add markers based on test type
    case $test_type in
        "smoke")
            pytest_cmd="$pytest_cmd -m 'tiktok and smoke'"
            ;;
        "regression")
            pytest_cmd="$pytest_cmd -m 'tiktok and regression'"
            ;;
        "all"|*)
            pytest_cmd="$pytest_cmd -m tiktok"
            ;;
    esac
    
    # Add reporting options
    pytest_cmd="$pytest_cmd --alluredir=$ALLURE_RESULTS_DIR"
    pytest_cmd="$pytest_cmd --html=$HTML_REPORT_DIR/tiktok_report_$(date +%Y%m%d_%H%M%S).html"
    pytest_cmd="$pytest_cmd --junitxml=$JUNIT_REPORT_DIR/tiktok_junit_$(date +%Y%m%d_%H%M%S).xml"
    pytest_cmd="$pytest_cmd -v --tb=short"
    
    print_info "Executing: $pytest_cmd"
    
    # Run the tests
    if eval $pytest_cmd; then
        print_success "Tests completed successfully"
        return 0
    else
        print_error "Tests failed"
        return 1
    fi
}

# Function to generate Allure report
generate_allure_report() {
    print_info "Generating Allure report..."
    
    if command -v allure &> /dev/null; then
        allure generate "$ALLURE_RESULTS_DIR" --clean -o "$REPORT_DIR/allure-report"
        print_success "Allure report generated at $REPORT_DIR/allure-report"
        
        # Open report if requested
        if [ "$1" = "--open" ]; then
            print_info "Opening Allure report..."
            allure open "$REPORT_DIR/allure-report"
        fi
    else
        print_warning "Allure is not installed. Skipping Allure report generation."
        print_info "To install Allure, visit: https://docs.qameta.io/allure/"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -l, --language LANGUAGE    Set test language (en/zh, default: en)"
    echo "  -t, --type TYPE            Set test type (smoke/regression/all, default: all)"
    echo "  -o, --open-report          Open Allure report after test completion"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run all tests in English"
    echo "  $0 -l zh                             # Run all tests in Chinese"
    echo "  $0 -t smoke                          # Run smoke tests only"
    echo "  $0 -l zh -t regression -o            # Run regression tests in Chinese and open report"
}

# Main execution
main() {
    local language="en"
    local test_type="all"
    local open_report=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -l|--language)
                language="$2"
                shift 2
                ;;
            -t|--type)
                test_type="$2"
                shift 2
                ;;
            -o|--open-report)
                open_report=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Validate language
    if [[ "$language" != "en" && "$language" != "zh" ]]; then
        print_error "Invalid language: $language. Use 'en' or 'zh'"
        exit 1
    fi
    
    # Validate test type
    if [[ "$test_type" != "smoke" && "$test_type" != "regression" && "$test_type" != "all" ]]; then
        print_error "Invalid test type: $test_type. Use 'smoke', 'regression', or 'all'"
        exit 1
    fi
    
    print_info "Starting TikTok App Test Suite"
    print_info "Language: $language"
    print_info "Test Type: $test_type"
    
    # Check prerequisites
    check_prerequisites
    
    # Create report directories
    create_report_dirs
    
    # Run tests
    if run_tests "$language" "$test_type"; then
        print_success "All tests passed!"
        
        # Generate Allure report
        if [ "$open_report" = true ]; then
            generate_allure_report --open
        else
            generate_allure_report
        fi
        
        print_info "Test execution completed successfully"
        print_info "Reports available at:"
        print_info "  - HTML: $HTML_REPORT_DIR"
        print_info "  - JUnit: $JUNIT_REPORT_DIR"
        print_info "  - Allure: $REPORT_DIR/allure-report"
        
        exit 0
    else
        print_error "Some tests failed"
        
        # Generate Allure report even on failure
        generate_allure_report
        
        print_info "Reports available at:"
        print_info "  - HTML: $HTML_REPORT_DIR"
        print_info "  - JUnit: $JUNIT_REPORT_DIR"
        print_info "  - Allure: $REPORT_DIR/allure-report"
        
        exit 1
    fi
}

# Run main function with all arguments
main "$@"

