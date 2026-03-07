# 🚀 devops-pipeline

> **终极全自动发版流水线（零手工双阶段方案）**
>
> 一套专为 OpenClaw AI Agent 设计的 DevOps 技能，让版本发布从「繁琐手工」变为「一句话搞定」。

---

## 设计哲学

### 脑体分离，各司其职

传统发版流程最大的问题是**边界模糊**——人既要思考版本号，又要手动改文件，还要记得打 Tag、触发构建。稍有遗漏就是一次不完整的发版。

`devops-pipeline` 的设计哲学是：

> **Agent 出谋划策，Actions 埋头苦干。**

整个发版流程被精确切分为**两个阶段**，互不越界：

```
┌──────────────────────────────────────────────────────────┐
│   🤖 第一阶段（本地）：OpenClaw Agent 负责「文书与指令」    │
│                                                          │
│   读 commit 历史 → 算版本号 → 更新 CHANGELOG → 更新 README │
│   → 打 Annotated Tag → git push origin main --tags       │
│                                                          │
│   ← Agent 工作至此画上句号 →                              │
└──────────────────────────────────────────────────────────┘
                          │ push v* tag
                          ▼
┌──────────────────────────────────────────────────────────┐
│   ☁️ 第二阶段（云端）：GitHub Actions 负责「苦力打包」     │
│                                                          │
│   监听 v* tag → xcodebuild 编译 → 压缩 zip → 上传 Release │
│   → 自动标记 prerelease（-beta/-alpha）                   │
│                                                          │
│   ← 全程无需人工干预 →                                    │
└──────────────────────────────────────────────────────────┘
```

**核心原则**：版本号由 commit 语义驱动，发版流程由 Agent 一键执行，云端构建由 GitHub Actions 自动完成。

---

## 功能概览

### 📝 模块一：约定式提交（Conventional Commits）

严格遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范，Subject 强制使用精炼中文：

```
feat(首页): 新增深色模式自适应切换
fix(网络): 修复弱网环境下请求超时崩溃
chore: 升级 Swift 工具链至 5.10
```

**语义版本自动映射：**

| Commit 类型 | 版本影响 |
|------------|---------|
| `BREAKING CHANGE` / `feat!` | MAJOR +1（大版本）|
| `feat` | MINOR +1（小版本）|
| `fix` / `docs` / `chore` | PATCH +1（补丁）|

**分支保护内置：** 禁止在 `main` / `master` 上直接提交功能代码，发版 Release Commit 除外。

---

### 📦 模块二：本地发版大管家（Release Manager）

[Project Lead]只需一句话触发完整发版：

```
"发布小版本"  /  "发 major"  /  "发布 v2.1.0"
```

Agent 自动按序执行 **7 个步骤**：

| 步骤 | 动作 |
|-----|------|
| Step 0 | Pre-flight 检查（工作区干净 + 确认在 main）|
| Step 1 | 根据 commit 历史计算下一个语义版本号 |
| Step 2 | 提取上一个 Tag 到 HEAD 的所有 commit |
| Step 3 | 生成/更新 `CHANGELOG.md`（高颜值中文 Emoji 分类排版）|
| **Step 4** | **强制分析并全面更新 `README.md`**（见下文重点说明）|
| Step 5–6 | `git commit` 并打 Annotated Tag（附注标签，非轻量 tag）|
| Step 7 | `git push origin main --tags`，触发云端流水线 |

#### ⭐ README.md 强制更新机制

每次发版，Agent **必须**主动分析 README 全文并更新：

- ✅ 版本号徽章（`img.shields.io`、`github/v/release`）
- ✅ `## What's New` / `## 最新版本` 等特性清单区块
- ✅ 安装/下载命令中的版本号引用
- ✅ 截图/演示媒体路径（如含版本号，提醒确认更新）
- ✅ 兼容性/系统要求说明
- ✅ 若无任何版本区块，自动追加 `## 最新版本：vX.X.X` 摘要块

> 发版完成后，README 必须与实际发布内容完全一致。宁多不少。

#### 高颜值 CHANGELOG 格式

```markdown
## [v1.2.0] - 2026-03-06

### 🚀 新特性
- 首页新增深色模式自适应切换 (abc1234)

### 🐛 问题修复
- 修复弱网环境下请求超时崩溃 (def5678)

### ♻️ 重构优化
- 将 CoreData 迁移至 SwiftData (ghi9012)
```

Emoji 分类：🚀 新特性 · 🐛 问题修复 · 💥 破坏性变更 · ♻️ 重构优化 · ⚡️ 性能提升 · 📝 文档更新 · ✅ 测试补充 · 👷 CI/CD · 🔧 其他变更

---

### ☁️ 模块三：云端流水线（GitHub Actions）

为 macOS 原生 App 提供开箱即用的 CI/CD 模板：

**文件路径**：`.github/workflows/release.yml`

**触发机制**：仅响应 `v*` annotated tag 推送

**构建流程**：

```
v* tag push
    │
    ▼
Checkout 代码
    │
    ▼
xcodebuild Release 构建（不签名）
    │
    ▼
zip 压缩 .app 产物
    │
    ▼
创建 GitHub Release + 上传附件
    │
    ▼
自动判断 prerelease（含 -beta / -alpha 自动标记）
```

**支持的项目类型：**
- `.xcodeproj` 标准项目
- `.xcworkspace`（CocoaPods / SPM 工作区）
- 可选：Notarization 公证流程（需 Apple Developer 账号）

---

## 使用方法

### 前提条件

1. 安装 [OpenClaw](https://openclaw.ai)（AI Agent 运行时）
2. 项目已使用 Git 管理，推荐遵循 Conventional Commits 规范

### 激活技能

将 `devops-pipeline` 目录放置于 OpenClaw 技能路径下（通常为 `~/.openclaw/workspace/skills/`）。

技能描述关键词会自动匹配以下场景：
- 发布版本、写 commit、版本号变更
- 更新 Changelog、打 Tag
- 配置 GitHub Actions CI/CD
- macOS App 自动构建

### 触发发版示例

```
[Project Lead]：发布小版本
Agent：
  ✅ Step 0: 工作区干净，当前在 main 分支
  ✅ Step 1: 上一版本 v1.1.0 → 新版本 v1.2.0（有 feat commit）
  ✅ Step 2: 提取到 8 条 commit（3 feat, 4 fix, 1 chore）
  ✅ Step 3: CHANGELOG.md 已更新（中文 Emoji 分类）
  ✅ Step 4: README.md 已更新（版本号徽章、最新特性列表、安装命令）
  ✅ Step 5-6: git commit + git tag -a v1.2.0
  ✅ Step 7: git push origin main --tags
  🎉 v1.2.0 发版完成！GitHub Actions 已触发云端构建。
```

### 配置 GitHub Actions

在项目根目录创建 `.github/workflows/release.yml`，修改以下变量：

```yaml
env:
  APP_NAME: MyApp        # ← 你的 App 名称
  SCHEME: MyApp          # ← Xcode Scheme 名称
  PROJECT_FILE: MyApp.xcodeproj  # ← 项目文件名
```

确保 GitHub Repo Settings → Actions → Workflow permissions 设置为 **Read and write**。

推送 `v*` annotated tag 即自动触发构建：

```bash
git push origin main --tags
# → GitHub Actions 自动触发 → 构建 → 发布 Release
```

---

## 技能文件结构

```
devops-pipeline/
├── SKILL.md     # 技能主文件（OpenClaw Agent 读取的指令集）
└── README.md    # 本文件（技能介绍与使用指南）
```

---

## 设计原则总结

| 原则 | 说明 |
|-----|------|
| **零手工** | 发版全流程由 Agent + Actions 自动完成，人只需下达一句指令 |
| **语义驱动** | 版本号由 commit 类型自动计算，消除人工判断误差 |
| **边界清晰** | 本地文书（Agent）与云端构建（Actions）严格分离 |
| **README 强制更新** | 每次发版必须同步更新项目门面，确保用户看到最新信息 |
| **中文优先** | commit、changelog、tag 说明全部使用精炼中文 |
| **Annotated Tag** | 强制使用附注标签，携带完整元数据，是发版的标准做法 |

---

## License

MIT — 自由使用、修改与分发。

---

*Built with ❤️ for [OpenClaw](https://openclaw.ai) · 让 AI 做脏活，你来做决策*
