import os
from convert.markdown import markdown_to_html, extract_title

def copy_index(start_dir, template_path, dest_path):
  md = open(f"{start_dir}/index.md").read()
  html = markdown_to_html(md).to_html()
  title = extract_title(md)

  with open(template_path) as f:
    newText=f.read().replace('{{ Title }}', title).replace("{{ Content }}", html)

  final_path = dest_path.rsplit('/', 1)[0]
  if not os.path.exists(final_path):
    os.makedirs(final_path, exist_ok=True)
  with open(dest_path, "w") as f:
    f.write(newText)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  current = os.getcwd()
  print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")
  start_dir = f"{current}/{dir_path_content}"
  _, directories, files = next(os.walk(start_dir))

  if "index.md" in files:
    if dir_path_content == "content":
      to_path = f"{current}/{dest_dir_path}/index.html"
    else:
      page_name = os.path.basename(dir_path_content)
      to_path = f"{current}/{os.path.dirname(dest_dir_path)}/{page_name}.html"
    copy_index(start_dir, template_path, to_path)

  for directory in directories:
    sub_content_path = f"{dir_path_content}/{directory}"
    sub_dest_path = f"{dest_dir_path}/{directory}"
    generate_pages_recursive(sub_content_path, template_path, sub_dest_path)