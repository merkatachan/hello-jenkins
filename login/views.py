from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from .forms import *
from setup.models import tblUsers
import random, string

from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def index(request):
	# return render(request, 'login/login.html')
	form_class = loginForm
	if request.method == 'POST':

		form = loginForm(request.POST)

		if form.is_valid():
			# company = request.POST.get('companyName', '')
			# address = request.POST.get('address', '')
			# city = request.POST.get('city', '')
			# province = request.POST.get('province', '')
			# country = request.POST.get('country', '')
			# postalCode = request.POST.get('postalCode', '')
			# phone = request.POST.get('phone', '')
			# dateAdded = timezone.localtime(timezone.now())

			username = request.POST.get('username', '')
			password = request.POST.get('password', '')

			# Check username exists
			try:
				match = tblUsers.objects.get(username=username)
			except tblUsers.DoesNotExist:
				match = None
			if (match is None):
				return render(request, "login/login.html", {'form': form_class,
					'errorMsg': 'Login credentials incorrect. Please try again.'})

			# Next, password verification
			if (password != match.password):
				return render(request, "login/login.html", {'form': form_class,
					'errorMsg': 'Login credentials incorrect. Please try again.'})

			# Getting here means password verified.
			# Update last login timestamp.
			# Establish an active session with this account.
			match.lastLogin = timezone.localtime(timezone.now())
			match.save()

			request.session['username'] = match.username
			request.session['firstname'] = match.firstName
			request.session['userID'] = str(match.userID)
			request.session['mineID'] = str(match.mineID)
			request.session.set_expiry(0)

			return render(request, 'login/success.html', { }) #Redirect

		form_class = loginForm
		return render_to_response("login/login.html", {'form': form_class})

	else:
		return render(request, "login/login.html", {'form': form_class})


def passwordReset(request):
	form_class = passwordResetForm
	if request.method == "POST":
		form = passwordResetForm(request.POST)

		if form.is_valid():
			email = request.POST.get('email', '')

			# Check email exists
			try:
				match = tblUsers.objects.get(email=email)
			except tblUsers.DoesNotExist:
				match = None
			if (match is None):
				return render(request, "login/passwordReset.html", {'form': form_class,
					'errorMsg': 'No account associated with this email was found. Please try again.'})

			resetCode = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
			resetExpiry = timezone.localtime(timezone.now()) + timedelta(days=3)

			host = request.get_host()
			firstName = match.firstName
			msgRecipients = [match.email]
			msgSender = "admin@magemi.com"
			msgSubject = "Magemi Mine Optimizer: Account Password Reset"
			msgBody = "Hi, " + firstName + ". We have received your password reset request. Your 6-digit activation code is " + resetCode + ". Please click here to begin the reset process: http://" + host + "/PasswordResetActivation" + "\n\nYour activation code expires in 3 days."

			match.reset = resetCode
			match.resetExpiry = resetExpiry
			match.save()

			send_mail(msgSubject, msgBody, settings.DEFAULT_FROM_EMAIL, msgRecipients, fail_silently=False)
			return render(request, "login/passwordEmailSent.html", {})
	else:
		return render(request, "login/passwordReset.html", {'form': form_class})


def passwordResetActivation(request):
	if request.method == "POST":
		form = passwordResetActivationForm(request.POST)
		if form.is_valid():
			email = request.POST.get('email', '')
			activationCode = request.POST.get('activationCode', '')

			# Check email exists
			try:
				match = tblUsers.objects.get(email=email)
			except tblUsers.DoesNotExist:
				match = None
			if (match is None):
				return render(request, "login/passwordResetActivation.html", {'form': form_class,
					'errorMsg': 'No account associated with this email was found. Please try again.'})

			# Check activation code is correct
			if match.reset != activationCode:
				return render(request, "login/passwordResetActivation.html", {'form': form_class,
					'errorMsg': 'Activation Code incorrect. Please try again.'})

			# Check activation code has not expired
			if match.resetExpiry < timezone.localtime(timezone.now()):
				return render(request, "login/passwordResetActivation.html", {'form': form_class,
					'errorMsg': 'Your activation code has expired. Please request for another password reset.'})

			form_class = confirmPasswordForm
			return render(request, "login/confirmPassword.html", {'form': form_class, 'email': email})
	else:
		form_class = passwordResetActivationForm
		return render(request, "login/passwordResetActivation.html", {'form': form_class})

def confirmPassword(request):
	form_class = confirmPasswordForm
	if request.method == "POST":
		form = confirmPasswordForm(request.POST)

		if form.is_valid():
			newPW = request.POST.get('newPW', '')
			confirmPW = request.POST.get('confirmPW', '')
			email = request.POST.get('email', '')

			# Check password and confirmPW fields are equal
			if newPW != confirmPW:
				return render(request, "login/confirmPassword.html", {'form': form_class,
					'errorMsg': 'Password and Confirm Password fields did not match. Please try again.',
					'email': email})

			match = tblUsers.objects.get(email=email)
			match.password = newPW
			match.save()

			return render(request, 'login/confirmPasswordSuccess.html', { }) #Redirect
	else:
		return render(request, 'login/confirmPassword.html', {'form': form_class})
