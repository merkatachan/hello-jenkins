from django import forms

class loginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=50)
	password = forms.CharField(label='Password',
		widget=forms.PasswordInput, max_length=50)

class passwordResetForm(forms.Form):
	email = forms.CharField(label='Enter Your Email', max_length=100)

class passwordResetActivationForm(forms.Form):
	email = forms.CharField(label='Your Email Address', max_length=100)
	activationCode = forms.CharField(label='Reset Activation Code', max_length=100)

class confirmPasswordForm(forms.Form):
	newPW = forms.CharField(label='Enter Your New Password',
		widget=forms.PasswordInput, max_length=50)
	confirmPW = forms.CharField(label='Confirm Password',
		widget=forms.PasswordInput, max_length=50)
