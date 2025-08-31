# Monoxer App Test Suite

Monoxer应用测试套件，基于ATF框架实现，支持多语言测试。

## 📁 目录结构

```
tests/com.monoxer/
├── conftest.py              # Pytest配置和fixtures
├── test_monoxer_features.py # 主要测试文件
├── datas/
│   └── test_data.py         # 多语言测试数据定义
├── pages/
│   ├── __init__.py
│   ├── main_page.py         # 主页面对象
│   ├── search_page.py       # 搜索页面对象
│   └── library_page.py      # Library页面对象
├── screenshots/             # 截图目录
│   ├── base/               # 基准截图
│   └── cur/                # 当前测试截图
└── README.md               # 本文档
```

## 🌍 多语言支持

### 支持的语言
- **英文 (en)**: 默认语言，使用 `emulator-5554` (Android 13)
- **日文 (ja)**: 使用 `emulator-5556` (Android 14)

### 语言相关配置
- **Appium配置**: 不同语言对应不同的模拟器和平台版本
- **定位器**: 语言相关的UI文本使用对应语言的定位器
- **测试数据**: 搜索关键词等测试数据支持多语言

### 架构设计
- **基类**: `BaseMonoxerTestData` 包含公共元素和配置
- **语言类**: 继承基类，提供语言特定的定位器和配置
- **页面对象**: 支持传入语言特定的测试数据类

## 🚀 功能特性

### ✅ 已实现功能

1. **邀请码功能测试** (`test_invitation_code_feature`)
   - 打开侧边栏
   - 点击"Enter invitation code" / "招待コードを入力"
   - 验证页面跳转
   - 返回主页面

2. **同步功能测试** (`test_sync_feature`)
   - 打开侧边栏
   - 点击"Sync" / "同期" 按钮
   - 等待同步完成
   - 检查"Synced" toast消息
   - 返回主页面

3. **搜索功能测试** (`test_search_feature`)
   - 点击搜索标签
   - 输入搜索关键词"日本の祝日"
   - 点击第一个搜索结果
   - 点击contents按钮查看详情
   - 多次返回操作
   - 返回主页面

4. **Library功能测试** (`test_library_feature`)
   - 点击Library标签
   - 点击"My Books" / "マイブック" 标签
   - 自适应点击auto_test标题或open_deck按钮
   - 打开deck并返回
   - 测试STUDY模式
   - 回答两个问题（支持选择题和填空题）
   - 返回主页面

### 📸 截图管理

- **自动截图**: 每个测试步骤自动保存截图
- **目录结构**: `tests/com.monoxer/screenshots/base/` 和 `tests/com.monoxer/screenshots/cur/`
- **截图对比**: 自动对比base和cur目录的截图
- **基准管理**: 测试成功后自动设置基准截图
- **会话级截图**: 一次测试运行中保留所有功能测试的截图
- **公共初始化**: 提取公共的"initial"截图步骤

## 🛠️ 运行测试

### 运行单个测试

```bash
# 英文版测试
python -m pytest test_monoxer_features.py::TestMonoxerFeatures::test_invitation_code_feature -v --language=en

# 日文版测试
python -m pytest test_monoxer_features.py::TestMonoxerFeatures::test_invitation_code_feature -v --language=ja

```

### 运行所有测试

```bash
# 英文版所有测试
python -m pytest test_monoxer_features.py -v --language=en

# 日文版所有测试
python -m pytest test_monoxer_features.py -v --language=ja

```

### 使用marker运行

```bash
# 英文版测试
python -m pytest -m monoxer -v --language=en

# 日文版测试
python -m pytest -m monoxer -v --language=ja

```

## 📸 截图管理工具

### 使用独立脚本

```bash
# 查看可用命令
python scripts/manage_screenshots.py -a com.monoxer --list

# 对比截图
python scripts/manage_screenshots.py -a com.monoxer --compare

# 设置基准截图
python scripts/manage_screenshots.py -a com.monoxer --set-base

# 清空基准截图
python scripts/manage_screenshots.py -a com.monoxer --clear-base

# 清空当前截图
python scripts/manage_screenshots.py -a com.monoxer --clear-cur
```

## 🔧 配置说明

### 环境要求
- Python 3.12+
- Appium Server
- Android模拟器
- ATF虚拟环境 (`pyenv activate atf`)

### 模拟器配置
- **英文**: `emulator-5554` (Android 13)
- **日文**: `emulator-5556` (Android 14)

### 语言配置映射
```python
LANGUAGE_CONFIG_MAP = {
    "en": EnglishMonoxerTestData,
    "ja": JapaneseMonoxerTestData,    
}
```

## 🏗️ 架构设计

### 测试数据组织
```python
# 基类 - 公共元素和配置
class BaseMonoxerTestData:
    class CommonLocators:  # 不依赖语言的定位器
    class CommonTestData:  # 不依赖语言的测试数据

# 语言特定类 - 继承基类
class EnglishMonoxerTestData(BaseMonoxerTestData):
    class Locators(BaseMonoxerTestData.CommonLocators):  # 英文定位器
    class TestData(BaseMonoxerTestData.CommonTestData):  # 英文测试数据
    class AppiumConfig:  # 英文Appium配置
```

### 页面对象设计
```python
class MainPage(PageObject):
    def __init__(self, driver, test_data=None):
        self.test_data = test_data or MonoxerTestData  # 支持多语言
        # 使用 self.test_data.Locators.XXX 获取语言特定定位器
```

## 🎯 最佳实践

1. **语言隔离**: 不同语言的测试数据完全隔离，避免冲突
2. **公共元素复用**: 不依赖语言的元素在基类中定义
3. **配置统一**: 通过命令行参数统一管理语言配置
4. **错误处理**: 针对不同语言的错误信息进行适当处理
5. **截图管理**: 多语言测试的截图分别管理

## 🐛 调试技巧

1. **语言切换**: 使用 `--language` 参数切换测试语言
2. **截图分析**: 查看截图确认UI元素是否正确识别
3. **日志分析**: 查看详细日志了解测试执行过程
4. **元素定位**: 使用Appium Inspector验证元素定位器

## ⚠️ 注意事项

1. **模拟器环境**: 确保对应语言的模拟器已启动并正确配置
2. **应用语言**: 确保应用已安装对应语言版本
3. **定位器更新**: 当应用UI变化时，需要更新对应语言的定位器
4. **测试数据**: 不同语言的测试数据可能需要调整
5. **截图对比**: 多语言测试的截图对比需要考虑UI差异

## 📝 扩展指南

### 添加新语言支持
1. 创建新的语言测试数据类
2. 继承 `BaseMonoxerTestData`
3. 实现语言特定的定位器和配置
4. 更新 `LANGUAGE_CONFIG_MAP`
5. 测试新语言功能

### 添加新功能测试
1. 在基类中添加公共定位器
2. 在语言类中添加语言特定定位器
3. 更新页面对象方法
4. 添加测试用例
5. 验证多语言支持
