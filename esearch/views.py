from django.shortcuts import render
from django.http import JsonResponse
from esearch.search import search_es, search_contain, search_full_text_index
import json
# Create your views here.
def index(request):
    msg = 'My Message'
    return render(request, 'index.html', {'message' : msg})

def search(request, search_content):
    return JsonResponse(search_es(search_content), safe=False, json_dumps_params={'ensure_ascii': False})

def searchcontain(request, search_content):
    return JsonResponse(search_contain(search_content), safe=False, json_dumps_params={'ensure_ascii': False})

def searchfulltextindex(request, search_content):
    return JsonResponse(search_full_text_index(search_content), safe=False, json_dumps_params={'ensure_ascii': False})