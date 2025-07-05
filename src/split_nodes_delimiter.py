from textnode import TextNode, TextType


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
