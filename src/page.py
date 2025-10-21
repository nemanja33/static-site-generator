import os
from markdown import markdown_to_html, extract_title

def generate_page(from_path, template_path, dest_path):
  current = os.getcwd()
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  md = open(from_path).read()
  html = markdown_to_html(md).to_html()
  title = extract_title(md)

  with open(template_path) as f:
    newText=f.read().replace('{{ Title }}', title).replace("{{ Content }}", html)

  final_path = dest_path.rsplit('/', 1)[0]
  if (os.path.exists(f"{current}/{final_path}") == False):
    os.mkdir(f"{current}/{final_path}")
  with open(dest_path, "w") as f:
    f.write(newText)
