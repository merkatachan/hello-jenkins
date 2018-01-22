from django import forms
from .models import tblCommodity

class commodityMainForm(forms.Form):
	OPTIONS1 = (
		('1',  "Ag"),
		('2',  "Al"),
		('5',  "Au"),
		('6',  "Be"),
		('7',  "Bi"),
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

	mineProductChoices = (
		('1', 'High Grade Ore'),
		('2', 'Low Grade Ore'),
		('3', 'Waste'),
		('4', 'Overburden')
		)

	mineProduct = forms.MultipleChoiceField(label='Mine Products', required=True, widget=forms.CheckboxSelectMultiple, choices=mineProductChoices)

	plantProductChoices = (
		('1', 'Lump'),
		('2', 'Fines'),
		('3', 'Ultra Fines'),
		('4', 'Rejects')
		)

	plantProduct = forms.MultipleChoiceField(label='Plant Products', required=True, widget=forms.CheckboxSelectMultiple, choices=plantProductChoices)

	LOM = forms.IntegerField(required=True, label='LOM', min_value=1, initial=1)

class CAPEXForm(forms.Form):
	def __init__(self, *args, **kwargs):
			LOM = kwargs.pop('LOM')
			super(CAPEXForm, self).__init__(*args, **kwargs)

			for i in range(int(LOM)):
				i += 1
				self.fields["year{0}PreStripping".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Pre-Stripping".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}MiningEquipmentInitial".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Mining Equipment Initial".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}MiningEquipmentSustaining".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Mining Equipment Sustaining".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}InfrastructureDirectCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Infrastructure Direct Costs".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}InfrastructureIndirectCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Infrastructure Indirect Costs".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}Contingency".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Contingency".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}Railcars".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Railcars".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}OtherMobileEquipment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Other Mobile Equipment".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}ClosureAndRehabAssurancePayment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Closure and Rehab Assurance Payment".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}DepositsProvisionPayment".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Deposits Provision Payment".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}WorkingCapCurrentProd".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} WorkingCapCurrentProd".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}WorkingCapCostsOfLG".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} WorkingCapCostsofLG".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}EPCM".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} EPCM".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				self.fields["year{0}OwnersCosts".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Owner's Costs".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


class OPEXForm(forms.Form):
	def __init__(self, *args, **kwargs):
	        LOM = kwargs.pop('LOM')
	        super(OPEXForm, self).__init__(*args, **kwargs)

	        for i in range(int(LOM)):
	        	i += 1
	        	self.fields["year{0}Mining".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Mining".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}Infrastructure".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Infrastructure".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}StockpileLG".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Stockpile LG Reclaiming".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}Dewatering".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Dewatering".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}Processing".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Processing".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}ProductHauling".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Product Hauling".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}LoadoutRailLoop".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Load-out and Rail Loop".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}GASite".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A (Site)".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}GARoomBoardFIFO".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A (Room & Board and FIFO)".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}RailTransportation".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Rail Transportation, Port and Shiploading".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}GACorporate".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A (Corporate)".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}Royalties".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Royalties".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}Transportation".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Transportation".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}GA".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} G&A".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["year{0}ShippingCost".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Shipping Cost".format(i),
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


class smelterForm(forms.Form):
	def __init__(self, *args, **kwargs):
		idList = kwargs.pop('idList')
		nameList = kwargs.pop('nameList')
		super(smelterForm, self).__init__(*args, **kwargs)

		for i in range(len(idList)):
	        	self.fields["LGMinGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " Low Grade Min Grade",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["LGMaxGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " Low Grade Max Grade",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["LGMinPenalty{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " Low Grade Min Penalty",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["LGMaxPenalty{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " Low Grade Max Penalty",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				#self.fields["LGMinMaxPenalty{0}".format(idList[i])] = forms.DecimalField(required=True,
	        	#	label=nameList[i] + " LGMinMaxPenalty",
	        	#	decimal_places=2, max_digits=20,
	        	#	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["LGPremium{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " Low Grade Premium",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["HGMinGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " High Grade Min Grade",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["HGMaxGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " High Grade Max Grade",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["HGMinPenalty{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " High Grade Min Penalty",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["HGMaxPenalty{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " High Grade Max Penalty",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["HGPremium{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " High Grade Premium",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
	        	self.fields["increments{0}".format(idList[i])] = forms.DecimalField(required=True,
	        		label=nameList[i] + " Increments",
	        		decimal_places=2, max_digits=20,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				#self.fields["LGPFMinGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
	        	#	label=nameList[i] + " LGPFMinGrade",
	        	#	decimal_places=2, max_digits=20,
	        	#	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				#self.fields["HGPFMinGrade{0}".format(idList[i])] = forms.DecimalField(required=True,
	        	#	label=nameList[i] + " HGPFMinGrade",
	        	#	decimal_places=2, max_digits=20,
	        	#	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

class financialsForm(forms.Form):
	HGLump = forms.DecimalField(required=True, label='High Grade Lump Price',
		max_digits=12, decimal_places=2)
	HGLumpPrem = forms.DecimalField(required=True, label='High Grade Lump Premium',
		max_digits=12, decimal_places=2)
	HGFines = forms.DecimalField(required=True, label='High Grade Fines Price',
		max_digits=12, decimal_places=2)
	HGUltraFines = forms.DecimalField(required=True, label='High Grade Ultra Fines',
		max_digits=12, decimal_places=2)
	LGLump = forms.DecimalField(required=True, label='Low Grade Lump Price',
		max_digits=12, decimal_places=2)
	LGLumpPrem = forms.DecimalField(required=True, label='Low Grade Lump Premium',
		max_digits=12, decimal_places=2)
	LGFines = forms.DecimalField(required=True, label='Low Grade Fines Price',
		max_digits=12, decimal_places=2)
	LGUltraFines = forms.DecimalField(required=True, label='Low Grade Ultra Fines',
		max_digits=12, decimal_places=2)
	HGLumpAvg = forms.DecimalField(required=True, label='High Grade Lump Average',
		max_digits=12, decimal_places=2)
	LGLumpAvg = forms.DecimalField(required=True, label='Low Grade Lump Average',
		max_digits=12, decimal_places=2)


class taxesForm(forms.Form):
	def __init__(self, *args, **kwargs):
	        LOM = kwargs.pop('LOM')
	        super(taxesForm, self).__init__(*args, **kwargs)

	        for i in range(int(LOM)):
	        	i += 1
	        	self.fields["year{0}Federal".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Federal".format(i),
	        		decimal_places=4, min_value=0, max_value=1,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 4 Decimal Places'}))
	        	self.fields["year{0}Provincial".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Provincial".format(i),
	        		decimal_places=4, min_value=0, max_value=1,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 4 Decimal Places'}))
	        	self.fields["year{0}Mining".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} Mining".format(i),
	        		decimal_places=4, min_value=0, max_value=1,
	        		widget=forms.NumberInput(attrs={'placeholder': 'Max 4 Decimal Places'}))


class inputsForm(forms.Form):
	Fe2O3Iron = forms.DecimalField(required=True, label='Fe2O3 Iron',
		max_digits=12, decimal_places=6)
	totalGrade = forms.DecimalField(required=True, label='Total Grade',
		max_digits=12, decimal_places=6)
	avgCommodity1Grade = forms.DecimalField(required=True, label='Average Commodity 1 Grade',
		max_digits=12, decimal_places=6)
	lumpRecovery = forms.DecimalField(required=True, label='Lump Percent Recovery',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	finesRecovery = forms.DecimalField(required=True, label='Fines Percent Recovery',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	lumpGrade = forms.DecimalField(required=True, label='Lump Percent Grade',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	finesGrade = forms.DecimalField(required=True, label='Fines Percent Grade',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	feedMoisture = forms.DecimalField(required=True, label='Feed Percent Moisture',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	lumpMoisture = forms.DecimalField(required=True, label='Lump Percent Moisture',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	finesMoisture = forms.DecimalField(required=True, label='Fines Percent Moisture',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	ultraFinesMoisture = forms.DecimalField(required=True, label='Ultra Fines Percent Moisture',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	rejectsMoisture = forms.DecimalField(required=True, label='Rejects Percent Moisture',
		max_digits=12, decimal_places=6, min_value=0, max_value=100)
	mineOpsDays = forms.IntegerField(required=True, label='Mine Operations (Days)', min_value=1,
		max_value=365, initial=1)
	plantOpsDays = forms.IntegerField(required=True, label='Plant Operations (Days)', min_value=1,
		max_value=365, initial=1)
	mineCapacity = forms.DecimalField(required=True, label='Mine Capacity (TPD)',
		max_digits=20, decimal_places=2, min_value=0)
	plantCapacity = forms.DecimalField(required=True, label='Plant Capacity (TPD)',
		max_digits=20, decimal_places=2, min_value=0)
	discountRate1 = forms.DecimalField(required=True, label='Discount Rate 1',
		max_digits=12, decimal_places=6, min_value=0)
	discountRate2 = forms.DecimalField(required=True, label='Discount Rate 2',
		max_digits=12, decimal_places=6, min_value=0)
	discountRate3 = forms.DecimalField(required=True, label='Discount Rate 3',
		max_digits=12, decimal_places=6, min_value=0)
	discountRate4 = forms.DecimalField(required=True, label='Discount Rate 4',
		max_digits=12, decimal_places=6, min_value=0)
	discountRate5 = forms.DecimalField(required=True, label='Discount Rate 5',
		max_digits=12, decimal_places=6, min_value=0)
	discountRate6 = forms.DecimalField(required=True, label='Discount Rate 6',
		max_digits=12, decimal_places=6, min_value=0)
	exchangeRate = forms.DecimalField(required=True, label='Exchange Rate',
		max_digits=4, decimal_places=4, min_value=0)
