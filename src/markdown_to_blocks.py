

def markdown_to_blocks(markdown):
    result = []
    for block in markdown.split("\n\n"):
        block_items = block.split("\n")
        for i in range(len(block_items)):
            block_items[i] = block_items[i].strip()
        block = "\n".join(block_items)
        block = block.strip()
        if len(block) > 0:
            result.append(block)
    return result
