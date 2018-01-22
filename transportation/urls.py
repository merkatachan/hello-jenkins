from django.conf.urls import url
from . import views

app_name = 'transportation'

urlpatterns = [
	url(r'^$', views.index, name='index')
]
