from django.conf.urls import url
from . import views

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	url(r'^iso', views.iso, name = 'iso'),
	url(r'^$', views.calc, name='calc'),
]