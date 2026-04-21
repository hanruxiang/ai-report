#!/usr/bin/env python3
"""
AI资讯简报生成器
每天自动抓取AI相关资讯并生成简报
"""
import os
import sys
import argparse
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fetchers.rss_fetcher import RSSFetcher
from fetchers.web_fetcher import WebFetcher, ArxivFetcher
from formatters.markdown import MarkdownFormatter, ConsoleFormatter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AIReportGenerator:
    """AI资讯报告生成器"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or PROJECT_ROOT / "config" / "sources.yaml"

        # 加载配置
        self.config = self._load_config()

        # 初始化抓取器
        self.rss_fetcher = RSSFetcher()
        self.web_fetcher = WebFetcher()
        self.arxiv_fetcher = ArxivFetcher()

        # 初始化格式化器
        self.markdown_formatter = MarkdownFormatter()
        self.console_formatter = ConsoleFormatter()

    def _load_config(self) -> dict:
        """加载配置文件"""
        import yaml

        if not os.path.exists(self.config_path):
            logger.warning(f"配置文件不存在: {self.config_path}，使用默认配置")
            return {
                "rss_sources": [],
                "web_sources": [],
                "keywords": {"include": [], "exclude": []}
            }

        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def fetch_all(self, days: int = 1, use_web: bool = False, use_arxiv: bool = True) -> list:
        """
        获取所有资讯

        Args:
            days: 获取最近几天的资讯
            use_web: 是否使用网页抓取
            use_arxiv: 是否获取ArXiv论文

        Returns:
            资讯列表
        """
        all_items = []
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        # 1. RSS源
        logger.info("=== 开始获取RSS源 ===")
        rss_sources = self.config.get("rss_sources", [])
        if rss_sources:
            rss_items = self.rss_fetcher.fetch_multiple(rss_sources, max_items_per_source=15)
            # 过滤时间
            rss_items = [
                item for item in rss_items
                if not item.get("published") or item["published"] > cutoff_date
            ]
            all_items.extend(rss_items)
            logger.info(f"RSS源获取 {len(rss_items)} 条资讯")

        # 2. 网页源
        if use_web:
            logger.info("=== 开始抓取网页源 ===")
            web_sources = self.config.get("web_sources", [])
            if web_sources:
                web_items = self.web_fetcher.fetch_multiple(web_sources)
                all_items.extend(web_items)
                logger.info(f"网页源获取 {len(web_items)} 条资讯")

        # 3. ArXiv论文
        if use_arxiv:
            logger.info("=== 开始获取ArXiv论文 ===")
            arxiv_items = self.arxiv_fetcher.fetch_recent_ai_papers(max_results=10)
            all_items.extend(arxiv_items)

        # 去重（基于URL）
        all_items = self._deduplicate(all_items)

        # 关键词过滤
        all_items = self._filter_by_keywords(all_items)

        logger.info(f"总共获取 {len(all_items)} 条资讯")
        return all_items

    def _deduplicate(self, items: list) -> list:
        """根据URL去重"""
        seen_urls = set()
        unique_items = []

        for item in items:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_items.append(item)
            elif not url:
                # 没有URL的也保留
                unique_items.append(item)

        removed = len(items) - len(unique_items)
        if removed > 0:
            logger.info(f"去重: 移除 {removed} 条重复资讯")

        return unique_items

    def _filter_by_keywords(self, items: list) -> list:
        """根据关键词过滤"""
        keywords_config = self.config.get("keywords", {})
        include_keywords = keywords_config.get("include", [])
        exclude_keywords = keywords_config.get("exclude", [])

        if not include_keywords and not exclude_keywords:
            return items

        filtered_items = []

        for item in items:
            text = (
                item.get("title", "") + " " +
                item.get("description", "") + " " +
                item.get("source", "")
            ).lower()

            # 检查排除关键词
            if exclude_keywords:
                if any(kw.lower() in text for kw in exclude_keywords):
                    continue

            # 检查包含关键词
            if include_keywords:
                if any(kw.lower() in text for kw in include_keywords):
                    filtered_items.append(item)
            else:
                filtered_items.append(item)

        logger.info(f"关键词过滤: {len(items)} -> {len(filtered_items)} 条")
        return filtered_items

    def generate(self, output_path: str = None, format: str = "markdown", **kwargs) -> str:
        """
        生成报告

        Args:
            output_path: 输出文件路径
            format: 输出格式 (markdown/console)
            **kwargs: 传递给fetch_all的参数

        Returns:
            报告内容
        """
        logger.info("开始生成AI资讯简报...")

        # 获取资讯
        items = self.fetch_all(**kwargs)

        if not items:
            logger.warning("没有获取到任何资讯")
            return ""

        # 格式化输出
        if format == "markdown":
            content = self.markdown_formatter.format(items)

            # 保存到文件
            if not output_path:
                output_path = PROJECT_ROOT / "output" / f"AI简报_{datetime.now().strftime('%Y%m%d')}.md"

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            self.markdown_formatter.save(items, output_path)
            logger.info(f"报告已保存到: {output_path}")

        else:
            content = self.console_formatter.format(items)

        return content


def main():
    parser = argparse.ArgumentParser(description="AI资讯简报生成器")
    parser.add_argument(
        "--days", "-d", type=int, default=1,
        help="获取最近几天的资讯 (默认: 1)"
    )
    parser.add_argument(
        "--output", "-o", type=str,
        help="输出文件路径"
    )
    parser.add_argument(
        "--format", "-f", choices=["markdown", "console"], default="markdown",
        help="输出格式 (默认: markdown)"
    )
    parser.add_argument(
        "--web", action="store_true",
        help="启用网页抓取（较慢）"
    )
    parser.add_argument(
        "--no-arxiv", action="store_true",
        help="不获取ArXiv论文"
    )
    parser.add_argument(
        "--config", "-c", type=str,
        help="配置文件路径"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="详细输出"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 生成报告
    generator = AIReportGenerator(config_path=args.config)

    try:
        content = generator.generate(
            output_path=args.output,
            format=args.format,
            days=args.days,
            use_web=args.web,
            use_arxiv=not args.no_arxiv
        )

        # 如果是控制台输出，打印内容
        if args.format == "console":
            print("\n" + content)

        logger.info("✅ 简报生成完成!")
        return 0

    except Exception as e:
        logger.error(f"❌ 生成失败: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
