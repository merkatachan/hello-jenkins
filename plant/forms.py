from django import forms
from decimal import Decimal

class plantForm(forms.Form):
	def __init__(self, *args, **kwargs):
		commIDs = kwargs.pop('commIDs')
		commNameList = kwargs.pop('commNameList')
		PPIDs = kwargs.pop('PPIDs')

		lumpWMTs = kwargs.pop('lumpWMTs')
		lumpDMTs = kwargs.pop('lumpDMTs')
		lumpGradeVals = kwargs.pop('lumpGradeVals')
		lumpWMTTotal = kwargs.pop('lumpWMTTotal')
		lumpDMTTotal = kwargs.pop('lumpDMTTotal')

		finesWMTs = kwargs.pop('finesWMTs')
		finesDMTs = kwargs.pop('finesDMTs')
		finesGradeVals = kwargs.pop('finesGradeVals')
		finesWMTTotal = kwargs.pop('finesWMTTotal')
		finesDMTTotal = kwargs.pop('finesDMTTotal')

		ultraFinesWMTs = kwargs.pop('ultraFinesWMTs')
		ultraFinesDMTs = kwargs.pop('ultraFinesDMTs')
		ultraFinesGradeVals = kwargs.pop('ultraFinesGradeVals')
		ultraFinesWMTTotal = kwargs.pop('ultraFinesWMTTotal')
		ultraFinesDMTTotal = kwargs.pop('ultraFinesDMTTotal')

		rejectsWMTs = kwargs.pop('rejectsWMTs')
		rejectsDMTs = kwargs.pop('rejectsDMTs')
		rejectsWMTTotal = kwargs.pop('rejectsWMTTotal')
		rejectsDMTTotal = kwargs.pop('rejectsDMTTotal')

		sumWMTs = kwargs.pop('sumWMTs')
		sumDMTs = kwargs.pop('sumDMTs')
		sumWMTTotal = kwargs.pop('sumWMTTotal')
		sumDMTTotal = kwargs.pop('sumDMTTotal')
		super(plantForm, self).__init__(*args, **kwargs)

		if 1 in PPIDs:
			for year in range(1, len(lumpWMTs)+1):
				self.fields["year{0}LumpWMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Lump WMT".format(year),
					decimal_places=2, max_digits=20,
					initial=lumpWMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}LumpDMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Lump DMT".format(year),
					decimal_places=2, max_digits=20,
					initial=lumpDMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			for i in range(len(commIDs)):
				self.fields["year{0}Lump{1}Grade".format(year,commNameList[i])] = forms.DecimalField(required=True,
					label="Year{0} Lump {1} Grade".format(year,commNameList[i]),
					decimal_places=2, max_digits=20,
					initial=lumpGradeVals[commNameList[i]][year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["lumpDMTTotal"] = forms.DecimalField(required=True,
				label="Lump DMT Total",
				decimal_places=2, max_digits=20,
				initial=lumpDMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["lumpWMTTotal"] = forms.DecimalField(required=True,
				label="Lump WMT Total",
				decimal_places=2, max_digits=20,
				initial=lumpWMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if 2 in PPIDs:
			for year in range(1, len(lumpWMTs)+1):
				self.fields["year{0}FinesWMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Fines WMT".format(year),
					decimal_places=2, max_digits=20,
					initial=finesWMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}FinesDMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Fines DMT".format(year),
					decimal_places=2, max_digits=20,
					initial=finesDMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			for i in range(len(commIDs)):
				self.fields["year{0}Fines{1}Grade".format(year,commNameList[i])] = forms.DecimalField(required=True,
					label="Year{0} Fines {1} Grade".format(year,commNameList[i]),
					decimal_places=2, max_digits=20,
					initial=finesGradeVals[commNameList[i]][year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["finesDMTTotal"] = forms.DecimalField(required=True,
				label="Fines DMT Total",
				decimal_places=2, max_digits=20,
				initial=finesDMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["finesWMTTotal"] = forms.DecimalField(required=True,
				label="Fines WMT Total",
				decimal_places=2, max_digits=20,
				initial=finesWMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if 3 in PPIDs:
			for year in range(1, len(lumpWMTs)+1):
				self.fields["year{0}UltraFinesWMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Ultra Fines WMT".format(year),
					decimal_places=2, max_digits=20,
					initial=ultraFinesWMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}UltraFinesDMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Ultra Fines DMT".format(year),
					decimal_places=2, max_digits=20,
					initial=ultraFinesDMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			for i in range(len(commIDs)):
				self.fields["year{0}UltraFines{1}Grade".format(year,commNameList[i])] = forms.DecimalField(required=True,
					label="Year{0} Ultra Fines {1} Grade".format(year,commNameList[i]),
					decimal_places=2, max_digits=20,
					initial=ultraFinesGradeVals[commNameList[i]][year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["ultraFinesDMTTotal"] = forms.DecimalField(required=True,
				label="Ultra Fines DMT Total",
				decimal_places=2, max_digits=20,
				initial=ultraFinesDMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["ultraFinesWMTTotal"] = forms.DecimalField(required=True,
				label="Ultra Fines WMT Total",
				decimal_places=2, max_digits=20,
				initial=ultraFinesWMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if 4 in PPIDs:
			for year in range(1, len(lumpWMTs)+1):
				self.fields["year{0}RejectsWMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Rejects WMT".format(year),
					decimal_places=2, max_digits=20,
					initial=rejectsWMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}RejectsDMT".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Rejects DMT".format(year),
					decimal_places=2, max_digits=20,
					initial=rejectsDMTs[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["rejectsDMTTotal"] = forms.DecimalField(required=True,
				label="Rejects DMT Total",
				decimal_places=2, max_digits=20,
				initial=rejectsDMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["rejectsWMTTotal"] = forms.DecimalField(required=True,
				label="Rejects WMT Total",
				decimal_places=2, max_digits=20,
				initial=rejectsWMTTotal,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		for year in range(1, len(lumpWMTs)+1):
			self.fields["year{0}SumWMT".format(year)] = forms.DecimalField(required=True,
				label="Year {0} Total WMT".format(year),
				decimal_places=2, max_digits=20,
				initial=sumWMTs[year-1],
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

			self.fields["year{0}SumDMT".format(year)] = forms.DecimalField(required=True,
				label="Year {0} Total DMT".format(year),
				decimal_places=2, max_digits=20,
				initial=sumWMTs[year-1],
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		self.fields["sumWMTTotal"] = forms.DecimalField(required=True,
			label="Sum WMT Total",
			decimal_places=2, max_digits=20,
			initial=sumWMTTotal,
			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		self.fields["sumDMTTotal".format(year)] = forms.DecimalField(required=True,
			label="Sum DMT Total",
			decimal_places=2, max_digits=20,
			initial=sumDMTTotal,
			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
