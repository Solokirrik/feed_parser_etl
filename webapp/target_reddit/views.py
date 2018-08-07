from http import HTTPStatus
from parser.base import etl_builder, ETLProcess, HTTPExtractor
from django.http.response import HttpResponse
from target_reddit.reddit import RedditTransformer, RedditLoader


def reddit_loader(request):
    try:
        builder = etl_builder(ETLProcess, HTTPExtractor("https://www.reddit.com/r/news/.rss"),
                              RedditTransformer(), RedditLoader())
        builder.start()
        return HttpResponse(status=HTTPStatus.OK)
    except:
        return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)
