# AI Daily Brief

<p align="center">
  <strong>An automated AI news aggregation & briefing generator</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/RSS-20%2B%20Sources-orange.svg" alt="Sources">
  <img src="https://img.shields.io/badge/ArXiv-Integrated-purple.svg" alt="ArXiv">
  <img src="https://img.shields.io/badge/Output-Markdown%20%7C%20Console-cyan.svg" alt="Output">
</p>

<p align="center">
  <a href="#-features">Features</a> &bull;
  <a href="#-quick-start">Quick Start</a> &bull;
  <a href="#-configuration">Configuration</a> &bull;
  <a href="#-architecture">Architecture</a> &bull;
  <a href="#-sample-output">Sample Output</a> &bull;
  <a href="#中文文档">中文文档</a>
</p>

---

## Features

- **Multi-source Aggregation** — Fetch from 20+ RSS feeds, web pages, and ArXiv papers in a single run
- **Smart Filtering** — Keyword-based include/exclude rules to surface only relevant AI news
- **Auto Deduplication** — URL-level dedup across all sources
- **Flexible Output** — Generate Markdown files or print to console
- **Schedulable** — Designed for cron / CI integration; zero-downtime daily runs
- **Configurable** — YAML-driven source list and keyword rules; add or remove sources without code changes

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/ai-report.git
cd ai-report

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate today's briefing
python src/main.py
```

The briefing will be saved to `output/AI简报_YYYYMMDD.md`.

### CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `-d, --days N` | Fetch news from the last N days | `1` |
| `-o, --output PATH` | Custom output file path | `output/` |
| `-f, --format` | Output format: `markdown` or `console` | `markdown` |
| `--web` | Enable web scraping (slower) | off |
| `--no-arxiv` | Skip ArXiv papers | off |
| `-c, --config PATH` | Custom config file | `config/sources.yaml` |
| `-v, --verbose` | Debug-level logging | off |

### Examples

```bash
# 3-day briefing with web scraping
python src/main.py --days 3 --web

# Console output only (no file)
python src/main.py --format console

# Custom config and output
python src/main.py -c my_sources.yaml -o ~/briefing.md
```

### Cron Scheduling

```bash
# Run daily at 08:00
crontab -e
# Add:
0 8 * * * cd /path/to/ai-report && python src/main.py >> log.txt 2>&1
```

## Configuration

Edit `config/sources.yaml` to customize sources and filters.

### Adding an RSS Source

```yaml
rss_sources:
  - name: "My AI Blog"
    url: "https://example.com/feed.xml"
    category: "Company Name"
    language: "en"   # en | zh
```

### Adding a Web Source

```yaml
web_sources:
  - name: "Some AI News"
    url: "https://example.com/news"
    category: "Category"
    language: "zh"
```

### Keyword Filtering

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

## Architecture

```
ai-report/
├── src/
│   ├── main.py                 # Entry point & CLI
│   ├── fetchers/
│   │   ├── rss_fetcher.py      # RSS feed parser (feedparser)
│   │   └── web_fetcher.py      # Web scraper (requests + BS4) & ArXiv API
│   └── formatters/
│       └── markdown.py         # Markdown & console formatters
├── config/
│   └── sources.yaml            # Source list & keyword rules
├── output/                     # Generated briefings
├── docs/
│   └── examples/               # Sample output
├── requirements.txt
├── LICENSE
└── README.md
```

### Data Flow

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  RSS Feeds  │   │ Web Pages   │   │   ArXiv     │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       └────────────┬────┘─────────────────┘
                    │
            ┌───────▼───────┐
            │   Deduplicate │
            │  (by URL)     │
            └───────┬───────┘
                    │
            ┌───────▼───────┐
            │ Keyword Filter│
            └───────┬───────┘
                    │
          ┌─────────▼─────────┐
          │   Formatter       │
          │ (Markdown/Console)│
          └─────────┬─────────┘
                    │
            ┌───────▼───────┐
            │  Output File  │
            └───────────────┘
```

## Covered Sources

### Official Blogs (RSS)
OpenAI, Google AI, Meta AI, Microsoft AI, Microsoft Research, NVIDIA, Mistral AI, Hugging Face

### Web Sources
Anthropic, xAI, Google DeepMind, Apple ML, DeepSeek, Zhipu AI, Tongyi Qianwen, Kimi (Moonshot), MiniMax, GitHub Trending AI, LM Arena, Hugging Face Trending

### Academic
ArXiv CS.AI (latest submissions)

## Sample Output

See [`docs/examples/`](docs/examples/) for a full sample briefing.

Excerpt:

> **OpenAI 发布 GPT-5.4 mini 与 GPT-5.4 nano 模型**
>
> GPT-5.4 mini 在编码、多模态理解、工具调用及计算机操控能力上显著优于上一代 GPT-5 mini，运行速度提升超过 2 倍...

## Tech Stack

| Component | Technology |
|-----------|-----------|
| RSS Parsing | [feedparser](https://github.com/kurtmckee/feedparser) |
| Web Scraping | [requests](https://docs.python-requests.org/) + [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) |
| HTML Parsing | [lxml](https://lxml.de/) |
| Config | [PyYAML](https://pyyaml.org/) |
| ArXiv API | Atom feed via `xml.etree` |

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes (`git commit -m 'feat: add ...'`)
4. Push to the branch (`git push origin feat/my-feature`)
5. Open a Pull Request

## License

[MIT](LICENSE)

---

## 中文文档

每天自动抓取 AI 相关资讯并生成 Markdown 简报。支持 RSS、网页抓取和 ArXiv 论文获取，内置关键词过滤和自动去重。

### 功能特性

- 支持 20+ RSS 源和网页源
- 自动去重和关键词过滤
- 输出 Markdown 文件或控制台打印
- YAML 配置驱动，无需改代码即可增减源
- 适配 cron 定时任务

### 快速开始

```bash
pip install -r requirements.txt
python src/main.py
```

### 注意事项

1. 部分网站有反爬措施，网页抓取可能不稳定，建议优先使用 RSS 源
2. 首次运行可能需要较长时间（需逐个拉取源）
3. 建议配置 cron 定时执行，每日自动生成简报
