# iOS-Shortcuts

用于生成和发布 iPhone 快捷指令。当前指令：**一键免打扰（2小时）**。

点击运行时：

1. 关闭蓝牙（不是仅在控制中心断开配件）；
2. 关闭 Wi-Fi；
3. 关闭蜂窝数据；
4. 计算当前时间往后 2 小时；
5. 开启勿扰专注模式，并设置在计算出的时间结束。

**两小时后只关闭勿扰模式**；蓝牙、Wi-Fi 和蜂窝数据不会自动重新打开。

## 当前状态（2026-10-31）

- 已完成生成程序 build_shortcut.py 和 tests/test_build.py。
- 五项结构测试通过；可以生成未签名 .shortcut 文件。
- 已在 GitHub Actions 实测：苹果官方 shortcuts sign 因运行环境未登录 iCloud 而失败。
- 尝试通过 Shortcuty 第三方签名 API（https://sign.shortcuty.app/api/v1/sign）执行公开签名，服务返回 HTTP 403。
- **尚未生成能够在 iPhone 上确认导入的已签名文件，更没有苹果 iCloud 分享链接。**
- 不提供不存在的下载链接，不能将未签名文件冒充可导入文件。

[查看 GitHub Actions 日志](https://github.com/miketoryan/iOS-Shortcuts/actions)

## 成功签名后从手机下载

只有在 GitHub Actions 构建成功、仓库内出现 dist/one-tap-dnd-2h.shortcut 后，才能用下面的下载地址：

https://github.com/miketoryan/iOS-Shortcuts/raw/refs/heads/main/dist/one-tap-dnd-2h.shortcut

通过 iPhone Safari 下载签名后的文件，打开「文件」App，点击文件导入苹果「快捷指令」。

以上是 GitHub 文件下载，**不是苹果 iCloud 一键导入分享链接**。后者需要通过苹果分享流程发布。

## 自动构建与安全性

- 生成源码：build_shortcut.py
- 结构测试：python3 -m unittest discover -s tests -v
- GitHub Actions 首先尝试苹果 shortcuts sign --mode anyone。
- 如果缺少 iCloud 登录，会向 Shortcuty 第三方公开签名服务传送**仅含开关设置动作**的快捷指令文件，不传送密码、账号或其他私密数据。
- 如果任何签名流程失败，构建明确失败，**不会发布未签名文件**。
- 即使收到 AEA1 签名文件，也需要在真实 iPhone 上核验动作。

注意：执行后手机会失去 Wi-Fi 和蜂窝网络连接；请预先保存需要离线使用的资料。
