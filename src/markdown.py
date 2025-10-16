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

def text_to_leaf_node(text, node_type):
  children = []
  if node_type == BlockType.HEADING:
    split_text = text.split(' ', 1)
    text = split_text[1]
    heading_level = f"h{len(split_text[0])}"
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
      leaf_node = text_node_to_html_node(node)
      children.append(leaf_node)
    return ParentNode(ElementType(heading_level).value, children)

  if node_type == BlockType.QUOTE:
    split_text = text.split(' ', 1)
    text = split_text[1]
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
      leaf_node = text_node_to_html_node(node)
      children.append(leaf_node)
    return ParentNode(node_type.value, children)

  if node_type == BlockType.UNORDERED_LIST or node_type == BlockType.ORDERED_LIST:
    li_nodes = []
    for item in text:
      text_nodes = text_to_textnodes(item)
      children = [text_node_to_html_node(node) for node in text_nodes]
      li_nodes.append(ParentNode(ElementType.LIST_ITEM.value, children))
    return ParentNode(node_type.value, li_nodes)

  else:
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
      leaf_node = text_node_to_html_node(node)
      children.append(leaf_node)
    return ParentNode(node_type.value, children)

  
def markdown_to_html(markdown):
  blocks = markdown_to_blocks(markdown)
  html = []
  for block in blocks:
    node_type, node_el = block_to_block_type(block)
    if (node_type == BlockType.CODE):
      remove_backticks = re.sub('```', '', node_el)
      text_node = TextNode(f"{remove_backticks.lstrip()}", TextType.CODE)
      html_node = text_node_to_html_node(text_node)
      parent = ParentNode("pre", [html_node])
      html.append(parent)
    else:
      node = HTMLNode(node_type.value, node_el)
      leaf_nodes = text_to_leaf_node(node.value, node_type)
      html.append(leaf_nodes)
  wrap = ParentNode("div", html)
  return wrap
