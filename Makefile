# ATF Makefile - 简化测试运行
# 使用方法: make <target>

.PHONY: help install setup test test-smoke test-daily test-regression test-cocokara test-all clean

# 默认目标
help:
	@echo "ATF Test Runner - 可用命令:"
	@echo ""
	@echo "环境设置:"
	@echo "  install     - 安装依赖"
	@echo "  setup       - 设置环境"
	@echo ""
	@echo "测试运行:"
	@echo "  test        - 运行所有测试"
	@echo "  test-smoke  - 运行冒烟测试"
	@echo "  test-daily  - 运行每日测试"
	@echo "  test-regression - 运行回归测试"
	@echo "  test-cocokara - 运行Cocokara测试"
	@echo "  test-all    - 运行所有业务测试"
	@echo ""
	@echo "工具:"
	@echo "  clean       - 清理报告和日志"
	@echo "  help        - 显示帮助信息"

# 安装依赖
install:
	@echo "Installing dependencies..."
	@eval "$$(pyenv init -)" && pyenv activate atf && pip install -r requirements.txt

# 设置环境
setup:
	@echo "Setting up environment..."
	@if command -v pyenv > /dev/null; then \
		echo "Activating pyenv environment 'atf'..."; \
		eval "$$(pyenv init -)" && pyenv activate atf; \
	else \
		echo "pyenv not found, using system Python"; \
	fi
	@echo "Environment setup completed"

# 运行所有测试
test: setup
	@echo "Running all tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all

# 运行冒烟测试
test-smoke: setup
	@echo "Running smoke tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --markers smoke

# 运行每日测试
test-daily: setup
	@echo "Running daily tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --markers daily

# 运行回归测试
test-regression: setup
	@echo "Running regression tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --markers regression --allure

# 运行Cocokara测试
test-cocokara: setup
	@echo "Running Cocokara tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --business jp.co.matsukiyococokara.app --markers smoke daily

# 运行所有业务测试（并行）
test-all: setup
	@echo "Running all business tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --parallel 4

# 使用业务特定脚本运行Cocokara测试
test-cocokara-script: setup
	@echo "Running Cocokara tests using business script..."
	@chmod +x scripts/run_cocokara_tests.sh
	./scripts/run_cocokara_tests.sh -m smoke daily

# 运行特定业务测试
test-business:
	@echo "Usage: make test-business BUSINESS=<business_path>"
	@echo "Example: make test-business BUSINESS=jp.co.matsukiyococokara.app"
	@if [ -z "$(BUSINESS)" ]; then \
		echo "Error: BUSINESS parameter is required"; \
		exit 1; \
	fi
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --business $(BUSINESS)

# 运行特定标记的测试
test-markers:
	@echo "Usage: make test-markers MARKERS=<marker1> <marker2>"
	@echo "Example: make test-markers MARKERS=smoke daily"
	@if [ -z "$(MARKERS)" ]; then \
		echo "Error: MARKERS parameter is required"; \
		exit 1; \
	fi
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --markers $(MARKERS)

# 并行运行测试
test-parallel:
	@echo "Usage: make test-parallel PARALLEL=<number>"
	@echo "Example: make test-parallel PARALLEL=4"
	@if [ -z "$(PARALLEL)" ]; then \
		echo "Error: PARALLEL parameter is required"; \
		exit 1; \
	fi
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --parallel $(PARALLEL)

# 生成Allure报告
allure-report: setup
	@echo "Generating Allure report..."
	@if command -v allure > /dev/null; then \
		allure generate reports/allure-results --clean -o reports/allure-report; \
		echo "Allure report generated: reports/allure-report/index.html"; \
	else \
		echo "Allure command not found. Please install allure-commandline"; \
		exit 1; \
	fi

# 打开Allure报告
allure-serve: setup
	@echo "Starting Allure server..."
	@if command -v allure > /dev/null; then \
		allure serve reports/allure-results; \
	else \
		echo "Allure command not found. Please install allure-commandline"; \
		exit 1; \
	fi

# 清理报告和日志
clean:
	@echo "Cleaning reports and logs..."
	rm -rf reports/
	rm -rf logs/
	rm -rf screenshots/
	rm -rf test-results/
	rm -rf allure-results/
	rm -rf allure-report/
	@echo "Cleanup completed"

# 检查环境
check-env:
	@echo "Checking environment..."
	@echo "Python version:"
	@eval "$$(pyenv init -)" && pyenv activate atf && python --version
	@echo "Pytest version:"
	@eval "$$(pyenv init -)" && pyenv activate atf && pytest --version
	@echo "Available business paths:"
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py

# 启动Appium服务器
start-appium:
	@echo "Starting Appium server..."
	@if command -v appium > /dev/null; then \
		appium --base-path /wd/hub & \
		echo "Appium server started"; \
	else \
		echo "Appium not found. Please install appium"; \
		exit 1; \
	fi

# 停止Appium服务器
stop-appium:
	@echo "Stopping Appium server..."
	@pkill -f appium || echo "No Appium process found"

# 检查设备连接
check-devices:
	@echo "Checking connected devices..."
	@if command -v adb > /dev/null; then \
		adb devices; \
	else \
		echo "ADB not found. Please install Android SDK"; \
	fi

# 运行完整测试流程
full-test: setup check-env start-appium
	@echo "Running full test suite..."
	@make test-smoke
	@make test-daily
	@make test-regression
	@make stop-appium
	@echo "Full test suite completed"

# 开发模式运行（快速反馈）
dev-test: setup
	@echo "Running development tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --markers smoke --parallel 2 --no-html

# 生产模式运行（完整测试）
prod-test: setup
	@echo "Running production tests..."
	@eval "$$(pyenv init -)" && pyenv activate atf && python scripts/run_business_tests.py --all --markers regression --parallel 4 --allure

# 显示测试报告
show-reports:
	@echo "Available reports:"
	@if [ -d "reports" ]; then \
		find reports -name "*.html" -o -name "*.xml" | head -10; \
	else \
		echo "No reports found. Run tests first."; \
	fi

# 显示日志
show-logs:
	@echo "Recent logs:"
	@if [ -d "logs" ]; then \
		ls -la logs/ | head -10; \
	else \
		echo "No logs found."; \
	fi
