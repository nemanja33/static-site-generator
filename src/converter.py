from textnode import TextNode, TextType
import re

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
  
    delimiter_part_one = list(filter(None, node.text.split(delimiter, 1)))
    if (len(delimiter_part_one) < 2):
      node = TextNode(delimiter_part_one[0], TextType.PLAIN)
      new_nodes.extend([node])
      continue

    if (delimiter not in delimiter_part_one[1]):
      raise Exception("Invalid markdown!")
    
    delimeter_part_two = list(filter(None, delimiter_part_one[1].split(delimiter, 1)))
    
    # nodes 
    node_one = TextNode(delimiter_part_one[0], TextType.PLAIN)
    node_two = TextNode(delimeter_part_two[0], text_type)
    if (len(delimeter_part_two) > 1):
      rest = TextNode(delimeter_part_two[1], TextType.PLAIN)

      # recursevily apply to add instances with delimeter
      if delimiter in rest.text:
        node_three = split_nodes_delimiter([rest], delimiter, text_type)
      else:
        node_three = [rest]

    new_nodes.extend([node_one, node_two])
    if (len(delimeter_part_two) > 1):
      new_nodes.extend(node_three)
  return new_nodes


def extract_markdown_links(text, is_image=False):
  if (is_image):
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  else:
    match = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return match

def split_nodes_link(old_nodes, is_image=False):
  if (isinstance(old_nodes, list) != True):
    raise Exception("Please submit an array of elements") 
  if (len(old_nodes) == 0):
    raise Exception("Empty list not allowed!")
  new_nodes = []
  for node in old_nodes:
    extracted_links = extract_markdown_links(node.text, is_image)
    if len(extracted_links) == 0:
      new_nodes.extend([node])
      continue
    extracted_link = extracted_links[0]
    image_delimeter = "!" if is_image else ''
    extracted_link_text = f"{image_delimeter}[{extracted_link[0]}]({extracted_link[1]})"
    if (extracted_link_text not in node.text):
      node = TextNode(node.text, node.type)
      new_nodes.extend([node])
      continue

    parted_array = list(filter(None, node.text.split(extracted_link_text, 1)))
    
    node_one = TextNode(parted_array[0], TextType.PLAIN)
    type = TextType.IMAGE if is_image else TextType.LINK
    node_two = TextNode(extracted_link[0], type, extracted_link[1])
    if len(parted_array) > 1:
      node_three = split_nodes_link([TextNode(parted_array[1], TextType.PLAIN)], is_image)
      new_nodes.extend([node_one, node_two])
      new_nodes.extend(node_three)
    else:
      new_nodes.extend([node_one, node_two])

  return new_nodes

def text_to_textnodes(text):
  if (isinstance(text, str) == False):
    raise Exception("Text needs to be a string!")
  node = TextNode(text, TextType.PLAIN)
  bold = split_nodes_delimiter([node], '**', TextType.BOLD)
  italic = split_nodes_delimiter(bold, '_', TextType.ITALIC)
  code = split_nodes_delimiter(italic, '`', TextType.CODE)
  is_image = True
  image = split_nodes_link(code, is_image)
  link = split_nodes_link(image)
  return link


def get_heading_tag(heading):
  count = heading.count('*')
  return f"h{count}"