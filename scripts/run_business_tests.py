#!/usr/bin/env python3
"""
Business Test Runner Script
业务测试运行脚本 - 支持本地和CI/CD环境
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 确保当前工作目录也在Python路径中
current_dir = os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from core.utils.logger import Log
from core.utils.file_utils import FileUtils


class BusinessTestRunner:
    """业务测试运行器"""
    
    def __init__(self):
        self.project_root = project_root
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "reports"
        self.logs_dir = self.project_root / "logs"
        
        # 确保目录存在
        FileUtils.ensure_dir(str(self.reports_dir))
        FileUtils.ensure_dir(str(self.logs_dir))
    
    def get_business_paths(self) -> List[str]:
        """获取所有业务路径"""
        business_paths = []
        if self.tests_dir.exists():
            for item in self.tests_dir.iterdir():
                if item.is_dir() and not item.name.startswith('_'):
                    business_paths.append(item.name)
        return sorted(business_paths)
    
    def validate_business_path(self, business_path: str) -> bool:
        """验证业务路径是否存在"""
        path = self.tests_dir / business_path
        return path.exists() and path.is_dir()
    
    def get_test_files(self, business_path: str) -> List[str]:
        """获取业务路径下的测试文件"""
        test_files = []
        path = self.tests_dir / business_path
        
        if path.exists():
            for file in path.glob("test_*.py"):
                test_files.append(str(file.relative_to(self.project_root)))
        
        return test_files
    
    def run_pytest_command(self, 
                          test_path: str,
                          markers: Optional[List[str]] = None,
                          parallel: Optional[int] = None,
                          html_report: bool = True,
                          junit_report: bool = True,
                          allure_report: bool = False,
                          verbose: bool = True,
                          capture: str = "no") -> bool:
        
        # 注意：pyenv环境激活需要在shell脚本中处理，这里只是记录
        Log.info("Using Python environment (pyenv activation should be handled by shell script)")
        """
        运行pytest命令
        
        Args:
            test_path: 测试路径
            markers: 测试标记
            parallel: 并行数量
            html_report: 是否生成HTML报告
            junit_report: 是否生成JUnit报告
            allure_report: 是否生成Allure报告
            verbose: 是否详细输出
            capture: 输出捕获模式
            
        Returns:
            bool: 是否成功
        """
        cmd_parts = ["python", "-m", "pytest", test_path]
        
        # 添加标记
        if markers:
            for marker in markers:
                cmd_parts.extend(["-m", marker])
        
        # 并行执行
        if parallel and parallel > 1:
            cmd_parts.extend(["-n", str(parallel)])
        
        # 报告配置
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        business_name = Path(test_path).parts[-1] if test_path != "tests/" else "all"
        
        if html_report:
            html_file = f"{self.reports_dir}/html/{business_name}_{timestamp}.html"
            FileUtils.ensure_dir(str(Path(html_file).parent))
            cmd_parts.extend([
                "--html", html_file,
                "--self-contained-html"
            ])
        
        if junit_report:
            junit_file = f"{self.reports_dir}/junit/{business_name}_{timestamp}.xml"
            FileUtils.ensure_dir(str(Path(junit_file).parent))
            cmd_parts.extend(["--junitxml", junit_file])
        
        if allure_report:
            allure_results = f"{self.reports_dir}/allure-results/{business_name}_{timestamp}"
            FileUtils.ensure_dir(allure_results)
            cmd_parts.extend(["--alluredir", allure_results])
        
        # 输出配置
        if verbose:
            cmd_parts.append("-v")
        
        cmd_parts.extend(["--tb=short", f"--capture={capture}"])
        
        # 执行命令
        command = " ".join(cmd_parts)
        Log.info(f"Executing command: {command}")
        
        try:
            result = subprocess.run(
                cmd_parts,
                cwd=self.project_root,
                capture_output=False,
                text=True
            )
            
            success = result.returncode == 0
            if success:
                Log.success(f"Test execution completed successfully for {test_path}")
            else:
                Log.error(f"Test execution failed for {test_path}")
            
            return success
            
        except Exception as e:
            Log.error(f"Failed to execute test command: {str(e)}")
            return False
    
    def run_business_tests(self,
                          business_path: str,
                          markers: Optional[List[str]] = None,
                          parallel: Optional[int] = None,
                          html_report: bool = True,
                          junit_report: bool = True,
                          allure_report: bool = False) -> bool:
        """
        运行指定业务的测试
        
        Args:
            business_path: 业务路径
            markers: 测试标记
            parallel: 并行数量
            html_report: 是否生成HTML报告
            junit_report: 是否生成JUnit报告
            allure_report: 是否生成Allure报告
            
        Returns:
            bool: 是否成功
        """
        Log.info(f"Starting tests for business: {business_path}")
        
        # 验证业务路径
        if not self.validate_business_path(business_path):
            Log.error(f"Invalid business path: {business_path}")
            return False
        
        # 获取测试文件
        test_files = self.get_test_files(business_path)
        if not test_files:
            Log.warning(f"No test files found in {business_path}")
            return False
        
        Log.info(f"Found {len(test_files)} test files: {test_files}")
        
        # 运行测试
        test_path = f"tests/{business_path}/"
        return self.run_pytest_command(
            test_path=test_path,
            markers=markers,
            parallel=parallel,
            html_report=html_report,
            junit_report=junit_report,
            allure_report=allure_report
        )
    
    def run_all_business_tests(self,
                              markers: Optional[List[str]] = None,
                              parallel: Optional[int] = None,
                              html_report: bool = True,
                              junit_report: bool = True,
                              allure_report: bool = False) -> Dict[str, bool]:
        """
        运行所有业务的测试
        
        Args:
            markers: 测试标记
            parallel: 并行数量
            html_report: 是否生成HTML报告
            junit_report: 是否生成JUnit报告
            allure_report: 是否生成Allure报告
            
        Returns:
            Dict[str, bool]: 各业务测试结果
        """
        Log.info("Starting all business tests")
        
        business_paths = self.get_business_paths()
        if not business_paths:
            Log.warning("No business paths found")
            return {}
        
        Log.info(f"Found business paths: {business_paths}")
        
        results = {}
        for business_path in business_paths:
            Log.info(f"Running tests for {business_path}")
            success = self.run_business_tests(
                business_path=business_path,
                markers=markers,
                parallel=parallel,
                html_report=html_report,
                junit_report=junit_report,
                allure_report=allure_report
            )
            results[business_path] = success
        
        return results
    
    def generate_summary_report(self, results: Dict[str, bool]) -> None:
        """生成测试结果摘要报告"""
        Log.info("Generating test summary report")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary_file = f"{self.reports_dir}/test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Test Execution Summary\n")
            f.write(f"=====================\n")
            f.write(f"Execution Time: {timestamp}\n")
            f.write(f"Total Businesses: {len(results)}\n")
            f.write(f"Successful: {sum(results.values())}\n")
            f.write(f"Failed: {len(results) - sum(results.values())}\n\n")
            
            f.write("Detailed Results:\n")
            f.write("----------------\n")
            for business, success in results.items():
                status = "✅ PASS" if success else "❌ FAIL"
                f.write(f"{business}: {status}\n")
        
        Log.info(f"Summary report saved: {summary_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Business Test Runner")
    
    # 基本参数
    parser.add_argument(
        "--business", "-b",
        help="Business path to test (e.g., jp.co.matsukiyococokara.app)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all business tests"
    )
    
    # 测试标记
    parser.add_argument(
        "--markers", "-m",
        nargs="+",
        help="Test markers (e.g., smoke daily regression)"
    )
    
    # 执行配置
    parser.add_argument(
        "--parallel", "-n",
        type=int,
        help="Number of parallel processes"
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Disable HTML report generation"
    )
    parser.add_argument(
        "--no-junit",
        action="store_true",
        help="Disable JUnit report generation"
    )
    parser.add_argument(
        "--allure",
        action="store_true",
        help="Enable Allure report generation"
    )
    
    # 环境配置
    parser.add_argument(
        "--env",
        choices=["local", "ci", "staging", "production"],
        default="local",
        help="Environment (default: local)"
    )
    
    args = parser.parse_args()
    
    # 初始化运行器
    runner = BusinessTestRunner()
    
    # 根据环境调整配置
    if args.env == "ci":
        # CI环境配置
        if not args.parallel:
            args.parallel = 4  # CI环境默认4个并行进程
        if not args.markers:
            args.markers = ["smoke"]  # CI环境默认运行冒烟测试
    
    # 运行测试
    if args.all:
        Log.info("Running all business tests")
        results = runner.run_all_business_tests(
            markers=args.markers,
            parallel=args.parallel,
            html_report=not args.no_html,
            junit_report=not args.no_junit,
            allure_report=args.allure
        )
        runner.generate_summary_report(results)
        
        # 检查整体结果
        all_passed = all(results.values())
        if all_passed:
            Log.success("All business tests passed!")
            sys.exit(0)
        else:
            Log.error("Some business tests failed!")
            sys.exit(1)
    
    elif args.business:
        Log.info(f"Running tests for business: {args.business}")
        success = runner.run_business_tests(
            business_path=args.business,
            markers=args.markers,
            parallel=args.parallel,
            html_report=not args.no_html,
            junit_report=not args.no_junit,
            allure_report=args.allure
        )
        
        if success:
            Log.success(f"Business tests for {args.business} passed!")
            sys.exit(0)
        else:
            Log.error(f"Business tests for {args.business} failed!")
            sys.exit(1)
    
    else:
        # 显示可用的业务路径
        business_paths = runner.get_business_paths()
        if business_paths:
            Log.info("Available business paths:")
            for path in business_paths:
                Log.info(f"  - {path}")
        else:
            Log.warning("No business paths found")
        
        parser.print_help()


if __name__ == "__main__":
    main()
