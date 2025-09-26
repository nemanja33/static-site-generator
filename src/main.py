from textnode import TextNode, TextType
def main():
  link_node = TextType.LINK
  node = TextNode("This is some anchor text", link_node, "https://www.boot.dev")
  print(node)

main()
