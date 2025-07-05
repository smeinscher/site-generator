import unittest
from markdown_to_blocks import markdown_to_blocks
from blocks import BlockType, block_to_block_type
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        markdown_block = "###### This is a heading"
        self.assertEqual(BlockType.HEADING,
                         block_to_block_type(markdown_block))

    def test_block_to_block_type_code(self):
        markdown_block = "``` def this_is_code:\nprint('This is code')\n```"
        self.assertEqual(BlockType.CODE,
                         block_to_block_type(markdown_block))

    def test_block_to_block_type_quote(self):
        markdown_block = "> This is a quote block\n> Another quote line"
        self.assertEqual(BlockType.QUOTE,
                         block_to_block_type(markdown_block))

    def test_block_to_block_type_unordered_list(self):
        markdown_block = "- This is a list\n- with items"
        self.assertEqual(BlockType.UNORDERED_LIST,
                         block_to_block_type(markdown_block))

    def test_block_to_block_type_ordered_list(self):
        markdown_block = "1. This is an ordered list\n2. Another item\n3. Yet another item"
        self.assertEqual(BlockType.ORDERED_LIST,
                         block_to_block_type(markdown_block))

    def test_block_to_block_type_heading_invalid(self):
        markdown_block = "####### This is an invalid heading"
        self.assertEqual(BlockType.PARAGRAPH,
                         block_to_block_type(markdown_block))

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
        # Heading 1

        ## Heading 2

        ### Heading 3

        #### Heading 4

        ##### Heading 5

        ###### Heading 6

        ####### Invalid Heading
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6><p>####### Invalid Heading</p></div>",
        )

    def test_quote(self):
        md = """
        > Quote block
        > The same block
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote block The same block</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
        - something
        - something else
        - unrelated thing
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>something</li><li>something else</li><li>unrelated thing</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
        1. something
        2. something else
        3. unrelated thing
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>something</li><li>something else</li><li>unrelated thing</li></ol></div>"
        )

    def test_extract_title(self):
        md = """
        # Heading
        """
        title = extract_title(md)
        self.assertEqual(title, "Heading")


if __name__ == "__main__":
    unittest.main()
