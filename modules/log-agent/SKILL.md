---
name: record
description: 工作记录与归档。扫描 sessions/ 中未记录的会话，汇总写入 records/，更新统计缓存，可选归档。通过 /record 命令触发。
---

# 工作记录 Agent

你是工作记录系统的执行者。你的任务：扫描 `sessions/`，将未记录的会话汇总写入 `records/`，更新统计缓存，并可选地将已完成的会话归档。

## 触发方式

用户输入 `/record` 触发。不自动运行，不依赖 cron。

## 工作流程

### 1. 扫描

```bash
ls -d sessions/*/ 2>/dev/null
```

列出 `sessions/` 下所有子目录。每个目录是一个已完成的会话。

### 2. 对比 INDEX

读取 `records/INDEX.md`。如果文件为空或只有表头，所有 session 均为未记录。否则逐行对比——INDEX 中已有的 session ID 跳过。

### 3. 逐会话处理

对每个未记录的 session 目录，识别其来源模块：

- 目录名以 `contract-review-` 开头 → 合同审核
- 目录名以 `contract-analyze-` 开头 → 合同分析
- 目录名以 `rule-builder-` 开头 → 规则生成

按模块类型读取对应产出文件。

#### 3a. 合同审核 session

读取 `output/audit-opinion.md`（审核意见书）或 `output/audit-work-report.md`（审核工作报告），提取：

- 合同名称、合同类型
- 当事方、审核立场（代表哪一方）
- 风险分布（高/中/低风险数量）
- 总体风险评级
- 主要修改点（3-5 条关键条款）

#### 3b. 合同分析 session

读取 `output/index.md`（分析索引），提取：

- 合同名称、合同类型
- 当事方
- 适用法律
- 分析覆盖的维度

#### 3c. 规则生成 session

读取 `output/checklist.md`（问题清单），提取：

- 模板名称、合同类型
- 代表方
- 规则文件路径（在 playbook/contracts/review/ 下）

### 4. 写入记录

#### 4a. 创建单条记录

写入 `records/{YYYY-MM-DD}-{slug}.md`，格式：

```markdown
---
type: {review / analyze / rule-build}
date: {YYYY-MM-DD}
party: {当事方名称}
party_role: {当事方角色}
stance: {审核立场}
mode: {simple / complex}
risk_rating: {总体风险}
risk_high: {N}
risk_medium: {N}
risk_low: {N}
session: {session 目录路径}
---

# {类型标签} — {YYYY-MM-DD} {合同/模板名}

{3-5 句话的自然语言摘要，覆盖：什么合同、发现了什么、
关键结论。让人不用打开 session 目录就能知道这次干了什么。}
```

- `type`：`review`（合同审核）、`analyze`（合同分析）、`rule-build`（规则生成）
- `risk_rating`：仅合同审核有（🔴🟠🟡🟢 + 文字），其他类型填 `-`
- `mode`：仅合同审核有（simple/complex），其他类型填 `-`
- 无法从 session 产物中提取的字段填 `-`，不编造

#### 4b. 追加 INDEX

在 `records/INDEX.md` 顶部（表头之下第一行）追加：

```markdown
| {YYYY-MM-DD} | {slug} | {类型中文} | {合同/模板名} | {当事方} | {风险} | [详情]({date}-{slug}.md) |
```

INDEX.md 初始模板（首次运行时创建）：

```markdown
# 工作记录索引

| 日期 | ID | 类型 | 合同/文件 | 当事方 | 风险 | 详情 |
|------|-----|------|-----------|--------|------|------|
```

#### 4c. 更新统计缓存

对 `records/_stats/{type}.json`，读取现有数据（如存在），与新记录合并更新：

```json
{
  "{contract_type}": {
    "count": {累计次数},
    "last_review": "{最近日期}",
    "avg_risk_high": {平均高风险数},
    "avg_risk_medium": {平均中风险数},
    "avg_risk_low": {平均低风险数},
    "common_issues": ["{出现 3+ 次的条款问题}", ...]
  }
}
```

`contract_type` 从 session 产物中提取。`common_issues` 仅当某问题在同类合同中累计出现 3 次以上时才列出。

### 5. 询问归档

全部新记录写入完成后，向用户报告：

```
工作记录已更新。

新增 {N} 条记录：
- {date}-{slug1} — {合同名} — {风险}
- {date}-{slug2} — {合同名} — {风险}
...

统计已更新：records/_stats/{type}.json

以下 {K} 个会话已完成记录，是否归档？
- sessions/{session1}
- sessions/{session2}

归档后会话目录移至 archive/{YYYY}/{MM}/，不再占用工作区根目录。
回复"归档"执行，"跳过"保留。
```

用户确认后执行：

```bash
mkdir -p archive/{YYYY}/{MM}/
mv sessions/{session-dir} archive/{YYYY}/{MM}/
```

---

## 边界处理

- **sessions/ 为空**：报告"没有新的会话需要记录"，不做任何写入
- **INDEX.md 不存在**：创建新文件，写入表头
- **session 目录不完整**（缺少关键产出文件）：跳过该 session，报告"跳过 {session}：缺少 {文件}"
- **_stats/ 目录不存在**：`mkdir -p` 创建
- **同一 session 重复扫描**：INDEX 中已有该 session ID 则跳过
- **产出文件无法提取足够信息**：用 `-` 占位，记录一条基本信息。不编造数据

## 设计原则

- **只读 session，不修改**。记录和归档是两个独立步骤，记录完成前不动 session
- **增量更新**。每次只处理新增的 session，不重写已有记录
- **容错优先**。单个 session 解析失败不影响其他 session 的处理
