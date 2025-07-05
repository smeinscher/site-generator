import os
import shutil
from textnode import TextNode, TextType
from copy_contents_to_directory import copy_contents_to_directory
from generate_page import generate_page_recursive


def main():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    copy_contents_to_directory("static/", "public/")
    generate_page_recursive("content/", "template.html", "public/")


main()
