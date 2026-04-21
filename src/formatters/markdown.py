"""
资讯格式化模块
"""
from datetime import datetime, timezone
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class MarkdownFormatter:
    """Markdown格式化输出"""

    def __init__(self, show_description: bool = True, max_items: int = 50):
        self.show_description = show_description
        self.max_items = max_items

    def format(self, items: List[Dict], title: str = None) -> str:
        """
        格式化资讯列表为Markdown

        Args:
            items: 资讯列表
            title: 报告标题

        Returns:
            Markdown文本
        """
        # 按类别分组
        grouped = self._group_by_category(items)

        # 生成标题
        date_str = datetime.now(timezone.utc).astimezone().strftime("%Y年%m月%d日")
        md_lines = [
            f"# 🤖 AI资讯简报",
            f"",
            f"**日期**: {date_str}",
            f"**资讯数量**: {len(items)} 条",
            f"",
            f"---",
            f"",
        ]

        # 按类别输出（动态获取所有类别）
        # 论文优先，然后按类别名称排序
        category_order = ["论文"]
        other_categories = sorted([c for c in grouped.keys() if c != "论文"])
        category_order.extend(other_categories)

        for category in category_order:
            if category not in grouped:
                continue

            md_lines.append(f"## 📌 {category}")
            md_lines.append("")

            # 计算每个类别最多显示多少条
            max_per_category = self.max_items // len(grouped) if len(grouped) > 0 else self.max_items

            for item in grouped[category][:max_per_category]:
                md_lines.extend(self._format_item(item))
                md_lines.append("")

            md_lines.append("---")
            md_lines.append("")

        # 添加页脚
        md_lines.extend([
            "",
            "---",
            "",
            f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        ])

        return "\n".join(md_lines)

    def _group_by_category(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """按类别分组"""
        grouped = {}
        for item in items:
            category = item.get("category", "未分类")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(item)
        return grouped

    def _format_item(self, item: Dict) -> List[str]:
        """格式化单条资讯"""
        lines = []

        # 标题和链接
        title = item.get("title", "无标题")
        url = item.get("url", "")
        source = item.get("source", "")

        if url:
            lines.append(f"### [{title}]({url})")
        else:
            lines.append(f"### {title}")

        # 元信息
        meta = []
        if source:
            meta.append(f"来源: {source}")

        if item.get("published"):
            try:
                pub_time = item["published"]
                if isinstance(pub_time, str):
                    pub_time = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))
                time_str = pub_time.astimezone().strftime("%m-%d %H:%M")
                meta.append(f"时间: {time_str}")
            except:
                pass

        if meta:
            lines.append(f"*{' | '.join(meta)}*")

        # 描述
        if self.show_description and item.get("description"):
            desc = item["description"]
            if len(desc) > 200:
                desc = desc[:200] + "..."
            lines.append(f">{desc}")

        lines.append("")

        return lines

    def save(self, items: List[Dict], filepath: str, title: str = None):
        """保存到文件"""
        content = self.format(items, title)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"已保存到 {filepath}")


class ConsoleFormatter:
    """控制台输出格式化"""

    def format(self, items: List[Dict]) -> str:
        """格式化为控制台友好的文本"""
        lines = [
            "=" * 60,
            "🤖 AI资讯简报",
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"数量: {len(items)} 条",
            "=" * 60,
            "",
        ]

        # 按类别分组显示
        grouped = {}
        for item in items:
            category = item.get("category", "未分类")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(item)

        for category, items in grouped.items():
            lines.append(f"\n【{category}】")
            lines.append("-" * 40)

            for i, item in enumerate(items[:10], 1):
                lines.append(f"\n{i}. {item.get('title', '无标题')}")
                if item.get("url"):
                    lines.append(f"   链接: {item['url']}")
                if item.get("description"):
                    desc = item["description"][:100] + "..." if len(item["description"]) > 100 else item["description"]
                    lines.append(f"   摘要: {desc}")

        lines.append("\n" + "=" * 60)

        return "\n".join(lines)
