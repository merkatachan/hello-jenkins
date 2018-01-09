from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from formtools.wizard.views import SessionWizardView

from .forms import companyForm, mineForm, signUpForm
from setup.models import tblCompany, tblMine, tblUsers

FORMS = [("company", companyForm),
		 ("mine", mineForm),
		 ("user", signUpForm)]

TEMPLATES = {"company": "signup/block_signup.html",
			 "mine": "signup/block_signup2.html",
			 "user": "signup/block_signup3.html"}

# Create your views here.
def registerCompany(request):
	if request.method == 'POST':

		form = companyForm(request.POST)

		if form.is_valid():
			# company = request.POST.get('companyName', '')
			# address = request.POST.get('address', '')
			# city = request.POST.get('city', '')
			# province = request.POST.get('province', '')
			# country = request.POST.get('country', '')
			# postalCode = request.POST.get('postalCode', '')
			# phone = request.POST.get('phone', '')
			# dateAdded = timezone.localtime(timezone.now())

			cleanData = form.cleaned_data
			request.session["companyName"] = cleanData["companyName"]
			request.session["companyAddress"] = cleanData["address"]
			request.session["companyCity"] = cleanData["city"]
			request.session["companyProvince"] = cleanData["province"]
			request.session["companyCountry"] = cleanData["country"]
			request.session["companyPostalCode"] = cleanData["postalCode"]
			request.session["companyPhone"] = cleanData["phone"]

			# companyObj = tblCompany(company=company, address=address, 
			# 	city=city, province=province, country=country, 
			# 	postalCode=postalCode, phone=phone, dateAdded=dateAdded)
			# companyObj.save()

			next_form_class = mineForm
			return render(request, 'signup/signup2.html', {'form': next_form_class,
				'company_registered':True}) #Redirect
			# return render(request, 'signup/signup2.html', {'form': next_form_class,
			# 	'company_registered':True,
			# 	'companyID': companyObj.companyID }) #Redirect

		# form_class = companyForm
		# return render(request, "signup/signup.html", {'form': form_class})

	else:
		form_class = companyForm
		return render(request, "signup/signup.html", {'form': form_class})


def registerMine(request):
	if request.method == 'POST':

		form = mineForm(request.POST)

		if form.is_valid():
			# mine = request.POST.get('mineName', '')
			# address = request.POST.get('address', '')
			# city = request.POST.get('city', '')
			# province = request.POST.get('province', '')
			# country = request.POST.get('country', '')
			# postalCode = request.POST.get('postalCode', '')
			# phone = request.POST.get('phone', '')
			# dateAdded = timezone.localtime(timezone.now())

			# companyID = request.POST.get('companyID', '')

			cleanData = form.cleaned_data
			request.session["mineName"] = cleanData["mineName"]
			request.session["mineAddress"] = cleanData["address"]
			request.session["mineCity"] = cleanData["city"]
			request.session["mineProvince"] = cleanData["province"]
			request.session["mineCountry"] = cleanData["country"]
			request.session["minePostalCode"] = cleanData["postalCode"]
			request.session["minePhone"] = cleanData["phone"]

			# mineObj = tblMine(mine=mine, address=address, 
			# 	city=city, province=province, country=country, fax=None, 
			# 	postalCode=postalCode, phone=phone, dateAdded=dateAdded)
			# mineObj.save()

			next_form_class = signUpForm()
			return render(request, 'signup/signup3.html', {'form': next_form_class,  
				'mine_registered':True}) #Redirect
			# return render(request, 'signup/signup3.html', {'form': next_form_class, 
			# 	'companyID': companyID,
			# 	'mineID': mineObj.mineID, 
			# 	'mine_registered':True}) #Redirect

		# form_class = mineForm
		# return render(request, "signup/signup2.html", {'form': form_class})

	else:
		form_class = mineForm
		return render(request, "signup/signup2.html", {'form': form_class})


def registerUser(request):
	# return render_to_response("signup/signup3.html", RequestContext(request, {}))
	if request.method == 'POST':

		form = signUpForm(request.POST)
		form_class = signUpForm

		if form.is_valid():
			# username = forms.CharField(label='Username', max_length=50)
			# password = forms.CharField(label='Password', max_length=50)
			# confirmPW = forms.CharField(label='Confirm Password', max_length=50)
			# firstName = forms.CharField(label='First Name', max_length=50)
			# lastName = forms.CharField(label='Last Name', max_length=50)
			# email = forms.CharField(label='Email', max_length=100)
			# phone = forms.CharField(label='Phone', max_length=32)
			# jobTitle = forms.CharField(label='Job Title', max_length=50)

			# username = request.POST.get('username', '')
			# password = request.POST.get('password', '')
			# confirmPW = request.POST.get('confirmPW', '')
			# firstName = request.POST.get('firstName', '')
			# lastName = request.POST.get('lastName', '')
			# email = request.POST.get('email', '')
			# phone = request.POST.get('phone', '')
			# jobTitle = request.POST.get('jobTitle', '')
			# dateAdded = timezone.localtime(timezone.now())

			# companyID = int(request.POST.get('companyID', ''))
			# company = tblCompany.objects.get(companyID=companyID)

			# mineID = int(request.POST.get('mineID', ''))
			# mine = tblMine.objects.get(mineID=mineID)

			cleanData = form.cleaned_data
			username = cleanData["username"]
			password = cleanData["password"]
			confirmPW = cleanData["confirmPW"]
			firstName = cleanData["firstName"]
			lastName = cleanData["lastName"]
			email = cleanData["email"]
			phone = cleanData["phone"]
			jobTitle = cleanData["jobTitle"]
			dateAdded = timezone.localtime(timezone.now())

			# Check username is unique
			try:
				dup = tblUsers.objects.get(username=username)
			except tblUsers.DoesNotExist:
				dup = None
			if (dup is not None):
				return render(request, "signup/signup3.html", {'form': form_class,
					'errorMsg': 'Username has been taken. Please try another one.',
					'firstName': firstName,
					'lastName': lastName,
					'email': email,
					'phone': phone,
					'jobTitle': jobTitle,
					'companyID': companyID,
					'mineID': mineID, 
					'mine_registered':True})

			# Check email is unique
			try:
				emailDup = tblUsers.objects.get(email=email)
			except tblUsers.DoesNotExist:
				emailDup = None
			if (emailDup is not None):
				return render(request, "signup/signup3.html", {'form': form_class,
					'errorMsg': 'The email address has been used already. Please try another one.',
					'firstName': firstName,
					'lastName': lastName,
					'email': email,
					'phone': phone,
					'jobTitle': jobTitle,
					'companyID': companyID,
					'mineID': mineID, 
					'mine_registered':True})

			# Check password and confirmPW fields are equal
			if password != confirmPW:
				return render(request, "signup/signup3.html", {'form': form_class,
					'errorMsg': 'Password and Confirm Password fields did not match. Please try again.',
					'firstName': firstName,
					'lastName': lastName,
					'email': email,
					'phone': phone,
					'jobTitle': jobTitle,
					'companyID': companyID,
					'mineID': mineID, 
					'mine_registered':True})

			companyObj = tblCompany(company=request.session["companyName"], address=request.session["companyAddress"], 
				city=request.session["companyCity"], province=request.session["companyProvince"],
				country=request.session["companyCountry"], postalCode=request.session["companyPostalCode"], 
				phone=request.session["companyPhone"], dateAdded=dateAdded)
			companyObj.save()

			mineObj = tblMine(mine=request.session["mineName"], address=request.session["mineAddress"], 
				city=request.session["mineCity"], province=request.session["mineProvince"],
				country=request.session["mineCountry"], fax=None, postalCode=request.session["minePostalCode"], 
				phone=request.session["minePhone"], dateAdded=dateAdded)
			mineObj.save()

			userObj = tblUsers(username=username, password=password,
				companyID=companyObj, mineID=mineObj, firstName=firstName,
				lastName=lastName, email=email, phone=phone,
				jobTitle=jobTitle, dateAdded=dateAdded, userRole=1)
			userObj.save()

			request.session.flush()
			return render(request, 'signup/success.html', { }) #Redirect

		return render_to_response("signup/signup3.html", {'form': form_class})

	else:
		form_class = signUpForm
		return render(request, "signup/signup3.html", {'form': form_class})


class SignupWizard(SessionWizardView):
	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	def done(self, form_list, **kwargs):
		return render(request, 'signup/success.html', { }) #Redirect
