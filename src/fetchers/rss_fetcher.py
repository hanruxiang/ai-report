"""
RSS资讯抓取模块
"""
import feedparser
import requests
from datetime import datetime, timezone
from typing import List, Dict, Optional
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSFetcher:
    """RSS源资讯抓取器"""

    def __init__(self, timeout: int = 10, user_agent: str = None):
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

    def fetch_feed(self, url: str, source_name: str = "", max_items: int = 20) -> List[Dict]:
        """
        从RSS源获取资讯

        Args:
            url: RSS feed URL
            source_name: 来源名称
            max_items: 最多获取条数

        Returns:
            资讯列表
        """
        try:
            logger.info(f"正在获取RSS: {source_name or url}")

            # 设置请求头
            headers = {"User-Agent": self.user_agent}

            # 解析RSS
            feed = feedparser.parse(url, request_headers=headers)

            if feed.bozo:
                logger.warning(f"RSS解析警告 {source_name}: {feed.bozo_exception}")

            items = []
            for entry in feed.entries[:max_items]:
                item = self._parse_entry(entry, source_name or feed.feed.get("title", ""))
                if item:
                    items.append(item)

            logger.info(f"从 {source_name} 获取 {len(items)} 条资讯")
            return items

        except Exception as e:
            logger.error(f"获取RSS失败 {url}: {e}")
            return []

    def _parse_entry(self, entry, source_name: str) -> Optional[Dict]:
        """解析单条RSS条目"""
        try:
            # 获取发布时间
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

            # 获取内容摘要
            description = ""
            if hasattr(entry, "description"):
                description = entry.description
            elif hasattr(entry, "summary"):
                description = entry.summary
            elif hasattr(entry, "content"):
                description = entry.content[0].value if entry.content else ""

            # 清理HTML标签
            description = self._strip_html(description)

            return {
                "title": entry.get("title", "无标题"),
                "url": entry.get("link", ""),
                "description": description[:500],  # 限制长度
                "source": source_name,
                "published": published,
                "author": entry.get("author", ""),
            }

        except Exception as e:
            logger.error(f"解析条目失败: {e}")
            return None

    def _strip_html(self, text: str) -> str:
        """简单清理HTML标签"""
        import re

        # 移除HTML标签
        text = re.sub(r"<[^>]+>", "", text)
        # 移除多余空白
        text = " ".join(text.split())
        return text.strip()

    def fetch_multiple(
        self, sources: List[Dict], max_items_per_source: int = 10
    ) -> List[Dict]:
        """
        从多个RSS源获取资讯

        Args:
            sources: 源列表，每个源包含 name 和 url
            max_items_per_source: 每个源最多获取条数

        Returns:
            所有资讯列表
        """
        all_items = []

        for source in sources:
            items = self.fetch_feed(
                url=source["url"],
                source_name=source.get("name", ""),
                max_items=max_items_per_source,
            )

            # 添加额外元数据
            for item in items:
                item["category"] = source.get("category", "未分类")
                item["language"] = source.get("language", "unknown")

            all_items.extend(items)
            time.sleep(1)  # 礼貌延迟

        return all_items
