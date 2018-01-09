from django import forms
from decimal import Decimal
from setup.models import *

class commodityForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		super(commodityForm, self).__init__(*args, **kwargs)

		# Get the latest project by this user/mine
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]

		commodityEntries = tblCommodity.objects.filter(projectID=latestProject.projectID)
		initialCommIDs = []
		for entry in commodityEntries:
			initialCommIDs.append(str(entry.commodityID))

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
			('43', "REE"))

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

		self.fields["mainCommodity1"] = forms.MultipleChoiceField(required=False,
			choices=MAINOPTIONS1,
			widget=forms.CheckboxSelectMultiple,
			initial=initialCommIDs)

		self.fields["mainCommodity2"] = forms.MultipleChoiceField(required=False,
			choices=MAINOPTIONS2,
			widget=forms.CheckboxSelectMultiple,
			initial=initialCommIDs)

		self.fields["mainCommodity3"] = forms.MultipleChoiceField(required=False,
			choices=MAINOPTIONS3,
			widget=forms.CheckboxSelectMultiple,
			initial=initialCommIDs)

		self.fields["delCommodity1"] = forms.MultipleChoiceField(required=False,
			choices=DELOPTIONS1,
			widget=forms.CheckboxSelectMultiple,
			initial=initialCommIDs)

		self.fields["delCommodity2"] = forms.MultipleChoiceField(required=False,
			choices=DELOPTIONS2,
			widget=forms.CheckboxSelectMultiple,
			initial=initialCommIDs)

		self.fields["delCommodity3"] = forms.MultipleChoiceField(required=False,
			choices=DELOPTIONS3,
			widget=forms.CheckboxSelectMultiple,
			initial=initialCommIDs)

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
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		super(productsForm, self).__init__(*args, **kwargs)

		# Get the latest project by this user/mine
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		initialProjectTypeID = str(latestProject.projectTypeID_id)
		initialLOM = latestProject.LOM

		latestMineProduct = tblMineProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		timestamp = latestMineProduct.dateAdded
		mineProds = tblMineProduct.objects.filter(mineID=int(mineID), dateAdded=timestamp).values_list('mineProductID_id', flat=True)
		initialMineProds = []
		for prod in mineProds:
			initialMineProds.append(str(prod))

		latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		plantProds = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=timestamp).values_list('plantProductID_id', flat=True)
		initialPlantProds = []
		for prod in plantProds:
			initialPlantProds.append(str(prod))

		projectChoices = (
			('1', 'Study'),
			('2', 'Operation')
			)
		# projectType = forms.ChoiceField(choices=projectChoices, required=True, label="Project Type", initial=('2','Operation'))

		self.fields["projectType"] = forms.ChoiceField(required=True,
		        		label="Project Type",
		        		choices=projectChoices,
		        		initial=initialProjectTypeID)

		mineProductChoices = (
			('1', 'High Grade Ore'),
			('2', 'Low Grade Ore'),
			('3', 'Waste'),
			('4', 'Overburden')
			)

		# mineProduct = forms.MultipleChoiceField(label='Mine Products', required=True,
		# 	widget=forms.CheckboxSelectMultiple, choices=mineProductChoices, initial=initialMineProds)

		self.fields["mineProduct"] = forms.MultipleChoiceField(required=True,
		        		label="Mine Products",
		        		choices=mineProductChoices,
		        		widget=forms.CheckboxSelectMultiple,
		        		initial=initialMineProds)

		plantProductChoices = (
			('1', 'Lump'),
			('2', 'Fines'),
			('3', 'Ultra Fines'),
			('4', 'Rejects')
			)

		# plantProduct = forms.MultipleChoiceField(label='Plant Products', required=True,
		# 	widget=forms.CheckboxSelectMultiple, choices=plantProductChoices, initial=initialPlantProds)

		self.fields["plantProduct"] = forms.MultipleChoiceField(required=True,
		        		label="Plant Products",
		        		choices=plantProductChoices,
		        		widget=forms.CheckboxSelectMultiple,
		        		initial=initialPlantProds)

		# LOM = forms.IntegerField(required=True, label='LOM', min_value=1, initial=initialLOM)

		self.fields["LOM"] = forms.IntegerField(required=True,
		        		label="LOM",
		        		min_value=1,
		        		initial=initialLOM
		        		)


class mineProductionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		LOM = kwargs.pop('LOM')
		MPIDs = kwargs.pop('mineProducts')
		idList = kwargs.pop('idList')
		commNameList = kwargs.pop('commNameList')
		super(mineProductionForm, self).__init__(*args, **kwargs)

		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		LOM = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()

		# Get list of Mine Product IDs
		mineProductMatches = tblMineProduct.objects.filter(projectID=latestProject.projectID)
		MPIDs = mineProductMatches.values_list('mineProductID', flat=True)

		# Get list of Commodity IDs
		commodities = tblCommodity.objects.filter(projectID=latestProject.projectID)
		idList = commodities.values_list('commodityID', flat=True)

		commNameList = []
		for ID in idList:
			commodityMatch = tblCommodityList.objects.get(commodityID=ID)
			commNameList.append(commodityMatch.name)

		if 1 in MPIDs:
			for i in range(int(LOM)):
				i += 1
				# currEntry = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=1, year=i)
				self.fields["year{0}MinePlanHighGradeTonnage".format(i)] = forms.DecimalField(required=True, 
					label="Year{0} Mine Plan High Grade Tonnage".format(i), decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				for j in range(len(idList)):
					# currEntry = tblMineProductGrade.objects.get(projectID=latestProject.projectID, mineProductID=1,
					# 		commodityID=idList[j], year=i)
					self.fields["year{0}MinePlanHGGrade{1}".format(i, commNameList[j])] = forms.DecimalField(required=True, 
						label="Year{0} Mine Plan High Grade {1} %".format(i, commNameList[j]), decimal_places=6, max_digits=20,
						widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

		if 2 in MPIDs:
			for i in range(int(LOM)):
				i += 1
				# currEntry = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=2, year=i)
				self.fields["year{0}MinePlanLowGradeTonnage".format(i)] = forms.DecimalField(required=True, 
					label="Year{0} Mine Plan Low Grade Tonnage".format(i), decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				for j in range(len(idList)):
					# currEntry = tblMineProductGrade.objects.get(projectID=latestProject.projectID, mineProductID=2,
					# 		commodityID=idList[j], year=i)
					self.fields["year{0}MinePlanLGGrade{1}".format(i, commNameList[j])] = forms.DecimalField(required=True, 
						label="Year{0} Mine Plan Low Grade {1} %".format(i, commNameList[j]), decimal_places=6, max_digits=20,
						widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

		if 3 in MPIDs:
			for i in range(int(LOM)):
				i += 1
				# currEntry = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=3, year=i)
				self.fields["year{0}MinePlanWasteTonnage".format(i)] = forms.DecimalField(required=True, 
					label="Year{0} Mine Plan Waste Tonnage".format(i), decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		if 4 in MPIDs:
			for i in range(int(LOM)):
				i += 1
				# currEntry = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=4, year=i)
				self.fields["year{0}MinePlanOverburdenTonnage".format(i)] = forms.DecimalField(required=True, 
					label="Year{0} Mine Plan Overburden Tonnage".format(i), decimal_places=2, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


class CAPEXForm(forms.Form):
	def __init__(self, *args, **kwargs):
			mineID = kwargs.pop('mineID')
			super(CAPEXForm, self).__init__(*args, **kwargs)

			# Get the latest project by this user/mine
			latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
			LOM = latestProject.LOM

			# latestCAPEX = tblCAPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
			# timestamp = latestCAPEX.dateAdded

			for i in range(LOM):
				i += 1
				self.fields["year{0}PreStripping".format(i)] = forms.DecimalField(required=True,
		        		label="Year{0} Pre-Stripping".format(i),
		        		decimal_places=2, max_digits=20,
		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
				# self.declared_fields["year{0}PreStripping".format(i)].initial = 0.33
				# self.fields["year{0}PreStripping".format(i)].initial = float(0.33)
				# result = tblCAPEX.objects.filter(mineID=int(mineID), year=i, dateAdded=timestamp)
				# if result:
				# 	row = result[0]
				# 	# self.initial["year{0}PreStripping".format(i)] = Decimal(row.preStrip)
				# 	self.fields["year{0}PreStripping".format(i)].initial = row.preStrip
				# else:
				# 	# self.initial["year{0}PreStripping".format(i)] = 0.33
				# 	self.fields["year{0}PreStripping".format(i)].initial = 0.33
				# else:
				# 	self.fields["year{0}PreStripping".format(i)] = forms.DecimalField(required=True,
		  #       		label="Year{0} Pre-Stripping".format(i),
		  #       		decimal_places=2, max_digits=20, initial=Decimal(22.22),
		  #       		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


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
			mineID = kwargs.pop('mineID')
			super(OPEXForm, self).__init__(*args, **kwargs)

	        # Get the latest project by this user/mine
			latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
			LOM = latestProject.LOM

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
				self.fields["year{0}OpexPT".format(i)] = forms.DecimalField(required=True,
	        		label="Year{0} OPEX (CAD$/t)".format(i),
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


class priceForm(forms.Form):
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


# class inputsForm(forms.Form):
	# Fe2O3Iron = forms.DecimalField(required=True, label='Fe2O3 Iron',
		# max_digits=12, decimal_places=6)
	# totalGrade = forms.DecimalField(required=True, label='Total Grade',
		# max_digits=12, decimal_places=6)
	# avgCommodity1Grade = forms.DecimalField(required=True, label='Average Commodity 1 Grade',
		# max_digits=12, decimal_places=6)
	# lumpRecovery = forms.DecimalField(required=True, label='Lump Percent Recovery',
		# max_digits=12, decimal_places=6)
	# finesRecovery = forms.DecimalField(required=True, label='Fines Percent Recovery',
		# max_digits=12, decimal_places=6)
	# lumpGrade = forms.DecimalField(required=True, label='Lump Percent Grade',
		# max_digits=12, decimal_places=6)
	# finesGrade = forms.DecimalField(required=True, label='Fines Percent Grade',
		# max_digits=12, decimal_places=6)
	# feedMoisture = forms.DecimalField(required=True, label='Feed Percent Moisture',
		# max_digits=12, decimal_places=6)
	# lumpMoisture = forms.DecimalField(required=True, label='Lump Percent Moisture',
		# max_digits=12, decimal_places=6)
	# finesMoisture = forms.DecimalField(required=True, label='Fines Percent Moisture',
		# max_digits=12, decimal_places=6)
	# ultraFinesMoisture = forms.DecimalField(required=True, label='Ultra Fines Percent Moisture',
		# max_digits=12, decimal_places=6)
	# rejectsMoisture = forms.DecimalField(required=True, label='Rejects Percent Moisture',
		# max_digits=12, decimal_places=6)
	# mineOpsDays = forms.IntegerField(required=True, label='Mine Operations (Days)', 
		# max_digits=12, decimal_places=6)
	# plantOpsDays = forms.IntegerField(required=True, label='Plant Operations (Days)', 
		# max_digits=3, decimal_places=2)
	# mineCapacity = forms.DecimalField(required=True, label='Mine Capacity (TPD)',
		# max_digits=20, decimal_places=2)
	# plantCapacity = forms.DecimalField(required=True, label='Plant Capacity (TPD)',
		# max_digits=20, decimal_places=2)
	# discountRate1 = forms.DecimalField(required=True, label='Discount Rate 1',
		# max_digits=12, decimal_places=6)
	# discountRate2 = forms.DecimalField(required=True, label='Discount Rate 2',
		# max_digits=12, decimal_places=6)
	# discountRate3 = forms.DecimalField(required=True, label='Discount Rate 3',
		# max_digits=12, decimal_places=6)
	# discountRate4 = forms.DecimalField(required=True, label='Discount Rate 4',
		# max_digits=12, decimal_places=6)
	# discountRate5 = forms.DecimalField(required=True, label='Discount Rate 5',
		# max_digits=12, decimal_places=6)
	# discountRate6 = forms.DecimalField(required=True, label='Discount Rate 6',
		# max_digits=12, decimal_places=6)
	# exchangeRate = forms.DecimalField(required=True, label='Exchange Rate',
		# max_digits=12, decimal_places=4)

class inputsForm(forms.Form):
	Fe2O3Iron = forms.DecimalField(required=True, label='Fe2O3 Iron',
		max_digits=12, decimal_places=6)
	totalGrade = forms.DecimalField(required=True, label='Total Grade',
		max_digits=12, decimal_places=6)
	avgCommodity1Grade = forms.DecimalField(required=True, label='Average Commodity 1 Grade',
		max_digits=12, decimal_places=6)
	lumpRecovery = forms.DecimalField(required=True, label='Lump Percent Recovery',
		max_digits=12, decimal_places=6, max_value=100)
	finesRecovery = forms.DecimalField(required=True, label='Fines Percent Recovery',
		max_digits=12, decimal_places=6, max_value=100)
	lumpGrade = forms.DecimalField(required=True, label='Lump Percent Grade',
		max_digits=12, decimal_places=6, max_value=100)
	finesGrade = forms.DecimalField(required=True, label='Fines Percent Grade',
		max_digits=12, decimal_places=6, max_value=100)
	feedMoisture = forms.DecimalField(required=True, label='Feed Percent Moisture',
		max_digits=12, decimal_places=6, max_value=100)
	lumpMoisture = forms.DecimalField(required=True, label='Lump Percent Moisture',
		max_digits=12, decimal_places=6, max_value=100)
	finesMoisture = forms.DecimalField(required=True, label='Fines Percent Moisture',
		max_digits=12, decimal_places=6, max_value=100)
	ultraFinesMoisture = forms.DecimalField(required=True, label='Ultra Fines Percent Moisture',
		max_digits=12, decimal_places=6, max_value=100)
	rejectsMoisture = forms.DecimalField(required=True, label='Rejects Percent Moisture',
		max_digits=12, decimal_places=6, max_value=100)
	mineOpsDays = forms.DecimalField(required=True, label='Mine Operations (Days)', 
		max_digits=12, decimal_places=6)
	plantOpsDays = forms.DecimalField(required=True, label='Plant Operations (Days)',
		max_digits=12, decimal_places=6)
	mineCapacity = forms.DecimalField(required=True, label='Mine Capacity (TPD)',
		max_digits=20, decimal_places=2)
	plantCapacity = forms.DecimalField(required=True, label='Plant Capacity (TPD)',
		max_digits=20, decimal_places=2)
	discountRate1 = forms.DecimalField(required=True, label='Discount Rate 1',
		max_digits=12, decimal_places=6, max_value=100)
	discountRate2 = forms.DecimalField(required=True, label='Discount Rate 2',
		max_digits=12, decimal_places=6, max_value=100)
	discountRate3 = forms.DecimalField(required=True, label='Discount Rate 3',
		max_digits=12, decimal_places=6, max_value=100)
	discountRate4 = forms.DecimalField(required=True, label='Discount Rate 4',
		max_digits=12, decimal_places=6, max_value=100)
	discountRate5 = forms.DecimalField(required=True, label='Discount Rate 5',
		max_digits=12, decimal_places=6, max_value=100)
	discountRate6 = forms.DecimalField(required=True, label='Discount Rate 6',
		max_digits=12, decimal_places=6, max_value=100)
	exchangeRate = forms.DecimalField(required=True, label='Exchange Rate',
		max_digits=12, decimal_places=4, max_value=100)
		
	# def __init__(self, *args, **kwargs):
		# mineID = kwargs.pop('mineID')
		# super(inputsForm, self).__init__(*args, **kwargs)

		# #Get list of Plant Product IDs
		# latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# PPTimestamp = latestPlantProduct.dateAdded
		# PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
		# PPIDs = PPMatches.values_list('plantProductID', flat=True)

		# self.fields["Fe2O3Iron"] = forms.DecimalField(required=True,
        	# label="Fe2O3Iron", decimal_places=6, max_digits=12,
        	# widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

		# self.fields["totalGrade"] = forms.DecimalField(required=True,
    		# label="totalGrade", decimal_places=2, max_digits=12,
    		# max_value=100,
    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# self.fields["avgCommodity1Grade"] = forms.DecimalField(required=True,
    		# label="Average Commodity 1 Grade", decimal_places=2, max_digits=12,
    		# max_value=100,
    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 1 in PPIDs:
			# self.fields["lumpRecovery"] = forms.DecimalField(required=True,
	    		# label="Lump Percent Recovery", decimal_places=2, max_digits=12,
	    		# max_value=100,
	    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 2 in PPIDs:
			# self.fields["finesRecovery"] = forms.DecimalField(required=True,
	    		# label="Fines Percent Recovery", decimal_places=2, max_digits=12,
	    		# max_value=100,
	    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 3 in PPIDs:
			# self.fields["ultraFinesRecovery"] = forms.DecimalField(required=True,
    			# label="Ultra Fines Percent Recovery", decimal_places=2, max_digits=12,
    			# max_value=100,
    			# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 4 in PPIDs:
			# self.fields["rejectsRecovery"] = forms.DecimalField(required=True,
    			# label="Rejects Percent Recovery", decimal_places=2, max_digits=12,
    			# max_value=100,
    			# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 1 in PPIDs:
			# self.fields["lumpGrade"] = forms.DecimalField(required=True,
	    		# label="Lump Percent Grade", decimal_places=2, max_digits=12,
	    		# max_value=100,
	    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 2 in PPIDs:
			# self.fields["finesGrade"] = forms.DecimalField(required=True,
	    		# label="Fines Percent Grade", decimal_places=2, max_digits=12,
	    		# max_value=100,
	    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 3 in PPIDs:
			# self.fields["ultraFinesGrade"] = forms.DecimalField(required=True,
    			# label="Ultra Fines Percent Grade", decimal_places=2, max_digits=12,
    			# max_value=100,
    			# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 4 in PPIDs:
			# self.fields["rejectsGrade"] = forms.DecimalField(required=True,
    			# label="Rejects Percent Grade", decimal_places=2, max_digits=12,
    			# max_value=100,
    			# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# self.fields["feedMoisture"] = forms.DecimalField(required=True,
    		# label="Feed Percent Moisture", decimal_places=2, max_digits=12,
    		# max_value=100,
    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 1 in PPIDs:
			# self.fields["lumpMoisture"] = forms.DecimalField(required=True,
	    		# label="Lump Percent Moisture", decimal_places=2, max_digits=12,
	    		# max_value=100,
	    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 2 in PPIDs:
			# self.fields["finesMoisture"] = forms.DecimalField(required=True,
	    		# label="Fines Percent Moisture", decimal_places=2, max_digits=12,
	    		# max_value=100,
	    		# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 3 in PPIDs:
			# self.fields["ultraFinesMoisture"] = forms.DecimalField(required=True,
    			# label="Ultra Fines Percent Moisture", decimal_places=2, max_digits=12,
    			# max_value=100,
    			# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# if 4 in PPIDs:
			# self.fields["rejectsMoisture"] = forms.DecimalField(required=True,
    			# label="Rejects Percent Moisture", decimal_places=2, max_digits=12,
    			# max_value=100,
    			# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# self.fields["mineOpsDays"] = forms.DecimalField(required=True,
    		# label="Mine Operations (Days)", max_digits=12, decimal_places=6,
			# widget=forms.NumberInput(attrs={'placeholder': 'Between 0  - 365'}))

		# self.fields["plantOpsDays"] = forms.DecimalField(required=True,
    		# label="Plant Operations (Days)", max_digits=12, decimal_places=6,
			# widget=forms.NumberInput(attrs={'placeholder': 'Between 0 - 365'}))

		# self.fields["mineCapacity"] = forms.DecimalField(required=True,
    		# label="Mine Capacity (TPD)", max_digits=20, decimal_places=2,
    		# min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# self.fields["plantCapacity"] = forms.DecimalField(required=True,
    		# label="Plant Capacity (TPD)", max_digits=20, decimal_places=2,
    		# min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# self.fields["discountRate1"] = forms.DecimalField(required=True,
    		# label="Discount Rate 1 (%)", max_digits=12, decimal_places=6, max_value=100, widget=forms.NumberInput(attrs={'placeholder': '0-100%, Max 2 Decimal Places'}))

		# self.fields["discountRate2"] = forms.DecimalField(required=True,
    		# label="Discount Rate 2 (%)", max_digits=12, decimal_places=6, max_value=100, widget=forms.NumberInput(attrs={'placeholder': '0-100%, Max 2 Decimal Places'}))

		# self.fields["discountRate3"] = forms.DecimalField(required=True,
    		# label="Discount Rate 3 (%)", max_digits=12, decimal_places=6, max_value=100, widget=forms.NumberInput(attrs={'placeholder': '0-100%, Max 2 Decimal Places'}))

		# self.fields["discountRate4"] = forms.DecimalField(required=True,
    		# label="Discount Rate 4 (%)", max_digits=12, decimal_places=6, max_value=100, widget=forms.NumberInput(attrs={'placeholder': '0-100%, Max 2 Decimal Places'}))

		# self.fields["discountRate5"] = forms.DecimalField(required=True,
    		# label="Discount Rate 5 (%)", max_digits=12, decimal_places=6, max_value=100, widget=forms.NumberInput(attrs={'placeholder': '0-100%, Max 2 Decimal Places'}))

		# self.fields["discountRate6"] = forms.DecimalField(required=True,
    		# label="Discount Rate 6 (%)", max_digits=12, decimal_places=6, max_value=100, widget=forms.NumberInput(attrs={'placeholder': '0-100%, Max 2 Decimal Places'}))

		# self.fields["exchangeRate"] = forms.DecimalField(label=" Exchange Rate (US$-CAN$)", decimal_places=6,
			# max_digits=12, widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))
