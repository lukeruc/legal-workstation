# Legal Workstation

## 愿景

**让律师从操作者变成导演。** AI 负责执行（读合同、查法规、写意见、做修订），律师负责判断（定标准、做决策、最终签字）。

跑在 [Claude Code](https://claude.ai/code) 之上。

---

## 快速开始

### 1. 安装

```bash
mkdir ~/my-legal-work && cd ~/my-legal-work
git clone https://github.com/lukeruc/legal-workstation.git /tmp/legal-workstation
cp -r /tmp/legal-workstation/coldstart/. ./
rm -rf /tmp/legal-workstation
```

功能模块和工具 skill 在仓库 `modules/` 下，按需复制到 `.claude/skills/`：

```bash
cp -r /tmp/legal-workstation/modules/contract-review ~/my-legal-work/.claude/skills/
cp -r /tmp/legal-workstation/modules/contract-analyze ~/my-legal-work/.claude/skills/
cp -r /tmp/legal-workstation/modules/rule-builder ~/my-legal-work/.claude/skills/
cp -r /tmp/legal-workstation/modules/yd-law ~/my-legal-work/.claude/skills/
cp -r /tmp/legal-workstation/modules/qcc ~/my-legal-work/.claude/skills/
cp -r /tmp/legal-workstation/modules/mdconverter ~/my-legal-work/.claude/skills/
```

### 2. 冷启动

在工作目录下打开 Claude Code。Agent 检测到尚未配置，自动启动对话，大约 3-5 分钟：

1. **种子文件提取**（可选）。给合同模板，agent 自动识别公司业务、法域、风格。模板自动归档到 `playbook/contracts/templates/`。
2. **对话补充**。输出风格偏好、风险评级体系等。
3. **工具测试**。实际调用验证连通性。
4. **写入档案**。对话内容写入 `.claude/profiles/`（五条领域：公司、角色、语境、工具、输出）。
5. **自清理**。`scripts/` 目录删除。

冷启动只记**能改变模型输出行为的信息**。不记审批链和内部政策红线。想改档案说 "update my profile"。

### 3. 日常使用

```
/contract-review path/to/合同.docx    → 审核意见书 + 修订 .docx
/contract-analyze path/to/合同.md     → 当事人画像、条款分析、冲突检测
/rule-builder path/to/模板.docx       → 对话式问答，生成审查规则
/record                                → 扫描会话，写入记录，可选归档
```

- contract-review 支持 .docx 和 .pdf，附带施工合同和保密协议两份种子审查规则
- contract-analyze 接受 Markdown，不改合同、不做法律判断
- rule-builder 生成的规则直接写入 `playbook/contracts/review/`，contract-review 自动加载

---

## 系统架构

法律 AI 工作站包含三层：

```
┌──────────────────────────────────────────────┐
│              法律 AI 工作站                   │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │         基础设施层（共享 · 不拆）        │ │
│  │                                          │ │
│  │  CLAUDE.md       .claude/profiles/      │ │
│  │  人格·路由·地图   用户档案               │ │
│  │                                          │ │
│  │  playbook/        records/   archive/    │ │
│  │  操作规程         工作记录   审查归档     │ │
│  │                                          │ │
│  │  sessions/                               │ │
│  │  任务工作区                               │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │      功能模块层（松耦合 · 独立发版）     │ │
│  │                                          │ │
│  │  contract-review   contract-analyze      │ │
│  │  rule-builder                            │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │        工具层（MCP · 即插即用）          │ │
│  │  agentdocx  mdconverter  yd-law  qcc    │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  Claude Code（运行时）                        │
└──────────────────────────────────────────────┘
```

### 设计原则

1. **基础设施定义物理定律。** 路径约定、字段格式、加载规则——所有模块遵守。改基础设施影响所有模块，因此变更频率远低于模块。
2. **模块之间互不依赖。** contract-review 不知道 contract-analyze 的存在。每个模块只依赖基础设施。
3. **接口只有文件路径 + 字段名。** 不存在 API 调用、函数导入、RPC。模块声明"我需要 profiles 里的公司名、playbook/contracts/review/ 下的规则"，找不到就降级运行。

### 路径契约

基础设施层对各模块的承诺。稳定路径，模块可硬编码：

| 路径 | 说明 |
|------|------|
| `.claude/profiles/*.md` | 用户档案（冷启动生成，1 到 N 个文件） |
| `playbook/process/approach.md` | 任务判断规则 |
| `playbook/process/information.md` | 信息可靠性规则 |
| `playbook/process/role.md` | 角色边界规则 |
| `playbook/contracts/review/` | 审查规则目录（0 到 N 个 .md） |
| `playbook/contracts/templates/` | 公司合同模板目录 |
| `sessions/` | 任务工作区 |
| `records/INDEX.md` | 工作记录索引 |
| `records/_stats/` | 统计缓存 |

---

## 与其它仓库的关系

以下独立仓库的功能已整合进本项目，在 `modules/` 下统一开发。成熟后提取为独立仓库，届时可通过 `git clone` 直接安装到 `.claude/skills/`。

| 仓库 | 在 `modules/` 中的位置 | 说明 |
|------|----------------------|------|
| contract-review | `modules/contract-review/` | 合同审核，EPC 三层架构，双模式 |
| contract-analyze | `modules/contract-analyze/` | 合同结构分析，PM 委托模式 |
| rule-builder | `modules/rule-builder/` | 审查规则生成，交互式问答 |
| mdconverter | `modules/mdconverter/` | 文档格式转换 |
| yd-law | `modules/yd-law/` | 法律数据检索 |
| qcc | `modules/qcc/` | 企业工商信息查询 |

---

## 外部依赖

- [Claude Code](https://claude.ai/code)
- [agentdocx](https://github.com/lukeruc/agentdocx) — .docx 读写与修订（MCP server，需单独安装）

## License

MIT
