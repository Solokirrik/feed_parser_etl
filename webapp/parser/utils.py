import re
from typing import Dict
from collections import defaultdict
import xml.etree.ElementTree as ET


def remove_htmltags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', text)


def etree2dict(tree: ET.Element) -> Dict:
    if '{' in tree.tag and '}' in tree.tag:
        namespace = "{" + tree.tag.partition("{")[2].partition("}")[0] + "}"
    else:
        namespace = ''
    tag_name = tree.tag[len(namespace):]
    tree_dict = {tag_name: {} if tree.attrib else None}
    childrens = list(tree)
    if childrens:
        def_dict = defaultdict(list)
        for dchild in map(etree2dict, childrens):
            for key, val in dchild.items():
                def_dict[key].append(val)
        tree_dict = {tag_name: {key: val[0] if len(val) == 1 else val for key, val in def_dict.items()}}
    if tree.attrib:
        tree_dict[tag_name].update(('@' + key, val) for key, val in tree.attrib.items())
    if tree.text:
        text = tree.text.strip()
        if childrens or tree.attrib:
            if text:
                tree_dict[tag_name]['#text'] = text
        else:
            tree_dict[tag_name] = text
    return tree_dict
