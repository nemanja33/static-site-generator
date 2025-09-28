import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)
    
  def test_text(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.value, "This is a text node")

  def test_image(self):
    node = TextNode("Image alt", TextType.IMAGE, "./src/image.jpg")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.to_html(),'<img src="./src/image.jpg" alt="Image alt" />')
    
  def test_link(self):
    node = TextNode("Link", TextType.LINK, "google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.to_html(),'<a href="google.com">Link</a>')

if __name__ == "__main__":
  unittest.main()