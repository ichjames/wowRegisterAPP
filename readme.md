# 魔兽世界CMaNGOS模拟器账户注册系统

这是一个基于 Python 和 Gradio 构建的魔兽世界账户注册系统，专为 CMaNGOS 模拟器设计。该系统实现了 SRP6 协议来安全地处理用户账户注册，并提供了直观的 Web 界面。

## 功能特性

- 🔐 安全的 SRP6 协议实现，用于账户认证
- 🎮 直观的 Web 界面，易于用户操作
- 🛡️ 支持 GM 权限等级设置
- 📧 邮箱信息收集
- 🐍 基于 Python 和 Gradio 构建

## 技术特点

- 使用 SRP6 协议生成安全的 verifier 和 salt
- 兼容 CMaNGOS 模拟器要求
- Verifier 采用小端序字节存储并进行适当填充
- 自动生成 32 字节的 salt 值

## 安装与运行

1. 克隆仓库:
   ```bash
   git clone https://github.com/ichjames/wowRegisterAPP.git
   cd wowRegisterAPP
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用:
   ```bash
   python app.py
   ```

4. 访问 `http://localhost:7860` 使用注册系统

## 配置说明

应用连接数据库需要配置以下环境变量：
- `DB_HOST`: 数据库主机地址
- `DB_USER`: 数据库用户名
- `DB_PASSWORD`: 数据库密码
- `DB_NAME`: 数据库名称

## 界面功能

- **账户信息**: 输入用户名和密码
- **联系信息**: 提供邮箱地址
- **GM权限等级**: 可设置用户权限级别（0-3级）
- **注册结果**: 显示注册成功或失败信息

## 安全提醒

注册时请注意：
- 密码至少需要6位字符
- 妥善保管账户信息
- 不要与他人分享密码

## 适用环境

本系统适用于:
- CMaNGOS 魔兽世界模拟器
- MySQL 数据库环境

## 开发者信息

此工具基于 SRP6 协议标准实现，符合CMaNGOS模拟器的要求，可轻松集成到现有服务器架构中。

## 许可证

[待定]
```

这个 README 包含了项目的概述、主要功能、安装指南、配置说明以及使用注意事项。您可以根据实际需求进一步调整内容，例如添加具体的许可证信息或者更详细的配置参数说明。
