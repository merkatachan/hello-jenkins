from django.conf.urls import url
from . import views

app_name = 'settings'

urlpatterns = [
	url(r'^commodities$', views.editCommodities, name='editCommodities'),
	url(r'^minePlan$', views.editMinePlan, name='editMinePlan'),
	url(r'^products$', views.editProject, name='editProject'),
    url(r'^(?i)CAPEX$', views.editCAPEX, name='editCAPEX'),
    url(r'^(?i)OPEX$', views.editOPEX, name='editOPEX'),
	url(r'^smelter$', views.editSmelter, name='editSmelter'),
	url(r'^prices$', views.editPrices, name='editPrices'),
	url(r'^inputs$', views.editInputs, name='editInputs'),
]
