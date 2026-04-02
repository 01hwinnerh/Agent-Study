# 🤖 Agent 技能与工具报告 (Skills & Tools Report)

## 1. Skill (技能) 与 Tool (工具) 的核心区别

### 什么是 Tool (工具)？
Tool 是 Agent 能够执行的**底层原子操作**，它们就像是我的“手和脚”。
- **定位**：功能性接口、系统级能力。
- **特点**：通用、无状态、不包含业务逻辑。
- **示例**：`Read`（读取文件）、`Write`（写入文件）、`RunCommand`（执行终端命令）、`WebSearch`（联网搜索）、`Grep`（代码搜索）。
- **使用场景**：当需要与操作系统、文件系统、网络进行基础交互时。

### 什么是 Skill (技能)？
Skill 是建立在 Tool 之上的**领域专家模式**和**专业工作流**，它们就像是我大脑中加载的“专业知识芯片”。
- **定位**：专业认知框架、行业最佳实践、特定领域的代码/设计规范。
- **特点**：包含强业务约束、特定的提示词扩展、特定场景的高级指南。
- **机制**：当调用一个 Skill 时，实际上是向当前会话注入了该领域详尽的指导手册和上下文。这改变了我的“思考方式”，让我不再是用通用逻辑写代码，而是以该领域专家的身份进行工作。
- **使用场景**：当面对具有特定专业要求的任务时（如高水准的 UI 设计、专业的数据分析、深度的代码安全审查等）。

---

## 2. 当前可用 Skill 详细报告 (Available Skills)

根据能力类型，我将现有的 40+ 种 Skills 划分为以下几个主要类别：

### 🛠️ 1. 开发与架构类 (Development & Architecture)
*(用于提升代码质量、规范和开发效率)*

| 技能名称 (Skill) | 作用 (What it does) | 触发时机 (When to use) |
| :--- | :--- | :--- |
| **`test-driven-development`** | 测试驱动开发 (TDD) 指南 | 在实现任何新功能或修复 Bug 之前，指导先写测试再写实现代码。 |
| **`security-best-practices`** | 安全最佳实践代码审查 | 当明确要求进行安全审查，或需要确保 Python/JS/Go 代码安全时。 |
| **`vercel-react-best-practices`** | Vercel 的 React/Next.js 性能优化指南 | 编写、审查或重构 React/Next.js 代码，追求极致性能时。 |
| **`vercel-composition-patterns`** | React 高级组件组合模式指南 | 当重构臃肿的组件（布尔属性泛滥）、构建组件库或设计可复用 API 时。 |
| **`vercel-react-native-skills`** | React Native 与 Expo 移动端最佳实践 | 开发移动端 App，优化列表性能或处理原生平台 API 时。 |
| **`redis-development`** | Redis 性能优化与最佳实践 | 涉及 Redis 数据结构、向量搜索 (RedisVL)、缓存架构优化时。 |
| **`web-artifacts-builder`** | 复杂多组件 Web 制品构建 | 构建包含状态管理、路由或复杂 Shadcn UI 的大型 Web 产出物时。 |

### 🎨 2. 设计与前端界面类 (Design & UI/Frontend)
*(用于生成高质量、非 AI 感的视觉界面)*

| 技能名称 (Skill) | 作用 (What it does) | 触发时机 (When to use) |
| :--- | :--- | :--- |
| **`frontend-design`** | 生产级前端界面设计 | 构建高设计质量的 Web 组件、页面、看板，拒绝通用 AI 审美。 |
| **`frontend-skill`** | 视觉强化的落地页设计指南 | 需要视觉冲击力强的落地页、网站或原型时，强调排版与品牌感。 |
| **`web-dev`** | 从零构建现代 Web 应用 | 从头开始（From scratch）构建新网站、网页或 Web 游戏时。 |
| **`shadcn`** | Shadcn UI 组件管理 | 在项目中添加、搜索、调试、应用 `--preset` 或组合 shadcn 组件时。 |
| **`web-design-guidelines`** | Web 界面设计规范审计 | 当被要求“审查我的 UI”、“检查无障碍性”或对照最佳实践审计时。 |
| **`brand-guidelines`** | 官方品牌视觉规范应用 | 当需要为任何产出物应用 Anthropic 官方品牌色彩、排版和设计标准时。 |

### 🤖 3. 自动化与测试类 (Automation & Testing)
*(用于模拟用户操作或自动化系统流程)*

| 技能名称 (Skill) | 作用 (What it does) | 触发时机 (When to use) |
| :--- | :--- | :--- |
| **`agent-browser`** | 强大的浏览器自动化 CLI | 任何需要与网页交互的任务（如登录、填表、爬取数据、截图、点击按钮）。 |
| **`webapp-testing`** | 基于 Playwright 的本地 Web 测试 | 测试本地 Web 应用、调试 UI 行为或捕获浏览器日志与截图。 |
| **`dogfood`** | 探索性 QA 测试与 Bug 追踪 | 当被要求对应用进行 "dogfood"、"找 Bug" 或系统性功能审查时。 |
| **`electron`** | 桌面端 Electron 应用自动化 | 需要通过 Chrome 协议控制 VS Code、Slack、Discord 等桌面端应用时。 |

### 📊 4. 数据、分析与研究类 (Data, Analysis & Research)
*(用于处理数据、生成图表和专业报告)*

| 技能名称 (Skill) | 作用 (What it does) | 触发时机 (When to use) |
| :--- | :--- | :--- |
| **`data-analysis`** | 结构化数据分析工具 | 用户上传 Excel/CSV 并需要统计、透视表、SQL 查询或导出 Markdown 时。 |
| **`chart-visualization`** | 数据图表可视化生成 | 需要将数据转换为图表图像（从 26 种类型中智能选择并生成 JS 脚本）时。 |
| **`consulting-analysis`** | 咨询级别的专业报告生成 | 撰写市场分析、消费者洞察、财务分析等具有完整骨架的咨询级研究报告。 |
| **`hook-analyzer`** | 视频前三秒“钩子”分析 | 需要提取分镜数据并对视频的前三秒吸引力进行结构化评估时。 |
| **`report-generator`** | 视频分析报告生成器 | 整合分镜拆解和钩子分析，生成包含 BGM、场景分析的完整 Markdown 报告。 |

### 📝 5. 规划、文档与协作类 (Planning, Docs & Productivity)
*(用于项目管理、知识沉淀和规范化写作)*

| 技能名称 (Skill) | 作用 (What it does) | 触发时机 (When to use) |
| :--- | :--- | :--- |
| **`brainstorming`** | 创意探索与需求澄清工作流 | 在任何创造性工作（写代码、加功能）之前，深入探索用户意图。 |
| **`writing-plans`** | 多步骤任务的规格说明编写 | 在实际写代码之前，为复杂任务编写架构设计、需求规格。 |
| **`executing-plans`** | 执行已写好的实施计划 | 当有现成的实施计划，需要在独立会话中分步骤执行并设立审查点时。 |
| **`doc-coauthoring`** | 结构化文档共同创作 | 编写技术规范、提案、决策文档时，用于转移上下文、迭代并验证内容。 |
| **`internal-comms`** | 内部沟通文案指南 | 撰写状态报告、领导层更新、内部新闻通讯、FAQ 或事故报告时。 |
| **`notion-*` (系列)** | Notion 生态集成套件 | 包括 CLI交互(`notion-cli`)、对话转知识库(`notion-knowledge-capture`)、会议文档准备(`notion-meeting-intelligence`)、跨页面研究整合(`notion-research-documentation`)、需求转任务(`notion-spec-to-implementation`)。 |
| **`obsidian-*` (系列)** | Obsidian 笔记生态套件 | 包括 CLI控制库操作(`obsidian-cli`)、特殊 Markdown 语法编辑(`obsidian-markdown`)、数据库视图处理(`obsidian-bases`)。 |

### 🎨 6. 创意艺术与多媒体 (Creative Arts & Media)
*(用于生成图像、视频、PPT和视觉资产)*

| 技能名称 (Skill) | 作用 (What it does) | 触发时机 (When to use) |
| :--- | :--- | :--- |
| **`byted-seedream-image-generate`** | 豆包高质量 AI 图像生成 | 用户通过文本描述需要生成多种艺术风格的图片、视觉内容时。 |
| **`byted-seedance-video-generate`** | 豆包 AI 视频生成 | 用户需要从文本提示、图像或参考材料创建生成式视频时。 |
| **`algorithmic-art`** | 算法生成艺术 (p5.js) | 用户要求使用代码生成原创艺术、流场、生成式艺术或粒子系统时。 |
| **`canvas-design`** | 静态海报与视觉排版设计 | 用户要求制作带有设计哲学的 PDF/PNG 海报、传单或静态视觉作品时。 |
| **`slides`** | PowerPoint (PPTX) 生成与编辑 | 需要从零构建 PPT、还原参考幻灯片、添加图表或诊断溢出重叠问题时。 |
| **`theme-factory`** | 产出物主题样式工厂 | 为幻灯片、文档、HTML网页等产出物应用 10 种预设色彩/字体主题时。 |

### 🛠 7. 外部工具与集成库 (External Integrations & Utilities)

| 技能名称 (Skill) | 作用 (What it does) | 触发时机 (When to use) |
| :--- | :--- | :--- |
| **`gh-cli`** | GitHub CLI 综合参考库 | 命令行操作 Issue、PR、Actions、Releases 等所有 GitHub 资源时。 |
| **`git-commit`** | 智能 Git 提交助手 | 分析差异并自动生成符合 Conventional Commits 规范的提交信息。 |
| **`mcp-builder`** | MCP 服务构建指南 | 使用 Python (FastMCP) 或 TS 构建高品质的 MCP 服务器接入外部 API 时。 |
| **`defuddle`** | 网页正文纯净化提取 (Defuddle) | 提供 URL 时，用于去除网页杂乱内容/导航，提取干净的 Markdown 以节省 Token。 |
| **`screenshot`** | 操作系统级屏幕截图 | 明确要求对系统全屏、特定 APP 窗口或特定像素区域进行截图时。 |
| **`json-canvas`** | JSON Canvas 节点图构建 | 创建或编辑具有节点连线的 `.canvas` 文件（如思维导图、流程图）时。 |
| **`figma`** | Figma 设计稿深度解析 | 获取 Figma 设计上下文、节点 ID、变量或实现“设计稿转生产代码”时。 |

---

### 💡 核心总结
- **Tool (工具)** 决定了我 **“能操作什么”**（如读写文件、跑命令）。
- **Skill (技能)** 决定了我 **“能做到多专业”**（如成为前端大牛、专业数据分析师或PPT排版专家）。
通过在恰当的时机加载合适的 Skill，我能够跳出通用的 AI 问答模式，提供真正符合行业标准的专业级输出。