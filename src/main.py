import os
import shutil
import sys
from textnode import TextNode, TextType
from copy_contents_to_directory import copy_contents_to_directory
from generate_page import generate_page_recursive


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    if os.path.exists("docs/"):
        shutil.rmtree("docs/")
    copy_contents_to_directory("static/", "docs/")
    generate_page_recursive("content/", "template.html", "docs/", base_path)


main()
