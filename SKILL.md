---
name: devops-pipeline
description: Use when releasing a version, writing commit messages, bumping changelogs, tagging git releases, or setting up GitHub Actions CI/CD for macOS app builds.
---

# DevOps 全自动化流水线 (DevOps Pipeline)

## Overview

三合一 DevOps 自动化：**提交规范 + 发版大管家 + 云端 CI/CD**。

---

### 🧠 设计理念：终极全自动发版流水线（零手工方案）

> 脑体分离。Agent 出谋划策，Actions 埋头苦干。

整个发版流程被精确切分为**两个阶段**，各司其职，互不越界：

#### 🤖 第一阶段：OpenClaw 负责「文书与指令」（本地执行）

> 动动嘴皮子，Agent 包圆。

- 读取 commit 历史，计算语义版本号
- 生成高颜值中文 Emoji CHANGELOG
- **【强制】自动分析并全面更新目标项目的 `README.md`**：
  - 版本号徽章（如 `![Version](https://img.shields.io/badge/version-vX.X.X-blue)`）
  - `## What's New` / `## 最新版本` 区块的最新特性清单
  - 安装/下载命令中的版本号引用
  - 若 README 包含截图路径、演示 GIF 等媒体，检查是否需随版本更新
  - 若无上述任何区块，则在文件末尾追加 `## 最新版本：vX.X.X` 摘要块
- 打上 Annotated Tag（附注标签），写入发版说明
- 一键 `git push origin main --tags`，收工

**Agent 的工作在 push 完成时画上句号。**

#### ☁️ 第二阶段：GitHub Actions 负责「苦力打包」（云端静默执行）

> 人已离场，机器接管。

- 监听到 `v*` tag 推送，自动触发构建
- xcodebuild 编译 Release 产物
- 打包压缩，上传至 GitHub Release 页面
- 自动标记 prerelease（`-beta` / `-alpha`）

**全程无需人工干预，构建结束即见成品。**

---

**核心原则：** 版本号由 commit 语义驱动，发版流程由 Agent 一键执行，云端构建由 GitHub Actions 自动完成。

---

## 🛫 起飞前检查（Pre-flight）— 每次动工前必做

> **禁止在 `main` 上直接裸奔提交！** 所有新工作必须在独立分支进行。

### Step 0：起飞前例行检查

```bash
# 1. 查看当前状态与所在分支
git status

# 2. 确认分支命名
#   新功能 → feat/xxx
#   修 bug → fix/xxx
#   发版   → 在 main 上执行 release 流程
#   其他   → chore/xxx、docs/xxx、refactor/xxx

# 3. 如果还在 main，立即切换到功能分支
git checkout -b feat/my-new-feature   # 新功能
git checkout -b fix/crash-on-launch   # 修 bug
```

### 分支命名规范

| 类型 | 命名模式 | 示例 |
|------|---------|------|
| 新功能 | `feat/<简短描述>` | `feat/oauth-login` |
| 修 Bug | `fix/<简短描述>` | `fix/nil-crash-launch` |
| 重构 | `refactor/<简短描述>` | `refactor/view-model` |
| 文档 | `docs/<简短描述>` | `docs/update-readme` |
| 杂项 | `chore/<简短描述>` | `chore/bump-deps` |

> ⚠️ **Red Line**：绝对不允许 `git commit` 时当前分支为 `main` 或 `master`（发版 Release Commit 除外）。Agent 在提交前须检查当前分支。

---

## 模块一：代码提交与版本流转规范

### Conventional Commits（必须遵守）

```
<type>(<scope>): <中文描述>

[可选正文，中文]
[可选脚注]
```

| type | 版本影响 | Subject 示例（中文）|
|------|---------|------|
| `feat` | MINOR +1 | `feat(认证): 新增 OAuth2 登录` |
| `fix` | PATCH +1 | `fix(崩溃): 修复启动时空指针` |
| `feat!` / `BREAKING CHANGE` | MAJOR +1 | `feat!: 重新设计数据模型` |
| `chore` | 无 | `chore: 升级依赖版本` |
| `docs` | 无 | `docs: 更新 README 安装说明` |
| `refactor` | 无 | `refactor(界面): 提取视图模型层` |
| `test` | 无 | `test: 补充解析器单元测试` |
| `ci` | 无 | `ci: 添加发版工作流` |

### ✏️ Subject 书写规范

- **必须用精炼中文**，清晰表达改动意图
- 动词开头（新增、修复、重构、更新、移除、优化…）
- 不超过 50 个汉字（或 50 字符）
- 不加句号结尾
- 🚫 禁止：`fix bug`、`update`、`WIP`、`temp` 等模糊英文

**好的示例：**
```
feat(首页): 新增深色模式自适应切换
fix(网络): 修复弱网环境下请求超时崩溃
chore: 升级 Swift 工具链至 5.10
refactor(数据层): 将 CoreData 迁移至 SwiftData
```

### Semantic Versioning 映射

```
MAJOR.MINOR.PATCH
  ↑      ↑     ↑
破坏性  新特性  修复
```

**判断规则：**
- 任意 `BREAKING CHANGE` → 大版本
- 有 `feat` 无 breaking → 小版本
- 只有 `fix/docs/chore` → patch

---

## 模块二：Release Manager 发版大管家

### 触发指令

大刘下达以下任意指令时，立即启动完整发版流程：
- "发布大版本" / "发 major"
- "发布小版本" / "发 minor" / "发新功能版"
- "发 patch" / "发修复版"
- "发布 vX.X.X"

### 发版自动化流程（严格按序执行）

```
Step 0: Pre-flight 检查（git status + 确认在 main/master 分支）
Step 1: 确定新版本号
Step 2: 提取 commit 历史
Step 3: 更新 CHANGELOG.md（中文 Emoji 分类排版）
Step 4: 更新 README.md 版本号与特性列表
Step 5: git commit -am "chore: 发布 vX.X.X"
Step 6: git tag -a vX.X.X -m "发布 vX.X.X"
Step 7: git push origin main --tags
```

#### Step 0 — Pre-flight 发版检查

```bash
# 确认工作区干净
git status

# 确认在主分支
git branch --show-current   # 应输出 main 或 master

# 如有未合并的功能分支，先 merge 或 squash 合并进来
```

#### Step 1 — 确定版本号

```bash
# 获取当前最新 tag
git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"
```

根据 Conventional Commits 规则计算下一个版本号。

#### Step 2 — 提取 commit 历史

```bash
# 从上一个 tag 到 HEAD 的所有 commit
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
  git log --oneline --no-merges
else
  git log ${LAST_TAG}..HEAD --oneline --no-merges
fi
```

按 type 分类：feat / fix / 破坏性变更 / 其他。

#### Step 3 — 更新 CHANGELOG.md（高颜值中文 Emoji 排版）

在文件顶部插入新版本块，**强制使用以下中文 Emoji 分类标题**：

```markdown
## [vX.X.X] - YYYY-MM-DD

### 🚀 新特性
- 新增 OAuth2 登录支持 (`feat/oauth-login`, abc1234)
- 首页新增深色模式自适应切换 (def5678)

### 🐛 问题修复
- 修复弱网环境下请求超时崩溃 (ghi9012)
- 修复启动时空指针异常 (jkl3456)

### 💥 破坏性变更
- 重新设计数据模型，不兼容旧版本 (mno7890)

### ♻️ 重构优化
- 将 CoreData 迁移至 SwiftData (pqr1234)

### 📝 文档更新
- 更新 README 安装说明 (stu5678)

### 🔧 其他变更
- 升级 Swift 工具链至 5.10 (vwx9012)
```

**Emoji 分类对照表（强制遵守）：**

| Commit Type | 分类标题 |
|-------------|---------|
| `feat` | 🚀 新特性 |
| `fix` | 🐛 问题修复 |
| `BREAKING CHANGE` / `feat!` | 💥 破坏性变更 |
| `refactor` | ♻️ 重构优化 |
| `perf` | ⚡️ 性能提升 |
| `docs` | 📝 文档更新 |
| `test` | ✅ 测试补充 |
| `ci` | 👷 CI/CD |
| `chore` / 其他 | 🔧 其他变更 |

> 若某类别在本次发版中无 commit，则省略该标题，不留空节。

若 CHANGELOG.md 不存在，先创建并写入标准头部：

```markdown
# 更新日志

所有重要变更均记录于此。
格式参考 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [语义化版本](https://semver.org/)。
```

#### Step 4 — 更新 README.md（**强制必做，不得跳过**）

> **⚠️ 重要约束**：README.md 是项目的「门面」，每次发版必须确保其反映最新状态。Agent 必须主动分析 README 的完整内容，识别所有需要更新的位置，而非仅机械替换版本号字符串。

**必须逐项检查并更新以下内容：**

1. **版本号徽章**（如 `![Version](https://img.shields.io/badge/version-vX.X.X-blue)` 或 `![Release](https://img.shields.io/github/v/release/...)`)
2. **最新版本特性列表**（如有 `## What's New`、`## 最新版本`、`## Changelog`、`## 更新日志` 区块）：用本次 `feat` commit 的精炼摘要替换或补充
3. **安装/下载命令中的版本号**（如 `brew install vX.X.X`、`download vX.X.X`、`pip install==X.X.X`）
4. **截图/演示媒体路径**（如截图文件名包含版本号，或有「当前版本界面预览」区块，提醒大刘是否需要更新）
5. **兼容性/系统要求说明**（如有 `macOS 14+` 等版本要求随新版本变化时更新）

**若 README 中找不到任何版本相关区块：**

```markdown
## 最新版本：vX.X.X（YYYY-MM-DD）

### 🚀 本次新增
- [从 feat commit 提取的特性摘要]

### 🐛 本次修复
- [从 fix commit 提取的修复摘要]
```

**原则：** 宁可多更新，不可少更新。发版完成后 README 必须与实际发布内容一致。

#### Step 5–7 — Commit、Annotated Tag、Push

```bash
# 提交所有改动（Subject 用中文）
git commit -am "chore: 发布 vX.X.X"

# ✅ 必须使用 Annotated Tag，禁止轻量级 tag
git tag -a vX.X.X -m "发布 vX.X.X

🚀 新特性：简要列出核心新功能
🐛 修复：简要列出主要修复项"

# 推送 main 分支及所有 tag
git push origin main --tags
```

> ⚠️ **禁止使用** `git tag vX.X.X`（轻量级标签）。Annotated Tag 携带作者信息、时间戳和说明，是 Release 的标准做法。

### 发版前检查清单

- [ ] `git status` — 确认工作区干净
- [ ] `git branch` — 确认当前在 `main` / `master`
- [ ] `git log` — commit 历史符合预期，中文 Subject 规范
- [ ] CHANGELOG.md — 中文 Emoji 分类排版正确
- [ ] README.md — **完整检查并更新**（版本号、特性列表、安装命令、截图/媒体等，不得遗漏）
- [ ] 使用 `git tag -a`（Annotated Tag）打标

### 常见错误

| 错误 | 处理 |
|------|------|
| 无 commit 可发布 | 告知大刘，当前无新改动 |
| tag 已存在 | 询问是否覆盖 (`git tag -d vX.X.X` + 重建) |
| push 被拒绝 | 先 `git pull --rebase` 再 push |
| README 无版本区块 | 追加 `## 最新版本：vX.X.X` 区块（含特性/修复摘要） |
| README 更新被遗漏 | **严重错误**：返回 Step 4，补全所有版本相关内容后重新提交 |
| 在 main 上有未提交改动 | 先暂存 (`git stash`) 或切到功能分支 |

---

## 模块三：云端流水线 GitHub Actions 模板

当大刘需要为 macOS 原生 App 配置 CI/CD 时，输出以下模板并指导集成。

### 使用方法

1. 在项目根目录创建 `.github/workflows/release.yml`
2. 将 `APP_NAME`、`SCHEME`、`PROJECT_FILE` 替换为实际值
3. 确保 GitHub Repo Settings → Actions → Workflow permissions 设置为 **Read and write**
4. 推送 `v*` annotated tag 即触发自动构建和发布

### 标准模板：`.github/workflows/release.yml`

```yaml
name: Release macOS App

# 触发条件：仅 v* tag 推送时触发
on:
  push:
    tags:
      - 'v*'

env:
  # ✏️ 修改为你的 App 名称
  APP_NAME: MyApp
  # ✏️ Xcode Scheme 名称
  SCHEME: MyApp
  # ✏️ .xcodeproj 或 .xcworkspace 文件名（不含路径）
  PROJECT_FILE: MyApp.xcodeproj

jobs:
  build-and-release:
    name: Build & Release macOS App
    runs-on: macos-latest

    steps:
      # 1. 检出代码
      - name: Checkout repository
        uses: actions/checkout@v4

      # 2. 读取 tag 版本号（去掉 v 前缀）
      - name: Get version from tag
        id: version
        run: echo "VERSION=${GITHUB_REF_NAME#v}" >> $GITHUB_OUTPUT

      # 3. 构建 macOS .app（Release 配置，不签名）
      - name: Build with xcodebuild
        run: |
          xcodebuild \
            -project "$PROJECT_FILE" \
            -scheme "$SCHEME" \
            -configuration Release \
            -derivedDataPath ./build \
            CODE_SIGN_IDENTITY="" \
            CODE_SIGNING_REQUIRED=NO \
            CODE_SIGNING_ALLOWED=NO \
            clean build

      # 4. 定位 .app 产物
      - name: Locate built .app
        id: locate
        run: |
          APP_PATH=$(find ./build -name "*.app" -maxdepth 6 | head -1)
          echo "APP_PATH=$APP_PATH" >> $GITHUB_OUTPUT
          echo "Found: $APP_PATH"

      # 5. 压缩为 zip
      - name: Archive .app to zip
        run: |
          cd "$(dirname "${{ steps.locate.outputs.APP_PATH }}")"
          zip -r "$GITHUB_WORKSPACE/${APP_NAME}-macOS.zip" "$(basename "${{ steps.locate.outputs.APP_PATH }}")"

      # 6. 创建 GitHub Release 并上传附件
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ github.ref_name }}
          name: "Release ${{ github.ref_name }}"
          body: |
            ## ${{ env.APP_NAME }} ${{ github.ref_name }}

            ### 📥 下载安装（macOS 保姆级教程）

            1. 点击下方 **Assets** 中的 `${{ env.APP_NAME }}-macOS.zip` 下载压缩包
            2. 双击 zip 解压，得到 `${{ env.APP_NAME }}.app`
            3. 将 `.app` 拖入 `/Applications` 文件夹

            ### 🛡️ macOS 破防指南（打开闪退？看这里！）

            macOS Gatekeeper 会拦截未经公证的 App，导致「已损坏」或「无法打开」。
            在终端执行以下命令一键解除封印：

            ```bash
            xattr -cr /Applications/${{ env.APP_NAME }}.app
            ```

            > **说明：** `xattr -cr` 会递归移除 App 上的隔离属性（`com.apple.quarantine`），
            > 让系统放行运行。这是正常的开发者分发流程，安全无副作用。

            执行后重新双击打开即可。

            ### 📋 更新内容

            请查阅 [CHANGELOG.md](https://github.com/${{ github.repository }}/blob/main/CHANGELOG.md) 查看完整改动记录。
          files: ${{ env.APP_NAME }}-macOS.zip
          draft: false
          prerelease: ${{ contains(github.ref_name, '-beta') || contains(github.ref_name, '-alpha') }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 模板进阶选项

**使用 .xcworkspace（CocoaPods/SPM 项目）：**

```yaml
      - name: Build with xcodebuild (workspace)
        run: |
          xcodebuild \
            -workspace "${APP_NAME}.xcworkspace" \
            -scheme "$SCHEME" \
            -configuration Release \
            -derivedDataPath ./build \
            CODE_SIGN_IDENTITY="" \
            CODE_SIGNING_REQUIRED=NO \
            CODE_SIGNING_ALLOWED=NO \
            clean build
```

**Notarization（签名公证，需要 Apple Developer 账号）：**
签名公证需要额外的 Secrets 配置，适合 App Store 外发布。如需配置，告知大刘，Agent 将单独输出完整的 notarization workflow。

---

## Quick Reference

| 场景 | 动作 |
|------|------|
| 开始新功能 | `git checkout -b feat/xxx`，先 `git status` 确认 |
| 开始修 bug | `git checkout -b fix/xxx`，先 `git status` 确认 |
| 写 commit | `type(scope): 精炼中文描述`，动词开头 |
| 发小版本 | 执行 Step 0-7 发版流程 |
| 打 tag | `git tag -a vX.X.X -m "..."` ← 必须用 annotated |
| Changelog | 中文 Emoji 分类（🚀新特性、🐛修复…） |
| 新建 CI/CD | 输出 `release.yml` 模板并指导 |
| Tag 触发构建 | push `v*` annotated tag 自动触发 |
| 找构建产物 | `find ./build -name "*.app"` |
