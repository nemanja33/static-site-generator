from enum import Enum
from htmlnode import LeafNode, ElementType

class TextType(Enum):
	PLAIN = "plain"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

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
  tag = text_node.type.value
 
  if tag not in TextType:
    raise(Exception, "Not correct type")

  if tag == TextType.PLAIN.value:
    return LeafNode("", text_node.text)
  
  if tag == TextType.BOLD.value:
    return LeafNode(ElementType.B.value, text_node.text)
    
  if tag == TextType.ITALIC.value:
    return LeafNode(ElementType.I.value, text_node.text)
    
  if tag == TextType.CODE.value:
    return LeafNode(ElementType.CODE.value, text_node.text)
    
  if tag == TextType.LINK.value:
    return LeafNode(ElementType.A.value, text_node.text, { "href": text_node.url })
    
  if tag == TextType.IMAGE.value:
    return LeafNode(ElementType.IMG.value, text_node.text, { "src": text_node.url })
  