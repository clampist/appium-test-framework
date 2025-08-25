#!/usr/bin/env python3
"""
Test Runner Script
测试运行脚本
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime
from core.utils.logger import Log
from core.utils.file_utils import FileUtils


def run_command(command, description):
    """运行命令"""
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
    """设置测试环境"""
    Log.info("Setting up test environment...")
    
    # 创建必要的目录
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
    """运行测试"""
    Log.info("Starting test execution...")
    
    # 构建pytest命令
    cmd_parts = ["python", "-m", "pytest"]
    
    # 添加测试路径
    if test_path:
        cmd_parts.append(test_path)
    else:
        cmd_parts.append("tests/")
    
    # 添加标记
    if markers:
        for marker in markers:
            cmd_parts.extend(["-m", marker])
    
    # 添加并行执行
    if parallel:
        cmd_parts.extend(["-n", str(parallel)])
    
    # 添加HTML报告
    if html_report:
        cmd_parts.extend([
            "--html=reports/report.html",
            "--self-contained-html"
        ])
    
    # 添加JUnit XML报告
    cmd_parts.extend(["--junitxml=reports/junit.xml"])
    
    # 添加详细输出
    cmd_parts.extend(["-v", "--tb=short"])
    
    command = " ".join(cmd_parts)
    
    # 运行测试
    result = run_command(command, "Test execution")
    
    if result:
        Log.info("Test execution completed successfully")
        return True
    else:
        Log.error("Test execution failed")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="ATF Test Runner")
    
    parser.add_argument(
        "--test-path",
        help="测试路径 (例如: tests/com.honda.roadsync.duo/)"
    )
    
    parser.add_argument(
        "--markers",
        nargs="+",
        help="测试标记 (例如: smoke regression)"
    )
    
    parser.add_argument(
        "--parallel",
        type=int,
        help="并行执行数量"
    )
    
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="不生成HTML报告"
    )
    
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="仅设置环境"
    )
    
    args = parser.parse_args()
    
    # 初始化日志
    Log.info("ATF Test Runner started")
    Log.info(f"Python version: {sys.version}")
    Log.info(f"Working directory: {os.getcwd()}")
    
    # 设置环境
    setup_environment()
    
    if args.setup_only:
        Log.info("Environment setup completed")
        return
    
    # 运行测试
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
