# iOS-Shortcuts

一键免打扰（2小时）——iPhone 快捷指令。

## 已修复版本（2026-10-31）

[手机获取最新版已签名 .shortcut](https://github.com/miketoryan/iOS-Shortcuts/raw/4e6908b/dist/one-tap-dnd-2h.shortcut)

**这是新版本，旧版文件不要继续使用。** 如果之前导入过，请先在快捷指令 App 中删除旧指令，再下载并添加新版本。

### 点击执行后，严格按照顺序

1. **关闭蓝牙**（设置为关，不是切换状态）。
2. **关闭 Wi-Fi**（设置为关）。
3. **关闭蜂窝数据**（设置为关）。
4. 获取点击时的当前时间。
5. 当前时间 **增加 2 小时** 得到截止时间。
6. **将勿扰模式设为开启**，并设置在第 5 步计算的日期时间自动结束。

例如 20:00 点击：立即关闭三个无线开关，打开勿扰模式；22:00 系统自动关闭勿扰模式。**蓝牙、Wi-Fi、蜂窝数据在 22:00 不会自动打开。**

### 修复原因

此前 Cherri 生成的默认 Focus 动作可能遗漏 Enabled=1。手动指定后，又发现它将 FocusModes 字段错误编码为 WFDictionaryFieldValue。最新版经过以下修复：
- 直接明确 Enabled=1 和 Operation=Turn；
- 编译后将 FocusModes 修正为苹果原生的字典格式；
- 验证六步动作顺序、三个无线关闭开关、当前日期、加两小时、勿扰的开始与结束时间引用；
- 仅在全部验证通过后，调用第三方 HubSign 签名，发布已签名文件。

[GitHub Actions 最新成功构建与结构验证](https://github.com/miketoryan/iOS-Shortcuts/actions/runs/41200503551)

**验证范围**：代码、编译出的原生 plist、签名文件与仓库发布已经验证通过；但苹果 iPhone iOS 26 上的实际运行及两个小时后的系统关停仍需设备验证。

### 仅用 iPhone 安装

用 iPhone Safari 打开上面的最新版文件链接，保存到「文件」App，点文件导入「快捷指令」。这是已签名文件方式，不是苹果 iCloud 分享链接，无法把 GitHub 链接伪装成 iCloud 链接。

注：HubSign 是第三方签名服务，仅接收不包含 Apple ID、密码或其他秘密的快捷指令内容。
