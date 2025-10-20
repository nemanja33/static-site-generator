from move_files import mv_files
from page import generate_page

def main():
  mv_files()
  generate_page("content/index.md", "src/template.html", "public/index.html")

main()
