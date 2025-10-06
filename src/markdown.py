import re

def markdown_to_blocks(markdown):
  splitted_md = markdown.split("\n\n")
  remove_empty_el = list(filter(None, splitted_md))
  trimmed_md = [block.strip() for block in remove_empty_el if block.strip()]
  removed_whitespace_inside_str = [re.sub(r'\n\s+', '\n', item) for item in trimmed_md]
  return removed_whitespace_inside_str