from typing import List, Tuple
from datetime import datetime
import xml.etree.ElementTree as ET

from parser.base import Transformer, Loader
from parser.utils import etree2dict
import requests
from target_reddit.models import Author, Category, Post


class RedditTransformer(Transformer):
    @staticmethod
    def updated_to_datetime(updated_at: str) -> datetime:
        return datetime.strptime(updated_at[:-3] + updated_at[-2:], "%Y-%m-%dT%H:%M:%S%z")

    def transform(self, content: requests.Response) -> List[Tuple[Author, Category, Post]]:
        models_list = []
        tree = ET.fromstring(content.text)
        tree_dict = etree2dict(tree)

        for entry in tree_dict['feed']['entry']:
            author = Author(**entry['author'])
            category = Category(**{key[1:]: val for key, val in entry['category'].items()})
            post = Post(updated_at=self.updated_to_datetime(entry['updated']),
                        id=entry['id'],
                        link=entry['link']['@href'],
                        author=author,
                        category=category,
                        title=entry['title'],
                        )
            models_list.append((author, category, post))
        return models_list


# pylint: disable=arguments-differ
class RedditLoader(Loader):
    def load(self, batch: List[Tuple[Author, Category, Post]]):
        for pack in batch:
            for model in pack:
                model.save()
