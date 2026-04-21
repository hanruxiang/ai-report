<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/RSS-20%2B%20Sources-orange.svg" alt="Sources">
  <img src="https://img.shields.io/badge/ArXiv-Integrated-purple.svg" alt="ArXiv">
  <img src="https://img.shields.io/badge/Output-Markdown%20%7C%20Console-cyan.svg" alt="Output">
</p>

<p align="center">
  <a href="README_EN.md">English</a> | <strong>中文</strong>
</p>

---

<h1 align="center">AI 资讯简报生成器</h1>

<p align="center">
  每天自动抓取 AI 领域最新资讯，一键生成结构化 Markdown 简报<br>
  <strong>覆盖 20+ 官方博客、科技媒体与学术论文源</strong>
</p>

---

## 功能特性

- **多源聚合** — 一键抓取 RSS 订阅、网页源和 ArXiv 论文
- **智能过滤** — 基于关键词的包含/排除规则，只保留你关心的 AI 资讯
- **自动去重** — URL 级别跨源去重，告别重复信息
- **灵活输出** — 生成 Markdown 文件或直接打印到终端
- **定时任务** — 天然适配 cron / CI，每日零干预运行
- **配置驱动** — YAML 配置源列表和过滤规则，增删资讯源无需改代码

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/hanruxiang/ai-report.git
cd ai-report

# 2. 安装依赖
pip install -r requirements.txt

# 3. 生成今日简报
python src/main.py
```

简报将保存到 `output/AI简报_YYYYMMDD.md`。

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-d, --days N` | 获取最近 N 天的资讯 | `1` |
| `-o, --output PATH` | 自定义输出路径 | `output/` |
| `-f, --format` | 输出格式：`markdown` 或 `console` | `markdown` |
| `--web` | 启用网页抓取（较慢） | 关闭 |
| `--no-arxiv` | 跳过 ArXiv 论文 | 关闭 |
| `-c, --config PATH` | 使用自定义配置文件 | `config/sources.yaml` |
| `-v, --verbose` | 开启调试日志 | 关闭 |

### 使用示例

```bash
# 获取最近 3 天的资讯，启用网页抓取
python src/main.py --days 3 --web

# 仅控制台输出
python src/main.py --format console

# 使用自定义配置和输出路径
python src/main.py -c my_sources.yaml -o ~/AI简报.md
```

### 定时任务

```bash
# 每天早上 8 点自动生成简报
crontab -e
# 添加以下行：
0 8 * * * cd /path/to/ai-report && python src/main.py >> log.txt 2>&1
```

## 配置说明

编辑 `config/sources.yaml` 自定义资讯源和过滤规则。

### 添加 RSS 源

```yaml
rss_sources:
  - name: "我的 AI 博客"
    url: "https://example.com/feed.xml"
    category: "公司名称"
    language: "zh"   # en | zh
```

### 添加网页源

```yaml
web_sources:
  - name: "某 AI 新闻"
    url: "https://example.com/news"
    category: "分类"
    language: "zh"
```

### 关键词过滤

```yaml
keywords:
  include:
    - "GPT"
    - "Claude"
    - "大模型"
  exclude:
    - "股价"
    - "财报"
```

## 项目结构

```
ai-report/
├── src/
│   ├── main.py                 # 主程序入口 & CLI
│   ├── fetchers/
│   │   ├── rss_fetcher.py      # RSS 抓取（feedparser）
│   │   └── web_fetcher.py      # 网页抓取（requests + BS4）& ArXiv API
│   └── formatters/
│       └── markdown.py         # Markdown & 终端格式化输出
├── config/
│   └── sources.yaml            # 资讯源配置 & 关键词规则
├── output/                     # 生成的简报文件
├── docs/
│   └── examples/               # 示例输出
├── requirements.txt
├── LICENSE
└── README.md
```

## 数据流

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  RSS 订阅源  │   │   网页源     │   │  ArXiv 论文  │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       └────────────┬────┘─────────────────┘
                    │
            ┌───────▼───────┐
            │   自动去重     │
            │  （按 URL）    │
            └───────┬───────┘
                    │
            ┌───────▼───────┐
            │  关键词过滤    │
            └───────┬───────┘
                    │
          ┌─────────▼─────────┐
          │   格式化输出       │
          │（Markdown/终端）   │
          └─────────┬─────────┘
                    │
            ┌───────▼───────┐
            │  简报文件      │
            └───────────────┘
```

## 覆盖资讯源

### 官方博客（RSS）
OpenAI、Google AI、Meta AI、Microsoft AI、Microsoft Research、NVIDIA、Mistral AI、Hugging Face

### 网页源
Anthropic、xAI、Google DeepMind、Apple ML、DeepSeek、智谱 AI、通义千问、Kimi（月之暗面）、MiniMax、GitHub Trending AI、LM Arena、Hugging Face Trending

### 学术论文
ArXiv CS.AI（最新提交）

## 示例输出

查看 [`docs/examples/`](docs/examples/) 获取完整示例简报。

摘录：

> **OpenAI 发布 GPT-5.4 mini 与 GPT-5.4 nano 模型**
>
> GPT-5.4 mini 在编码、多模态理解、工具调用及计算机操控能力上显著优于上一代 GPT-5 mini，运行速度提升超过 2 倍...

## 技术栈

| 组件 | 技术方案 |
|------|---------|
| RSS 解析 | [feedparser](https://github.com/kurtmckee/feedparser) |
| 网页抓取 | [requests](https://docs.python-requests.org/) + [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) |
| HTML 解析 | [lxml](https://lxml.de/) |
| 配置管理 | [PyYAML](https://pyyaml.org/) |
| ArXiv 接口 | Atom Feed + `xml.etree` |

## 参与贡献

欢迎提交贡献！

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feat/my-feature`）
3. 提交更改（`git commit -m 'feat: 添加 ...'`）
4. 推送到分支（`git push origin feat/my-feature`）
5. 发起 Pull Request

## 许可证

[MIT](LICENSE)
