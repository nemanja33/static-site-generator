from generate_files.move_files import mv_files
from generate_files.page import generate_pages_recursive

def main():
  mv_files()
  generate_pages_recursive("content", "src/template.html", "public")

main()