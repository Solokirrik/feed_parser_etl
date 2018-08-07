from unittest.mock import patch
import pytest
from http import HTTPStatus
from parser.base import (Extractor, Transformer, Loader, BaseETLProcess, HTTPExtractor, ETLProcess, etl_builder)


@patch('requests.Session.get')
def test_httpextractor(get_mock):
    test_text = 'test_text'
    test_url = "https://ya.ru"
    mock = get_mock.return_value
    mock.text = test_text
    mock.status_code = HTTPStatus.OK
    assert test_text == HTTPExtractor(test_url).extract().text


def test_extractor_exc():
    with pytest.raises(NotImplementedError):
        Extractor().extract()

@patch('requests.Response')
def test_transformer_exc(resp_mock):
    with pytest.raises(NotImplementedError):
        Transformer().transform(resp_mock)


def test_loader_exc():
    with pytest.raises(NotImplementedError):
        Loader().load([])


def test_baseetlprocess_exc():
    with pytest.raises(NotImplementedError):
        BaseETLProcess().start()


class ExtractTest(Extractor):
    def __init__(self, test_content):
        self.test_content = test_content

    def extract(self):
        return self.test_content

class TransformTest(Transformer):
    def transform(self, content):
        return content


class LoadTest(Loader):
    def load(self, content):
        self.saved = content

def test_etl_builder():
    test_str = 'totallynotteststr'
    loader = LoadTest()
    etl_builder(ETLProcess, ExtractTest(test_str), TransformTest(), loader).start()
    assert test_str == loader.saved
