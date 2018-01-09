from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class mineForm(forms.Form):
	mineName = forms.CharField(label='Mine name', max_length=100)
	# companyName = forms.CharField(label='Company', max_length=250)
	address = forms.CharField(label='Address', max_length=250)
	city = forms.CharField(label='City', max_length=100)
	province = forms.CharField(label='Province', max_length=50)
	country = forms.CharField(label='Country', max_length=50)
	postalCode = forms.CharField(label='Postal Code', max_length=10)
	phone = forms.CharField(label='Phone', max_length=32)

class companyForm(forms.Form):
	companyName = forms.CharField(required=True, label='Company', max_length=250)
	address = forms.CharField(required=True, label='Address', max_length=250)
	city = forms.CharField(required=True, label='City', max_length=100)
	province = forms.CharField(required=True, label='Province', max_length=50)
	country = forms.CharField(required=True, label='Country', max_length=50)
	postalCode = forms.CharField(required=True, label='Postal Code', max_length=10)
	phone = forms.CharField(required=True, label='Phone', max_length=32)

class signUpForm(forms.Form):
	username = forms.CharField(label='Username', max_length=50)
	password = forms.CharField(label='Password',
		widget=forms.PasswordInput, max_length=50)
	confirmPW = forms.CharField(label='Confirm Password',
		widget=forms.PasswordInput, max_length=50)
	firstName = forms.CharField(label='First Name', max_length=50)
	lastName = forms.CharField(label='Last Name', max_length=50)
	email = forms.CharField(label='Email', max_length=100)
	phone = forms.CharField(label='Phone', max_length=32)
	jobTitle = forms.CharField(label='Job Title', max_length=50)
