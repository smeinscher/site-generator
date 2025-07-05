import os
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    html = markdown_to_html_node(md_content).to_html()
    final_html = template_content.replace(
        "{{ Title }}", extract_title(md_content)).replace("{{ Content }}", html).replace("href=\"/", f"href=\"{base_path}").replace("src=\"/", f"src=\"{base_path}")
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for item in os.listdir(dir_path_content):
        item_source_path = os.path.join(dir_path_content, item)
        base_name, extension = os.path.splitext(item)
        item_destination_path = os.path.join(
            dest_dir_path, base_name)
        if os.path.isfile(item_source_path):
            generate_page(item_source_path, template_path,
                          item_destination_path + ".html", base_path)
        else:
            generate_page_recursive(
                item_source_path, template_path, item_destination_path, base_path)
