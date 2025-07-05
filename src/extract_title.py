def extract_title(markdown):
    if markdown.strip()[:2] != "# ":
        raise Exception("Need h1 header at beginning of file")
    return markdown.strip().split("\n")[0].replace("# ", "").strip()
