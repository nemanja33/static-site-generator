import unittest

from htmlnode import HTMLNode, ElementType, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
  def test_eq(self):
    el = HTMLNode(ElementType.PARAGRAPH, "first tag", { "class": "p" })
    html1 = el.props_to_html()
    el2 = HTMLNode(ElementType.PARAGRAPH, "first tag", { "class": "p" })
    html2 = el2.props_to_html()
    self.assertEqual(html1, html2)
    
  def test_tag(self):
    el = HTMLNode(ElementType.H2, "content", {"class": "wrap"})
    self.assertTrue(el.tag in ElementType)

  def test_props(self):
    el = HTMLNode(ElementType.LINK, "link", { "class": "wrap"})
    self.assertTrue(isinstance(el.props, dict))
      
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
  def test_tag(self):
    node = LeafNode(ElementType.H1, "Title")
    self.assertTrue(node.tag in ElementType)
    
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span><b>grandchild</b></span></div>",
    )
    
  def test_img(self):
    child_node = LeafNode(ElementType.IMAGE.value, "alt", { "src": "image.jpg" })
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), '<div><img src="image.jpg" alt="alt" /></div>')
    
  def test_deep_nested(self):
    child_1 = LeafNode(ElementType.SPAN.value, "Lorem ipsum")
    child_2 = ParentNode(ElementType.PARAGRAPH.value, [child_1])
    child_3 = ParentNode(ElementType.LINK.value, [child_2], { "href": "/"})
    child_4 = ParentNode(ElementType.LIST_ITEM.value, [child_3])
    parent = ParentNode(ElementType.UNORDERED_LIST.value, [child_4])
    self.assertEqual(parent.to_html(), '<ul><li><a href="/"><p><span>Lorem ipsum</span></p></a></li></ul>')


      

if __name__ == "__main__":
  unittest.main()