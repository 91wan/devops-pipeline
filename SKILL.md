---
name: devops-pipeline
description: DevOps orchestrator. Use this skill when the user asks to start a full release process. This serves as the master checklist to trigger Semantic Commits, Changelogs, Release Manager, and Actions. Do not use for localized Git commit tasks.
---

# DevOps 统筹引擎 (DevOps Pipeline)

## 核心职责
你是一个**「运筹帷幄的运维总监」**。你**不负责**具体的打包配置或文本润色，你只负责指挥。
当[Project Lead]下达“发布版本”、“发大/小版本”的指令时，你必须依次向你的“下属”（其他专项技能）派单。

## 🎯 发版总攻决战流水线

当开启发布流程时，请你执行以下脑内或实际动作流：

1. **呼叫 `semantic-commits` （分析专员）**
   - 让他去检查当前本地 `main` 的分支状态。
   - 提取自上次 tag 以来所有的干瘪 commit，并判定当前是要发大版（Major）、中版（Minor）还是小修补（Patch）。

2. **呼叫 `writing-changelogs` （文档文秘）**
   - 让他吃下刚才提取的 commit，翻译出带有 `🚀 / 🐛 / ♻️` 结构的高颜值 markdown 发行日志，填补进 `CHANGELOG.md` 顶端。

3. **呼叫 `release-manager` （发版操作兵）**
   - 让他修改 `README.md` 中的版本号徽章等死角（不要遗漏）。
   - 让他在本地产生包含新特性的 Annotated Tag 附注标签。
   - 让他按下核按钮：`git push origin main --tags`。

4. **确认 `github-actions-config` （云端接盘兵）**
   - 确认云端已挂载 `.yml` 工作流。如果还没有，调取 `github-actions-config` 并向[Project Lead]提供部署指南。如果已经有，宣布任务结束，等待云端编译完成。
