# iOS-Shortcuts

此仓库用于构建和发布 iPhone 快捷指令。

## 一键免打扰（2小时）

**手机直接下载已签名成品：**

[下载「一键免打扰」已签名 Shortcut](https://github.com/miketoryan/iOS-Shortcuts/raw/refs/heads/main/dist/one-tap-dnd-2h.shortcut)

2026-10-31 GitHub Actions 已实际成功：官方 Cherri v2.3.0 Linux 编译器通过 RoutineHub HubSign 签名，验证输出以 AEA1 开头并发布至 dist/one-tap-dnd-2h.shortcut（签名文件约 22 KB）。

**注意：这是已签名的 .shortcut 文件下载地址，不是苹果官方 iCloud 分享链接。** 只能在 iPhone 导入后，经快捷指令 App 的「拷贝 iCloud 链接」分享得到 iCloud 官方链接。

### 仅用 iPhone 导入

1. 在 iPhone Safari 打开上方已签名文件链接并下载。
2. 打开苹果「文件」App →「下载项」，点击 one-tap-dnd-2h.shortcut。
3. 由「快捷指令」App 打开，检查动作，再点击「添加快捷指令」。
4. 添加后可以重命名或添加到主屏幕。

功能：关闭蓝牙、Wi-Fi、蜂窝数据，开启勿扰模式，两小时后自动退出勿扰模式。两小时后无线开关**不会**自动重新打开。

### 自动构建

- one-tap-dnd-2h.cherri — Cherri 原生源码（真正用于发布）
- build_shortcut.py — Python 版结构参考生成器
- tests/test_build.py — Python 版配置测试
- .github/workflows/build-shortcut.yml — Actions：运行测试、调用 Cherri、签名并发布
- sign_hubsign.py — 研究用旧版 HubSign 客户端，目前旧接口返回网页而非签名文件，不在发布流水线使用

[查看成功的 GitHub Actions 构建](https://github.com/miketoryan/iOS-Shortcuts/actions/runs/41199505316)

本项目没有上传 Apple ID、密码或账号信息。第三方签名方会收到不包含账号或秘密信息的快捷指令动作定义。

**验证边界：** 构建和签名已成功，但尚未在用户的 iOS 26 真机上检验每项动作及两小时后自动关闭的实际效果。

**提醒：** 启用后手机会失去无线网络及蜂窝数据连接，导入前确保已完成下载，并了解恢复联网的方法。
