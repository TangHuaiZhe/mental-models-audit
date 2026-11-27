from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from seo_metadata import extract_course_description, on_page_markdown


class SeoMetadataTests(unittest.TestCase):
    def test_extracts_plain_definition_section(self):
        markdown = """# 标题

## 一句话定义

**公共物品（Public Goods）**通常具有两个特征：

- **非排他性**：很难阻止未付费者使用；
- **非竞争性**：一个人使用不显著减少别人使用。

## 下一节
"""
        description = extract_course_description(markdown)
        self.assertIn("公共物品", description)
        self.assertIn("非排他性", description)
        self.assertNotIn("**", description)
        self.assertNotIn("## 下一节", description)

    def test_description_is_bounded(self):
        markdown = "## 一句话定义\n\n" + "很长的定义。" * 80
        description = extract_course_description(markdown, limit=80)
        self.assertLessEqual(len(description), 80)
        self.assertTrue(description.endswith("。"))

    def test_hook_only_sets_course_pages_without_override(self):
        class File:
            src_uri = "course/001-example.md"

        class Page:
            file = File()
            meta = {}

        markdown = "# 标题\n\n## 一句话定义\n\n这是课程摘要。\n"
        self.assertEqual(on_page_markdown(markdown, Page, None, None), markdown)
        self.assertEqual(Page.meta["description"], "这是课程摘要。")

        Page.meta = {"description": "人工摘要"}
        on_page_markdown(markdown, Page, None, None)
        self.assertEqual(Page.meta["description"], "人工摘要")


if __name__ == "__main__":
    unittest.main()
