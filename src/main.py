from move_files import mv_files
from page import generate_pages_recursive

def main():
  mv_files()
  generate_pages_recursive("content", "src/template.html", "public")

main()