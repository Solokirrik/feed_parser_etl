from django.utils.crypto import get_random_string
from random import randint
from datetime import datetime
import pytest
import pytz
from unittest.mock import patch
from target_habr.habr import HabrTransformer, HabrLoader
from target_habr.models import Category, Creator, Post


@pytest.fixture
def data_dict():
    posts_n = 20
    creators_n = 10
    categories_n = 30
    creators = [get_random_string(length=randint(5, 50)) for _ in range(creators_n)]
    categories = [get_random_string(length=randint(5, 30)) for _ in range(categories_n)]
    generated_posts = []
    for _ in range(posts_n):
        post_id = randint(10 ** 8, 10 ** 9 - 1)
        post_categories = (categories[randint(0, categories_n - 1)] for _ in range(7))
        generated_datetime = datetime.fromtimestamp(randint(8 * 10 ** 8, 15 * 10 ** 8))
        generated_posts.append({
            "title": get_random_string(length=randint(50, 250)),
            "guid": {
                "@isPermaLink": "true",
                "#text": f"https://habr.com/post/{post_id}/"
            },
            "link": f"https://habr.com/{post_id}?utm_campaign={post_id}",
            "description": get_random_string(length=randint(50, 2 * 10 ** 3 - 1)),
            "pubDate": pytz.utc.localize(generated_datetime).strftime("%a, %d %b %Y %H:%M:%S %Z"),
            "creator": creators[randint(0, creators_n - 1)],
            "category": list(post_categories)
        })

    return {"rss": {"channel": {"item": generated_posts}}}


@pytest.fixture
def content():
    posts_n = 3
    creators_n = 3
    categories_n = 10
    generated_pack = []
    creators = [get_random_string(length=randint(5, 50)) for _ in range(creators_n)]
    categories = [get_random_string(length=randint(5, 30)) for _ in range(categories_n)]
    for _ in range(posts_n):
        post_id = randint(10 ** 8, 10 ** 9 - 1)
        generated_datetime = datetime.fromtimestamp(randint(8 * 10 ** 8, 15 * 10 ** 8))

        creator = Creator(name=creators[randint(0, creators_n - 1)])
        post_categories = [Category(label=categories[randint(0, categories_n - 1)]) for _ in range(7)]
        post = Post(id=post_id,
                    title=get_random_string(length=randint(50, 250)),
                    guid=f"https://habr.com/post/{post_id}/",
                    link=f"https://habr.com/{post_id}?utm_campaign={post_id}",
                    description=get_random_string(length=randint(50, 2 * 10 ** 3 - 1)),
                    pub_date=pytz.utc.localize(generated_datetime),
                    creator=creator)
        generated_pack.append((creator, post_categories, post))
    return generated_pack


@patch("target_habr.habr.etree2dict", autospec=True)
@patch("requests.Response", autospec=True)
def test_transform(resp_moc, et2dict_moc, data_dict):
    et2dict_moc.return_value = data_dict
    easy_xml = '<feed></feed>'
    resp_moc.text = easy_xml
    transformed = HabrTransformer().transform(content=resp_moc)
    for ind, (creator, categories, post) in enumerate(transformed):
        item = data_dict['rss']['channel']['item'][ind]
        assert item['creator'] == creator.name
        assert item['creator'] == post.creator.name
        assert item['category'] == [cat.label for cat in categories]
        assert item['description'] == post.description
        assert item['guid']['#text'] == post.guid
        assert item['title'] == post.title


@pytest.mark.django_db
def test_load(content):
    _ = HabrLoader().load(content)
    for creator, categories, post in content:
        assert Post.objects.filter(id=post.id).exists()
        post_cats = Post.objects.filter(id=post.id).values_list('category__label', flat=True)
        assert set([cat.label for cat in categories]) == set(post_cats)
        assert Creator.objects.filter(name=creator.name).exists()
        assert creator.name == Post.objects.filter(id=post.id).get().creator.name
