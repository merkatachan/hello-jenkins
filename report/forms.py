from django import forms
from setup.models import *

class csvForm(forms.Form):
	def __init__(self, *args, **kwargs):
		reportRows = kwargs.pop('reportRows')
		super(csvForm, self).__init__(*args, **kwargs)

		self.fields["rowCount"] = forms.IntegerField(initial=len(reportRows), widget=forms.HiddenInput())
		for i in range(1,len(reportRows)+1):
			self.fields["row{0}".format(i)] = forms.CharField(initial=reportRows[i-1], widget=forms.HiddenInput())

class defaultFilterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		thisYearStartDate = kwargs.pop('thisYearStartDate')
		thisYearEndDate = kwargs.pop('thisYearEndDate')
		lastYearStartDate = kwargs.pop('lastYearStartDate')
		lastYearEndDate = kwargs.pop('lastYearEndDate')
		thisQuarterStartDate = kwargs.pop('thisQuarterStartDate')
		thisQuarterEndDate = kwargs.pop('thisQuarterEndDate')
		lastQuarterStartDate = kwargs.pop('lastQuarterStartDate')
		lastQuarterEndDate = kwargs.pop('lastQuarterEndDate')
		# projectStartDate = kwargs.pop('startDate')
		# projectEndDate = kwargs.pop('endDate')

		super(defaultFilterForm, self).__init__(*args, **kwargs)

		# self.fields["startDate"] = forms.DateField(required=True, label='Start Date',
		# 	widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))

		# self.fields["endDate"] = forms.DateField(required=True, label='End Date',
		# 	widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))

		defaultFilterChoices = []
		defaultFilterChoices.append(("", ""))
		defaultFilterChoices.append(("thisYear", "This Year"))
		defaultFilterChoices.append(("lastYear", "Last Year"))
		defaultFilterChoices.append(("thisQuarter", "This Quarter"))
		defaultFilterChoices.append(("lastQuarter", "Last Quarter"))

		# if thisYearStartDate:
		# 	defaultFilterChoices.append(("thisYear", "This Year"))
		# else:
		# 	defaultFilterChoices.append(("thisYearDisabled", "This Year (Not Available)"))

		# if lastYearStartDate:
		# 	defaultFilterChoices.append(("lastYear", "Last Year"))
		# else:
		# 	defaultFilterChoices.append(("lastYearDisabled", "Last Year (Not Available)"))

		# if thisQuarterStartDate:
		# 	defaultFilterChoices.append(("thisQuarter", "This Quarter"))
		# else:
		# 	defaultFilterChoices.append(("thisQuarterDisabled", "This Quarter (Not Available)"))

		# if lastQuarterStartDate:
		# 	defaultFilterChoices.append(("lastQuarter", "Last Quarter"))
		# else:
		# 	defaultFilterChoices.append(("lastQuarterDisabled", "Last Quarter (Not Available)"))

		defaultFilterChoices = tuple(defaultFilterChoices)

		self.fields["defaultFilter"] = forms.ChoiceField(choices=defaultFilterChoices, required=True, label="Default Filters")

		# defaultFilter = forms.ChoiceField(choices=defaultFilterChoices, required=True, label="Default Filters")

		self.fields["thisYearStartDate"] = forms.DateField(required=False, initial=thisYearStartDate,
			widget=forms.HiddenInput())

		self.fields["thisYearEndDate"] = forms.DateField(required=False, initial=thisYearEndDate,
			widget=forms.HiddenInput())

		self.fields["lastYearStartDate"] = forms.DateField(required=False, initial=lastYearStartDate,
			widget=forms.HiddenInput())

		self.fields["lastYearEndDate"] = forms.DateField(required=False, initial=lastYearEndDate,
			widget=forms.HiddenInput())

		self.fields["thisQuarterStartDate"] = forms.DateField(required=False, initial=thisQuarterStartDate,
			widget=forms.HiddenInput())

		self.fields["thisQuarterEndDate"] = forms.DateField(required=False, initial=thisQuarterEndDate,
			widget=forms.HiddenInput())

		self.fields["lastQuarterStartDate"] = forms.DateField(required=False, initial=lastQuarterStartDate,
			widget=forms.HiddenInput())

		self.fields["lastQuarterEndDate"] = forms.DateField(required=False, initial=lastQuarterEndDate,
			widget=forms.HiddenInput())

		# self.fields["defaultStartDate"] = forms.DateField(required=False, initial=projectStartDate,
		# 	widget=forms.HiddenInput())

		# self.fields["defaultEndDate"] = forms.DateField(required=False, initial=projectEndDate,
		# 	widget=forms.HiddenInput())

class filterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		projectStartDate = kwargs.pop('startDate')
		projectEndDate = kwargs.pop('endDate')
		# reportData = kwargs.pop('reportData')

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

		# self.fields["reportData"] = forms.CharField(required=False, initial=reportData,
		# 	widget=forms.HiddenInput())

		self.fields["startDate"] = forms.DateField(required=True, label='Start Date',
			widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))

		self.fields["endDate"] = forms.DateField(required=True, label='End Date',
			widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))

		self.fields["projectStartDate"] = forms.DateField(required=False, initial=projectStartDate,
			widget=forms.HiddenInput())

		self.fields["projectEndDate"] = forms.DateField(required=False, initial=projectEndDate,
			widget=forms.HiddenInput())

class reportForm(forms.Form):
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

		super(reportForm, self).__init__(*args, **kwargs)

		# self.fields["startYear"] = forms.IntegerField(label='Start Year:', widget=forms.Select(choices=YEAR_CHOICES))
		# self.fields["startMonth"] = forms.CharField(label='Start Month:', widget=forms.Select(choices=MONTH_CHOICES))
		# self.fields["endYear"] = forms.IntegerField(label='End Year:', widget=forms.Select(choices=YEAR_CHOICES))
		# self.fields["endMonth"] = forms.CharField(label='End Month:', widget=forms.Select(choices=MONTH_CHOICES))

		self.fields["reportData"] = forms.CharField(required=False, initial=reportData,
			widget=forms.HiddenInput())
