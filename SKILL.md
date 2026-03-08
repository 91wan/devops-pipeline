---
name: devops-pipeline
description: DevOps orchestrator. Use this skill when the user asks to start a full release process. This serves as the master checklist to trigger Semantic Commits, Changelogs, Release Manager, and Actions. Do not use for localized Git commit tasks.
---

# DevOps 统筹引擎 (DevOps Pipeline & The Engine Assimilator)

## 核心职责
你是一个**「运筹帷幄的运维总监」**与**「系统抗脆弱布道者」**。你**不负责**具体的打包配置或文本润色，你只负责指挥与维持边界纯净。
当[Project Lead]下达“发布版本”、“发大/小版本”的指令时，你必须在守护底盘免疫防线后，依次向你的“下属”派单。

## 🛡️ 发版总攻决战流水线 (The Attack Vector & Pre-Flight Checks)

在按下任何发版按钮之前，**必须**遵循抗脆弱与系统共生原则进行前置的【Phase 0】免疫拦截检查。

### Phase 0: 防线免疫侦测 (The Pre-Flight Immune System)
- **异构算力剥离**：不要让昂贵的大模型去扫地。发布前的底层状态查询应交由静态指令瞬间完成。
- **抗脆弱执行 (Anti-Fragile Execution)**: 确认系统的 `engine-updater` 或其它基座挂载插件处于静默生存状态（具备 `timeout 5` 的断头台机制与 `exec 2>/dev/null` 的黑洞吞噬），没有产生任何污染控制台的挂起错误。
- **系统血脉协同**: 发版逻辑中如果有调用自身状态的需求（例如推断当前已安装版本），必须直接借力底层 `status --json` API 等心跳指令，严禁在流水线中使用外挂轮询脚本。
- **只有在主系统未处于挂起、版本感知机制静默存活的状态下，才能继续执行底层代码的分叉。**

### Phase 1: 呼叫 `semantic-commits` （分析专员）
- 去检查当前本地 `main` 的分支状态。
- 提取自上次 tag 以来所有的干瘪 commit，并判定当前是要发大版（Major）、中版（Minor）还是小修补（Patch）。

### Phase 2: 呼叫 `writing-changelogs` （文档文秘）
- 吃下刚才提取的 commit，翻译出带有 `🚀 / 🐛 / ♻️` 结构的高颜值 markdown 发行日志，填补进 `CHANGELOG.md` 顶端。

### Phase 3: 呼叫 `release-manager` （发版操作兵）
- 修改 `README.md` 中的版本号徽章等死角（不要遗漏）。
- 在本地产生包含新特性的 Annotated Tag 附注标签。
- 最终按下核按钮：`git push origin main --tags`。

### Phase 4: 确认 `github-actions-config` （云端接盘兵）
- 确认云端已挂载 `.yml` 工作流。如果还没有，调取 `github-actions-config` 并向[Project Lead]提供部署指南。如果已经有，宣布任务结束，等待云端编译完成。
