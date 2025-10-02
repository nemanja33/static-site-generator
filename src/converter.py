from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  if (isinstance(old_nodes, list) != True):
    raise Exception("Please submit an array of elements") 
  if (len(old_nodes) == 0):
    raise Exception("Empty list not allowed!")
  if (text_type not in TextType):
    raise Exception("Please submit a valid type") 
  new_nodes = []
  for node in old_nodes:
    if (delimiter not in node.text):
      node = TextNode(node.text, node.type)
      new_nodes.extend([node])
      continue 
    fist_split = node.text.split(delimiter, 1)
    if (delimiter not in fist_split[1]):
      raise Exception("Invalid markdown!")
    second_split = fist_split[1].split(delimiter, 1)
    node_two = TextNode(second_split[0], text_type)
    node_three = TextNode(second_split[1], TextType.PLAIN)
    if (fist_split[0] != ''):
      node_one = TextNode(fist_split[0], TextType.PLAIN)
      new_nodes.extend([node_one, node_two, node_three])
    else:
      new_nodes.extend([node_two, node_three])
  return new_nodes
  