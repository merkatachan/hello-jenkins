from django import forms
from .models import *


class commodityForm(forms.Form):
	MAINOPTIONS1 = (
		('1', "Ag"),
		('2', "Al"),
		('5', "Au"),
		('6', "Be"),
		('7', "Bi"),
		('10', "C"),
		('13', "Cd"),
		('16', "Co"),
		('18', "Cr"),
		('20', "Cu"),
		('22', "Fe"))

	MAINOPTIONS2 = (
		('26', "In"),
		('27', "K"),
		('29', "Li"),
		('30', "Mg"),
		('32', "Mn"),
		('34', "Mo"),
		('36', "Ni"),
		('39', "Pb"),
		('41', "Pd"),
		('42', "Pt"),
		('43', "REO"))

	MAINOPTIONS3 = (
		('44', "S"),
		('47', "Se"),
		('49', "Si"),
		('51', "Sn"),
		('53', "Te"),
		('54', "Ti"),
		('55', "U"),
		('57', "V"),
		('59', "W"),
		('61', "Zn"))

	mainCommodity1 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=MAINOPTIONS1)
	mainCommodity2 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=MAINOPTIONS2)
	mainCommodity3 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=MAINOPTIONS3)


	DELOPTIONS1 = (
		('3', "Al"),
		('4', "As"),
		('8', "Bi"),
		('9', "Br"),
		('11', "C"),
		('12', "Ca"),
		('14', "Cd"),
		('15', "Cl"),
		('17', "Co"),
		('19', "Cr"))

	DELOPTIONS2 = (
		('21', "Cu"),
		('23', "Fe"),
		('24', "Fl"),
		('25', "Hg"),
		('28', "K"),
		('31', "Mg"),
		('33', "Mn"),
		('35', "Na"),
		('37', "Ni"),
		('38', "P"))

	DELOPTIONS3 = (
		('40', "Pb"),
		('45', "S"),
		('46', "Sb"),
		('48', "Se"),
		('50', "Si"),
		('52', "Sn"),
		('56', "U"),
		('58', "V"),
		('60', "W"),
		('62', "Zn"))

	delCommodity1 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=DELOPTIONS1)
	delCommodity2 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=DELOPTIONS2)
	delCommodity3 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=DELOPTIONS3)


class commodityMainForm(forms.Form):
	OPTIONS1 = (
		('1', "Ag"),
		('2', "Al"),
		('5', "Au"),
		('6', "Be"),
		('7', "Bi"),
		('10', "C"),
		('13', "Cd"),
		('16', "Co"),
		('18', "Cr"),
		('20', "Cu"),
		('22', "Fe"))

	OPTIONS2 = (
		('26', "In"),
		('27', "K"),
		('29', "Li"),
		('30', "Mg"),
		('32', "Mn"),
		('34', "Mo"),
		('36', "Ni"),
		('39', "Pb"),
		('41', "Pd"),
		('42', "Pt"),
		('43', "REO"))

	OPTIONS3 = (
		('44', "S"),
		('47', "Se"),
		('49', "Si"),
		('51', "Sn"),
		('53', "Te"),
		('54', "Ti"),
		('55', "U"),
		('57', "V"),
		('59', "W"),
		('61', "Zn"))

	commodity1 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS1)
	commodity2 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS2)
	commodity3 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS3)


class commodityDelForm(forms.Form):
	OPTIONS1 = (
		('3', "Al"),
		('4', "As"),
		('8', "Bi"),
		('9', "Br"),
		('11', "C"),
		('12', "Ca"),
		('14', "Cd"),
		('15', "Cl"),
		('17', "Co"),
		('19', "Cr"))

	OPTIONS2 = (
		('21', "Cu"),
		('23', "Fe"),
		('24', "Fl"),
		('25', "Hg"),
		('28', "K"),
		('31', "Mg"),
		('33', "Mn"),
		('35', "Na"),
		('37', "Ni"),
		('38', "P"))

	OPTIONS3 = (
		('40', "Pb"),
		('45', "S"),
		('46', "Sb"),
		('48', "Se"),
		('50', "Si"),
		('52', "Sn"),
		('56', "U"),
		('58', "V"),
		('60', "W"),
		('62', "Zn"))

	commodity1 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS1)
	commodity2 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS2)
	commodity3 = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS3)


class productsForm(forms.Form):
	projectChoices = (
		('1', 'Study'),
		('2', 'Operation')
		)
	projectType = forms.ChoiceField(choices=projectChoices, required=True, label="Project Type")

	# mineProductChoices = (
	# 	('1', 'High Grade Ore'),
	# 	('2', 'Low Grade Ore'),
	# 	('3', 'Waste'),
	# 	('4', 'Overburden')
	# 	)

	# mineProduct = forms.MultipleChoiceField(label='Mine Products', required=True, widget=forms.CheckboxSelectMultiple, choices=mineProductChoices)

	stockpiles = forms.IntegerField(label='Number of Stockpiles', required=True, min_value=1, max_value=6, initial=1)

	plantProductChoices = (
		('1', 'Lump'),
		('2', 'Fines'),
		('3', 'Ultra Fines'),
		('4', 'Rejects')
		)

	plantProduct = forms.MultipleChoiceField(label='Plant Products', required=True, widget=forms.CheckboxSelectMultiple, choices=plantProductChoices)

	LOM = forms.IntegerField(required=True, label='LOM', min_value=1, initial=1)

	startDate = forms.DateField(required=True, label='Start Date',
		widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))


class mineProductionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		LOM = kwargs.pop('LOM')
		numStockpiles = kwargs.pop('numStockpiles')
		idList = kwargs.pop('idList')
		commNameList = kwargs.pop('commNameList')
		super(mineProductionForm, self).__init__(*args, **kwargs)

		for curr in range(1, numStockpiles+1):
			for i in range(int(LOM)):
				i += 1
				self.fields["year{0}MinePlanStockpile{1}Tonnage".format(i, curr)] = forms.DecimalField(required=True, 
					label="Year{0} Mine Plan Stockpile {1} Tonnage".format(i, curr), decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				for j in range(len(idList)):
					self.fields["year{0}MinePlanSP{1}Grade{2}".format(i, curr, commNameList[j])] = forms.DecimalField(required=True, 
						label="Year{0} Mine Plan Stockpile {1} Grade {2} %".format(i, curr, commNameList[j]), decimal_places=6, max_digits=20,
						widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

		# if str(1) in MPIDs:
		# 	for i in range(int(LOM)):
		# 		i += 1
		# 		self.fields["year{0}MinePlanHighGradeTonnage".format(i)] = forms.DecimalField(required=True, 
		# 			label="Year{0} Mine Plan High Grade Tonnage".format(i), decimal_places=2, max_digits=20,
		# 			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# 		for j in range(len(idList)):
		# 			self.fields["year{0}MinePlanHGGrade{1}".format(i, commNameList[j])] = forms.DecimalField(required=True, 
		# 				label="Year{0} Mine Plan High Grade {1} %".format(i, commNameList[j]), decimal_places=6, max_digits=20,
		# 				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

		# if str(2) in MPIDs:
		# 	for i in range(int(LOM)):
		# 		i += 1
		# 		self.fields["year{0}MinePlanLowGradeTonnage".format(i)] = forms.DecimalField(required=True, 
		# 			label="Year{0} Mine Plan Low Grade Tonnage".format(i), decimal_places=2, max_digits=20,
		# 			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# 		for j in range(len(idList)):
		# 			self.fields["year{0}MinePlanLGGrade{1}".format(i, commNameList[j])] = forms.DecimalField(required=True, 
		# 				label="Year{0} Mine Plan Low Grade {1} %".format(i, commNameList[j]), decimal_places=6, max_digits=20,
		# 				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

		# if str(3) in MPIDs:
		# 	for i in range(int(LOM)):
		# 		i += 1
		# 		self.fields["year{0}MinePlanWasteTonnage".format(i)] = forms.DecimalField(required=True, 
		# 			label="Year{0} Mine Plan Waste Tonnage".format(i), decimal_places=2, max_digits=20,
		# 			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(4) in MPIDs:
		# 	for i in range(int(LOM)):
		# 		i += 1
		# 		self.fields["year{0}MinePlanOverburdenTonnage".format(i)] = forms.DecimalField(required=True, 
		# 			label="Year{0} Mine Plan Overburden Tonnage".format(i), decimal_places=2, max_digits=20,
		# 			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


class CAPEXForm(forms.Form):
	def __init__(self, *args, **kwargs):
			LOM = kwargs.pop('LOM')
			super(CAPEXForm, self).__init__(*args, **kwargs)

			for i in [-3, -2, -1]:
				self.fields["year{0}PreStripping".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Pre-Stripping".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}MiningEquipmentInitial".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Mining Equipment Initial".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}MiningEquipmentSustaining".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Mining Equipment Sustaining".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}InfrastructureDirectCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Infrastructure Direct Costs".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}InfrastructureIndirectCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Infrastructure Indirect Costs".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}Contingency".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Contingency".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}Railcars".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Railcars".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}OtherMobileEquipment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Other Mobile Equipment".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}ClosureAndRehabAssurancePayment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Closure and Rehab Assurance Payment".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}DepositsProvisionPayment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Deposits Provision Payment".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}WorkingCapCurrentProd".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} WorkingCapCurrentProd".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}WorkingCapCostsOfLG".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} WorkingCapCostsofLG".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}EPCM".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} EPCM".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}OwnersCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Owner's Costs".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))

			for i in range(int(LOM)):
				i += 1
				self.fields["year{0}PreStripping".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Pre-Stripping".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}MiningEquipmentInitial".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Mining Equipment Initial".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}MiningEquipmentSustaining".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Mining Equipment Sustaining".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}InfrastructureDirectCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Infrastructure Direct Costs".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}InfrastructureIndirectCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Infrastructure Indirect Costs".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}Contingency".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Contingency".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}Railcars".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Railcars".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}OtherMobileEquipment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Other Mobile Equipment".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}ClosureAndRehabAssurancePayment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Closure and Rehab Assurance Payment".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}DepositsProvisionPayment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Deposits Provision Payment".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}WorkingCapCurrentProd".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} WorkingCapCurrentProd".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}WorkingCapCostsOfLG".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} WorkingCapCostsofLG".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}EPCM".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} EPCM".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
				self.fields["year{0}OwnersCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Owner's Costs".format(i),
		        		decimal_places=8, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))


class OPEXForm(forms.Form):
	def __init__(self, *args, **kwargs):
	        LOM = kwargs.pop('LOM')
	        super(OPEXForm, self).__init__(*args, **kwargs)

	        for i in range(int(LOM)):
	        	i += 1
	        	self.fields["year{0}Mining".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Mining".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}Infrastructure".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Infrastructure".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}StockpileLG".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Stockpile Reclaim".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}Dewatering".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Dewatering".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}Processing".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Processing".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}ProductHauling".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Product Hauling".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}LoadoutRailLoop".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Load-out and Rail Loop".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}GASite".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A (Site)".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}GARoomBoardFIFO".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A (Room & Board and FIFO)".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}RailTransportation".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Rail Transportation, Port and Shiploading".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}GACorporate".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A (Corporate)".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}Royalties".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Royalties".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}Transportation".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Transportation".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}GA".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}ShippingCost".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Shipping Cost (US$/t)".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}OpexPT".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} OPEX (CAD$/t)".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))



class smelterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		idList = kwargs.pop('idList')
		nameList = kwargs.pop('nameList')
		numStockpiles = kwargs.pop('numStockpiles')
		super(smelterForm, self).__init__(*args, **kwargs)

		for curr in range(1, numStockpiles+1):
			for i in range(len(idList)):
				self.fields["Stockpile{0}MinGrade{1}".format(curr,idList[i])] = forms.DecimalField(required=True,
					label=nameList[i] + " Stockpile {0} Min Grade %".format(curr),
					decimal_places=2, max_digits=20, 
					widget=forms.NumberInput(attrs={'placeholder': 'Between 0-100%'}))
				self.fields["Stockpile{0}MaxGrade{1}".format(curr,idList[i])] = forms.DecimalField(required=True,
					label=nameList[i] + " Stockpile {0} Max Grade %".format(curr),
					decimal_places=2, max_digits=20, 
					widget=forms.NumberInput(attrs={'placeholder': 'Between 0-100%'}))
				self.fields["Stockpile{0}MinPenalty{1}".format(curr,idList[i])] = forms.DecimalField(required=True,
					label=nameList[i] + " Stockpile {0} Min Penalty".format(curr),
					decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["Stockpile{0}MaxPenalty{1}".format(curr,idList[i])] = forms.DecimalField(required=True,
					label=nameList[i] + " Stockpile {0} Max Penalty".format(curr),
					decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["Stockpile{0}MinMaxPenalty{1}".format(curr,idList[i])] = forms.DecimalField(required=True,
					label=nameList[i] + " Stockpile {0} Penalty Between Min and Max".format(curr),
					decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["Stockpile{0}Premium{1}".format(curr,idList[i])] = forms.DecimalField(required=True,
					label=nameList[i] + " Stockpile {0} Premium".format(curr),
					decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["Stockpile{0}Increments{1}".format(curr,idList[i])] = forms.DecimalField(required=True,
					label=nameList[i] + " Stockpile {0} Increments %".format(curr),
					decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 2 Decimal Places'}))

		# for i in range(len(idList)):
			# self.fields["increments{0}".format(idList[i])] = forms.DecimalField(required=True,
			# 	label=nameList[i] + " Increments %",
			# 	decimal_places=2, max_digits=20,
			# 	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 2 Decimal Places'}))
			# self.fields["LGPlantMinGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
				# label=nameList[i] + " Low Grade Plant Feed Min Grade",
				# decimal_places=2, max_digits=20,
				# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			# self.fields["LGPlantMinPenalty{0}".format(idList[i])] = forms.DecimalField(required=True,
				# label=nameList[i] + " Low Grade Plant Feed Min Penalty",
				# decimal_places=2, max_digits=20,
				# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			# self.fields["HGPlantMinGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
				# label=nameList[i] + " High Grade Plant Feed Min Grade",
				# decimal_places=2, max_digits=20,
				# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			# self.fields["HGPlantMinPenalty{0}".format(idList[i])] = forms.DecimalField(required=True,
				# label=nameList[i] + " High Grade Plant Feed Min Penalty",
				# decimal_places=2, max_digits=20,
				# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


class financialsForm(forms.Form):
	def __init__(self, *args, **kwargs):
		# mineID = kwargs.pop('mineID')
		# PPIDs = kwargs.pop('plantProducts')
		numStockpiles = kwargs.pop('numStockpiles')
		PPIDs = kwargs.pop('plantProducts')
		super(financialsForm, self).__init__(*args, **kwargs)

		# Get list of Plant Product IDs
		# latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# PPTimestamp = latestPlantProduct.dateAdded
		# PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
		# PPIDs = PPMatches.values_list('plantProductID', flat=True)

		for curr in range(1, numStockpiles+1):
			if str(1) in PPIDs:
				self.fields["Stockpile{0}Lump".format(curr)] = forms.DecimalField(required=True,
		        		label="Stockpile {0} Lump Price".format(curr),
		        		decimal_places=2, max_digits=12,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["Stockpile{0}LumpPrem".format(curr)] = forms.DecimalField(required=True,
		        		label="Stockpile {0} Lump Premium".format(curr),
		        		decimal_places=2, max_digits=12,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			if str(2) in PPIDs:
				self.fields["Stockpile{0}Fines".format(curr)] = forms.DecimalField(required=True,
		        		label="Stockpile {0} Fines Price".format(curr),
		        		decimal_places=2, max_digits=12,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			if str(3) in PPIDs:
				self.fields["Stockpile{0}UltraFines".format(curr)] = forms.DecimalField(required=True,
		        		label="Stockpile {0} Ultra Fines Price".format(curr),
		        		decimal_places=2, max_digits=12,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			if str(1) in PPIDs:
				self.fields["Stockpile{0}LumpAvg".format(curr)] = forms.DecimalField(required=True,
		        		label="Stockpile {0} Lump Average".format(curr),
		        		decimal_places=2, max_digits=12,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(1) in PPIDs:
		# 	self.fields["HGLump"] = forms.DecimalField(required=True,
	 #        		label="High Grade Lump Price",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# 	self.fields["HGLumpPrem"] = forms.DecimalField(required=True,
	 #        		label="High Grade Lump Premium",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(2) in PPIDs:
		# 	self.fields["HGFines"] = forms.DecimalField(required=True,
	 #        		label="High Grade Fines Price",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(3) in PPIDs:
		# 	self.fields["HGUltraFines"] = forms.DecimalField(required=True,
	 #        		label="High Grade Ultra Fines Price",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(1) in PPIDs:
		# 	self.fields["LGLump"] = forms.DecimalField(required=True,
	 #        		label="Low Grade Lump Price",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# 	self.fields["LGLumpPrem"] = forms.DecimalField(required=True,
	 #        		label="Low Grade Lump Premium",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(2) in PPIDs:
		# 	self.fields["LGFines"] = forms.DecimalField(required=True,
	 #        		label="Low Grade Fines Price",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(3) in PPIDs:
		# 	self.fields["LGUltraFines"] = forms.DecimalField(required=True,
	 #        		label="Low Grade Ultra Fines Price",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if str(1) in PPIDs:
		# 	self.fields["HGLumpAvg"] = forms.DecimalField(required=True,
	 #        		label="High Grade Lump Average",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# 	self.fields["LGLumpAvg"] = forms.DecimalField(required=True,
	 #        		label="Low Grade Lump Average",
	 #        		decimal_places=2, max_digits=12,
	 #        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


class taxesForm(forms.Form):
	def __init__(self, *args, **kwargs):
	        LOM = kwargs.pop('LOM')
	        super(taxesForm, self).__init__(*args, **kwargs)

	        for i in range(int(LOM)):
	        	i += 1
	        	self.fields["year{0}Federal".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Federal".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}Provincial".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Provincial".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))
	        	self.fields["year{0}Mining".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Mining".format(i),
	        		decimal_places=8, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 8 Decimal Places'}))


# class inputsForm(forms.Form):
# 	Fe2O3Iron = forms.DecimalField(required=True, label='Fe2O3 Iron',
# 		max_digits=12, decimal_places=6)
# 	totalGrade = forms.DecimalField(required=True, label='Total Grade',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	avgCommodity1Grade = forms.DecimalField(required=True, label='Average Commodity 1 Grade',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	lumpRecovery = forms.DecimalField(required=True, label='Lump Percent Recovery',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	finesRecovery = forms.DecimalField(required=True, label='Fines Percent Recovery',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	lumpGrade = forms.DecimalField(required=True, label='Lump Percent Grade',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	finesGrade = forms.DecimalField(required=True, label='Fines Percent Grade',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	feedMoisture = forms.DecimalField(required=True, label='Feed Percent Moisture',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	lumpMoisture = forms.DecimalField(required=True, label='Lump Percent Moisture',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	finesMoisture = forms.DecimalField(required=True, label='Fines Percent Moisture',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	ultraFinesMoisture = forms.DecimalField(required=True, label='Ultra Fines Percent Moisture',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	rejectsMoisture = forms.DecimalField(required=True, label='Rejects Percent Moisture',
# 		max_digits=12, decimal_places=2, min_value=0, max_value=100)
# 	mineOpsDays = forms.IntegerField(required=True, label='Mine Operations (Days)', min_value=1,
# 		max_value=365, initial=1)
# 	plantOpsDays = forms.IntegerField(required=True, label='Plant Operations (Days)', min_value=1,
# 		max_value=365, initial=1)
# 	mineCapacity = forms.DecimalField(required=True, label='Mine Capacity (TPD)',
# 		max_digits=20, decimal_places=2, min_value=0)
# 	plantCapacity = forms.DecimalField(required=True, label='Plant Capacity (TPD)',
# 		max_digits=20, decimal_places=2, min_value=0)
# 	discountRate1 = forms.DecimalField(required=True, label='Discount Rate 1',
# 		max_digits=12, decimal_places=6, min_value=0)
# 	discountRate2 = forms.DecimalField(required=True, label='Discount Rate 2',
# 		max_digits=12, decimal_places=6, min_value=0)
# 	discountRate3 = forms.DecimalField(required=True, label='Discount Rate 3',
# 		max_digits=12, decimal_places=6, min_value=0)
# 	discountRate4 = forms.DecimalField(required=True, label='Discount Rate 4',
# 		max_digits=12, decimal_places=6, min_value=0)
# 	discountRate5 = forms.DecimalField(required=True, label='Discount Rate 5',
# 		max_digits=12, decimal_places=6, min_value=0)
# 	discountRate6 = forms.DecimalField(required=True, label='Discount Rate 6',
# 		max_digits=12, decimal_places=6, min_value=0)
# 	exchangeRate = forms.DecimalField(required=True, label='Exchange Rate',
# 		max_digits=12, decimal_places=6, min_value=0)

class inputsForm(forms.Form):
	def __init__(self, *args, **kwargs):
		PPIDs = kwargs.pop('plantProducts')
		super(inputsForm, self).__init__(*args, **kwargs)

		# Get list of Plant Product IDs
		# latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# PPTimestamp = latestPlantProduct.dateAdded
		# PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
		# PPIDs = PPMatches.values_list('plantProductID', flat=True)

		self.fields["Fe2O3Iron"] = forms.DecimalField(required=True,
        	label="Fe2O3Iron", decimal_places=6, max_digits=12,
        	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		self.fields["totalGrade"] = forms.DecimalField(required=True,
    		label="totalGrade", decimal_places=6, max_digits=12,
    		widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		self.fields["avgCommodity1Grade"] = forms.DecimalField(required=True,
    		label="Average Commodity 1 Grade", decimal_places=6, max_digits=12,
    		widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(1) in PPIDs:
			self.fields["lumpRecovery"] = forms.DecimalField(required=True,
	    		label="Lump Percent Recovery", decimal_places=2, max_digits=12,
	    		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if str(2) in PPIDs:
			self.fields["finesRecovery"] = forms.DecimalField(required=True,
	    		label="Fines Percent Recovery", decimal_places=6, max_digits=12,
	    		widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(3) in PPIDs:
			self.fields["ultraFinesRecovery"] = forms.DecimalField(required=True,
    			label="Ultra Fines Percent Recovery", decimal_places=6, max_digits=12,
    			widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(4) in PPIDs:
			self.fields["rejectsRecovery"] = forms.DecimalField(required=True,
    			label="Rejects Percent Recovery", decimal_places=6, max_digits=12,
    			widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(1) in PPIDs:
			self.fields["lumpGrade"] = forms.DecimalField(required=True,
	    		label="Lump Percent Grade", decimal_places=6, max_digits=12,
	    		widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(2) in PPIDs:
			self.fields["finesGrade"] = forms.DecimalField(required=True,
	    		label="Fines Percent Grade", decimal_places=6, max_digits=12,
	    		widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(3) in PPIDs:
			self.fields["ultraFinesGrade"] = forms.DecimalField(required=True,
    			label="Ultra Fines Percent Grade", decimal_places=6, max_digits=12,
    			widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(4) in PPIDs:
			self.fields["rejectsGrade"] = forms.DecimalField(required=True,
    			label="Rejects Percent Grade", decimal_places=2, max_digits=12,
    			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		self.fields["feedMoisture"] = forms.DecimalField(required=True,
    		label="Feed Percent Moisture", decimal_places=2, max_digits=12,
    		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if str(1) in PPIDs:
			self.fields["lumpMoisture"] = forms.DecimalField(required=True,
	    		label="Lump Percent Moisture", decimal_places=6, max_digits=12,
	    		widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(2) in PPIDs:
			self.fields["finesMoisture"] = forms.DecimalField(required=True,
	    		label="Fines Percent Moisture", decimal_places=6, max_digits=12,
	    		widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(3) in PPIDs:
			self.fields["ultraFinesMoisture"] = forms.DecimalField(required=True,
    			label="Ultra Fines Percent Moisture", decimal_places=6, max_digits=12,
    			widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		if str(4) in PPIDs:
			self.fields["rejectsMoisture"] = forms.DecimalField(required=True,
    			label="Rejects Percent Moisture", decimal_places=6, max_digits=12,
    			widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 6 Decimal Places'}))

		self.fields["mineOpsDays"] = forms.IntegerField(required=True,
    		label="Mine Operations (Days)", min_value=1, max_value=365, initial=365)

		self.fields["plantOpsDays"] = forms.IntegerField(required=True,
    		label="Plant Operations (Days)", min_value=1, max_value=365, initial=240)

		self.fields["mineCapacity"] = forms.DecimalField(required=True,
    		label="Mine Capacity (TPD)", decimal_places=2, max_digits=20,
			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		self.fields["plantCapacity"] = forms.DecimalField(required=True,
    		label="Plant Capacity (TPD)", decimal_places=2, max_digits=20,
    		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		self.fields["discountRate1"] = forms.IntegerField(required=True,
    		label="Discount Rate 1", min_value=0, max_value=100, initial=0)

		# self.fields["discountRate1"] = forms.DecimalField(required=True,
  #   		label="Discount Rate 1", decimal_places=4, max_digits=20, max_value=100,
		# 	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 4 Decimal Places'}))

		self.fields["discountRate2"] = forms.IntegerField(required=True,
    		label="Discount Rate 2", min_value=0, max_value=100, initial=0)

		# self.fields["discountRate2"] = forms.DecimalField(required=True,
  #   		label="Discount Rate 2", decimal_places=4, max_digits=20, max_value=100,
		# 	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 4 Decimal Places'}))

		self.fields["discountRate3"] = forms.IntegerField(required=True,
    		label="Discount Rate 3", min_value=0, max_value=100, initial=0)

		# self.fields["discountRate3"] = forms.DecimalField(required=True,
  #   		label="Discount Rate 3", decimal_places=4, max_digits=20, max_value=100,
		# 	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 4 Decimal Places'}))

		self.fields["discountRate4"] = forms.IntegerField(required=True,
    		label="Discount Rate 4", min_value=0, max_value=100, initial=0)

		# self.fields["discountRate4"] = forms.DecimalField(required=True,
  #   		label="Discount Rate 4", decimal_places=4, max_digits=20, max_value=100,
		# 	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 4 Decimal Places'}))

		self.fields["discountRate5"] = forms.IntegerField(required=True,
    		label="Discount Rate 5", min_value=0, max_value=100, initial=0)

    	# self.fields["discountRate5"] = forms.DecimalField(required=True,
  #   		label="Discount Rate 5", decimal_places=4, max_digits=20, max_value=100,
		# 	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 4 Decimal Places'}))		

		self.fields["discountRate6"] = forms.IntegerField(required=True,
    		label="Discount Rate 6", min_value=0, max_value=100, initial=0)

		# self.fields["discountRate6"] = forms.DecimalField(required=True,
  #   		label="Discount Rate 6", decimal_places=4, max_digits=20, max_value=100,
		# 	widget=forms.NumberInput(attrs={'placeholder': '1-100%, Max 4 Decimal Places'}))

		self.fields["exchangeRate"] = forms.DecimalField(label="CADUSD Rate", decimal_places=4,
			max_digits=12, min_value=0, 
			widget=forms.NumberInput(attrs={'placeholder': 'Max 4 Decimal Places'}))
		
		# self.fields["exchangeRate"] = forms.DecimalField(label="Exchange Rate", decimal_places=6,
			# max_digits=12,
    		# min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))
