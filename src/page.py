from markdown import markdown_to_html, extract_title

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  md = open(from_path).read()
  html = markdown_to_html(md).to_html()
  title = extract_title(md)

  with open(template_path) as f:
    newText=f.read().replace('{{ Title }}', title).replace("{{ Content }}", html)

  with open(dest_path, "w") as f:
    f.write(newText)