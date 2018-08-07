from typing import List, Tuple
from datetime import datetime
import xml.etree.ElementTree as ET

from parser.base import Transformer, Loader
from parser.utils import etree2dict, remove_htmltags
import requests
from target_habr.models import Category, Creator, Post


class HabrTransformer(Transformer):
    def transform(self, content: requests.Response) -> List[Tuple[Creator, List[Category], Post]]:
        models_list = []
        tree = ET.fromstring(content.text)
        tree_dict = etree2dict(tree)

        for item in tree_dict['rss']['channel']['item']:
            categories = []
            for category in item['category']:
                categories.append(Category(label=category))
            creator = Creator(name=item['creator'])
            post = Post(id=list(filter(lambda x: x != '', item['guid']['#text'].split('/')))[-1],
                        title=item['title'],
                        guid=item['guid']['#text'],
                        link=item['link'],
                        description=remove_htmltags(item['description']),
                        pub_date=datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S %Z"),
                        creator=creator,
                        )
            models_list.append((creator, categories, post))
        return models_list

class HabrLoader(Loader):
    def load(self, content: List[Tuple[Creator, List[Category], Post]]):
        for creator, categories, post in content:
            creator.save()
            post.save()
            for category_item in categories:
                category_item.save()
            post.category.add(*categories)
