import re
from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def text_to_textnodes(text):
    result = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_links(result)
    return result


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if delimiter not in ["**", "_", "`"]:
        raise Exception("Delimiter is invalid")
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) == 1:
            new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            continue
        if len(split_text) % 2 != 1:
            raise Exception("Mismatch of delimiters")
        result = []
        for i in range(len(split_text)):
            if i % 2 == 0:
                result.append(TextNode(split_text[i], TextType.TEXT))
            else:
                result.append(
                    TextNode(split_text[i], text_type))
        new_nodes.extend(result)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        result = []
        image_text = extract_markdown_images(node.text)
        if len(image_text) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for image in image_text:
            split_text = text.split(f"![{image[0]}]({image[1]})")
            result.append(TextNode(split_text[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            if len(split_text) > 1:
                text = split_text[1]
        if len(text) != 0:
            result.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(result)
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        result = []
        link_text = extract_markdown_links(node.text)
        if len(link_text) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for link in link_text:
            split_text = text.split(f"[{link[0]}]({link[1]})")
            result.append(TextNode(split_text[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            split_text = text.split(f"[{link[0]}]({link[1]})")
            if len(split_text) > 1:
                text = split_text[1]
        if len(text) != 0:
            result.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(result)
    return new_nodes
