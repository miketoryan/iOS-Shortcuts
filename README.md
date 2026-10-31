# iOS-Shortcuts

用于生成和发布 iPhone 快捷指令。当前指令：**一键免打扰（2小时）**。

点击运行时：

1. 关闭蓝牙（不是仅在控制中心断开配件）；
2. 关闭 Wi-Fi；
3. 关闭蜂窝数据；
4. 计算当前时间往后 2 小时；
5. 开启勿扰专注模式，并设置在计算出的时间结束。

**两小时后只关闭勿扰模式**；蓝牙、Wi-Fi 和蜂窝数据不会自动重新打开。

## 手机导入

仅当 [GitHub Actions 构建](../../actions/workflows/build-shortcut.yml) 显示成功，并且仓库中存在 dist/one-tap-dnd-2h.shortcut，才可点击：

[下载经苹果签名的快捷指令](https://github.com/miketoryan/iOS-Shortcuts/raw/refs/heads/main/dist/one-tap-dnd-2h.shortcut)

在 iPhone Safari 下载 .shortcut 文件，然后打开「文件」App，点击文件导入苹果「快捷指令」。

注意：这是 **GitHub 文件下载方式**，不是苹果官方 iCloud 一键分享链接；后者需要通过苹果的分享流程另行发布。

## 自动构建与验证

- 生成源码：build_shortcut.py
- 结构测试：python3 -m unittest discover -s tests -v
- Actions 使用 macOS 运行环境与苹果 shortcuts sign --mode anyone 命令。
- 不收集 Apple ID、密码或其他密钥。
- 如果运行环境无法完成苹果签名，构建将失败，并且**不会发布未签名文件**。
- 即便签名完成，也需要在 iPhone 上检查动作是否正常；结构测试不能代替设备测试。

**安全提醒：** 执行后手机将失去 Wi-Fi 和蜂窝互联网连接；请事先保存需要离线使用的资料。
