# Legal Workstation

## 愿景

**让律师从操作者变成导演。**

法律 AI 工作站不是"用 AI 辅助律师"，是让律师像导演一样工作——AI 负责执行（读合同、查法规、写意见、做修订），律师负责判断（定标准、做决策、最终签字）。

传统法律 AI 产品是 SaaS：你上传合同，它返回结果。法律 AI 工作站是另一种范式：你在自己电脑上有一个完整的工作环境，它知道你是谁、你在哪个法域执业、你的公司是什么业务、你的输出风格是什么。每次打开 Claude Code，它不需要你重新说明。

这不是一个软件产品。这是一个工作方式。

---

## 是什么

Legal Workstation 跑在 [Claude Code](https://claude.ai/code) 之上。它包含三层：

| 层 | 说明 | 当前状态 |
|----|------|---------|
| **基础设施层** | CLAUDE.md（人格+路由）、用户档案、操作规程（playbook）、工作记录系统 | 可用 |
| **功能模块层** | 合同审核（contract-review）、合同分析（contract-analyze）、规则生成（rule-builder） | 可用 |
| **工具层** | 文档转换（mdconverter）、法律检索（yd-law）、企业查询（qcc）、Word 修订（agentdocx） | 可用 |

功能模块之间互不依赖。每个模块只认基础设施层的路径和字段——这叫"路径契约"。新增一个模块不需要修改任何现有代码。

---

## 安装

你的工作目录是一个普通的文件夹。安装就是把发行物复制进去：

```bash
mkdir ~/my-legal-work
cd ~/my-legal-work
git clone https://github.com/lukeruc/legal-workstation.git /tmp/legal-workstation
cp -r /tmp/legal-workstation/coldstart/. ./
rm -rf /tmp/legal-workstation
```

安装后目录内容：

```
CLAUDE.md                          # Agent 指令（人格、路由、工作区地图）
scripts/                           # 冷启动脚本（临时，配置后自删）
playbook/                          # 操作规程
├── README.md                      #   使用手册
├── process/                       #   通用底线规则（每次会话必读）
│   ├── approach.md                #     任务判断
│   ├── information.md             #     信息可靠
│   └── role.md                    #     角色边界
└── contracts/                     #   合同工作
    ├── README.md                  #     工作流程
    ├── review/                    #     审查规则
    └── templates/                 #     公司模板
.claude/
├── profiles/                      # 空，等待冷启动写入
└── settings.local.json
```

---

## 冷启动——第一次对话

在这个目录下打开 Claude Code。CLAUDE.md 检测到 profiles/ 为空，自动启动冷启动对话。大约 3-5 分钟：

1. **种子文件提取**（可选）。给合同模板、制度文件，agent 自动提取公司业务、法域、风格。模板自动归档到 `playbook/contracts/templates/`。
2. **对话补充**。种子文件看不出来的——输出风格偏好、风险评级体系——聊天补充。
3. **工具测试**。你提到的工具，agent 实际调用验证连通性。
4. **写入档案**。对话内容写入 `.claude/profiles/`，五条领域指引：公司、角色、语境、工具、输出。
5. **创建目录**。`sessions/`、`records/`、`archive/` 就位。
6. **自清理**。`scripts/` 目录删除。

冷启动只记**能改变模型输出行为的信息**——公司名、法域、工作语言、输出偏好。不记审批链，不记内部政策红线。条款立场在每次审查时根据具体交易判断。

想改档案？说 "update my profile"。

---

## 日常使用

### 审查合同

安装 contract-review skill 后：

```
/contract-review path/to/合同.docx
```

Agent 自动判断简单/复杂模式，匹配审查规则，产出审核意见书 + 修订模式 .docx。支持 .docx 和 .pdf 格式。识别到你的公司出现在当事方中时，自动以公司立场审核。

目前附带两份种子审查规则：
- 建设工程施工合同（`playbook/contracts/review/construction-contract.md`）
- 保密协议（`playbook/contracts/review/nda.md`）

### 分析合同结构

安装 contract-analyze skill 后：

```
/contract-analyze path/to/合同.md
```

接受 Markdown 格式合同，产出结构化文档集：当事人画像、术语词典、条款分析、交叉引用映射、冲突检测。不改合同、不做法律判断。适用于需要深入理解一份复杂合同时。

### 生成审查规则

安装 rule-builder skill 后：

```
/rule-builder path/to/模板.docx
```

从公司合同模板生成审查规则。Agent 分析模板结构，在对话中逐组向你提问（付款条款、违约责任等），你的回答直接转化为审查规则，写入 `playbook/contracts/review/`——contract-review 下次自动加载。

### 记录与归档

```
/record
```

扫描已完成会话，生成工作记录，更新统计缓存。可选归档到 `archive/`。

---

## 安装功能模块

功能模块是独立的 Git 仓库，安装到 `.claude/skills/`：

```bash
# 合同审核（contract-review — 核心模块）
git clone https://github.com/lukeruc/contract-review.git .claude/skills/contract-review

# 合同分析（contract-analyze）
git clone https://github.com/lukeruc/contract-analyze.git .claude/skills/contract-analyze

# 审核规则生成（rule-builder）
git clone https://github.com/lukeruc/rule-builder.git .claude/skills/rule-builder
```

工具 skill（mdconverter、yd-law、qcc）同理。

模块只依赖路径契约——不需要修改本工作区的任何文件。

---

## 架构设计

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
│  │  sessions/        稳定性契约             │ │
│  │  任务工作区       路径·字段·存在性        │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │      功能模块层（松耦合 · 独立发版）     │ │
│  │                                          │ │
│  │  contract-review   contract-analyze      │ │
│  │  rule-builder      [more coming...]      │ │
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

**设计原则：**

1. **基础设施定义物理定律。** 路径约定、字段格式、加载规则——所有模块遵守同一套物理定律。改基础设施影响所有模块，因此变更频率远低于模块。
2. **模块之间互不依赖。** contract-review 不知道 contract-analyze 的存在。每个模块只依赖基础设施。
3. **接口只有文件路径 + 字段名。** 不存在 API 调用、函数导入、RPC。模块声明"我需要 profiles 里的公司名、playbook/contracts/review/ 下的规则"，找不到就降级运行。

详细设计见 `docs/concept-design.md`。

---

## 依赖

### 必需的

- [Claude Code](https://claude.ai/code) — 运行时。所有功能跑在 Claude Code 之上。

### 功能模块（按需安装）

基础设施层是骨架，功能模块是肌肉。安装你需要的：

| 模块 | 用途 | 安装方式 |
|------|------|---------|
| contract-review | 合同审核 | `git clone` 到 `.claude/skills/` |
| contract-analyze | 合同结构分析 | 同上 |
| rule-builder | 审查规则生成 | 同上 |

### 工具（按需安装）

| 工具 | 用途 | 协议 |
|------|------|------|
| agentdocx | .docx 读写、修订模式、批注 | MCP server |
| mdconverter | PDF/DOCX/图片 → Markdown | Claude Code skill |
| yd-law | 案例、法规检索 | Claude Code skill |
| qcc | 企业工商信息查询 | Claude Code skill |

工具 skill 同样安装到 `.claude/skills/`，agentdocx 通过 MCP 协议连接。

---

## 开发

本仓库包含基础设施层和模块开发副本。功能模块成熟后提取为独立仓库。`coldstart/` 是发行物——用户只关心这个目录。`CLAUDE.md` 在本仓库存在但不进入发行物（发行物使用 `coldstart/CLAUDE.md`）。

## License

MIT
