# 测试运行最佳实践

## 概述

本文档描述了ATF框架中测试运行的最佳实践，包括本地运行和CI/CD流水线运行的各种方式。

## 目录结构

```
scripts/
├── run_business_tests.py          # 通用业务测试运行器
├── run_cocokara_tests.sh          # Cocokara业务特定脚本
└── ...

.github/workflows/
└── ci-tests.yml                   # GitHub Actions CI配置

Jenkinsfile                        # Jenkins Pipeline配置
Makefile                          # 本地运行简化脚本
```

## 本地运行最佳实践

### 1. 使用Makefile（推荐）

Makefile提供了简化的命令接口，是最推荐的本地运行方式：

```bash
# 查看所有可用命令
make help

# 环境设置
make install    # 安装依赖
make setup      # 设置环境

# 基本测试运行
make test-smoke     # 冒烟测试
make test-daily     # 每日测试
make test-regression # 回归测试
make test-cocokara  # Cocokara测试

# 高级用法
make test-business BUSINESS=jp.co.matsukiyococokara.app
make test-markers MARKERS=smoke daily
make test-parallel PARALLEL=4

# 工具命令
make clean          # 清理报告和日志
make check-env      # 检查环境
make show-reports   # 显示报告
```

### 2. 使用通用测试运行器

```bash
# 运行所有业务测试
python scripts/run_business_tests.py --all

# 运行特定业务测试
python scripts/run_business_tests.py --business jp.co.matsukiyococokara.app

# 运行特定标记的测试
python scripts/run_business_tests.py --all --markers smoke daily

# 并行运行
python scripts/run_business_tests.py --all --parallel 4

# 生成Allure报告
python scripts/run_business_tests.py --all --allure
```

### 3. 使用业务特定脚本

```bash
# Cocokara测试
./scripts/run_cocokara_tests.sh -m smoke daily
./scripts/run_cocokara_tests.sh --env ci -m smoke
./scripts/run_cocokara_tests.sh --allure
```

### 4. 环境检查

在运行测试前，建议进行环境检查：

```bash
# 检查Python环境
make check-env

# 检查设备连接
make check-devices

# 启动Appium服务器
make start-appium

# 停止Appium服务器
make stop-appium
```

## CI/CD流水线最佳实践

### 1. GitHub Actions

GitHub Actions配置支持多种测试场景：

#### 触发条件
- **Push/Pull Request**: 自动触发冒烟测试
- **Main分支**: 触发完整测试套件
- **定时任务**: 每天凌晨2点运行每日测试

#### 测试类型
- **Smoke Tests**: 快速验证（30分钟超时）
- **Daily Tests**: 每日功能验证（60分钟超时）
- **Regression Tests**: 完整回归测试（120分钟超时）
- **Business Specific**: 特定业务测试

#### 报告生成
- HTML报告
- JUnit XML报告
- Allure报告（回归测试）

### 2. Jenkins Pipeline

Jenkins Pipeline提供更灵活的CI/CD配置：

#### 阶段划分
1. **Checkout**: 代码检出
2. **Setup Environment**: 环境设置
3. **Start Appium Server**: 启动Appium服务器
4. **Smoke Tests**: 冒烟测试
5. **Daily Tests**: 每日测试
6. **Regression Tests**: 回归测试
7. **Business Specific Tests**: 业务特定测试（并行）
8. **Test Summary**: 测试总结

#### 条件执行
- 根据分支和事件类型决定执行哪些测试
- 支持并行执行提高效率
- 失败时自动重试机制

#### 报告发布
- HTML报告发布
- JUnit测试结果集成
- Allure报告生成
- 测试摘要生成

## 测试标记策略

### 标记定义

```python
@pytest.mark.smoke        # 冒烟测试 - 快速验证核心功能
@pytest.mark.daily        # 每日测试 - 日常功能验证
@pytest.mark.regression   # 回归测试 - 完整功能验证
@pytest.mark.integration  # 集成测试 - 系统集成验证
@pytest.mark.unit         # 单元测试 - 组件级别测试
@pytest.mark.slow         # 慢速测试 - 长时间运行的测试
@pytest.mark.android      # Android平台测试
@pytest.mark.ios          # iOS平台测试
```

### 标记使用

```bash
# 运行冒烟测试
python scripts/run_business_tests.py --all --markers smoke

# 运行多个标记的测试
python scripts/run_business_tests.py --all --markers smoke daily

# 排除特定标记
pytest tests/ -m "not slow"

# 组合标记
pytest tests/ -m "smoke and not slow"
```

## 并行执行策略

### 本地并行

```bash
# 2个并行进程（适合开发环境）
python scripts/run_business_tests.py --all --parallel 2

# 4个并行进程（适合CI环境）
python scripts/run_business_tests.py --all --parallel 4

# 8个并行进程（适合高性能环境）
python scripts/run_business_tests.py --all --parallel 8
```

### CI/CD并行

- **GitHub Actions**: 使用矩阵策略并行运行不同业务
- **Jenkins**: 使用parallel stage并行执行
- **资源优化**: 根据可用资源调整并行数量

## 报告生成策略

### 报告类型

1. **HTML报告**: 适合本地查看和分享
2. **JUnit XML**: 适合CI/CD集成
3. **Allure报告**: 适合详细分析和趋势跟踪
4. **自定义报告**: 业务特定的报告格式

### 报告配置

```bash
# 生成HTML报告
python scripts/run_business_tests.py --all

# 生成JUnit报告
python scripts/run_business_tests.py --all

# 生成Allure报告
python scripts/run_business_tests.py --all --allure

# 禁用特定报告
python scripts/run_business_tests.py --all --no-html --no-junit
```

## 环境配置策略

### 环境类型

1. **local**: 本地开发环境
2. **ci**: CI/CD环境
3. **staging**: 预发布环境
4. **production**: 生产环境

### 环境特定配置

```python
# CI环境自动配置
if args.env == "ci":
    if not args.parallel:
        args.parallel = 4  # CI环境默认4个并行进程
    if not args.markers:
        args.markers = ["smoke"]  # CI环境默认运行冒烟测试
```

## 错误处理和恢复

### 错误处理策略

1. **环境检查**: 运行前检查必要环境
2. **优雅降级**: 部分失败时继续执行其他测试
3. **重试机制**: 网络或临时错误时自动重试
4. **资源清理**: 测试完成后清理资源

### 恢复机制

```bash
# 清理环境
make clean

# 重启Appium服务器
make stop-appium
make start-appium

# 重新运行失败的测试
pytest tests/ --lf  # 运行上次失败的测试
```

## 性能优化

### 执行时间优化

1. **并行执行**: 使用多进程并行运行测试
2. **测试分组**: 按业务或功能分组执行
3. **资源复用**: 复用驱动和会话
4. **缓存机制**: 缓存测试数据和配置

### 资源使用优化

1. **内存管理**: 及时释放不需要的资源
2. **连接池**: 复用网络连接
3. **设备管理**: 合理分配设备资源
4. **日志级别**: 根据环境调整日志级别

## 监控和告警

### 监控指标

1. **执行时间**: 测试执行总时间
2. **成功率**: 测试通过率
3. **失败率**: 测试失败率
4. **资源使用**: CPU、内存、网络使用情况

### 告警机制

1. **失败告警**: 测试失败时发送通知
2. **性能告警**: 执行时间超过阈值时告警
3. **资源告警**: 资源使用异常时告警
4. **趋势告警**: 失败率上升趋势告警

## 最佳实践总结

### 本地开发

1. **使用Makefile**: 简化命令，提高效率
2. **环境检查**: 运行前检查环境状态
3. **快速反馈**: 使用冒烟测试快速验证
4. **资源管理**: 及时清理不需要的资源

### CI/CD集成

1. **分层测试**: 按重要性分层执行测试
2. **并行执行**: 充分利用并行能力
3. **报告集成**: 生成多种格式的报告
4. **失败处理**: 优雅处理失败情况

### 维护和扩展

1. **模块化设计**: 保持脚本的模块化
2. **配置管理**: 集中管理配置信息
3. **文档更新**: 及时更新相关文档
4. **版本控制**: 使用版本控制管理脚本

## 常见问题解决

### 环境问题

```bash
# Python环境问题
pyenv activate atf
pip install -r requirements.txt

# Appium服务器问题
pkill -f appium
appium --base-path /wd/hub &

# 设备连接问题
adb devices
adb kill-server && adb start-server
```

### 测试问题

```bash
# 测试失败
pytest tests/ --lf --tb=short

# 超时问题
pytest tests/ --timeout=300

# 内存问题
pytest tests/ --maxfail=5
```

### 报告问题

```bash
# 报告生成失败
make clean
make test-smoke

# Allure报告问题
allure generate reports/allure-results --clean
allure serve reports/allure-results
```

通过遵循这些最佳实践，可以确保测试运行的稳定性、效率和可维护性。
