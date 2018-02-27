from django import forms
from setup.models import *

class csvForm(forms.Form):
	def __init__(self, *args, **kwargs):
		reportRows = kwargs.pop('reportRows')
		super(csvForm, self).__init__(*args, **kwargs)

		self.fields["rowCount"] = forms.IntegerField(initial=len(reportRows), widget=forms.HiddenInput())
		for i in range(1,len(reportRows)+1):
			self.fields["row{0}".format(i)] = forms.CharField(initial=reportRows[i-1], widget=forms.HiddenInput())
