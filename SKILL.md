---
name: devops-pipeline
description: DevOps orchestrator. Use this skill when the user asks to start a full release process or pipeline check. Integrates V8 defensive gating, Narrative extraction, and strict release hand-offs. Do not use for localized Git commit tasks.
---

# DevOps 战术编排中心 (V8 架构升维版)

## 核心职责
作为整个 DevOps 矩阵的总开关。当你被呼叫，意味着一次全面的『架构检阅+归档+发版推流』被启动。在此过程中，你必须绝对捍卫 V8 宪法（三维主权隔离、意图分类器、静态防线门卫）。

## Pipeline 黄金执行链

### Phase 1: 扫描隔离防线 (The Pure Room Audit)
1. **呼叫安保**：运行本地或架构配置的 `quarantine_sweep.py`。
2. **零容忍灰度**：如果检测到任何 untracked 废废代码或数字垃圾，直接执行无情移出。

### Phase 2: DNA 自动测序引擎 (The DNA Sensor)
检查项目环境或推断此主体的 `governance_level`：
- 若属于 **Product (公司产品/业务核心)**：启动高危静默挂载！后续必须开启首席口谕审核。
- 若属于 **Infra (开源基座/工具脚本)**：全自动通关机制启动，零打扰直达推流终端。

### Phase 3: 架构师轶事萃取 (Narrative Harvest)
梳理未上报的 Commit、尤其是打有 `Lesson-Learned` 的架构教训。利用这批数据更新 `docs/RELEASE_NARRATIVE.md` 弹药匣，为下一个 Release 提供充足的内容子弹。

### Phase 4: 移交指挥权至专属 Operator
根据需要，在你的框架分析完毕后，调用 `release-manager` 执行打 tag 工作；或是如果涉及到特殊的 CI 重连，委派相关的特遣队操作。一旦执行，此 Pipeline 的主线程宣告闭环，交由云端 GitHub Actions 放行。
