from django import forms
from setup.models import *

class csvForm(forms.Form):
	def __init__(self, *args, **kwargs):
		reportRows = kwargs.pop('reportRows')
		super(csvForm, self).__init__(*args, **kwargs)

		self.fields["rowCount"] = forms.IntegerField(initial=len(reportRows), widget=forms.HiddenInput())
		for i in range(1,len(reportRows)+1):
			self.fields["row{0}".format(i)] = forms.CharField(initial=reportRows[i-1], widget=forms.HiddenInput())

class filterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		reportData = kwargs.pop('reportData')

		# Obtain latest projectID
		# latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# startYear = latestProject.startDate.year
		# LOM = latestProject.LOM

		# YEAR_CHOICES = [tuple([startYear+x, startYear+x]) for x in range(LOM)]
		# MONTH_CHOICES = [
		# 	('JAN', 'JAN'),
		# 	('FEB', 'FEB'),
		# 	('MAR', 'MAR'),
		# 	('APR', 'APR'),
		# 	('MAY', 'MAY'),
		# 	('JUN', 'JUN'),
		# 	('JUL', 'JUL'),
		# 	('AUG', 'AUG'),
		# 	('SEP', 'SEP'),
		# 	('OCT', 'OCT'),
		# 	('NOV', 'NOV'),
		# 	('DEC', 'DEC')
		# ]

		super(filterForm, self).__init__(*args, **kwargs)

		# self.fields["startYear"] = forms.IntegerField(label='Start Year:', widget=forms.Select(choices=YEAR_CHOICES))
		# self.fields["startMonth"] = forms.CharField(label='Start Month:', widget=forms.Select(choices=MONTH_CHOICES))
		# self.fields["endYear"] = forms.IntegerField(label='End Year:', widget=forms.Select(choices=YEAR_CHOICES))
		# self.fields["endMonth"] = forms.CharField(label='End Month:', widget=forms.Select(choices=MONTH_CHOICES))

		self.fields["reportData"] = forms.CharField(required=False, initial=reportData,
			widget=forms.HiddenInput())
