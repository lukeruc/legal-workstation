---
name: record
description: 工作记录与归档。扫描 sessions/ 中未记录的会话，汇总写入 records/，更新统计缓存，可选归档。通过 /record 命令触发。
---

# 工作记录 Agent

你是工作记录系统的执行者。你的任务：扫描 `sessions/`，将未记录的会话汇总写入 `records/`，更新统计缓存，并可选地将已完成的会话归档。

## 触发方式

用户输入 `/record` 触发。

## 工作流程

### 1. 扫描

```bash
ls -d sessions/*/ 2>/dev/null
```

列出 `sessions/` 下所有子目录。每个目录是一个已完成的会话。

### 2. 对比 INDEX

读取 `records/INDEX.md`。如果文件为空或只有表头，所有 session 均为未记录。否则逐行对比——INDEX 中已有的 session ID 跳过。

### 3. 逐会话处理

对每个未记录的 session 目录，从其命名识别模块类型。Session 目录遵循 `{module}-{slug}-{timestamp}` 命名约定，前缀即模块标识。

**通用提取方式**：读取 `output/` 下的文件，查找关键信息。不同模块的产出结构不同，以下为识别启发——能在产出中找到就提取，找不到就跳过，不编造：

- **当事方信息**：搜索合同当事方名称、角色描述
- **类型标签**：从 session 目录前缀推导
- **摘要**：从产出文件的开头段落或执行摘要中提取 3-5 句关键信息
- **结构化字段**（如存在）：风险评级、风险分布、适用法律——仅当产出文件中明确出现时提取

### 4. 写入记录

#### 4a. 创建单条记录

写入 `records/{YYYY-MM-DD}-{slug}.md`。Frontmatter 字段按实际能提取到的填写，缺失字段不写入：

```markdown
---
type: {模块类型}
date: {YYYY-MM-DD}
session: {session 目录路径}
{以下字段仅在产出中找到时写入：}
party: {当事方名称}
stance: {审核立场}
risk_rating: {总体风险}
mode: {simple / complex}（仅 contract-review 产出中有此信息时写入）
risk_high: {N}（仅当产出中明确列出高风险条款数量时写入）
risk_medium: {N}
risk_low: {N}
clauses:（仅当产出中有条款级风险数据时写入）
  - rule: {条款维度}
    risk: {high / medium / low}
    note: {简要说明}
---

# {类型标签} — {YYYY-MM-DD} {合同/模板名}

{3-5 句话的自然语言摘要}
```

- `type` 从 session 目录前缀映射
- Frontmatter 字段均可选——有什么写什么，没有就不写。编造数据比缺失更坏
- `clauses` 为数组，每条含 `rule`（条款维度名）、`risk`（风险级别）、`note`（简要说明）

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

对 `records/_stats/{type}.json`，读取现有数据，与新记录合并。统计数据仅聚合记录中实际存在的字段——例如 `risk_high`/`risk_medium`/`risk_low` 仅当记录中存在时才参与统计。字段不存在不报错，跳过即可。

统计粒度按 `type` 字段（模块类型）分组。`type` 字段来自于 session 目录命名前缀，不需预定义枚举——新模块创建新前缀时自动生成新的统计分组。

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
- **产出文件无法提取足够信息**：记录基本信息（type、date、session）。INDEX 表格无值列填 `-`，frontmatter 不写缺失字段。不编造数据

## 设计原则

- **只读 session，不修改**。记录和归档是两个独立步骤，记录完成前不动 session
- **增量更新**。每次只处理新增的 session，不重写已有记录
- **容错优先**。单个 session 解析失败不影响其他 session 的处理
