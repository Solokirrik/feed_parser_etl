from http import HTTPStatus
from parser.base import etl_builder, ETLProcess, HTTPExtractor
from django.http.response import HttpResponse
from target_habr.habr import HabrTransformer, HabrLoader


def habr_loader(request):
    try:
        builder = etl_builder(ETLProcess, HTTPExtractor("https://habrahabr.ru/rss/hubs/all/"),
                              HabrTransformer(), HabrLoader())
        builder.start()
        return HttpResponse(status=HTTPStatus.OK)
    except:
        return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)
