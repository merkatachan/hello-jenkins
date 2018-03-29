from django import forms
from decimal import Decimal

class smelterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		commIDs = kwargs.pop('commIDs')
		commNameList = kwargs.pop('commNameList')
		PPIDs = kwargs.pop('PPIDs')

		lumpRevenues = kwargs.pop('lumpRevenues')
		finesRevenues = kwargs.pop('finesRevenues')
		ultraFinesRevenues = kwargs.pop('ultraFinesRevenues')
		sumLumpRevenues = kwargs.pop('sumLumpRevenues')
		sumFinesRevenues = kwargs.pop('sumFinesRevenues')
		sumUltraFinesRevenues = kwargs.pop('sumUltraFinesRevenues')

		lumpPenaltyVals = kwargs.pop('lumpPenaltyVals')
		finesPenaltyVals = kwargs.pop('finesPenaltyVals')
		ultraFinesPenaltyVals = kwargs.pop('ultraFinesPenaltyVals')
		sumLumpPenaltyVals = kwargs.pop('sumLumpPenaltyVals')
		sumFinesPenaltyVals = kwargs.pop('sumFinesPenaltyVals')
		sumUltraFinesPenaltyVals = kwargs.pop('sumUltraFinesPenaltyVals')

		super(smelterForm, self).__init__(*args, **kwargs)

		if 1 in PPIDs:
			self.fields["sumLumpRevenues"] = forms.DecimalField(required=True,
				label="Total Lump Revenues",
				decimal_places=2, max_digits=20,
				initial=sumLumpRevenues,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			for year in range(1, len(lumpRevenues)+1):
				self.fields["year{0}LumpRevenue".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Lump Revenue".format(year),
					decimal_places=2, max_digits=20,
					initial=lumpRevenues[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}SumLumpPenalty".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Total Lump Penalties".format(year),
					decimal_places=2, max_digits=20,
					initial=sumLumpPenaltyVals[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				for i in range(len(commIDs)):
					self.fields["year{0}Lump{1}Pen".format(year,commNameList[i])] = forms.DecimalField(required=True,
						label="Year{0} Lump {1} Penalty".format(year,commNameList[i]),
						decimal_places=2, max_digits=20,
						initial=lumpPenaltyVals[commNameList[i]][year-1],
						widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if 2 in PPIDs:
			self.fields["sumFinesRevenues"] = forms.DecimalField(required=True,
				label="Total Fines Revenues",
				decimal_places=2, max_digits=20,
				initial=sumFinesRevenues,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			for year in range(1, len(lumpRevenues)+1):
				self.fields["year{0}FinesRevenue".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Fines Revenue".format(year),
					decimal_places=2, max_digits=20,
					initial=finesRevenues[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}SumFinesPenalty".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Total Fines Penalties".format(year),
					decimal_places=2, max_digits=20,
					initial=sumFinesPenaltyVals[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				for i in range(len(commIDs)):
					self.fields["year{0}Fines{1}Pen".format(year,commNameList[i])] = forms.DecimalField(required=True,
						label="Year{0} Fines {1} Penalty".format(year,commNameList[i]),
						decimal_places=2, max_digits=20,
						initial=finesPenaltyVals[commNameList[i]][year-1],
						widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if 3 in PPIDs:
			self.fields["sumUltraFinesRevenues"] = forms.DecimalField(required=True,
				label="Total Ultra Fines Revenues",
				decimal_places=2, max_digits=20,
				initial=sumUltraFinesRevenues,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			for year in range(1, len(lumpRevenues)+1):
				self.fields["year{0}UltraFinesRevenue".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Ultra Fines Revenue".format(year),
					decimal_places=2, max_digits=20,
					initial=ultraFinesRevenues[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}SumUltraFinesPenalty".format(year)] = forms.DecimalField(required=True,
					label="Year{0} Total Ultra Fines Penalties".format(year),
					decimal_places=2, max_digits=20,
					initial=sumUltraFinesPenaltyVals[year-1],
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				for i in range(len(commIDs)):
					self.fields["year{0}UltraFines{1}Pen".format(year,commNameList[i])] = forms.DecimalField(required=True,
						label="Year{0} Ultra Fines {1} Penalty".format(year,commNameList[i]),
						decimal_places=2, max_digits=20,
						initial=ultraFinesPenaltyVals[commNameList[i]][year-1],
						widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
