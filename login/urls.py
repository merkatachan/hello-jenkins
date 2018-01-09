from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^PasswordReset$', views.passwordReset, name='passwordReset'),
	url(r'^PasswordResetActivation$', views.passwordResetActivation, name='passwordResetActivation'),
	url(r'^ConfirmPassword$', views.confirmPassword, name='confirmPassword')
]
