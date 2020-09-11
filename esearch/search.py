from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Keyword, Text, Integer, Date, Search, Q
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models
from django.db.models import Q as Query
from django.core import serializers
import time

connections.create_connection(hosts=['localhost'])

class NewaraIndex(Document):
    id = Integer()
    created_at = Date()
    updated_at = Date()
    deleted_at = Date()
    commented_at = Date()
    title = Text()
    content = Text()
    content_text = Text()
    is_anonymous = Integer()
    is_content_sexual = Integer()
    is_content_social = Integer()
    positive_vote_count = Integer()
    negative_vote_count = Integer()
    created_by_id = Integer()
    parent_board_id = Integer()
    parent_topic_id = Integer()
    url = Text()

    class Index:
        name = 'newara-index'

def bulk_indexing():
    NewaraIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.core_article.objects.all().iterator()))


def search_es(content_text):
    start = time.time()
    s = Search().filter(Q("match", content_text=content_text) | Q("match", title=content_text))
    response = s.execute()
    print(response.hits.total)
    # print(response.hits))
    result = response.to_dict()
    result["time"] = time.time() - start;
    return result

def search_contain(content_text):
    start = time.time()
    objects = models.core_article.objects.all().filter(Query(content_text__contains=content_text) | Query(title__contains=content_text)).values()
    print(len(objects))
    print("time :", time.time() - start)
    return [time.time() - start] + [len(objects)] + list(objects)[:100]

def search_full_text_index(content_text):
    start = time.time()
    objects = models.core_article.objects.all().filter(Query(title__search=content_text) | Query(content_text__search=content_text)).values()
    print(len(objects))
    print("time :", time.time() - start)
    return [time.time() - start] + [len(objects)] + list(objects)[:100]
