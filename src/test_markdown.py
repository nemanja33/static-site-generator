import unittest

from markdown import markdown_to_blocks

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

if __name__ == "__main__":
  unittest.main()