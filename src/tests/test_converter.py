import unittest
from convert.textnode import TextNode, TextType
from convert.converter import split_nodes_delimiter, extract_markdown_links, split_nodes_link, text_to_textnodes

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
    self.assertEqual(converted, [
      TextNode("Let's test ", TextType.PLAIN),
      TextNode("italic", TextType.ITALIC),
      TextNode(" text", TextType.PLAIN)
    ])
    
  def test_bold(self):
    node = TextNode("Let's test **bold** text", TextType.PLAIN)
    converted = split_nodes_delimiter([node], '**', TextType.BOLD)
    self.assertEqual(converted, [
      TextNode("Let's test ", TextType.PLAIN),
      TextNode("bold", TextType.BOLD),
      TextNode(" text", TextType.PLAIN)
    ])
    
  def test_code(self):
    node = TextNode("Let's test `code` text", TextType.PLAIN)
    converted = split_nodes_delimiter([node], '`', TextType.CODE)
    self.assertEqual(converted, [
      TextNode("Let's test ", TextType.PLAIN),
      TextNode("code", TextType.CODE),
      TextNode(" text", TextType.PLAIN)
    ])
    
  def test_multiple_nodes(self):
    node1 = TextNode("Let's test `code` text", TextType.PLAIN)
    node2 = TextNode("Let's test `code` text", TextType.PLAIN)
    converted = split_nodes_delimiter([node1, node2], '`', TextType.CODE)
    self.assertEqual(converted, [
      TextNode("Let's test ", TextType.PLAIN),
      TextNode("code", TextType.CODE),
      TextNode(" text", TextType.PLAIN),
      TextNode("Let's test ", TextType.PLAIN),
      TextNode("code", TextType.CODE),
      TextNode(" text", TextType.PLAIN)
    ])    
    
  def test_multi_convert(self):
    node = TextNode("Let's test `code` text and **bold** text", TextType.PLAIN)
    converted1 = split_nodes_delimiter([node], '`', TextType.CODE)
    converted2 = split_nodes_delimiter(converted1, '**', TextType.BOLD)
    self.assertEqual(converted2, [
      TextNode("Let's test ", TextType.PLAIN),
      TextNode("code", TextType.CODE),
      TextNode(" text and ", TextType.PLAIN),
      TextNode("bold", TextType.BOLD),
      TextNode(" text", TextType.PLAIN)
    ])
    
  def test_extract_markdown_images(self):
    matches = extract_markdown_links(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
      is_image=True
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
  def test_extract_markdown_images_multi(self):
    matches = extract_markdown_links(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a flower ![flower](https://flower.jpg)",
      is_image=True
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("flower", "https://flower.jpg")], matches)
    
  def test_extract_image_wrong_markdown(self):
    matches = extract_markdown_links(
        "This is text with an ![image(https://i.imgur.com/zjjcJKZ.png)",
        is_image=True
    )
    self.assertListEqual([], matches)

  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
  def test_extract_link_wrong_markdown(self):
    matches = extract_markdown_links(
        "This is text with a ![link(https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([], matches)
    
  def test_extract_markdown_links_multi(self):
    matches = extract_markdown_links(
      "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and a flower [flower](https://flower.jpg)"
    )
    self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("flower", "https://flower.jpg")], matches)
    
  def test_extract_markdown_link_one(self):
    node = TextNode("This is text with a link to [boot dev](https://www.boot.dev)", TextType.PLAIN)
    converted = split_nodes_link([node])
    self.assertEqual(converted, [
      TextNode("This is text with a link to ", TextType.PLAIN),
      TextNode("boot dev",TextType.LINK, "https://www.boot.dev")
    ])
    
      
  def test_extract_markdown_links_one(self):
    node = TextNode("This is text with a link to [boot dev](https://www.boot.dev) and to [google](google.com)", TextType.PLAIN)
    node2 = TextNode("This is text with a link to [boot dev](https://www.boot.dev) and to [google](google.com)", TextType.PLAIN)
    converted = split_nodes_link([node, node2])
    self.assertEqual(converted, [
      TextNode("This is text with a link to ", TextType.PLAIN),
      TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
      TextNode(" and to ", TextType.PLAIN),
      TextNode("google", TextType.LINK, "google.com"),
      TextNode("This is text with a link to ", TextType.PLAIN),
      TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
      TextNode(" and to ", TextType.PLAIN),
      TextNode("google", TextType.LINK, "google.com")
    ])


  def test_empty_links(self):
    with self.assertRaises(Exception) as context:
      split_nodes_link([])
    self.assertEqual(str(context.exception), "Empty list not allowed!")
    
  def test_non_list_links(self):
    with self.assertRaises(Exception) as context:
      split_nodes_link(123)
    self.assertEqual(str(context.exception), "Please submit an array of elements")
    
  def test_extract_markdown_image_one(self):
    node = TextNode("This is text with an image ![flower](flower.jpg)", TextType.PLAIN)
    converted = split_nodes_link([node], is_image=True)
    self.assertEqual(converted, [
      TextNode("This is text with an image ", TextType.PLAIN),
      TextNode("flower", TextType.IMAGE, "flower.jpg")
    ])
  
      
  def test_extract_markdown_images_one(self):
    node = TextNode("This is text with an image ![flower](flower.jpg) and an image of the ![sun](sun.jpg)", TextType.PLAIN)
    converted = split_nodes_link([node], is_image=True)
    self.assertEqual(converted, [
      TextNode("This is text with an image ", TextType.PLAIN),
      TextNode("flower", TextType.IMAGE, "flower.jpg"),
      TextNode(" and an image of the ", TextType.PLAIN),
      TextNode("sun", TextType.IMAGE, "sun.jpg")])

  def test_empty_images(self):
    with self.assertRaises(Exception) as context:
      split_nodes_link([], is_image=True)
    self.assertEqual(str(context.exception), "Empty list not allowed!")
    
  def test_non_list_images(self):
    with self.assertRaises(Exception) as context:
      split_nodes_link(123, is_image=True)
    self.assertEqual(str(context.exception), "Please submit an array of elements")
    
  def test_text_converter(self):
    converted = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    self.assertEqual(converted,
      [
        TextNode("This is ", TextType.PLAIN),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.PLAIN),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.PLAIN),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.PLAIN),
        TextNode("link", TextType.LINK, "https://boot.dev")
    ])
    
    
  def test_text_converted_italic_wrong_markdown(self):
    with self.assertRaises(Exception) as context:
      text_to_textnodes("This is **text** with an _italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    self.assertEqual(str(context.exception), "Invalid markdown!")
    
  def test_text_converted_image_wrong_markdown(self):
    converted = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image(https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    self.assertEqual(converted,
      [
        TextNode("This is ", TextType.PLAIN),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.PLAIN),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ![obi wan image(https://i.imgur.com/fJRm4Vk.jpeg) and a ", TextType.PLAIN),
        TextNode("link", TextType.LINK, "https://boot.dev")
    ])
    
  def test_text_is_string(self):
    with self.assertRaises(Exception) as context:
      text_to_textnodes([])
    self.assertEqual(str(context.exception), "Text needs to be a string!")
    
  def test_text_with_multiple_same_delimeters(self):
    converted = text_to_textnodes("Let's test multiple **bold**, _italic_, and `code` examples, but on multiple places, so here again: **another bold**, _another italic_, and `another code`. We should not forget about images or links: ![image 1](image1.jpg), [link 1](link1.com) and here is ![image 2](image2.jpg), [link 2](link2.com)!")
    self.assertEqual(converted, [
      TextNode("Let's test multiple ", TextType.PLAIN),
      TextNode("bold", TextType.BOLD),
      TextNode(", ", TextType.PLAIN),
      TextNode("italic", TextType.ITALIC),
      TextNode(", and ", TextType.PLAIN),
      TextNode("code", TextType.CODE),
      TextNode(" examples, but on multiple places, so here again: ", TextType.PLAIN),
      TextNode("another bold", TextType.BOLD),
      TextNode(", ", TextType.PLAIN),
      TextNode("another italic", TextType.ITALIC),
      TextNode(", and ", TextType.PLAIN),
      TextNode("another code", TextType.CODE),
      TextNode(". We should not forget about images or links: ", TextType.PLAIN),
      TextNode("image 1", TextType.IMAGE, "image1.jpg"),
      TextNode(", ", TextType.PLAIN),
      TextNode("link 1", TextType.LINK, "link1.com"),
      TextNode(" and here is ", TextType.PLAIN),
      TextNode("image 2", TextType.IMAGE, "image2.jpg"),
      TextNode(", ", TextType.PLAIN),
      TextNode("link 2", TextType.LINK, "link2.com"),
      TextNode("!", TextType.PLAIN),
    ])
if __name__ == "__main__":
  unittest.main()