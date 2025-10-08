import re
from enum import Enum

class BlockTpe(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "ul"
  ORDERED_LIST = "ol"

def block_to_block_type(block):
  if (block.startswith("```") and block.endswith("```")):
    return BlockTpe.CODE
  if (block.startswith(">")):
    return BlockTpe.QUOTE
  heading_match = re.match(r'^#{1,6} ', block)
  # ol_match = re.match(r'\d. ')
  if heading_match:
    return BlockTpe.HEADING
  list_block = block.split("\n")
  is_unorderd_list = all([block.startswith("- ") for block in list_block])
  if (is_unorderd_list):
    return BlockTpe.UNORDERED_LIST
  is_ordered_list = all([re.match(r'\d+. ', item) for item in list_block])
  if (is_ordered_list):
    return BlockTpe.ORDERED_LIST
  return BlockTpe.PARAGRAPH

print(block_to_block_type("- test\n+ test2"))

