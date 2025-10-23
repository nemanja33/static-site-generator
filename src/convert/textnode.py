from enum import Enum
from convert.htmlnode import LeafNode, ElementType

class TextType(Enum):
	PLAIN = "p"
	BOLD = "b"
	ITALIC = "i"
	CODE = "code"
	LINK = "a"
	IMAGE = "img"

class TextNode():
	def __init__(self, text, type, url=None):
		self.text = text
		self.type = type
		self.url = url

	def __eq__(self, node):
		return self.text == node.text and self.type == node.type and self.url == node.url

	def __repr__(self):
		return f"TextNode({self.text}, {self.type.value}, {self.url})"

def text_node_to_html_node(text_node):
  if type(text_node) == str:
    return LeafNode(ElementType.PARAGRAPH.value, text_node)
  tag = text_node.type

  if tag not in TextType:
    raise(Exception, "Not correct type")
  
  if tag == TextType.PLAIN:
    return LeafNode("", text_node.text)
  
  if tag == TextType.BOLD:
    return LeafNode(ElementType.BOLD.value, text_node.text)
    
  if tag == TextType.ITALIC:
    return LeafNode(ElementType.ITALIC.value, text_node.text)
    
  if tag == TextType.CODE:
    return LeafNode(ElementType.CODE.value, text_node.text)
    
  if tag == TextType.LINK:
    return LeafNode(ElementType.LINK.value, text_node.text, { "href": text_node.url })
    
  if tag == TextType.IMAGE:
    return LeafNode(ElementType.IMAGE.value, text_node.text, { "src": text_node.url })
  