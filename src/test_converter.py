import unittest
from textnode import TextNode, TextType
from converter import split_nodes_delimiter

class ConverterTest(unittest.TestCase):
  def test_plain_text(self):
    node = TextNode('This is just plain text', TextType.PLAIN)
    converted = split_nodes_delimiter([node], '`', TextType.PLAIN)
    self.assertEqual(converted, [node])
    
  def test_node_a_list(self):
    with self.assertRaises(Exception) as context:
      split_nodes_delimiter('', '', '')

    self.assertEqual(str(context.exception), "Please submit an array of elements")
    
  def test_empty_node(self):
    with self.assertRaises(Exception) as context:
      split_nodes_delimiter([], '`', TextType.PLAIN)
    
    self.assertEqual(str(context.exception), "Empty list not allowed!")
  
  def test_type(self):
    node = TextNode("Text node with `code`", TextType.PLAIN)
    with self.assertRaises(Exception) as context:
      split_nodes_delimiter([node], '`', "CODE")
    self.assertEqual(str(context.exception), "Please submit a valid type")
    
  def test_unclosed(self):
    node = TextNode("Let's test _italic text", TextType.PLAIN)
    with self.assertRaises(Exception) as context:
      split_nodes_delimiter([node], '_', TextType.ITALIC)
    self.assertEqual(str(context.exception), "Invalid markdown!")
    
    
  def test_italic(self):
    node = TextNode("Let's test _italic_ text", TextType.PLAIN)
    converted = split_nodes_delimiter([node], '_', TextType.ITALIC)
    self.assertEqual(converted, [TextNode("Let's test ", TextType.PLAIN), TextNode("italic", TextType.ITALIC), TextNode(" text", TextType.PLAIN)])
    
  def test_bold(self):
    node = TextNode("Let's test **bold** text", TextType.PLAIN)
    converted = split_nodes_delimiter([node], '**', TextType.BOLD)
    self.assertEqual(converted, [TextNode("Let's test ", TextType.PLAIN), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.PLAIN)])
    
  def test_code(self):
    node = TextNode("Let's test `code` text", TextType.PLAIN)
    converted = split_nodes_delimiter([node], '`', TextType.CODE)
    self.assertEqual(converted, [TextNode("Let's test ", TextType.PLAIN), TextNode("code", TextType.CODE), TextNode(" text", TextType.PLAIN)])
    
  def test_multiple_nodes(self):
    node1 = TextNode("Let's test `code` text", TextType.PLAIN)
    node2 = TextNode("Let's test `code` text", TextType.PLAIN)
    converted = split_nodes_delimiter([node1, node2], '`', TextType.CODE)
    self.assertEqual(converted, [TextNode("Let's test ", TextType.PLAIN), TextNode("code", TextType.CODE), TextNode(" text", TextType.PLAIN), TextNode("Let's test ", TextType.PLAIN), TextNode("code", TextType.CODE), TextNode(" text", TextType.PLAIN)])    
    
  def test_multi_convert(self):
    node = TextNode("Let's test `code` text and **bold** text", TextType.PLAIN)
    converted1 = split_nodes_delimiter([node], '`', TextType.CODE)
    converted2 = split_nodes_delimiter(converted1, '**', TextType.BOLD)
    self.assertEqual(converted2, [TextNode("Let's test ", TextType.PLAIN), TextNode("code", TextType.CODE), TextNode(" text and ", TextType.PLAIN), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.PLAIN)])
    
    
if __name__ == "__main__":
  unittest.main()