from move_files import mv_files
from page import generate_page

def main():
  mv_files()
  generate_page("content/index.md", "src/template.html", "public/index.html")
  generate_page("content/blog/glorfindel/index.md", "src/template.html", "public/blog/glorfindel.html")
  generate_page("content/blog/majesty/index.md", "src/template.html", "public/blog/majesty.html")
  generate_page("content/blog/tom/index.md", "src/template.html", "public/blog/tom.html")
  generate_page("content/contact/index.md", "src/template.html", "public/contact.html")

main()
