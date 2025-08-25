#!/bin/bash
# Cocokara Business Test Runner
# Cocokara业务测试运行脚本

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    echo "Cocokara Business Test Runner"
    echo "============================"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help             显示帮助信息"
    echo "  -m, --markers MARKERS  测试标记 (smoke, daily, regression)"
    echo "  -n, --parallel NUM     并行进程数"
    echo "  --no-html              禁用HTML报告"
    echo "  --no-junit             禁用JUnit报告"
    echo "  --allure               启用Allure报告"
    echo "  --env ENV              环境 (local, ci, staging, production)"
    echo ""
    echo "Examples:"
    echo "  $0 -m smoke                    # 运行冒烟测试"
    echo "  $0 -m daily -n 2               # 运行每日测试，2个并行进程"
    echo "  $0 --env ci -m smoke           # CI环境运行冒烟测试"
    echo "  $0 --allure                    # 启用Allure报告"
    echo ""
}

# 默认参数
BUSINESS_PATH="jp.co.matsukiyococokara.app"
MARKERS=""
PARALLEL=""
NO_HTML=false
NO_JUNIT=false
ALLURE=false
ENV="local"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -m|--markers)
            MARKERS="$2"
            shift 2
            ;;
        -n|--parallel)
            PARALLEL="$2"
            shift 2
            ;;
        --no-html)
            NO_HTML=true
            shift
            ;;
        --no-junit)
            NO_JUNIT=true
            shift
            ;;
        --allure)
            ALLURE=true
            shift
            ;;
        --env)
            ENV="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查Python环境
check_python_env() {
    log_info "Checking Python environment..."
    
    # 激活pyenv环境
    if command -v pyenv &> /dev/null; then
        log_info "pyenv detected, activating atf environment..."
        pyenv activate atf
    else
        log_warning "pyenv not found, using system Python"
    fi
    
    if ! command -v python &> /dev/null; then
        log_error "Python is not installed or not in PATH"
        exit 1
    fi
    
    # 检查依赖
    if ! python -c "import pytest" &> /dev/null; then
        log_error "pytest is not installed"
        exit 1
    fi
}

# 检查Appium环境
check_appium_env() {
    log_info "Checking Appium environment..."
    
    # 检查Appium服务器
    if ! curl -s http://127.0.0.1:4723/status &> /dev/null; then
        log_warning "Appium server is not running on http://127.0.0.1:4723"
        log_info "Please start Appium server first:"
        log_info "  appium --base-path /wd/hub"
    fi
    
    # 检查Android设备
    if ! adb devices | grep -q "device$"; then
        log_warning "No Android device connected"
        log_info "Please connect a device or start an emulator"
    fi
}

# 构建命令参数
build_command_args() {
    local args=""
    
    if [[ -n "$MARKERS" ]]; then
        args="$args --markers $MARKERS"
    fi
    
    if [[ -n "$PARALLEL" ]]; then
        args="$args --parallel $PARALLEL"
    fi
    
    if [[ "$NO_HTML" == true ]]; then
        args="$args --no-html"
    fi
    
    if [[ "$NO_JUNIT" == true ]]; then
        args="$args --no-junit"
    fi
    
    if [[ "$ALLURE" == true ]]; then
        args="$args --allure"
    fi
    
    args="$args --env $ENV"
    
    echo "$args"
}

# 主函数
main() {
    log_info "Starting Cocokara business test execution..."
    
    # 检查环境
    check_python_env
    check_appium_env
    
    # 构建命令
    local cmd_args=$(build_command_args)
    local full_command="python scripts/run_business_tests.py --business $BUSINESS_PATH $cmd_args"
    
    log_info "Executing: $full_command"
    
    # 执行测试
    if eval "$full_command"; then
        log_success "Cocokara tests completed successfully!"
        
        # 显示报告位置
        if [[ "$NO_HTML" != true ]]; then
            log_info "HTML report available in: reports/html/"
        fi
        if [[ "$NO_JUNIT" != true ]]; then
            log_info "JUnit report available in: reports/junit/"
        fi
        if [[ "$ALLURE" == true ]]; then
            log_info "Allure results available in: reports/allure-results/"
        fi
        
        exit 0
    else
        log_error "Cocokara tests failed!"
        exit 1
    fi
}

# 执行主函数
main "$@"
