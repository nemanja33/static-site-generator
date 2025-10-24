import sys
from generate_files.move_files import mv_files
from generate_files.page import generate_pages_recursive

def main():
  basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
  mv_files()
  generate_pages_recursive("content", "src/template.html", "docs", basepath)
main()