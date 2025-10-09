import re
from blocknode import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, ElementType, LeafNode
from converter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_blocks(markdown):
  splitted_md = markdown.split("\n\n")
  remove_empty_el = list(filter(None, splitted_md))
  trimmed_md = [block.strip() for block in remove_empty_el if block.strip()]
  return trimmed_md

def text_to_leaf_node(text_nodes):
  children = []
  for text in text_nodes:
    if type(text) != str:
      leaf_node = text_node_to_html_node(text)
      children.append(leaf_node.to_html())
    else:
      children.append(text)
  combined_text = ''.join(children)
  return LeafNode(ElementType.PARAGRAPH.value, combined_text)
  
def markdown_to_html(markdown):
  blocks = markdown_to_blocks(markdown)
  html = []
  for block in blocks:
    type = block_to_block_type(block)
    if (type == BlockType.CODE):
      remove_backticks = re.sub('```', '', block)
      text_node = TextNode(f"{remove_backticks.lstrip()}", TextType.CODE)
      html_node = text_node_to_html_node(text_node)
      parent = ParentNode("pre", [html_node])
      html.append(parent)
    else:
      removed_whitespace_inside_str = re.sub(r'\n', ' ', block)
      node = HTMLNode(type.value, removed_whitespace_inside_str)
      text_nodes = text_to_textnodes(node.value)
      leaf_nodes = text_to_leaf_node(text_nodes)
      html.append(leaf_nodes)
  wrap = ParentNode("div", html)
  return wrap
