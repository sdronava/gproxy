from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^.*$', views.cache, name='cache'),
    url(r'^.*$', views.index, name='index'),
    #url(r'^abcd$', views.search, name='search'),
]