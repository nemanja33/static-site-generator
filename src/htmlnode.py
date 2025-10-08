from enum import Enum

class ElementType(Enum):
    PARAGRAPH = "p"
    SPAN = "span"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    BOLD = "b"
    ITALIC = "i"
    LINK = "a"
    IMAGE = "img"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    LIST_ITEM = "li"
    QUOTE = "blockquote"
    CODE = "code"


class HTMLNode:
  def __init__(self, tag=None, value=None, props=None, children=None):
    self.tag = tag
    self.value = value
    self.props = props
    self.children = children

  def to_html(self):
    raise(NotImplemented)

  def props_to_html(self):
    all_props = " "
    if self.props is not None:
      for key in self.props:
        all_props += f'{key}="{self.props[key]}" '
    return all_props.rstrip()    
  
  def __repr__(self):
    return f"HTML node - tag: {self.tag}; value: {self.value}; props: {self.props}; children: {self.children};"
    
class LeafNode(HTMLNode):
  def __init__(self, tag, value=None, props=None):
    super().__init__(tag=tag, value=value, props=props)
      
  def to_html(self):
    if self.tag == ElementType.IMAGE.value:
      return f'<{self.tag}{self.props_to_html()} alt="{self.value}" />'
    
    if self.tag is None:
      return self.value
    
    if self.value is None:
      raise(ValueError)
    
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag=tag, children=children, props=props)
    
  def to_html(self):
    if self.tag is None:
      raise(ValueError)
    
    if self.children is None or len(self.children) == 0:
      raise(ValueError, "Parent node needs to have a child")
    
    final_tag = f"<{self.tag}{self.props_to_html()}>"
    for child in self.children:
      final_tag += child.to_html()
    
    final_tag += f"</{self.tag}>"
    
    return final_tag
    