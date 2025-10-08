import re
from enum import Enum

class BlockType(Enum):
  PARAGRAPH = "p"
  HEADING = "h"
  CODE = "code"
  QUOTE = "blockquote"
  UNORDERED_LIST = "ul"
  ORDERED_LIST = "ol"

def block_to_block_type(block):
  if (block.startswith("```") and block.endswith("```")):
    return BlockType.CODE
  if (block.startswith(">")):
    return BlockType.QUOTE
  heading_match = re.match(r'^#{1,6} ', block)
  if heading_match:
    return BlockType.HEADING
  list_block = block.split("\n")
  is_unorderd_list = all([block.startswith("- ") for block in list_block])
  if (is_unorderd_list):
    return BlockType.UNORDERED_LIST
  is_ordered_list = all([re.match(r'\d+. ', item) for item in list_block])
  if (is_ordered_list):
    return BlockType.ORDERED_LIST
  return BlockType.PARAGRAPH

