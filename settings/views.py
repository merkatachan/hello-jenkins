from django.shortcuts import render
from django.utils import timezone

from decimal import Decimal
from .forms import *
from setup.models import *

# Function index handles declaring of main commodities.
def editCommodities(request):
	mineID = request.session["mineID"]
	#form_class = commodityForm

	# Grab information about declared commodities
	latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	timestamp = latestCommodity.dateAdded
	commodityMatches = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=timestamp)
	idList = []
	commNameList = []
	tempIDs = commodityMatches.values_list('commodityID', flat=True)
	for match in tempIDs:
		idList.append(match)
		nameMatch = tblCommodityList.objects.get(commodityID=match)
		commNameList.append(nameMatch.name)

	if request.method == 'POST':

		form = commodityForm(request.POST, mineID=mineID)
		if form.is_valid():
			subCommodities1 = request.POST.getlist('mainCommodity1')
			subCommodities2 = request.POST.getlist('mainCommodity2')
			subCommodities3 = request.POST.getlist('mainCommodity3')
			mainCommodities = subCommodities1 + subCommodities2 + subCommodities3
			if len(mainCommodities) == 0:
				errorMsg = "You must select at least one main commodity. Try again."
				return render(request, 'setup/commodity.html', {'form': form_class,
					'errorMsg': errorMsg})
			elif len(mainCommodities) > 4:
				errorMsg = "You cannot select more than four main commodities. Try again."
				return render(request, 'setup/commodity.html', {'form': form_class,
					'errorMsg': errorMsg})


			subCommodities1 = request.POST.getlist('delCommodity1')
			subCommodities2 = request.POST.getlist('delCommodity2')
			subCommodities3 = request.POST.getlist('delCommodity3')
			delCommodities = subCommodities1 + subCommodities2 + subCommodities3
			if len(delCommodities) == 0:
				errorMsg = "You must select at least one deleterious commodity. Try again."
				return render(request, 'settings/commodity.html', {'form': form_class,
					'errorMsg': errorMsg})
			elif len(delCommodities) > 4:
				errorMsg = "You cannot select more than four deleterious commodities. Try again."
				return render(request, 'settings/commodity.html', {'form': form_class,
					'errorMsg': errorMsg})

			# mainCommodities = request.POST.getlist('commodity')
			mineID = request.session["mineID"]
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			dateAdded = timezone.localtime(timezone.now())

			for commodity in mainCommodities:
				commodityMatch = tblCommodityList.objects.get(commodityID=int(commodity))
				tblCommodityObj = tblCommodity(commodityID=commodityMatch,
					mineID=mineMatch, dateAdded=dateAdded)
				tblCommodityObj.save()

			for commodity in delCommodities:
				commodityMatch = tblCommodityList.objects.get(commodityID=int(commodity))
				tblCommodityObj = tblCommodity(commodityID=commodityMatch,
					mineID=mineMatch, dateAdded=dateAdded)
				tblCommodityObj.save()

			# next_form_class = commodityDelForm
			# return render(request, 'setup/delCommodity.html', {'form': next_form_class,
			# 	'mainCommodityRegistered': True}) #Redirect

			return render(request, 'settings/success.html', { }) #Redirect
			
		form_class = commodityForm(mineID=mineID)
		return render_to_response("settings/commodity.html", {'form': form_class})

	else:
		form_class = commodityForm(mineID=mineID)
		return render(request, "settings/commodity.html", {'form': form_class})



# Function editProject handles project info updates and changes made by the user.
def editProject(request):
	mineID = request.session["mineID"]
	if request.method == 'POST':
		form = productsForm(request.POST, mineID=mineID)
		mineProducts = request.POST.getlist('mineProduct')
		plantProducts = request.POST.getlist('plantProduct')
		if len(mineProducts) == 0 or len(plantProducts) == 0:
			errorMsg = "You must declare at least one mine product and one plant product. Try Again."
			return render(request, 'settings/products.html', {'form': form_class, 'errorMsg': errorMsg})

		LOM = str(request.POST.get('LOM', ''))
		if LOM is None:
			errorMsg = "You must declare an LOM. Try again."
			return render(request, 'settings/products.html', {'form': form_class, 'errorMsg': errorMsg})

		if form.is_valid():
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			dateAdded = timezone.localtime(timezone.now())

			# Insert into tblMineProduct
			for product in mineProducts:
				mineProductMatch = tblMineProductList.objects.get(mineProductID=int(product))
				tblMineProductObj = tblMineProduct(mineProductID=mineProductMatch,
					mineID=mineMatch, dateAdded=dateAdded)
				tblMineProductObj.save()

			# Insert into tblPlantProduct
			for product in plantProducts:
				plantProductMatch = tblPlantProductList.objects.get(plantProductID=int(product))
				tblPlantProductObj = tblPlantProduct(plantProductID=plantProductMatch,
					mineID=mineMatch, dateAdded=dateAdded)
				tblPlantProductObj.save()

			# Insert into tblProject
			projectTypeID = request.POST.get('projectType', '')
			projectTypeMatch = tblProjectTypeList.objects.get(projectTypeID=int(projectTypeID))
			tblProjectObj = tblProject(mineID=mineMatch, projectTypeID=projectTypeMatch,
				LOM=int(LOM), dateAdded=dateAdded)
			tblProjectObj.save()

			return render(request, 'settings/success.html', { }) #Redirect

		form_class = productsForm(mineID=mineID)
		return render(request, "settings/products.html", {'form': form_class})
	else:
		form_class = productsForm(mineID=mineID)
		return render(request, "settings/products.html", {'form': form_class})


# Function editMinePlan handles Mine Plan edits and updates by the user
def editMinePlan(request):
	mineID = request.session["mineID"]
	latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	numStockpiles = latestProject.numStockpiles
	LOM = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()

	# # Get list of Mine Product IDs
	# mineProductMatches = tblMineProduct.objects.filter(projectID=latestProject.projectID)
	# MPIDs = mineProductMatches.values_list('mineProductID', flat=True)

	# Get list of Commodity IDs
	commodities = tblCommodity.objects.filter(projectID=latestProject.projectID)
	idList = commodities.values_list('commodityID', flat=True)

	commNameList = []
	for ID in idList:
		commodityMatch = tblCommodityList.objects.get(commodityID=ID)
		commNameList.append(commodityMatch.name)

	form_class = mineProductionForm(LOM=LOM, numStockpiles=numStockpiles, idList=idList, commNameList=commNameList)
	if request.method == 'POST':
		form = mineProductionForm(request.POST, LOM=LOM, numStockpiles=numStockpiles, idList=idList, commNameList=commNameList)

		if form.is_valid():
			cleanData = form.cleaned_data
			dateAdded = timezone.localtime(timezone.now())

			for curr in range(1, numStockpiles+1):
				for year in range(1, LOM+1):
					tblMineProductTonnageObj = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, stockpileID=curr, year=year)
					tblMineProductTonnageObj.tonnage = float(cleanData["year{0}MinePlanStockpile{1}Tonnage".format(year, curr)])
					tblMineProductTonnageObj.dateAdded = dateAdded
					tblMineProductTonnageObj.save()

				for i in range(len(commNameList)):
					for year in range(1, LOM+1):
						tblMineProductGradeObj = tblMineProductGrade.objects.get(projectID=latestProject.projectID, stockpileID=curr,
							commodityID=idList[i], year=year)
						tblMineProductGradeObj.grade = float(cleanData["year{0}MinePlanSP{1}Grade{2}".format(year, curr, commNameList[i])])
						tblMineProductGradeObj.dateAdded = dateAdded
						tblMineProductGradeObj.save()

			return render(request, 'settings/success.html', { }) #Redirect

		return render(request, 'settings/mineProduction.html', {'form': form_class,
			'LOM': LOM, 'numStockpiles': list(range(1, numStockpiles+1)),
			'idList': idList, 'commNameList': commNameList})
	else:
		# minePlanHGTonnages = None
		# minePlanLGTonnages = None
		# minePlanWasteTonnages = None
		# minePlanOverburdenTonnages = None
		# minePlanHGGrades = {}
		# minePlanLGGrades = {}

		minePlanTonnages = {}
		minePlanGrades = {}

		for curr in range(1, numStockpiles+1):
			minePlanTonnages[curr] = {}
			for year in range(1, LOM+1):
				tblMineProductTonnageObj = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, stockpileID=curr, year=year)
				minePlanTonnages[curr][year] = tblMineProductTonnageObj.tonnage

			minePlanGrades[curr] = {}
			for i in range(len(commNameList)):
				tempGrades = {}
				for year in range(1, LOM+1):
					tblMineProductGradeObj = tblMineProductGrade.objects.get(projectID=latestProject.projectID, stockpileID=curr,
						commodityID=idList[i], year=year)
					tempGrades[year] = tblMineProductGradeObj.grade
				minePlanGrades[curr][commNameList[i]] = tempGrades

		# if 1 in MPIDs:
		# 	minePlanHGTonnages = []
		# 	for i in range(LOM):
		# 		i += 1
		# 		tblMineProductTonnageObj = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=1, year=i)
		# 		minePlanHGTonnages.append(tblMineProductTonnageObj.tonnage)

		# 		for i in range(len(commNameList)):
		# 			tempGrades = []
		# 			for year in range(LOM):
		# 				year += 1
		# 				tblMineProductGradeObj = tblMineProductGrade.objects.get(projectID=latestProject.projectID, mineProductID=1,
		# 					commodityID=idList[i], year=year)
		# 				tempGrades.append(tblMineProductGradeObj.grade)
		# 			minePlanHGGrades[commNameList[i]] = tempGrades

		# if 2 in MPIDs:
		# 	minePlanLGTonnages = []
		# 	for i in range(LOM):
		# 		i += 1
		# 		tblMineProductTonnageObj = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=2, year=i)
		# 		minePlanLGTonnages.append(tblMineProductTonnageObj.tonnage)

		# 		for i in range(len(commNameList)):
		# 			tempGrades = []
		# 			for year in range(LOM):
		# 				year += 1
		# 				tblMineProductGradeObj = tblMineProductGrade.objects.get(projectID=latestProject.projectID, mineProductID=2,
		# 					commodityID=idList[i], year=year)
		# 				tempGrades.append(tblMineProductGradeObj.grade)
		# 			minePlanLGGrades[commNameList[i]] = tempGrades

		# if 3 in MPIDs:
		# 	minePlanWasteTonnages = []
		# 	for i in range(LOM):
		# 		i += 1
		# 		tblMineProductTonnageObj = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=3, year=i)
		# 		minePlanWasteTonnages.append(tblMineProductTonnageObj.tonnage)

		# if 4 in MPIDs:
		# 	minePlanOverburdenTonnages = []
		# 	for i in range(LOM):
		# 		i += 1
		# 		tblMineProductTonnageObj = tblMineProductTonnage.objects.get(projectID=latestProject.projectID, mineProductID=4, year=i)
		# 		minePlanOverburdenTonnages.append(tblMineProductTonnageObj.tonnage)

		return render(request, 'settings/mineProduction.html', {'form': form_class,
			'LOM': list(range(1,LOM+1)), 'numStockpiles': list(range(1, numStockpiles+1)),
			'idList': idList, 'commNameList': commNameList,
			'minePlanTonnages': minePlanTonnages, 'minePlanGrades': minePlanGrades}) #Redirect


# Function editCAPEX handles CAPEX edits and updates by the user
def editCAPEX(request):
	mineID = request.session["mineID"]
	form_class = CAPEXForm(mineID=mineID)

	if request.method == 'POST':
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		LOM = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
		# LOM = projectMatch.LOM
		form = CAPEXForm(request.POST, mineID=mineID)
		if form.is_valid():
			cleanData = form.cleaned_data
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			dateAdded = timezone.localtime(timezone.now())

			for year in [-3,-2,-1]:
				preStrip = float(cleanData["year{0}PreStripping".format(year)])
				mineEquipInitial = float(cleanData["year{0}MiningEquipmentInitial".format(year)])
				mineEquipSustain = float(cleanData["year{0}MiningEquipmentSustaining".format(year)])
				infraDirectCost = float(cleanData["year{0}InfrastructureDirectCosts".format(year)])
				infraIndirectCost = float(cleanData["year{0}InfrastructureIndirectCosts".format(year)])
				contingency = float(cleanData["year{0}Contingency".format(year)])
				railcars = float(cleanData["year{0}Railcars".format(year)])
				otherMobEquip = float(cleanData["year{0}OtherMobileEquipment".format(year)])
				closureRehabAssure = float(cleanData["year{0}ClosureAndRehabAssurancePayment".format(year)])
				depoProvisionPay = float(cleanData["year{0}DepositsProvisionPayment".format(year)])
				workCapCurrentProd = float(cleanData["year{0}WorkingCapCurrentProd".format(year)])
				workCapCostsLG = float(cleanData["year{0}WorkingCapCostsOfLG".format(year)])
				EPCM = float(cleanData["year{0}EPCM".format(year)])
				ownerCost = float(cleanData["year{0}OwnersCosts".format(year)])

				latestCAPEX = tblCAPEX.objects.filter(mineID=int(mineID), year=year).order_by('-dateAdded')				
				if latestCAPEX:
					latestCAPEX = latestCAPEX[0]
					latestCAPEX.preStrip = preStrip
					latestCAPEX.mineEquipInitial = mineEquipInitial
					latestCAPEX.mineEquipSustain = mineEquipSustain
					latestCAPEX.infraDirectCost = infraDirectCost
					latestCAPEX.infraIndirectCost = infraIndirectCost
					latestCAPEX.contingency = contingency
					latestCAPEX.railcars = railcars
					latestCAPEX.otherMobEquip = otherMobEquip
					latestCAPEX.closureRehabAssure = closureRehabAssure
					latestCAPEX.depoProvisionPay = depoProvisionPay
					latestCAPEX.workCapCurrentProd = workCapCurrentProd
					latestCAPEX.workCapCostsLG = workCapCostsLG
					latestCAPEX.EPCM = EPCM
					latestCAPEX.ownerCost = ownerCost
					latestCAPEX.dateAdded = dateAdded
					latestCAPEX.save()
				else:
					mineMatch = tblMine.objects.get(mineID=int(mineID))
					tblCAPEXObj = tblCAPEX(mineID=mineMatch, year=year, preStrip=preStrip,
						mineEquipInitial=mineEquipInitial, mineEquipSustain=mineEquipSustain,
						infraDirectCost=infraDirectCost, infraIndirectCost=infraIndirectCost,
						contingency=contingency, railcars=railcars, otherMobEquip=otherMobEquip,
						closureRehabAssure=closureRehabAssure, depoProvisionPay=depoProvisionPay,
						workCapCurrentProd=workCapCurrentProd, workCapCostsLG=workCapCostsLG,
						EPCM=EPCM, ownerCost=ownerCost, dateAdded=dateAdded)
					tblCAPEXObj.save()

			for year in range(1, LOM+1):
				preStrip = float(cleanData["year{0}PreStripping".format(year)])
				mineEquipInitial = float(cleanData["year{0}MiningEquipmentInitial".format(year)])
				mineEquipSustain = float(cleanData["year{0}MiningEquipmentSustaining".format(year)])
				infraDirectCost = float(cleanData["year{0}InfrastructureDirectCosts".format(year)])
				infraIndirectCost = float(cleanData["year{0}InfrastructureIndirectCosts".format(year)])
				contingency = float(cleanData["year{0}Contingency".format(year)])
				railcars = float(cleanData["year{0}Railcars".format(year)])
				otherMobEquip = float(cleanData["year{0}OtherMobileEquipment".format(year)])
				closureRehabAssure = float(cleanData["year{0}ClosureAndRehabAssurancePayment".format(year)])
				depoProvisionPay = float(cleanData["year{0}DepositsProvisionPayment".format(year)])
				workCapCurrentProd = float(cleanData["year{0}WorkingCapCurrentProd".format(year)])
				workCapCostsLG = float(cleanData["year{0}WorkingCapCostsOfLG".format(year)])
				EPCM = float(cleanData["year{0}EPCM".format(year)])
				ownerCost = float(cleanData["year{0}OwnersCosts".format(year)])

				latestCAPEX = tblCAPEX.objects.filter(mineID=int(mineID), year=year).order_by('-dateAdded')[0]
				latestCAPEX.preStrip = preStrip
				latestCAPEX.mineEquipInitial = mineEquipInitial
				latestCAPEX.mineEquipSustain = mineEquipSustain
				latestCAPEX.infraDirectCost = infraDirectCost
				latestCAPEX.infraIndirectCost = infraIndirectCost
				latestCAPEX.contingency = contingency
				latestCAPEX.railcars = railcars
				latestCAPEX.otherMobEquip = otherMobEquip
				latestCAPEX.closureRehabAssure = closureRehabAssure
				latestCAPEX.depoProvisionPay = depoProvisionPay
				latestCAPEX.workCapCurrentProd = workCapCurrentProd
				latestCAPEX.workCapCostsLG = workCapCostsLG
				latestCAPEX.EPCM = EPCM
				latestCAPEX.ownerCost = ownerCost
				latestCAPEX.dateAdded = dateAdded
				latestCAPEX.save()

			# Toggle Processed tag in tblCashFlow
			# cashFlowEntry = tblCashFlow.objects.filter(projectID=latestProject.projectID).order_by('date')[0]
			# cashFlowEntry.processed = False
			# cashFlowEntry.save()
			cashFlowEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID)
			if cashFlowEntries:
				cashFlowEntry = tblCashFlow.objects.filter(projectID=latestProject.projectID).order_by('date')[0]
				cashFlowEntry.processed = False
				cashFlowEntry.save()

			return render(request, 'settings/success.html', { }) #Redirect

		return render(request, "settings/capex.html", {'form': form_class, 'LOM': LOM})
	else:
		# Get the latest project by this user/mine
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		LOM = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
		# LOM = latestProject.LOM

		latestCAPEX = tblCAPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		timestamp = latestCAPEX.dateAdded

		preStrip = []
		mineEquipInitial = []
		mineEquipSustain = []
		infraDirectCost = []
		infraIndirectCost = []
		contingency = []
		railcars = []
		otherMobEquip = []
		closureRehabAssure = []
		depoProvisionPay = []
		workCapCurrentProd = []
		workCapCostsLG = []
		EPCM = []
		ownerCost = []

		preStripNeg = {}
		mineEquipInitialNeg = {}
		mineEquipSustainNeg = {}
		infraDirectCostNeg = {}
		infraIndirectCostNeg = {}
		contingencyNeg = {}
		railcarsNeg = {}
		otherMobEquipNeg = {}
		closureRehabAssureNeg = {}
		depoProvisionPayNeg = {}
		workCapCurrentProdNeg = {}
		workCapCostsLGNeg = {}
		EPCMNeg = {}
		ownerCostNeg = {}

		CAPEXEntries = tblCAPEX.objects.filter(mineID=int(mineID), dateAdded=timestamp).order_by('year')
		for i in [-3,-2,-1]:
			row = CAPEXEntries.filter(year=i)
			if row:
				row = row[0]
				preStripNeg[i] = row.preStrip
				mineEquipInitialNeg[i] = row.mineEquipInitial
				mineEquipSustainNeg[i] = row.mineEquipSustain
				infraDirectCostNeg[i] = row.infraDirectCost
				infraIndirectCostNeg[i] = row.infraIndirectCost
				contingencyNeg[i] = row.contingency
				railcarsNeg[i] = row.railcars
				otherMobEquipNeg[i] = row.otherMobEquip
				closureRehabAssureNeg[i] = row.closureRehabAssure
				depoProvisionPayNeg[i] = row.depoProvisionPay
				workCapCurrentProdNeg[i] = row.workCapCurrentProd
				workCapCostsLGNeg[i] = row.workCapCostsLG
				EPCMNeg[i] = row.EPCM
				ownerCostNeg[i] = row.ownerCost
			else:
				preStripNeg[i] = Decimal(0.0)
				mineEquipInitialNeg[i] = Decimal(0.0)
				mineEquipSustainNeg[i] = Decimal(0.0)
				infraDirectCostNeg[i] = Decimal(0.0)
				infraIndirectCostNeg[i] = Decimal(0.0)
				contingencyNeg[i] = Decimal(0.0)
				railcarsNeg[i] = Decimal(0.0)
				otherMobEquipNeg[i] = Decimal(0.0)
				closureRehabAssureNeg[i] = Decimal(0.0)
				depoProvisionPayNeg[i] = Decimal(0.0)
				workCapCurrentProdNeg[i] = Decimal(0.0)
				workCapCostsLGNeg[i] = Decimal(0.0)
				EPCMNeg[i] = Decimal(0.0)
				ownerCostNeg[i] = Decimal(0.0)

		# for i in range(3):
		# 	row = results[i]
		# 	preStripNeg[i-3] = row.preStrip/Decimal(1000000.0)
		# 	mineEquipInitialNeg[i-3] = row.mineEquipInitial/Decimal(1000000.0)
		# 	mineEquipSustainNeg[i-3] = row.mineEquipSustain/Decimal(1000000.0)
		# 	infraDirectCostNeg[i-3] = row.infraDirectCost/Decimal(1000000.0)
		# 	infraIndirectCostNeg[i-3] = row.infraIndirectCost/Decimal(1000000.0)
		# 	contingencyNeg[i-3] = row.contingency/Decimal(1000000.0)
		# 	railcarsNeg[i-3] = row.railcars/Decimal(1000000.0)
		# 	otherMobEquipNeg[i-3] = row.otherMobEquip/Decimal(1000000.0)
		# 	closureRehabAssureNeg[i-3] = row.closureRehabAssure/Decimal(1000000.0)
		# 	depoProvisionPayNeg[i-3] = row.depoProvisionPay/Decimal(1000000.0)
		# 	workCapCurrentProdNeg[i-3] = row.workCapCurrentProd/Decimal(1000000.0)
		# 	workCapCostsLGNeg[i-3] = row.workCapCostsLG/Decimal(1000000.0)
		# 	EPCMNeg[i-3] = row.EPCM/Decimal(1000000.0)
		# 	ownerCostNeg[i-3] = row.ownerCost/Decimal(1000000.0)

		for i in range(LOM):
			# i += 1
			# result = tblCAPEX.objects.filter(mineID=int(mineID), year=i, dateAdded=timestamp)
			subEntry = CAPEXEntries.filter(year=i+1)		
			row = subEntry[0]
			preStrip.append(row.preStrip)
			mineEquipInitial.append(row.mineEquipInitial)
			mineEquipSustain.append(row.mineEquipSustain)
			infraDirectCost.append(row.infraDirectCost)
			infraIndirectCost.append(row.infraIndirectCost)
			contingency.append(row.contingency)
			railcars.append(row.railcars)
			otherMobEquip.append(row.otherMobEquip)
			closureRehabAssure.append(row.closureRehabAssure)
			depoProvisionPay.append(row.depoProvisionPay)
			workCapCurrentProd.append(row.workCapCurrentProd)
			workCapCostsLG.append(row.workCapCostsLG)
			EPCM.append(row.EPCM)
			ownerCost.append(row.ownerCost)

			# if result:
			# 	row = result[0]
			# 	# initialValues["year{0}PreStripping".format(i)] = row.preStrip
			# 	# initialValues["year{0}PreStripping".format(i)] = Float(0.33)
			# 	preStrip.append(row.preStrip/Decimal(1000000.0))
			# 	mineEquipInitial.append(row.mineEquipInitial/Decimal(1000000.0))
			# 	mineEquipSustain.append(row.mineEquipSustain/Decimal(1000000.0))
			# 	infraDirectCost.append(row.infraDirectCost/Decimal(1000000.0))
			# 	infraIndirectCost.append(row.infraIndirectCost/Decimal(1000000.0))
			# 	contingency.append(row.contingency/Decimal(1000000.0))
			# 	railcars.append(row.railcars/Decimal(1000000.0))
			# 	otherMobEquip.append(row.otherMobEquip/Decimal(1000000.0))
			# 	closureRehabAssure.append(row.closureRehabAssure/Decimal(1000000.0))
			# 	depoProvisionPay.append(row.depoProvisionPay/Decimal(1000000.0))
			# 	workCapCurrentProd.append(row.workCapCurrentProd/Decimal(1000000.0))
			# 	workCapCostsLG.append(row.workCapCostsLG/Decimal(1000000.0))
			# 	EPCM.append(row.EPCM/Decimal(1000000.0))
			# 	ownerCost.append(row.ownerCost/Decimal(1000000.0))

		return render(request, "settings/capex.html", {'form': form_class, 'LOM': LOM,
			'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial,
			'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
			'infraIndirectCost': infraIndirectCost, 'contingency': contingency,
			'railcars': railcars, 'otherMobEquip': otherMobEquip,
			'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay,
			'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
			'EPCM': EPCM, 'ownerCost': ownerCost,
			'preStripNeg': preStripNeg, 'mineEquipInitialNeg': mineEquipInitialNeg,
			'mineEquipSustainNeg': mineEquipSustainNeg, 'infraDirectCostNeg': infraDirectCostNeg,
			'infraIndirectCostNeg': infraIndirectCostNeg, 'contingencyNeg': contingencyNeg,
			'railcarsNeg': railcarsNeg, 'otherMobEquipNeg': otherMobEquipNeg,
			'closureRehabAssureNeg': closureRehabAssureNeg, 'depoProvisionPayNeg': depoProvisionPayNeg,
			'workCapCurrentProdNeg': workCapCurrentProdNeg, 'workCapCostsLGNeg': workCapCostsLGNeg,
			'EPCMNeg': EPCMNeg, 'ownerCostNeg': ownerCostNeg })



# Function editOPEX handles OPEX edits and updates by the user
def editOPEX(request):
	mineID = request.session["mineID"]
	form_class = OPEXForm(mineID=mineID)

	if request.method == 'POST':
		# projectMatch = tblProject.objects.filter(mineID=int(mineID)).order_by('-projectID')[0]
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		LOM = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
		# LOM = projectMatch.LOM
		form = OPEXForm(request.POST, mineID=mineID)
		if form.is_valid():
			cleanData = form.cleaned_data
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			dateAdded = timezone.localtime(timezone.now())

			for year in range(1, LOM+1):
				mining = float(cleanData["year{0}Mining".format(year)])
				infrastructure = float(cleanData["year{0}Infrastructure".format(year)])
				stockpileLG = float(cleanData["year{0}StockpileLG".format(year)])
				dewatering = float(cleanData["year{0}Dewatering".format(year)])
				processing = float(cleanData["year{0}Processing".format(year)])
				hauling = float(cleanData["year{0}ProductHauling".format(year)])
				loadOutRailLoop = float(cleanData["year{0}LoadoutRailLoop".format(year)])
				GASite = float(cleanData["year{0}GASite".format(year)])
				GARoomBoardFIFO = float(cleanData["year{0}GARoomBoardFIFO".format(year)])
				railTransport = float(cleanData["year{0}RailTransportation".format(year)])
				GACorp = float(cleanData["year{0}GACorporate".format(year)])
				royalties = float(cleanData["year{0}Royalties".format(year)])
				transportation = float(cleanData["year{0}Transportation".format(year)])
				GA = float(cleanData["year{0}GA".format(year)])
				shipping = float(cleanData["year{0}ShippingCost".format(year)])
				opexPT = float(cleanData["year{0}OpexPT".format(year)])

				latestOPEX = tblOPEX.objects.filter(mineID=int(mineID), year=year).order_by('-dateAdded')[0]
				latestOPEX.mining = mining
				latestOPEX.infrastructure = infrastructure
				latestOPEX.stockpileLG = stockpileLG
				latestOPEX.dewatering = dewatering
				latestOPEX.processing = processing
				latestOPEX.hauling = hauling
				latestOPEX.loadOutRailLoop = loadOutRailLoop
				latestOPEX.GASite = GASite
				latestOPEX.GARoomBoardFIFO = GARoomBoardFIFO
				latestOPEX.railTransport = railTransport
				latestOPEX.GACorp = GACorp
				latestOPEX.royalties = royalties
				latestOPEX.transportation = transportation
				latestOPEX.GA = GA
				latestOPEX.shipping = shipping
				latestOPEX.opexPT = opexPT
				latestOPEX.dateAdded = dateAdded

				latestOPEX.save()

			# Toggle Processed tag in tblCashFlow
			cashFlowEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID)
			if cashFlowEntries:
				cashFlowEntry = tblCashFlow.objects.filter(projectID=latestProject.projectID).order_by('date')[0]
				cashFlowEntry.processed = False
				cashFlowEntry.save()

			# cashFlowEntry = tblCashFlow.objects.filter(projectID=latestProject.projectID).order_by('date')[0]
			# cashFlowEntry.processed = False
			# cashFlowEntry.save()

			return render(request, 'settings/success.html', { }) #Redirect

		return render(request, "settings/opex.html", {'form': form_class, 'LOM': LOM})
	else:
		# Get the latest project by this user/mine
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		LOM = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
		# LOM = latestProject.LOM

		latestOPEX = tblOPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		timestamp = latestOPEX.dateAdded

		mining = []
		infrastructure = []
		stockpileLG = []
		dewatering = []
		processing = []
		hauling = []
		loadOutRailLoop = []
		GASite = []
		GARoomBoardFIFO = []
		railTransport = []
		GACorp = []
		royalties = []
		transportation = []
		GA = []
		shipping = []
		opexPT = []

		for i in range(LOM):
			i += 1
			result = tblOPEX.objects.filter(mineID=int(mineID), year=i, dateAdded=timestamp)
			if result:
				row = result[0]
				# initialValues["year{0}PreStripping".format(i)] = row.preStrip
				# initialValues["year{0}PreStripping".format(i)] = Float(0.33)
				mining.append(row.mining)
				infrastructure.append(row.infrastructure)
				stockpileLG.append(row.stockpileLG)
				dewatering.append(row.dewatering)
				processing.append(row.processing)
				hauling.append(row.hauling)
				loadOutRailLoop.append(row.loadOutRailLoop)
				GASite.append(row.GASite)
				GARoomBoardFIFO.append(row.GARoomBoardFIFO)
				railTransport.append(row.railTransport)
				GACorp.append(row.GACorp)
				royalties.append(row.royalties)
				transportation.append(row.transportation)
				GA.append(row.GA)
				shipping.append(row.shipping)
				opexPT.append(row.opexPT)

		return render(request, "settings/opex.html", {'form': form_class, 'LOM': LOM,
			'mining': mining, 'infrastructure': infrastructure,
			'stockpileLG': stockpileLG, 'dewatering': dewatering,
			'processing': processing, 'hauling': hauling,
			'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite,
			'GARoomBoardFIFO': GARoomBoardFIFO, 'railTransport': railTransport,
			'GACorp': GACorp, 'royalties': royalties,
			'transportation': transportation, 'GA': GA,
			'shipping': shipping, 'opexPT': opexPT})

# Function index6 handles Smelter Term declarations
def editSmelter(request):
	# form_class = smelterForm
	# mineID = request.session["mineID"]
	# latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	# timestamp = latestCommodity.dateAdded
	# commodityMatches = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=timestamp)

	# idList = []
	# commNameList = []
	# tempIDs = commodityMatches.values_list('commodityID', flat=True)
	# for match in tempIDs:
	# 	idList.append(match)
	# 	nameMatch = tblCommodityList.objects.get(commodityID=match)
	# 	commNameList.append(nameMatch.name)

	mineID = request.session["mineID"]
	latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	numStockpiles = latestProject.numStockpiles
	LOM = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()

	# Get list of Commodity IDs
	commodities = tblCommodity.objects.filter(projectID=latestProject.projectID)
	idList = commodities.values_list('commodityID', flat=True)

	commNameList = []
	for ID in idList:
		commodityMatch = tblCommodityList.objects.get(commodityID=ID)
		commNameList.append(commodityMatch.name)

	if request.method == 'POST':
		# mineID = request.session["mineID"]
		# latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# timestamp = latestCommodity.dateAdded
		# commodityMatches = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=timestamp)

		# idList = []
		# commNameList = []
		# tempIDs = commodityMatches.values_list('commodityID', flat=True)
		# for match in tempIDs:
		# 	idList.append(match)
		# 	nameMatch = tblCommodityList.objects.get(commodityID=match)
		# 	commNameList.append(nameMatch.name)

		form = smelterForm(request.POST, idList=idList, nameList=commNameList, numStockpiles=numStockpiles)
		if form.is_valid():
			cleanData = form.cleaned_data
			dateAdded = timezone.localtime(timezone.now())

			for curr in range(1, numStockpiles+1):
				for i in range(len(idList)):
					currSmelter = tblSmelterTerms.objects.get(projectID=latestProject.projectID, stockpileID=curr, commodityID=idList[i])
					currSmelter.minGrade = float(cleanData["Stockpile{0}MinGrade{1}".format(curr,idList[i])])
					currSmelter.maxGrade = float(cleanData["Stockpile{0}MaxGrade{1}".format(curr,idList[i])])
					currSmelter.minPenalty = float(cleanData["Stockpile{0}MinPenalty{1}".format(curr,idList[i])])
					currSmelter.maxPenalty = float(cleanData["Stockpile{0}MaxPenalty{1}".format(curr,idList[i])])
					currSmelter.minMaxPenalty = float(cleanData["Stockpile{0}MinMaxPenalty{1}".format(curr,idList[i])])
					currSmelter.premium = float(cleanData["Stockpile{0}Premium{1}".format(curr,idList[i])])
					currSmelter.increments = float(cleanData["Stockpile{0}Increments{1}".format(curr,idList[i])])
					currSmelter.dateAdded = dateAdded
					currSmelter.save()

		# form = smelterForm(request.POST, idList=idList, nameList=commNameList)
		# if form.is_valid():
		# 	mineMatch = tblMine.objects.get(mineID=int(mineID))
		# 	dateAdded = timezone.localtime(timezone.now())

		# 	for i in range(len(idList)):
		# 		commodityID = tblCommodityList.objects.get(commodityID=tempIDs[i])
		# 		LGMinGrade = request.POST.get("LGMinGrade{0}".format(idList[i]), '')
		# 		LGMaxGrade = request.POST.get("LGMaxGrade{0}".format(idList[i]), '')
		# 		LGMinPenalty = request.POST.get("LGMinPenalty{0}".format(idList[i]), '')
		# 		LGMaxPenalty = request.POST.get("LGMaxPenalty{0}".format(idList[i]), '')
		# 		LGMinMaxPenalty = request.POST.get("LGMinMaxPenalty{0}".format(idList[i]), '')
		# 		LGPremium = request.POST.get("LGPremium{0}".format(idList[i]), '')
		# 		HGMinGrade = request.POST.get("HGMinGrade{0}".format(idList[i]), '')
		# 		HGMaxGrade = request.POST.get("HGMaxGrade{0}".format(idList[i]), '')
		# 		HGMinPenalty = request.POST.get("HGMinPenalty{0}".format(idList[i]), '')
		# 		HGMaxPenalty = request.POST.get("HGMaxPenalty{0}".format(idList[i]), '')
		# 		HGMinMaxPenalty = request.POST.get("HGMinMaxPenalty{0}".format(idList[i]), '')
		# 		HGPremium = request.POST.get("HGPremium{0}".format(idList[i]), '')
		# 		increments = request.POST.get("increments{0}".format(idList[i]), '')
		# 		# LGPFMinGrade = request.POST.get("LGPlantMinGrade{0}".format(idList[i]), '')
		# 		# LGPFMinPenalty = request.POST.get("LGPlantMinPenalty{0}".format(idList[i]), '')
		# 		# HGPFMinGrade = request.POST.get("HGPlantMinGrade{0}".format(idList[i]), '')
		# 		# HGPFMinPenalty = request.POST.get("HGPlantMinPenalty{0}".format(idList[i]), '')

		# 		tblSmelterTermsObj = tblSmelterTerms(mineID=mineMatch, commodityID=commodityID,
		# 			LGMinGrade=LGMinGrade, LGMaxGrade=LGMaxGrade, LGMinPenalty=LGMinPenalty,
		# 			LGMaxPenalty=LGMaxPenalty, LGMinMaxPenalty=LGMinMaxPenalty,
		# 			LGPremium=LGPremium, HGMinGrade=HGMinGrade, HGMaxGrade=HGMaxGrade,
		# 			HGMinPenalty=HGMinPenalty, HGMaxPenalty=HGMaxPenalty, HGMinMaxPenalty=HGMinMaxPenalty,
		# 			HGPremium=HGPremium, increments=increments, LGPFMinGrade=LGPFMinGrade,
		# 			LGPFMinPenalty=LGPFMinPenalty, HGPFMinGrade=HGPFMinGrade, HGPFMinPenalty=HGPFMinPenalty,
		# 			dateAdded=dateAdded)
		# 		tblSmelterTermsObj.save()

			# Load up the Financials form
			# next_form = financialsForm
			# return render(request, 'settings/prices.html', {'form': next_form,
				# 'smelterRegistered': True})
			return render (request, 'settings/success.html', {})

		return render(request, 'settings/smelter.html', {'form': form_class, 'idList': idList, 'nameList': commNameList })		
	else:
		minGrades = {}
		maxGrades = {}
		minPenalties = {}
		maxPenalties = {}
		minMaxPenalties = {}
		premiums = {}
		increments = {}

		for curr in range(1, numStockpiles+1):
			minGrades[curr] = {}
			maxGrades[curr] = {}
			minPenalties[curr] = {}
			maxPenalties[curr] = {}
			minMaxPenalties[curr] = {}
			premiums[curr] = {}
			increments[curr] = {}
  
			for i in range(len(idList)):
				currSmelter = tblSmelterTerms.objects.get(projectID=latestProject.projectID, stockpileID=curr, commodityID=idList[i])
				minGrades[curr][idList[i]] = currSmelter.minGrade
				maxGrades[curr][idList[i]] = currSmelter.maxGrade
				minPenalties[curr][idList[i]] = currSmelter.minPenalty
				maxPenalties[curr][idList[i]] = currSmelter.maxPenalty
				minMaxPenalties[curr][idList[i]] = currSmelter.minMaxPenalty
				premiums[curr][idList[i]] = currSmelter.premium
				increments[curr][idList[i]] = currSmelter.increments

		form = smelterForm(idList=idList, nameList=commNameList, numStockpiles=numStockpiles)
		
		return render (request, "settings/smelter.html", {'form': form, 'idList': idList, 'nameList': commNameList,
			'numStockpiles': list(range(1, numStockpiles+1)),
			'minGrades': minGrades, 'maxGrades': maxGrades, 'minPenalties': minPenalties, 'maxPenalties': maxPenalties,
			'minMaxPenalties': minMaxPenalties, 'premiums': premiums, 'increments': increments})

def editPrices(request):
	mineID = request.session["mineID"]
	latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	numStockpiles = latestProject.numStockpiles

	# Get list of Plant Product IDs
	PPMatches = tblPlantProduct.objects.filter(projectID=latestProject.projectID)
	PPIDs = PPMatches.values_list('plantProductID', flat=True)

	# priceFields = (
	# 	'HGLump',
	# 	'HGLumpPrem',
	# 	'HGFines',
	# 	'HGUltraFines',
	# 	'LGLump',
	# 	'LGLumpPrem',
	# 	'LGFines',
	# 	'LGUltraFines',
	# 	'HGLumpAvg',
	# 	'LGLumpAvg'
	# 	)

	if request.method == 'POST':
		form = financialsForm(request.POST, numStockpiles=numStockpiles, plantProducts=PPIDs)
		if form.is_valid():
			cleanData = form.cleaned_data
			dateAdded = timezone.localtime(timezone.now())

			for curr in range(1, numStockpiles+1):
				currPrice = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=curr)
				if 1 in PPIDs:
					currPrice.lump = float(cleanData["Stockpile{0}Lump".format(curr)])
					currPrice.lumpPrem = float(cleanData["Stockpile{0}LumpPrem".format(curr)])
					currPrice.lumpAvg = float(cleanData["Stockpile{0}LumpAvg".format(curr)])
				if 2 in PPIDs:
					currPrice.fines = float(cleanData["Stockpile{0}Fines".format(curr)])
				if 3 in PPIDs:
					currPrice.ultraFines = float(cleanData["Stockpile{0}UltraFines".format(curr)])
				currPrice.dateAdded = dateAdded
				currPrice.save()

			# mineMatch = tblMine.objects.get(mineID=int(mineID))
			# tblPriceObj = tblPrice(mineID=mineMatch,
			# 	dateAdded=dateAdded,
			# 	**{ f:request.POST.get(f, '') for f in priceFields })
			# tblPriceObj.save()

			return render(request, 'settings/success.html', { }) #Redirect
	else:
		lumps = {}
		lumpPrems = {}
		fines = {}
		ultraFines = {}
		lumpAvgs = {}

		for curr in range(1, numStockpiles+1):
			currPrice = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=curr)
			if 1 in PPIDs:
				lumps[curr] = currPrice.lump
				lumpPrems[curr] = currPrice.lumpPrem
				lumpAvgs[curr] = currPrice.lumpAvg
			if 2 in PPIDs:
				fines[curr] = currPrice.fines
			if 3 in PPIDs:
				ultraFines[curr] = currPrice.ultraFines

		form = financialsForm(numStockpiles=numStockpiles, plantProducts=PPIDs)
		return render(request, 'settings/prices.html', {'form': form, 'lumps':lumps, 'lumpPrems':lumpPrems,
		'fines': fines, 'ultraFines': ultraFines, 'lumpAvgs': lumpAvgs, 
		'PPIDs': PPIDs, 'numStockpiles': list(range(1, numStockpiles+1)) })

		# priceMatch = tblPrice.objects.filter(mineID=int(mineID)).order_by('-dateAdded').values().first()
		# form = priceForm({ f:priceMatch[f] for f in priceFields })
		# return render(request, "settings/prices.html", {'form': form})


def editInputs(request):
	mineID = request.session["mineID"]
	# inputFields = (
	# 	'Fe2O3Iron',
	# 	'totalGrade',
	# 	'avgCommodity1Grade',
	# 	'lumpRecovery',
	# 	'finesRecovery',
	# 	'ultraFinesRecovery',
	# 	'lumpGrade',
	# 	'finesGrade',
	# 	'ultraFinesGrade',
	# 	'rejectsGrade',
	# 	'feedMoisture',
	# 	'lumpMoisture',
	# 	'finesMoisture',
	# 	'ultraFinesMoisture',
	# 	'rejectsMoisture',
	# 	'mineOpsDays',
	# 	'plantOpsDays',
	# 	'mineCapacity',
	# 	'plantCapacity',
	# 	'discountRate1',
	# 	'discountRate2',
	# 	'discountRate3',
	# 	'discountRate4',
	# 	'discountRate5',
	# 	'discountRate6',
	# 	'exchangeRate'
	# 	)

	# Obtain latest projectID
	latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	inputsMatch = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	
	# Get list of Plant Product IDs
	PPMatches = tblPlantProduct.objects.filter(projectID=latestProject.projectID)
	PPIDs = PPMatches.values_list('plantProductID', flat=True)

	if request.method == 'POST':
		form = inputsForm(request.POST, inputs=inputsMatch, plantProducts=PPIDs)
		if form.is_valid():
			dateAdded = timezone.localtime(timezone.now())
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			
			# if 3 in PPIDs:
			# 	ultraFinesRecovery = request.POST.get('ultraFinesRecovery', '')
			# 	ultraFinesGrade = request.POST.get('ultraFinesGrade', '')
			# 	ultraFinesMoisture = request.POST.get('ultraFinesMoisture', '')
			# else:
			# 	ultraFinesRecovery = None
			# 	ultraFinesGrade = None
			# 	ultraFinesMoisture = None

			# if 4 in PPIDs:
			# 	#rejectsRecovery = request.POST.get('rejectsRecovery', '')
			# 	rejectsGrade = request.POST.get('rejectsGrade', '')
			# 	rejectsMoisture = request.POST.get('rejectsMoisture', '')
			# else:
			# 	#rejectsRecovery = None
			# 	rejectsGrade = None
			# 	rejectsMoisture = None
				
			# tblInputsObj = tblInputs(mineID=mineMatch,
			# 	dateAdded=dateAdded,
			# 	**{ f:request.POST.get(f, '') for f in inputFields })
			# tblInputsObj.save()

			# return render(request, 'settings/success.html', { }) #Redirect

			# Insert into tblInputs
			Fe2O3Iron = request.POST.get('Fe2O3Iron', '')
			totalGrade = request.POST.get('totalGrade', '')
			avgCommodity1Grade = request.POST.get('avgCommodity1Grade', '')
			# lumpRecovery = request.POST.get('lumpRecovery', '')
			# finesRecovery = request.POST.get('finesRecovery', '')
			# lumpGrade = request.POST.get('lumpGrade', '')
			# finesGrade = request.POST.get('finesGrade', '')
			feedMoisture = request.POST.get('feedMoisture', '')
			# lumpMoisture = request.POST.get('lumpMoisture', '')
			# finesMoisture = request.POST.get('finesMoisture', '')
			# ultraFinesMoisture = request.POST.get('ultraFinesMoisture', '')
			# rejectsMoisture = request.POST.get('rejectsMoisture', '')
			mineOpsDays = request.POST.get('mineOpsDays', '')
			plantOpsDays = request.POST.get('plantOpsDays', '')
			mineCapacity = request.POST.get('mineCapacity', '')
			plantCapacity = request.POST.get('plantCapacity', '')
			discountRate1 = request.POST.get('discountRate1', '')
			discountRate2 = request.POST.get('discountRate2', '')
			discountRate3 = request.POST.get('discountRate3', '')
			discountRate4 = request.POST.get('discountRate4', '')
			discountRate5 = request.POST.get('discountRate5', '')
			discountRate6 = request.POST.get('discountRate6', '')
			exchangeRate = request.POST.get('exchangeRate', '')

			if 1 in PPIDs:
				lumpRecovery = request.POST.get('lumpRecovery', '')
				lumpGrade = request.POST.get('lumpGrade', '')
				lumpMoisture = request.POST.get('lumpMoisture', '')
			else:
				lumpRecovery = None
				lumpGrade = None
				lumpMoisture = None

			if 2 in PPIDs:
				finesRecovery = request.POST.get('finesRecovery', '')
				finesGrade = request.POST.get('finesGrade', '')
				finesMoisture = request.POST.get('finesMoisture', '')
			else:
				finesRecovery = None
				finesGrade = None
				finesMoisture = None

			if 3 in PPIDs:
				ultraFinesRecovery = request.POST.get('ultraFinesRecovery', '')
				ultraFinesGrade = request.POST.get('ultraFinesGrade', '')
				ultraFinesMoisture = request.POST.get('ultraFinesMoisture', '')
			else:
				ultraFinesRecovery = None
				ultraFinesGrade = None
				ultraFinesMoisture = None

			if 4 in PPIDs:
				rejectsRecovery = request.POST.get('rejectsRecovery', '')
				rejectsGrade = request.POST.get('rejectsGrade', '')
				rejectsMoisture = request.POST.get('rejectsMoisture', '')
			else:
				rejectsRecovery = None
				rejectsGrade = None
				rejectsMoisture = None

			inputsMatch.Fe2O3Iron = Fe2O3Iron
			inputsMatch.totalGrade = totalGrade
			inputsMatch.avgCommodity1Grade = avgCommodity1Grade
			inputsMatch.lumpRecovery = lumpRecovery
			inputsMatch.finesRecovery = finesRecovery
			inputsMatch.lumpGrade = lumpGrade
			inputsMatch.finesGrade = finesGrade
			inputsMatch.feedMoisture = feedMoisture
			inputsMatch.lumpMoisture = lumpMoisture
			inputsMatch.finesMoisture = finesMoisture
			inputsMatch.ultraFinesMoisture = ultraFinesMoisture
			inputsMatch.rejectsMoisture = rejectsMoisture
			inputsMatch.mineOpsDays = mineOpsDays
			inputsMatch.plantOpsDays = plantOpsDays
			inputsMatch.mineCapacity = mineCapacity
			inputsMatch.plantCapacity = plantCapacity
			inputsMatch.discountRate1 = discountRate1
			inputsMatch.discountRate2 = discountRate2
			inputsMatch.discountRate3 = discountRate3
			inputsMatch.discountRate4 = discountRate4
			inputsMatch.discountRate5 = discountRate5
			inputsMatch.discountRate6 = discountRate6
			inputsMatch.exchangeRate = exchangeRate
			inputsMatch.dateAdded = dateAdded
			inputsMatch.ultraFinesRecovery = ultraFinesRecovery
			inputsMatch.ultraFinesGrade = ultraFinesGrade
			inputsMatch.rejectsRecovery = rejectsRecovery
			inputsMatch.rejectsGrade = rejectsGrade

			inputsMatch.save()
			return render(request, 'settings/success.html', { }) #Redirect

			# tblInputsObj = tblInputs(mineID=mineMatch, Fe2O3Iron=Fe2O3Iron, 
			# 	totalGrade=totalGrade, avgCommodity1Grade=avgCommodity1Grade,
			# 	lumpRecovery=lumpRecovery, finesRecovery=finesRecovery,
			# 	lumpGrade=lumpGrade, finesGrade=finesGrade,
			# 	feedMoisture=feedMoisture, lumpMoisture=lumpMoisture,
			# 	finesMoisture=finesMoisture, ultraFinesMoisture=ultraFinesMoisture,
			# 	rejectsMoisture=rejectsMoisture, mineOpsDays=mineOpsDays,
			# 	plantOpsDays=plantOpsDays, mineCapacity=mineCapacity,
			# 	plantCapacity=plantCapacity, discountRate1=Decimal(discountRate1),
			# 	discountRate2=Decimal(discountRate2), discountRate3=Decimal(discountRate3),
			# 	discountRate4=Decimal(discountRate4), discountRate5=Decimal(discountRate5),
			# 	discountRate6=Decimal(discountRate6), exchangeRate=exchangeRate, dateAdded=dateAdded,
			# 	ultraFinesRecovery=ultraFinesRecovery, ultraFinesGrade=ultraFinesGrade,
			# 	rejectsRecovery=rejectsRecovery, rejectsGrade=rejectsGrade)
			# tblInputsObj.save()

	else:
		# inputsMatch = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded').values().first()
		# form = inputsForm({ f:inputsMatch[f] for f in inputFields })

		form = inputsForm(inputs=inputsMatch, plantProducts=PPIDs)
		return render(request, "settings/inputs.html", {'form': form})


def editTaxes(request):
	mineID = request.session["mineID"]

	