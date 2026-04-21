# AI 早报 2026-03-18

## 概览

### 要闻

#### 模型发布

1. **OpenAI 发布 GPT-5.4 mini 与 GPT-5.4 nano 模型**

OpenAI 正式发布了 GPT-5.4 mini 和 GPT-5.4 nano 两款轻量级模型，旨在为高并发工作负载与 Subagent 工作流提供更高效、低延迟的解决方案。

GPT-5.4 mini 在编码、多模态理解、工具调用及计算机操控能力上显著优于上一代 GPT-5 mini，运行速度提升超过 2 倍，并在 SWE-Bench Pro 和 OSWorld-Verified 等基准测试中逼近旗舰模型 GPT-5.4 的性能。目前已在 API、Codex 和 ChatGPT 平台上线，API 端输入输出价格分别为每百万 Token 0.75 美元和 4.50 美元。

GPT-5.4 nano 则是 GPT-5.4 系列中体积最小、成本最低的版本，专注于处理分类、数据提取及简单的编码子任务，目前仅通过 API 提供服务，价格为每百万 Token 输入 0.20 美元、输出 1.25 美元。

2. **H Company 联合 NVIDIA 发布 Holotron-12B 模型**

H Company 与 NVIDIA 联合发布开源多模态模型 Holotron-12B，旨在作为计算机使用 Agent 的模型。该模型基于 Nemotron-Nano-12B-v2-VL 后训练，采用混合 SSM-Attention 架构，解决 KV Cache 瓶颈。

3. **英伟达推出 120 亿参数 Nemotron 3 VoiceChat 语音模型**

NVIDIA 宣布推出 Nemotron 3 VoiceChat 抢先体验计划，这是一个拥有 120 亿（12B）参数的端到端实时全双工语音转语音模型。

该模型采用混合 Mamba/Transformer 架构，结合了快速 Conformer 语音编码器、Nemotron Nano V2 9B LLM 骨干网络以及 NVIDIA TTS 解码器，支持基于 NVIDIA PersonaPlex 的文本角色提示来控制 Agent 人设。

目前，合格开发者可以通过 NGC 获取该模型、参考部署容器及微调指南，用于评估和构建特定领域的全双工语音 Agent。

4. **Meta 发布 OMT 系统，支持 1600 多种语言**

Meta 发布 Omnilingual Machine Translation (OMT) 系统，支持语言扩展至 1600 多种，旨在突破大模型低资源语言生成瓶颈。该系统整合公共语料与 MeDLEY 等新数据集，探索 OMT-LLaMA 与 OMT-NLLB 两种架构。

据官方数据，其 1B 至 8B 参数模型翻译性能匹配甚至超越 70B 参数 LLM 基准，具备低算力优势。Meta 构建了包含 BLASER 3、OmniTOX 及最大规模多语言评估集 BOUQuET 在内的评估体系，并将排行榜及评估数据集免费开放。

5. **乐天发布 Rakuten AI 3.0，基于 DeepSeek V3**

乐天集团发布日语优化开源模型 Rakuten AI 3.0，属 "GENIAC" 项目。该模型采用 MoE 架构，拥有 6710 亿总参数和 370 亿激活参数，支持 128K 上下文。官方称其在日语文化测试中优于 GPT-4o，基于开源模型与自有数据研发。

然而，据媒体及社区发现，该模型配置文件含 deepseek_v3 标识。社区指控其删除了 DeepSeek 许可证文件，引发关于架构来源及自主研发程度的争议。

#### 开发生态

6. **Hermes Agent 发布 v0.3.0，引入插件架构**

Nous Research 正式发布 Hermes Agent v0.3.0。核心更新为引入一等公民级别插件架构，允许开发者打包分享工具无需修改核心库。

此外，Hermes Agent v0.3.0 还集成了通过 CDP 连接实时 Chrome 浏览器的自动化功能、基于本地 Whisper 的语音模式以及全局 PII 脱敏技术。并实现了跨 CLI 及所有平台的实时流式传输。

7. **Mistral AI 推出 Forge，支持企业从头训练 AI 模型**

Mistral AI 近日推出企业级系统 Forge，支持企业基于专有知识从头训练前沿 AI 模型。该平台涵盖预训练、后训练及强化学习全阶段，提供 Dense 和 MoE 架构及多模态输入支持，采用 Agent-first 设计理念以提升决策可靠性。

ASML、Ericsson 及欧洲航天局等已成为早期合作伙伴。

8. **Ollama 发布 0.18.1 版本，新增 Web 搜索功能**

Ollama 官方正式发布 0.18.1 版本。该版本为 OpenClaw 引入原生 Web 搜索与获取插件，支持本地或云端模型搜索最新网络内容及抓取网页可读内容。

此外，更新为 ollama launch 命令新增非交互式模式，旨在适配 Docker 容器、CI/CD 流水线及脚本自动化任务。

9. **LangChain 发布 Open SWE 开源框架**

LangChain 正式发布开源框架 Open SWE，专为构建内部编码 Agent 设计。该框架基于 Deep Agents 架构，灵感源于 Stripe、Ramp 和 Coinbase 等团队的技术实践。

核心组件包括隔离云沙盒、AGENTS.md 上下文机制及子代理编排系统。其支持通过 Slack、Linear 和 GitHub 触发任务，采用 MIT 许可证，具备高度模块化特性。目前项目已上线 GitHub，提供部署指南。

10. **Unsloth AI 发布 Unsloth Studio，开源本地训练工具显存降低百分之七十**

Unsloth AI 宣布推出 Unsloth Studio (Beta)，这是一个开源的本地 Web UI 界面，旨在为开发者和 AI 专业人士提供统一的工具，用于本地训练、运行和导出各种开放模型。

该工具支持在 Mac、Windows 和 Linux 上本地运行 GGUF 和 safetensors 模型。其核心采用了基于 OpenAI Triton 语言编写的定制化反向传播内核，使 500 多种模型的训练速度提升 2 倍，同时减少 70% 的 VRAM 占用且不损失精度。

11. **Box 推出官方 CLI 支持智能体调用云文件系统工具**

Aaron Levie 宣布推出官方 Box CLI，旨在将 Box 转化为 Agent 专属的完整云文件系统。该工具支持通过 Claude Code、Codex、Perplexity Computer 和 OpenClaw 等平台进行调用，现已面向所有用户开放。其中包括拥有 10GB 免费存储额度的免费用户群体，均可使用该功能。

开发者及用户可以通过执行 npm install --global @box/cli 命令全局安装该工具。

#### 产品应用

12. **OpenAI 简化 ChatGPT 模型选择，优化配置并修复 5.3 问题**

OpenAI 官方宣布简化 ChatGPT 模型选择器，重组为 Instant、Thinking 和 Pro 三类，对应日常快速、复杂深度及最先进推理能力，供 Plus 及以上账户使用。

该更新优化了 Configure 菜单，支持自动切换和思考力度设置，并简化了重试菜单。个性化方面，官方正逐步淘汰 Nerdy 基础风格，原用户将被迁移至默认个性设置。

此外，据 OpenAI 工程师 Mich Pokrass 透露，其团队已修复 5.3 instant 模型中存在的"标题党"倾向问题，承诺将继续消除此类行为。

13. **Claude Cowork 推出新特性 Dispatch 支持手机远程调度**

Claude Cowork 推出新特性 Dispatch，现处于研究预览阶段。该功能建立本地持久化对话，用户可手机远程发指令，电脑端查看成果。

官方称其依托 Cowork 架构，代码在本地沙箱运行且文件留存，操作前需用户批准。使用时需下载 Claude Desktop 并配对手机，电脑须保持运行。目前向 Max 订阅者开放，预计未来几天扩展至 Pro 用户。

14. **谷歌扩展 Personal Intelligence 功能至美国免费用户**

Google 宣布在美国扩展 Personal Intelligence 功能，覆盖 AI Mode in Search、Gemini app 及 Chrome 的免费用户。该功能允许用户主动连接 Gmail、Google Photos 等数据，提供高度定制化响应。

该功能默认关闭，需用户显式选择加入，仅限个人账号。

15. **Perplexity 发布 Comet Enterprise 浏览器**

Perplexity 正式发布 Comet Enterprise，官方称其为目前最强大的 AI 浏览器，面向企业团队。该产品集研究、任务自动化与办公于一体，基于 Perplexity 安全基础设施构建。

管理员可通过 MDM 工具部署至数千台设备，并提供遥测数据和审计日志。其企业版集成 CrowdStrike Falcon 平台，拦截可疑文件以防钓鱼和恶意软件。Fortune、AWS 等知名企业已投入使用。

16. **腾讯 ima 上线 ima skills，支持笔记读写检索**

腾讯 IMA 正式上线 IMA Skills，并邀请用户抢先体验。

根据官方介绍，该功能支持对笔记内容的读取、写入和检索操作。其支持 OpenClaw、OpenClaw 内网版及 WorkBuddy 等平台。

用户需获取 API Key，配置给模型部署的 skill，即可让 AI 助手"小龙虾"实现随时记录与查询笔记，或结合其他 skill 使用。

17. **阿里巴巴发布企业级 AI 原生工作平台悟空，内置钉钉**

阿里巴巴正式发布全球首个企业级 AI 原生工作平台"悟空"，定位为让企业拥有全天候 "AI Agent 军团"。该产品作为独立应用开启邀测，并将内置于钉钉，支持连接企业账号及系统。

官方称，其内置企业级运行环境，Agent 自动继承权限规则，操作均在安全沙箱中运行，Token 消耗透明。

18. **Gamma 发布最大规模更新，推出 AI 原生视觉创作工具**

Gamma 宣布推出"有史以来最大规模"更新，核心包含 AI 原生视觉工具 Gamma Imagine、重构模板及 Gamma Connectors。官方称，此举旨在消除知识工作者"设计税"。

Gamma Imagine 支持通过提示词生成海报、Logo 等品牌资产，新模板允许通过提示词修改整套演示文稿。

#### 技术与洞察

19. **Google DeepMind 发布 AGI 评估框架，联合 Kaggle 启动黑客松**

Google DeepMind 发布 AGI 进展认知框架，并联合 Kaggle 启动黑客马拉松。该框架基于心理学和神经科学，定义感知、生成、注意等 10 项关键认知能力，提出三阶段评估协议，通过人类基线对比衡量 AI 性能。

针对学习、元认知等五个评估差距最大领域，官方邀请社区构建基准测试。活动总奖金池为 20 万美元，设赛道奖及整体大奖。

#### 行业动态

20. **OpenAI 联手 AWS 签约五角大楼，战略调整削减 Sora 投入**

据 The Information 报道，OpenAI 与 AWS 签署协议，利用 AWS 云设施向包括五角大楼的美国政府机构提供涉密及非涉密 AI 工具。

另据《华尔街日报》，OpenAI 正进行战略转型，拟削减 Sora 及硬件等投入，聚焦编码工具和商业用户，以巩固核心业务。

21. **微软 AI 重组架构，计划在未来五年内构建世界级的 SOTA 模型**

Microsoft AI 日前宣布重大组织架构调整，CEO Mustafa Suleyman 将把工作重心全面转向 Superintelligence 研发，计划在未来五年内构建世界级的 SOTA 模型，以支持企业级调优谱系并提升大规模 AI 工作负载的 COGS 效率。

与此同时，Microsoft AI 正在统一 Copilot 的消费者与商业业务，将其合并为单一组织，并任命 Jacob Andreou 为新负责人。

22. **Linux 基金会获 Anthropic 等 1250 万美元开源安全资助**

Linux 基金会宣布获得来自 Anthropic、Amazon Web Services、GitHub、Google、Google DeepMind、Microsoft 和 OpenAI 等多家领先组织的 1250 万美元资助。该资金旨在通过 Alpha Omega 和 OpenSSF 推进开源软件的可持续安全解决方案。

23. **阶跃星辰 Step 3.5 Flash 接入吉利超级 Eva 上线极氪 8X**

阶跃星辰宣布 Step 3.5 Flash 模型接入吉利整车智能体超级 Eva，首发搭载于极氪 8X。该智能体由阶跃星辰、吉利及千里科技共同研发，以 Step 3.5 Flash 为核心驱动大脑，实现大模型与智驾、底盘等底层系统原生融合。

#### 前瞻与传闻

24. **小米 OpenRouter 隐形模型确认为 MiMo V2**

据 GitHub 代码记录显示，OpenRouter 平台隐形模型 Hunter Alpha 与 Healer Alpha 实为小米 MiMo V2 系列。

Hunter Alpha 对应 MiMo V2 Pro，支持 1M 上下文及 32000 最大 Token 输出，仅限文本推理。Healer Alpha 对应 MiMo V2 Omni，支持文本与图像推理，上下文为 262K。

#### Claw 专题

25. **MiniMax 推出 MaxClaw team，支持多 Agent 协作体系**

MiniMax 正式推出 "MaxClaw team" 新功能，标志着其服务从"一人一只龙虾"的单 Agent 模式演进为多 Agent 协作体系。可实现 24/7 全天候运行且无需人工持续看管。目前，该功能仅对订阅个人计划中 Pro 级别及以上的用户开放使用。

26. **讯飞推出 Loomy 桌面助理，采用目录级隔离安全机制**

讯飞正式推出基于 AstronClaw 打造的桌面级智能助理 Loomy，定位为"人人可用的桌面版 OpenClaw"。该产品主打零配置，用户授权后最快 1 分钟启动。其采用目录级隔离机制，仅访问授权目录以降低数据泄露风险。

---

**来源**: 橘鸦Juya
**日期**: 2026年3月18日
**链接**: https://mp.weixin.qq.com/s/kZVwZGJGeBQ9NtHjy31knQ
