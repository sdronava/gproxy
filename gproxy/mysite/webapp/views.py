# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import requests
import pprint
import json
from googleapiclient.discovery import build
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os
#from webapp import fileiterwrapper

# Create your views here.
def index(request):

    #1. Parse out the search token.
    token = request.path_info.split('/', 1)[1] 

    return (search(token))

def search(token):
    print ("*****request****:",token)

    #Root page handler.
    if not token:
       return HttpResponse("Welcome to Proxy Search Page")

    #1. Get cached page from memory hash
    #  ....
    #TODO: Add Redis or some memory based cache manager to get a cached path
    #      Also need to have an evict policy of both the memory cache and the
    #      cached file. Need a cachemanger + shared storage
    #      Shared storage - with docker swarm/docker stack for scaling.
    #      This is an app in itself.
    
    #Do the search
    resJson = search3(token) #Note this is a json object

    #Cache file.
    #cachepath = cacheWrite(resJson, token)
    #Load the response - right now is a pretty print of the google api search result.
    #return HttpResponse(FileIterWrapper(open(cachepath)), content_type="application/json")
    
    return HttpResponse(resJson, content_type="application/json")

    

def cacheWrite(response, token):
    cachepath = "cache/" + token 
    file = open(cachepath, "w+")
    file.write(response)
    file.close()
    return cachepath


#TODO: The keys should not be in the code hard-coded. 
#      Right now, enabled bose as one of the words that can be searched as an example
#Sample code courtesy: https://github.com/google/google-api-python-client/blob/master/samples/customsearch/main.py
def search3(token):
    pprint.pprint(token)

    #TODO - Use google service account and GOOGLE_APPLICATION_CREDENTIALS 
    #https://cloud.google.com/docs/authentication/getting-started
    service = build("customsearch", "v1", developerKey="SECRET")

    pprint.pprint(type(service))
    res = service.cse().list(
          q=token,
          cx='011651463339030237912:enjmhlpz0zu',
    ).execute()
    pprint.pprint(type(res))
    return json.dumps(res, indent=4)




#Courtesy: https://metalinguist.wordpress.com/2008/02/12/django-file-and-stream-serving-performance-gotcha/
class FileIterWrapper(object):
  def __init__(self, flo, chunk_size = 1024**2):
    self.flo = flo
    self.chunk_size = chunk_size

  def next(self):
    data = self.flo.read(self.chunk_size)
    if data:
      return data
    else:
      raise StopIteration

  def __iter__(self):
    return self

####################################   Unused stuff #######################################

# def cacheRead(path):
#     f = open(path, 'r')
#     out = f.read()
#     f.close()
#     return out

# # This is a no go. Google does not allow this. Redirect will work but breaks the assumption of the problem.
# # Client cannot access google.
# def search2(token):
#     print ("*****request****:",token)
#     URL = "http://www.google.com/search?q=" + token
#     return HttpResponse(FileIterWrapper(open('mysite/cache/123.htm')))



    # URL = "http://www.google.com/search"
    # PARAMS = {'q':token}
    # response = requests.get(url = URL, params = PARAMS)
    # print ("**** response ****:", response.status_code, response.headers['Content-Type'])
    # cachepath = cacheWrite(response, token)
    # print ("Response Content:", type(response.content))
    # django_response = HttpResponse(
    #     content=response.content,
    #     #content=cacheRead(cachepath),
    #     status=response.status_code,                     #This needs to be cached
    #     content_type=response.headers['Content-Type']    #This needs to be cached
    # )
    #return django_response
    #return HttpResponse("I am ok")
