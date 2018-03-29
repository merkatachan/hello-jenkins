from django import forms
from setup.models import *

class MineProductForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')

		# Obtain latest projectID
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		numStockpiles = latestProject.numStockpiles

		# # Get the list of declared mineProducts
		# latestMineProduct = tblMineProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# timestamp = latestMineProduct.dateAdded
		# mineProductMatches = tblMineProduct.objects.filter(mineID=int(mineID), dateAdded=timestamp)
		# MPIDs = mineProductMatches.values_list('mineProductID', flat=True)

		# Get list of Plant Product IDs
		latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		PPTimestamp = latestPlantProduct.dateAdded
		PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
		PPIDs = PPMatches.values_list('plantProductID', flat=True)

		# Handle initially declared values
		# hgTonnageInit = None
		# lgTonnageInit = None
		# wasteInit = None
		# overburdenInit = None
		tonnagesInit = None
		# hgInits = {}
		# lgInits = {}
		# wasteInits = {}
		gradesInit = None
		calcDateStr = None
		calculated = False

		overwrite = False

		# Grab optimized values if the calculation has been run
		if 'calculated' in kwargs:
			calculated = kwargs.pop('calculated')
			intermediates = kwargs.pop('intermediates')
			lumpGrades = kwargs.pop('lumpGrades')
			lumpPens = kwargs.pop('lumpPens')
			finesGrades = kwargs.pop('finesGrades')
			finesPens = kwargs.pop('finesPens')
			ultraFinesGrades = kwargs.pop('ultraFinesGrades')
			ultraFinesPens = kwargs.pop('ultraFinesPens')
			rejectsGrades = kwargs.pop('rejectsGrades')
			rejectsPens = kwargs.pop('rejectsPens')
			# hgTonnage = kwargs.pop('hgTonnage')
			# lgTonnage = kwargs.pop('lgTonnage')
			optimizedTonnages = kwargs.pop('optimizedTonnages')
			# hgTonnageInit = kwargs.pop('hgTonnageInit')
			# hgInits = kwargs.pop('hgInits')
			# lgTonnageInit = kwargs.pop('lgTonnageInit')
			# lgInits = kwargs.pop('lgInits')
			# wasteInit = kwargs.pop('wasteInit')
			# wasteInits = kwargs.pop('wasteInits')
			# overburdenInit = kwargs.pop('overburdenInit')
			tonnagesInit = kwargs.pop('tonnagesInit')
			gradesInit = kwargs.pop('gradesInit')
			calcDateStr = kwargs.pop('calcDateStr')
			year = kwargs.pop("year")

		# Grab overwritten values if the user has chosen to override
		if 'overwrite' in kwargs:
			overwrite = kwargs.pop('overwrite')
			OWTonnagesInit = kwargs.pop('OWTonnagesInit')
			# OWHGTonnageInit = kwargs.pop('OWHGTonnageInit')
			# OWLGTonnageInit = kwargs.pop('OWLGTonnageInit')
			OWIntermediates = kwargs.pop('OWIntermediates')
			OWLumpGrades = kwargs.pop('OWLumpGrades')
			OWLumpPens = kwargs.pop('OWLumpPens')
			OWFinesGrades = kwargs.pop('OWFinesGrades')
			OWFinesPens = kwargs.pop('OWFinesPens')
			OWUltraFinesGrades = kwargs.pop('OWUltraFinesGrades')
			OWUltraFinesPens = kwargs.pop('OWUltraFinesPens')
			OWRejectsGrades = kwargs.pop('OWRejectsGrades')
			OWRejectsPens = kwargs.pop('OWRejectsPens')

		super(MineProductForm, self).__init__(*args, **kwargs)

		# Get the list of declared mineProducts
		# latestMineProduct = tblMineProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# timestamp = latestMineProduct.dateAdded
		# mineProductMatches = tblMineProduct.objects.filter(mineID=int(mineID), dateAdded=timestamp)
		# tempIDs = mineProductMatches.values_list('mineProductID', flat=True)

		# if 1 in MPIDs:
		# 	self.fields["highGradeTonnage"] = forms.DecimalField(required=True, label="High Grade Tonnage",
		# 		decimal_places=2, max_digits=20, initial=hgTonnageInit,
		# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# if 2 in MPIDs:
		# 	self.fields["lowGradeTonnage"] = forms.DecimalField(required=True, label="Low Grade Tonnage",
		# 		decimal_places=2, max_digits=20, initial=lgTonnageInit,
		# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# if 3 in MPIDs:
		# 	self.fields["waste"] = forms.DecimalField(required=True, label="Waste",
		# 		decimal_places=2, max_digits=20, initial=wasteInit,
		# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
		# if 4 in MPIDs:
		# 	self.fields["overburden"] = forms.DecimalField(required=True, label="Overburden",
		# 		decimal_places=2, max_digits=20, initial=overburdenInit,
		# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


		latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		timestamp = latestCommodity.dateAdded
		commodities = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=timestamp)
		commIDs = commodities.values_list('commodityID', flat=True)


		for curr in range(1, numStockpiles+1):
			self.fields["stockpile{0}Tonnage".format(curr)] = forms.DecimalField(required=True, 
				label="Stockpile {0} Tonnage".format(curr),
				decimal_places=2, max_digits=20,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			if tonnagesInit:
				self.fields["stockpile{0}Tonnage".format(curr)].initial = tonnagesInit[curr-1]

		for curr in range(1, numStockpiles+1):
			for ID in commIDs:
				commMatch = tblCommodityList.objects.get(commodityID=ID)
				self.fields["stockpile{0}{1}".format(curr,ID)] = forms.DecimalField(required=True,
					label="Stockpile {0} % ".format(curr) + commMatch.name,
					decimal_places=6, max_digits=20,
					widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))
				if gradesInit:
					self.fields["stockpile{0}{1}".format(curr,ID)].initial = gradesInit[curr][ID]

		# if (1 in MPIDs) or (2 in MPIDs):
		# 	if (1 in MPIDs):
		# 		for ID in commIDs:
		# 			commMatch = tblCommodityList.objects.get(commodityID=ID)
		# 			self.fields["highGrade{0}".format(ID)] = forms.DecimalField(required=True,
		# 				label="High Grade % " + commMatch.name,
		# 				decimal_places=6, max_digits=20,
		# 				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))
		# 			if hgInits:
		# 				self.fields["highGrade{0}".format(ID)].initial = hgInits[ID]

		# 	if 2 in MPIDs:
		# 		for ID in commIDs:
		# 			commMatch = tblCommodityList.objects.get(commodityID=ID)
		# 			self.fields["lowGrade{0}".format(ID)] = forms.DecimalField(required=True,
		# 				label="Low Grade % " + commMatch.name,
		# 				decimal_places=6, max_digits=20,
		# 				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))
		# 			if lgInits:
		# 				self.fields["lowGrade{0}".format(ID)].initial = lgInits[ID]

		# if 3 in MPIDs:
		# 	for ID in commIDs:
		# 		commMatch = tblCommodityList.objects.get(commodityID=ID)
		# 		self.fields["waste{0}".format(ID)] = forms.DecimalField(required=True,
		# 			label="Waste Grade % " + commMatch.name,
		# 			decimal_places=6, max_digits=20,
		# 			widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))
		# 		if wasteInits:
		# 			self.fields["waste{0}".format(ID)].initial = wasteInits[ID]

		# Date Selection Field
		# if calculated:
		# 	self.fields["calcDate"] = forms.DateField(required=True, label='Date',
		# 		initial=calcDateStr, disabled=True, 
		# 		widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))
		# else:
		# 	self.fields["calcDate"] = forms.DateField(required=True, label='Date', 
		# 		widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))
		self.fields["calcDate"] = forms.DateField(required=True, label='Date', 
			widget=forms.DateInput(format="%Y-%m-%d", attrs={'class':'datepicker'}))

		if calculated:
			self.fields["calcDate"].initial = calcDateStr
			self.fields["calcDate"].widget.attrs['disabled'] = True
			self.fields["year"] = forms.IntegerField(required=False,
				initial=year, widget=forms.HiddenInput())

			# if 1 in MPIDs:
			# 	self.fields["wmtHighGrade"] = forms.DecimalField(required=True, label="Optimized High Grade Tonnage",
			# 		decimal_places=6, max_digits=20,
			# 		initial=round(hgTonnage,2),  
			# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			# if 2 in MPIDs:
			# 	self.fields["wmtLowGrade"] = forms.DecimalField(required=True, label="Optimized Low Grade Tonnage",
			# 		decimal_places=6, max_digits=20,
			# 		initial=round(lgTonnage,2), 
			# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			for curr in range(1, numStockpiles+1):
				self.fields["wmtStockpile{0}".format(curr)] = forms.DecimalField(required=True,
					label="Optimized Stockpile {0} Tonnage".format(curr),
					decimal_places=6, max_digits=20,
					initial=round(optimizedTonnages[curr-1],2), 
					widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			# for curr in range(1, numStockpiles+1):
			# 	for ID in commIDs:
			# 		commMatch = tblCommodityList.objects.get(commodityID=ID)
			# 		self.fields["stockpile{0}Grade{1}".format(curr,ID)] = forms.DecimalField(required=True,
			# 			label="Optimized Grade % {0}".format(commMatch.name),
			# 			decimal_places=6, max_digits=20,
			# 			initial=round(intermediates[ID],2), disabled=True, 
			# 			widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			for ID in commIDs:
				commMatch = tblCommodityList.objects.get(commodityID=ID)
				self.fields["intermediateGrade{0}".format(ID)] = forms.DecimalField(required=True,
					label="Optimized Grade % {0}".format(commMatch.name),
					decimal_places=6, max_digits=20,
					initial=round(intermediates[ID],2), disabled=True, 
					widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

				if 1 in PPIDs:
					self.fields["lumpGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(lumpGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["lumpPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(lumpPens[ID],2),
						widget=forms.HiddenInput())

					# Debug Mode
					# self.fields["lumpGrade{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(lumpGrades[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

					# self.fields["lumpPen{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(lumpPens[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

				if 2 in PPIDs:
					self.fields["finesGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(finesGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["finesPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(finesPens[ID],2),
						widget=forms.HiddenInput())

					# # Debug Mode
					# self.fields["finesGrade{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(finesGrades[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

					# self.fields["finesPen{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(finesPens[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

				if 3 in PPIDs:
					self.fields["ultraFinesGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(ultraFinesGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["ultraFinesPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(ultraFinesPens[ID],2),
						widget=forms.HiddenInput())

					# # Debug Mode
					# self.fields["ultraFinesGrade{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(ultraFinesGrades[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

					# self.fields["ultraFinesPen{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(ultraFinesPens[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

				if 4 in PPIDs:
					self.fields["rejectsGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(rejectsGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["rejectsPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(rejectsPens[ID],2),
						widget=forms.HiddenInput())

					# # Debug Mode
					# self.fields["rejectsGrade{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(rejectsGrades[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

					# self.fields["rejectsPen{0}".format(ID)] = forms.DecimalField(required=False,
					# 	decimal_places=6, max_digits=20,
					# 	initial=round(rejectsPens[ID],2), disabled=True,
					# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			# if 1 in MPIDs:
			# 	self.fields["wmtHighGradeOW"] = forms.DecimalField(required=False, label="Overwrite High Grade Tonnage",
			# 		decimal_places=6, max_digits=20,  
			# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			# if 2 in MPIDs:
			# 	self.fields["wmtLowGradeOW"] = forms.DecimalField(required=False, label="Overwrite Low Grade Tonnage",
			# 		decimal_places=6, max_digits=20,
			# 		widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			for curr in range(1, numStockpiles+1):
				self.fields["wmtStockpile{0}OW".format(curr)] = forms.DecimalField(required=False,
					label="Overwrite Stockpile {0} Tonnage".format(curr),
					decimal_places=6, max_digits=20,  
					widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

		if overwrite:
			# Initial Values for wmtHighGradeOW and wmtLowGradeOW, and disable the fields
			# self.fields["wmtHighGradeOW"].initial = OWHGTonnageInit
			# self.fields["wmtLowGradeOW"].initial = OWLGTonnageInit
			# self.fields["wmtHighGradeOW"].widget.attrs['disabled'] = True
			# self.fields["wmtLowGradeOW"].widget.attrs['disabled'] = True
			for curr in range(1, numStockpiles+1):
				self.fields["wmtStockpile{0}OW".format(curr)].initial = OWTonnagesInit[curr-1]

			# OWIntermediates
			for ID in commIDs:
				commMatch = tblCommodityList.objects.get(commodityID=ID)
				self.fields["OWIntermediateGrade{0}".format(ID)] = forms.DecimalField(required=True,
					label="Overwrite Grade % {0}".format(commMatch.name),
					decimal_places=6, max_digits=20,
					initial=round(OWIntermediates[ID],2), disabled=True, 
					widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

				# OWLumpGrades and OWLumpPens
				if 1 in PPIDs:
					self.fields["OWLumpGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWLumpGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["OWLumpPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWLumpPens[ID],2),
						widget=forms.HiddenInput())
			
				# OWFinesGrades and OWFinesPens
				if 2 in PPIDs:
					self.fields["OWFinesGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWFinesGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["OWFinesPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWFinesPens[ID],2),
						widget=forms.HiddenInput())

				# OWUltraFinesGrades and OWUltraFinesPens
				if 3 in PPIDs:
					self.fields["OWUltraFinesGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWUltraFinesGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["OWUltraFinesPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWUltraFinesPens[ID],2),
						widget=forms.HiddenInput())

				# OWRejectsGrades and OWRejectsPens
				if 4 in PPIDs:
					self.fields["OWRejectsGrade{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWRejectsGrades[ID],2),
						widget=forms.HiddenInput())

					self.fields["OWRejectsPen{0}".format(ID)] = forms.DecimalField(required=False,
						decimal_places=6, max_digits=20,
						initial=round(OWRejectsPens[ID],2),
						widget=forms.HiddenInput())

				# Removed HG and LG Ore Overwrite fields
				# if 1 in MPIDs:
					# self.fields["wmtHighGradeOW"] = forms.DecimalField(required=False, label="Optimized High Grade Tonnage Overwrite",
						# decimal_places=2, max_digits=20,
						# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

				# if 2 in MPIDs:
					# self.fields["wmtLowGradeOW"] = forms.DecimalField(required=False, label="Optimized Low Grade Tonnage Overwrite",
						# decimal_places=2, max_digits=20,
						# widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

				# self.fields["highGrade{0}".format(ID)] = forms.DecimalField(required=True,
				# 	label="High Grade % {0}".format(commMatch.name),
				# 	decimal_places=2, max_digits=20,
				# 	initial=round(lumpGrades[ID],2), disabled=True, 
				# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

				# self.fields["lowGrade{0}".format(ID)] = forms.DecimalField(required=True,
				# 	label="Low Grade % {0}".format(commMatch.name),
				# 	decimal_places=2, max_digits=20,
				# 	initial=round(finesGrades[ID],2), disabled=True,
				# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

				# self.fields["lumpPen{0}".format(ID)] = forms.DecimalField(required=True,
				# 	label="Lump Penalty {0}".format(commMatch.name),
				# 	decimal_places=2, max_digits=20,
				# 	initial=round(lumpPens[ID],2), disabled=True, 
				# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

				# self.fields["finesPen{0}".format(ID)] = forms.DecimalField(required=True,
				# 	label="Fines Penalty {0}".format(commMatch.name),
				# 	decimal_places=2, max_digits=20,
				# 	initial=round(finesPens[ID],2), disabled=True, 
				# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

				# if 3 in tempIDs:
				# 	self.fields["ultraFinesGrade{0}".format(ID)] = forms.DecimalField(required=True,
				# 	label="Ultra Fines Grade % {0}".format(commMatch.name),
				# 	decimal_places=2, max_digits=20,
				# 	initial=round(ultraFinesGrades[ID],2), disabled=True, 
				# 	widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))



				
class MineProductOptimizedForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		lumpGrades = kwargs.pop('lumpGrades')
		lumpPens = kwargs.pop('lumpPens')
		finesGrades = kwargs.pop('finesGrades')
		finesPens = kwargs.pop('finesPens')
		hgTonnage = kwargs.pop('hgTonnage')
		lgTonnage = kwargs.pop('lgTonnage')
		super(MineProductOptimizedForm, self).__init__(*args, **kwargs)

		self.fields["wmtHighGrade"] = forms.DecimalField(required=True, label="Optimized High Grade Tonnage",
			decimal_places=2, max_digits=20,
			initial=round(hgTonnage,2), disabled=True, 
			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		self.fields["wmtLowGrade"] = forms.DecimalField(required=True, label="Optimized Low Grade Tonnage",
			decimal_places=2, max_digits=20,
			initial=round(lgTonnage,2), disabled=True, 
			widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))

		# Get list of Commodity IDs
		latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		commtimestamp = latestCommodity.dateAdded
		commodities = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=commtimestamp)
		commIDs = commodities.values_list('commodityID', flat=True)

		for ID in commIDs:
			commMatch = tblCommodityList.objects.get(commodityID=ID)
			self.fields["highGrade{0}".format(ID)] = forms.DecimalField(required=True,
				label="High Grade % {0}".format(commMatch.name),
				decimal_places=6, max_digits=20,
				initial=round(lumpGrades[ID],2), disabled=True, 
				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			self.fields["lowGrade{0}".format(ID)] = forms.DecimalField(required=True,
				label="Low Grade % {0}".format(commMatch.name),
				decimal_places=6, max_digits=20,
				initial=round(finesGrades[ID],2), disabled=True,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			self.fields["lumpPen{0}".format(ID)] = forms.DecimalField(required=True,
				label="Lump Penalty {0}".format(commMatch.name),
				decimal_places=6, max_digits=20,
				initial=round(lumpPens[ID],2), disabled=True, 
				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

			self.fields["finesPen{0}".format(ID)] = forms.DecimalField(required=True,
				label="Fines Penalty {0}".format(commMatch.name),
				decimal_places=6, max_digits=20,
				initial=round(finesPens[ID],2), disabled=True, 
				widget=forms.NumberInput(attrs={'placeholder': 'Max 6 Decimal Places'}))

				
# class MineProductFormOverwrite(forms.Form):
# 	def __init__(self, *args, **kwargs):
# 			 = kwargs.pop('int(mineProductID)')
# 			super(MineProductForm, self).__init__(*args, **kwargs)

# 			for i in range(int(mineProductID)):
# 				i += 1
# 				self.fields["mineProductID{0}MineProductTonnage".format(i)] = forms.DecimalField(required=True,
# 		        		label="Year{0} Product Tonnage".format(i),
# 		        		decimal_places=2, max_digits=20,
# 		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
# 				self.fields["mineProductID{0}MineProductGrade".format(i)] = forms.DecimalField(required=True,
# 		        		label="Year{0} Mining Equipment Initial".format(i),
# 		        		decimal_places=2, max_digits=20,
# 		        		widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
# 				self.fields["mineProductID{0}Optimized".format(i)] = "TRUE"