from django.utils.crypto import get_random_string
from random import randint
from datetime import datetime
import pytest
import pytz
from unittest.mock import patch
from target_reddit.reddit import RedditTransformer


@pytest.fixture
def data_dict():
    posts_n = 3
    creators_n = 5
    categories_n = 5
    authors = [get_random_string(length=randint(5, 50)) for _ in range(creators_n)]
    categories = [get_random_string(length=randint(5, 30)) for _ in range(categories_n)]
    generated_posts = []
    for _ in range(posts_n):
        author = authors[randint(0, creators_n - 1)]
        category = categories[randint(0, categories_n - 1)]
        generated_datetime = datetime.fromtimestamp(randint(8 * 10 ** 8, 15 * 10 ** 8))
        timestring = pytz.utc.localize(generated_datetime).strftime("%Y-%m-%dT%H:%M:%S%z")
        generated_posts.append(
            {'author': {'name': author,
                        'uri': f'https://www.reddit.com/user/{author}',
                        },
             'category': {'@term': f'term{category}',
                          '@label': f'r/{category}'
                          },
             'id': get_random_string(length=9),
             'link': {'@href': f"https://www.reddit.com/{get_random_string(length=randint(20, 50))}"},
             'updated': timestring[:-2] + ':' + timestring[-2:],
             'title': get_random_string(length=randint(50, 250))
             }
        )
    return {'feed': {'entry': generated_posts}}


@patch("target_reddit.reddit.etree2dict", autospec=True)
@patch("requests.Response", autospec=True)
def test_transformer(resp_moc, et2dict_moc, data_dict):
    et2dict_moc.return_value = data_dict
    easy_xml = '<feed></feed>'
    resp_moc.text = easy_xml
    transformed = RedditTransformer().transform(content=resp_moc)
    for ind, (author, category, post) in enumerate(transformed):
        entry = data_dict['feed']['entry'][ind]
        assert entry['id'] == post.id
        assert entry['title'] == post.title
        assert entry['link']['@href'] == post.link
        assert entry['author']['name'] == post.author.name
        assert entry['author']['uri'] == author.uri
        assert entry['author']['name'] == author.name
        assert entry['category']['@label'] == post.category.label
        assert entry['category']['@term'] == category.term
        assert entry['category']['@label'] == category.label
