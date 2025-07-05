import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_to_blocks import markdown_to_blocks
from blocks import block_to_block_type, BlockType
from textnode import text_node_to_html_node, TextNode, TextType
from split_nodes import text_to_textnodes, split_nodes_delimiter


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def markdown_to_html_node(markdown):
    parent = ParentNode("div", [])
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type != BlockType.CODE:
            block = block.replace("\n", " ")
        match block_type:
            case BlockType.PARAGRAPH:
                paragraph = ParentNode("p", [])
                paragraph.children.extend(text_to_children(block))
                parent.children.append(paragraph)
            case BlockType.HEADING:
                heading_type = block.split(" ")[0].count("#")
                heading = ParentNode(f"h{heading_type}", [])
                heading.children.extend(
                    text_to_children(block.replace("#", "").strip()))
                parent.children.append(heading)
            case BlockType.CODE:
                text_nodes = split_nodes_delimiter(
                    [TextNode(block, TextType.TEXT)], "`", TextType.CODE)
                pre_html_node = ParentNode("pre", [])
                for node in text_nodes:
                    if len(node.text) > 0:
                        pre_html_node.children.append(
                            text_node_to_html_node(node))
                parent.children.append(pre_html_node)
            case BlockType.QUOTE:
                quote = ParentNode("blockquote", [])
                quote.children.extend(
                    text_to_children(block.replace("> ", "")))
                parent.children.append(quote)
            case BlockType.UNORDERED_LIST:
                unordered_list = ParentNode("ul", [])
                list_items = block.split("- ")
                for item in list_items:
                    if len(item) == 0:
                        continue
                    children = text_to_children(item)
                    if len(children) == 1:
                        unordered_list.children.append(
                            LeafNode("li", item.strip()))
                    else:
                        list_item = ParentNode("li", children)
                        unordered_list.children.append(list_item)
                parent.children.append(unordered_list)
            case BlockType.ORDERED_LIST:
                ordered_list = ParentNode("ol", [])
                list_items = re.split(r"[0-9]+\.", block)
                for item in list_items:
                    if len(item) == 0:
                        continue
                    children = text_to_children(item.strip())
                    if len(children) == 1:
                        ordered_list.children.append(
                            LeafNode("li", item.strip()))
                    else:
                        list_item = ParentNode("li", children)
                        ordered_list.children.append(list_item)
                parent.children.append(ordered_list)
            case _:
                raise Exception("Unrecognized block type")
    return parent
