from django.conf.urls import url
from . import views

app_name = 'setup'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^step2$', views.index2, name='index2'),
	url(r'^step3$', views.index3, name='index3'),
	url(r'^step4$', views.index4, name='index4'),
	url(r'^step5$', views.index5, name='index5'),
	url(r'^step6$', views.index6, name='index6'),
	url(r'^step7$', views.index7, name='index7'),
	url(r'^step8$', views.index8, name='index8'),
	url(r'^step9$', views.index9, name='index9'),
	url(r'^step10$', views.index10, name='index10')
]
