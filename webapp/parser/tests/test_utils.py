from random import randint
import pytest
from django.utils.crypto import get_random_string
from parser.utils import etree2dict, remove_htmltags
import xml.etree.ElementTree as ET


@pytest.fixture
def data_dict():
    return {'title': 'test_dict',
            'entry': [
                {'author': {'name': 'Alice',
                            'uri': 'https://alice.com'},
                 'category': {'@term': 'crypto',
                              '#text': 'totallynottesttext#1'},
                 'id': '1',
                 'updated': '2018-03-08T01:06:26+0300',
                 'title': 'totallynottesttitle#1'
                 },
                {'author': {'name': 'Bob',
                            'uri': 'http://bob.com'},
                 'category': {'@term': 'crypto',
                              '#text': 'totallynottesttext#2'},
                 'id': '2',
                 'updated': '2018-08-08T10:10:00-0500',
                 'title': 'totallynottesttitle#2'
                 }, ]
            }


def dict2xml(data_dict, root_node=None):
    wrap = False if root_node is None or isinstance(data_dict, list) else True
    root = 'objects' if root_node is None else root_node
    root_singular = root[:-1] if root.endswith('s') and root_node is None else root
    xml = ''
    children = []

    if isinstance(data_dict, dict):
        for key, value in data_dict.items():
            if isinstance(value, dict) or isinstance(value, list):
                children.append(dict2xml(value, key))
            else:
                if key.startswith('@'):
                    xml += f' {key[1:]}="{value}"'
                elif key == '#text':
                    xml += f'>{value}'
                else:
                    xml += f'<{key}>{value}</{key}>'
    else:
        for value in data_dict:
            children.append(dict2xml(value, root_singular))

    if wrap or isinstance(data_dict, dict):
        end_tag = '' if len(children) > 0 else f'</{root}>'
        if xml.startswith('<'):
            xml = f'<{root}>{xml}{end_tag}'
        else:
            xml = f'<{root} {xml}{end_tag}'

    if len(children) > 0:
        for child in children:
            xml = xml + child

        if wrap or isinstance(data_dict, dict):
            xml += f'</{root}>'

    return xml


def test_remove_htmltags():
    test_pack = []
    for _ in range(3):
        test_pack.append((get_random_string(length=randint(1, 16)), f'<{get_random_string(length=randint(1, 6))}>'))
    test_str = ''.join(text + tag for text, tag in test_pack)
    assert ''.join(text for text, _ in test_pack) == remove_htmltags(test_str)


def test_etree2dict(data_dict):
    assert {'feed': data_dict} == etree2dict(ET.fromstring(dict2xml(data_dict, 'feed')))
