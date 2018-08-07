import requests

AGENT_DEF = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/603.1.13 (KHTML, like Gecko) Version/10.1 "
             "Safari/603.1.13")


class Extractor:
    def extract(self):
        raise NotImplementedError(self.__class__.__name__)


class HTTPExtractor(Extractor):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def extract(self) -> requests.Response:
        session = requests.Session()
        session.headers.update({'User-Agent': AGENT_DEF})
        return session.get(self.url)


class Transformer:
    def transform(self, content: requests.Response):
        raise NotImplementedError(self.__class__.__name__)


class Loader:
    def load(self, content):
        raise NotImplementedError(self.__class__.__name__)


class BaseETLProcess:
    def start(self):
        raise NotImplementedError(self.__class__.__name__)


class ETLProcess(BaseETLProcess):
    def __init__(self, extractor: Extractor, transformer: Transformer, loader: Loader):
        super().__init__()
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def start(self):
        content = self.extractor.extract()
        content = self.transformer.transform(content)
        self.loader.load(content)


def etl_builder(process, extractor: Extractor, transformer: Transformer, loader: Loader):
    return process(extractor, transformer, loader)
