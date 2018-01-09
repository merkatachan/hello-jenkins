from django.conf.urls import url
from . import views

app_name = 'mine'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	# url(r'^optimize$', views.index2, name='index2'),
	# url(r'^overwrite$', views.index3, name='index3')
]
