from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'm2', views.main2, name = 'main2'), 
	url(r'^$', views.index, name='index'),
]