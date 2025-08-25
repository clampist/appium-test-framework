# ATF - Appium Test Framework

一个基于Appium的Python测试框架，支持移动端自动化测试。

## 项目结构

```
atf/
├── core/                    # 核心逻辑层 (git子项目)
│   ├── __init__.py
│   ├── driver/             # Appium驱动管理
│   ├── elements/           # 元素定位和操作
│   ├── utils/              # 工具类
│   └── config/             # 配置管理
├── api/                    # 对外对内交互层接口层 (git子项目)
│   ├── __init__.py
│   ├── client/             # API客户端
│   ├── server/             # API服务端
│   └── models/             # 数据模型
├── tests/                  # 测试用例层
│   ├── com.honda.roadsync.duo/    # 业务路径1
│   ├── com.honda.ms.dm.sab/       # 业务路径2
│   └── common/                    # 通用测试
├── requirements.txt        # 依赖包
├── setup.py               # 安装配置
└── README.md              # 项目说明
```

## 安装

```bash
# 激活Python环境
pyenv activate atf

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

```bash
# 运行所有测试
pytest tests/

# 运行特定业务路径的测试
pytest tests/com.honda.roadsync.duo/

# 运行特定测试文件
pytest tests/com.honda.roadsync.duo/test_login.py
```

## 配置

在 `core/config/` 目录下配置测试环境参数：

- `appium_config.py`: Appium服务器配置
- `device_config.py`: 设备配置
- `app_config.py`: 应用配置

## 最佳实践

1. 使用Page Object Model模式
2. 元素定位使用ID或Accessibility ID
3. 测试用例要独立且可重复执行
4. 使用显式等待而不是隐式等待
5. 合理使用测试夹具(fixtures)
