"""
网页资讯抓取模块
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from typing import List, Dict, Optional
import time
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebFetcher:
    """网页资讯抓取器"""

    def __init__(self, timeout: int = 10, user_agent: str = None):
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

    def fetch_page(self, url: str, source_info: Dict = None) -> List[Dict]:
        """
        从网页获取资讯

        Args:
            url: 目标网页URL
            source_info: 源信息，包含 name, category, selector 等

        Returns:
            资讯列表
        """
        try:
            logger.info(f"正在抓取网页: {source_info.get('name', url) if source_info else url}")

            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, "html.parser")

            # 根据配置的选择器提取内容
            selector = source_info.get("selector", "article, .news-item, .article")
            items = []

            for element in soup.select(selector)[:20]:  # 最多20条
                item = self._parse_element(element, source_info)
                if item and self._is_ai_related(item):
                    items.append(item)

            logger.info(f"从 {source_info.get('name', url)} 抓取 {len(items)} 条资讯")
            return items

        except Exception as e:
            logger.error(f"抓取网页失败 {url}: {e}")
            return []

    def _parse_element(self, element, source_info: Dict) -> Optional[Dict]:
        """解析单个新闻元素"""
        try:
            # 尝试获取标题
            title_elem = element.find(["h1", "h2", "h3", "h4", "a"])
            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            if not title:
                return None

            # 尝试获取链接
            link = element.find("a", href=True)
            url = link["href"] if link else ""
            if url and not url.startswith("http"):
                base_url = source_info.get("url", "")
                url = requests.utils.urlparse(base_url)._replace(path=url).geturl()

            # 获取描述
            desc = ""
            for p in element.find_all("p"):
                text = p.get_text(strip=True)
                if len(text) > 20:  # 至少20个字符
                    desc = text[:300]
                    break

            return {
                "title": title,
                "url": url,
                "description": desc,
                "source": source_info.get("name", ""),
                "category": source_info.get("category", "未分类"),
                "language": source_info.get("language", "unknown"),
                "published": None,  # 网页抓取通常难以获取准确时间
                "author": "",
            }

        except Exception as e:
            logger.debug(f"解析元素失败: {e}")
            return None

    def _is_ai_related(self, item: Dict) -> bool:
        """判断是否与AI相关"""
        ai_keywords = [
            "AI",
            "人工智能",
            "大模型",
            "LLM",
            "GPT",
            "ChatGPT",
            "Claude",
            "Gemini",
            "文心",
            "通义",
            "Kimi",
            "DeepSeek",
            "机器学习",
            "深度学习",
            "神经网络",
            "transformer",
            "diffusion",
            "Stable Diffusion",
            "Midjourney",
            "OpenAI",
            "模型",
            "Agent",
            "训练",
            "推理",
        ]

        text = (item.get("title", "") + " " + item.get("description", "")).lower()

        return any(keyword.lower() in text for keyword in ai_keywords)

    def fetch_multiple(self, sources: List[Dict]) -> List[Dict]:
        """
        从多个网页源获取资讯

        Args:
            sources: 源列表

        Returns:
            所有资讯列表
        """
        all_items = []

        for source in sources:
            items = self.fetch_page(url=source["url"], source_info=source)
            all_items.extend(items)
            time.sleep(2)  # 网页抓取延迟更长

        return all_items


class ArxivFetcher:
    """ArXiv论文抓取器"""

    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query?"

    def fetch_recent_ai_papers(self, max_results: int = 20) -> List[Dict]:
        """获取最近的AI相关论文"""
        try:
            logger.info("正在获取ArXiv AI论文...")

            # 查询条件：计算机科学 - 人工智能
            query = "cat:cs.AI"
            params = f"search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

            url = self.base_url + params
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # 解析Atom feed
            import xml.etree.ElementTree as ET

            root = ET.fromstring(response.content)
            papers = []

            # 命名空间
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom",
            }

            for entry in root.findall("atom:entry", ns):
                paper = {
                    "title": entry.find("atom:title", ns).text.strip(),
                    "url": entry.find("atom:id", ns).text,
                    "description": entry.find("atom:summary", ns).text.strip(),
                    "source": "ArXiv",
                    "category": "论文",
                    "language": "en",
                    "published": None,
                    "author": ", ".join(
                        [
                            author.find("atom:name", ns).text
                            for author in entry.findall("atom:author", ns)
                        ]
                    ),
                }
                papers.append(paper)

            logger.info(f"获取 {len(papers)} 篇论文")
            return papers

        except Exception as e:
            logger.error(f"获取ArXiv论文失败: {e}")
            return []
