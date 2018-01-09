from django.conf.urls import url
from . import views
from .forms import companyForm, mineForm, signUpForm

app_name = 'signup'

# FORMS = [("company", companyForm),
# 		 ("mine", mineForm),
# 		 ("user", signUpForm)]

# FORMS = [companyForm, mineForm, signUpForm]

urlpatterns = [
	url(r'^$', views.registerCompany, name='registerCompany'),
	url(r'^step2$', views.registerMine, name='registerMine'),
	url(r'^step3$', views.registerUser, name='registerUser'),
	# url(r'^$', views.SignupWizard.as_view(FORMS)),
]
