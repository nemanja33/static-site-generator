import re
from blocknode import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from converter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_blocks(markdown):
  splitted_md = markdown.split("\n\n")
  remove_empty_el = list(filter(None, splitted_md))
  trimmed_md = [block.strip() for block in remove_empty_el if block.strip()]
  removed_whitespace_inside_str = [re.sub(r'\n\s+', '\n', item) for item in trimmed_md]
  return removed_whitespace_inside_str

def text_to_children(text_nodes):
  nodes = []
  for node in text_nodes:
    leaf_node = text_node_to_html_node(node)
    nodes.append(leaf_node)
  return nodes

def markdown_to_html(markdown):
  blocks = markdown_to_blocks(markdown)
  html = []
  for block in blocks:
    type = block_to_block_type(block)
    if (type == BlockType.CODE):
      text_node = TextNode(block, TextType.CODE)
      html_node = text_node_to_html_node(text_node)
      html.append(html_node)
    else:
      node = HTMLNode(type.value, block)
      text_nodes = text_to_textnodes(node.value)
      leaf_nodes = text_to_children(text_nodes)
      html.extend(leaf_nodes)
  wrap = ParentNode("div", html)
  return wrap.to_html()