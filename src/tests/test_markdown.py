import unittest

from convert.markdown import markdown_to_blocks, markdown_to_html, extract_title

class TestTextNode(unittest.TestCase):
  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
          "This is **bolded** paragraph",
          "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
          "- This is a list\n- with items",
        ],
    )

  def test_markdown_multiple_lists(self):
    md = """
1. First item ol
2. Second item ol

- First item ul
- Second item ul

* Just a heading
"""
    blocks = markdown_to_blocks(md)

    self.assertEqual(
      blocks,
      ['1. First item ol\n2. Second item ol', '- First item ul\n- Second item ul', '* Just a heading']
    )

  def test_a_lot_of_empty_lines(self):
    md = """
first line





second line after empty lines





third line
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      ['first line', 'second line after empty lines', 'third line']
    )

  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

  def test_li_image(self):
    md = """
yo what's up with an image? ![image1](image.jpg)
"""
    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>yo what's up with an image? <img src=\"image.jpg\" alt=\"image1\" /></p></div>"
    )

  def test_unordered_list(self):
    md = """
## heading 2

- First item ul
- Second item ul
- text

just a paragraph
"""
    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h2>heading 2</h2><ul><li>First item ul</li><li>Second item ul</li><li>text</li></ul><p>just a paragraph</p></div>"
    )

  def test_ordered_list(self):
    md = """
## heading 2

- First item ul
- Second item ul
- text

1. ordered 1
2. ordered 2

just a paragraph
"""
    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h2>heading 2</h2><ul><li>First item ul</li><li>Second item ul</li><li>text</li></ul><ol><li>ordered 1</li><li>ordered 2</li></ol><p>just a paragraph</p></div>"
    )


  def test_a_lot_of_text(self):
    md = """
# Heading 1

Lorem ipsum

## Heading 2

Lorem ipsum
dolor

- list item ![image1](image.jpg)

lorem  porta lorem. Ut fr
entesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. In in mollis quam. Interdum et malesuada fames ac ante ips

##### Heading 5
"""
    node = markdown_to_html(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1>Heading 1</h1><p>Lorem ipsum</p><h2>Heading 2</h2><p>Lorem ipsum\ndolor</p><ul><li>list item <img src=\"image.jpg\" alt=\"image1\" /></li></ul><p>lorem  porta lorem. Ut fr\nentesque habitant morbi tristique senectus et netus et\nmalesuada fames ac turpis egestas. In in mollis quam. Interdum et malesuada fames ac ante ips</p><h5>Heading 5</h5></div>"
    )

  def test_title_no_heading(self):
    md = """
heading title

paragraph
"""

    with self.assertRaises(Exception) as context:
      extract_title(md)

    self.assertEqual(str(context.exception), "No H1 present in file!")

  def test_title_h2(self):
    md = """
## heading title
"""

    with self.assertRaises(Exception) as context:
      extract_title(md)

    self.assertEqual(str(context.exception), "No H1 present in file!")

  def test_title(self):
    md = """
# heading title
tes
"""

    title = extract_title(md)

    self.assertEqual(title, "heading title")
    
if __name__ == "__main__":
  unittest.main()