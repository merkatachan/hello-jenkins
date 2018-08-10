from django.shortcuts import render
from django.utils import timezone
from decimal import *
from django.shortcuts import render_to_response
import datetime
from dateutil.relativedelta import relativedelta

from .forms import *
from .models import *

# Function index handles declaring of main commodities.
def index(request):
	# return render(request, 'login/login.html')
	form_class = commodityForm
	if request.method == 'POST':

		form = commodityForm(request.POST)
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
				return render(request, 'setup/commodity.html', {'form': form_class,
					'errorMsg': errorMsg})
			elif len(delCommodities) > 4:
				errorMsg = "You cannot select more than four deleterious commodities. Try again."
				return render(request, 'setup/commodity.html', {'form': form_class,
					'errorMsg': errorMsg})

			# mineID = request.session["mineID"]
			# mineMatch = tblMine.objects.get(mineID=int(mineID))
			# dateAdded = timezone.localtime(timezone.now())

			request.session["mainCommodities"] = mainCommodities
			request.session["delCommodities"] = delCommodities

			next_form_class = productsForm()
			return render(request, 'setup/products.html', {'form': next_form_class,
				'delCommodityRegistered': True}) #Redirect

		return render_to_response("setup/commodity.html", {'form': form_class})

	else:
		return render(request, "setup/commodity.html", {'form': form_class})



# Function index2 handles declaring of deleterious commodities.
def index2(request):
	# return render(request, 'login/login.html')
	form_class = commodityDelForm
	if request.method == 'POST':

		form = commodityDelForm(request.POST)
		subCommodities1 = request.POST.getlist('commodity1')
		subCommodities2 = request.POST.getlist('commodity2')
		subCommodities3 = request.POST.getlist('commodity3')
		delCommodities = subCommodities1 + subCommodities2 + subCommodities3
		if len(delCommodities) == 0:
			errorMsg = "You must select at least one main commodity. Try again."
			return render(request, 'setup/delCommodity.html', {'form': form_class,
				'mainCommodityRegistered': True, 'errorMsg': errorMsg})
		elif len(delCommodities) > 4:
			errorMsg = "You cannot select more than four main commodities. Try again."
			return render(request, 'setup/delCommodity.html', {'form': form_class,
				'mainCommodityRegistered': True, 'errorMsg': errorMsg})

		if form.is_valid():
			# delCommodities = request.POST.getlist('commodity')
			mineID = request.session["mineID"]
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			# projectMatch = tblProject.objects.filter(mineID=int(mineID)).order_by('-projectID')[0]
			commodityMatch = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
			dateAdded = commodityMatch.dateAdded

			for commodity in delCommodities:
				commodityMatch = tblCommodityList.objects.get(commodityID=int(commodity))
				tblCommodityObj = tblCommodity(commodityID=commodityMatch,
					mineID=mineMatch, dateAdded=dateAdded)
				tblCommodityObj.save()

			next_form_class = productsForm
			return render(request, 'setup/products.html', {'form': next_form_class,
				'delCommodityRegistered': True}) #Redirect

		form_class = commodityMainForm
		return render_to_response("setup/delCommodity.html", {'form': form_class})

	else:
		form_class = commodityMainForm
		return render(request, "setup/delCommodity.html", {'form': form_class})


# Function index3 handles project type and product declarations.
def index3(request):
	# return render(request, 'login/login.html')
	form_class = productsForm()
	if request.method == 'POST':

		form = productsForm(request.POST)
		# mineProducts = request.POST.getlist('mineProduct')
		plantProducts = request.POST.getlist('plantProduct')
		# if len(mineProducts) == 0 or len(plantProducts) == 0:
		if len(plantProducts) == 0:
			# errorMsg = "You must declare at least one mine product and one plant product. Try Again."
			errorMsg = "You must declare at least one plant product. Try Again."
			return render(request, 'setup/products.html', {'form': form_class,
				'delCommodityRegistered': True, 'errorMsg': errorMsg})

		LOM = str(request.POST.get('LOM', ''))
		if LOM is None:
			errorMsg = "You must declare an LOM. Try again."
			return render(request, 'setup/products.html', {'form': form_class,
				'delCommodityRegistered': True, 'errorMsg': errorMsg})

		startDate = request.POST.get('startDate', '')
		if startDate is None:
			errorMsg = "You must declare a start date. Try again."
			return render(request, 'setup/products.html', {'form': form_class,
				'delCommodityRegistered': True, 'errorMsg': errorMsg})

		if form.is_valid():
			cleanData = form.cleaned_data

			request.session["projectType"] = cleanData["projectType"]
			request.session["LOM"] = cleanData["LOM"]
			# request.session["projectMineProducts"] = mineProducts
			request.session["projectPlantProducts"] = plantProducts
			request.session["numStockpiles"] = numStockpiles = cleanData["stockpiles"]

			request.session["projectStartYear"] = cleanData["startDate"].year
			request.session["projectStartMonth"] = cleanData["startDate"].month
			request.session["projectStartDay"] = cleanData["startDate"].day

			# # Insert into tblProjectPeriods
			# start = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()

			# if (start.month == 1) and (start.day == 1):
			# 	endYear = int(LOM)
			# else:
			# 	endYear = int(LOM) + 1

			# tblProjectPeriodsObj = tblProjectPeriods(mineID=mineMatch, projectID=tblProjectObj, year=1,
			# 	startDate=start, endDate=datetime.date(start.year, 12, 31), dateAdded=dateAdded)
			# tblProjectPeriodsObj.save()
			# currYear = 2
			# while currYear <= endYear:
			# 	currStartDate = datetime.date(start.year+currYear-1, 1, 1)
			# 	currEndDate = datetime.date(start.year+currYear-1, 12, 31)
			# 	tblProjectPeriodsObj = tblProjectPeriods(mineID=mineMatch, projectID=tblProjectObj, year=currYear,
			# 		startDate=currStartDate, endDate=currEndDate, dateAdded=dateAdded)
			# 	tblProjectPeriodsObj.save()
			# 	currYear += 1

			if (cleanData["startDate"].month == 1) and (cleanData["startDate"].day == 1):
				yearCount = int(LOM)
			else:
				yearCount = int(LOM) + 1
			request.session["yearCount"] = yearCount

			# Pass LOM to next form (CAPEX)
			tempIDs = request.session["mainCommodities"] + request.session["delCommodities"]
			idList = []
			commNameList = []
			for match in tempIDs:
				idList.append(int(match))
				nameMatch = tblCommodityList.objects.get(commodityID=int(match))
				commNameList.append(nameMatch.name)
			request.session["idList"] = idList
			request.session["commNameList"] = commNameList
			numElements = len(idList)

			# next_form = mineProductionForm(LOM=yearCount, mineProducts=mineProducts, idList=idList, commNameList=commNameList)
			next_form = mineProductionForm(LOM=yearCount, numStockpiles=numStockpiles, idList=idList, commNameList=commNameList)
			# return render(request, 'setup/mineProduction.html', {'form': next_form,
			# 	'productsRegistered': True, 'LOM': yearCount, 'mineProducts': mineProducts,
			# 	'idList': idList, 'commNameList': commNameList, 'numElements': numElements}) #Redirect
			return render(request, 'setup/mineProduction.html', {'form': next_form,
				'productsRegistered': True, 'LOM': yearCount, 'numStockpiles': list(range(1, numStockpiles+1)),
				'idList': idList, 'commNameList': commNameList, 'numElements': numElements}) #Redirect

		return render_to_response("setup/products.html", {'form': form_class,
			'delCommodityRegistered': True})

	else:
		return render(request, "setup/products.html", {'form': form_class})


# Function index4 handles Mine Plan declarations
def index4(request):
	numStockpiles = request.session["numStockpiles"]
	yearCount = request.session["yearCount"]
	idList = request.session["idList"]
	commNameList = request.session["commNameList"]
	form_class = mineProductionForm(LOM=request.session["yearCount"], numStockpiles=request.session["numStockpiles"],
		idList=request.session["idList"], commNameList=request.session["commNameList"])
	if request.method == 'POST':
		# numStockpiles = request.session["numStockpiles"]
		# yearCount = request.session["yearCount"]
		# idList = request.session["idList"]
		# commNameList = request.session["commNameList"]
		form = mineProductionForm(request.POST, LOM=yearCount, numStockpiles=request.session["numStockpiles"],
			idList=idList, commNameList=commNameList)
		if form.is_valid():
			cleanData = form.cleaned_data

			minePlanTonnages = {}
			minePlanGrades = {}

			# minePlanHGTonnages = None
			# minePlanLGTonnages = None
			# minePlanWasteTonnages = None
			# minePlanOverburdenTonnages = None

			for curr in range(1, numStockpiles+1):
				currTonnages = []
				currGrades = {}

				for i in range(yearCount):
					i += 1
					currTonnages.append(float(cleanData["year{0}MinePlanStockpile{1}Tonnage".format(i, curr)]))
				minePlanTonnages[curr] = currTonnages

				for name in commNameList:
					tempGrades = []
					for year in range(yearCount):
						year += 1
						tempGrades.append(float(cleanData["year{0}MinePlanSP{1}Grade{2}".format(year,curr,name)]))
					currGrades[name] = tempGrades
				minePlanGrades[curr] = currGrades

			# if str(1) in mineProducts:
			# 	minePlanHGTonnages = []
			# 	minePlanHGGrades = {}
				
			# 	for i in range(yearCount):
			# 		i += 1
			# 		minePlanHGTonnages.append(float(cleanData["year{0}MinePlanHighGradeTonnage".format(i)]))

			# 	for name in commNameList:
			# 		tempGrades = []
			# 		for year in range(yearCount):
			# 			year += 1
			# 			tempGrades.append(float(cleanData["year{0}MinePlanHGGrade{1}".format(year,name)]))
			# 		minePlanHGGrades[name] = tempGrades

			# if str(2) in mineProducts:
			# 	minePlanLGTonnages = []
			# 	minePlanLGGrades = {}

			# 	for i in range(yearCount):
			# 		i += 1
			# 		minePlanLGTonnages.append(float(cleanData["year{0}MinePlanLowGradeTonnage".format(i)]))

			# 	for name in commNameList:
			# 		tempGrades = []
			# 		for year in range(yearCount):
			# 			year += 1
			# 			tempGrades.append(float(cleanData["year{0}MinePlanLGGrade{1}".format(year,name)]))
			# 		minePlanLGGrades[name] = tempGrades

			# if str(3) in mineProducts:
			# 	minePlanWasteTonnages = []
			# 	for i in range(yearCount):
			# 		i += 1
			# 		minePlanWasteTonnages.append(float(cleanData["year{0}MinePlanWasteTonnage".format(i)]))

			# if str(4) in mineProducts:
			# 	minePlanOverburdenTonnages = []
			# 	for i in range(yearCount):
			# 		i += 1
			# 		minePlanOverburdenTonnages.append(float(cleanData["year{0}MinePlanOverburdenTonnage".format(i)]))

			# request.session["minePlanHGTonnages"] = minePlanHGTonnages
			# request.session["minePlanLGTonnages"] = minePlanLGTonnages
			# request.session["minePlanWasteTonnages"] = minePlanWasteTonnages
			# request.session["minePlanOverburdenTonnages"] = minePlanOverburdenTonnages
			# request.session["minePlanHGGrades"] = minePlanHGGrades
			# request.session["minePlanLGGrades"] = minePlanLGGrades

			request.session["minePlanTonnages"] = minePlanTonnages
			request.session["minePlanGrades"] = minePlanGrades

			# Pass LOM to next form (CAPEX)
			next_form = CAPEXForm(LOM=yearCount)
			return render(request, 'setup/capex.html', {'form': next_form,
				'minePlanRegistered': True, 'LOM': yearCount}) #Redirect

# Function index4 handles CAPEX declarations
def index5(request):
	form_class = CAPEXForm

	if request.method == 'POST':
		mineID = request.session["mineID"]
		# latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-projectID')[0]
		# yearCount = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
		yearCount = int(request.POST.get("LOM", ''))
		# LOM = projectMatch.LOM
		form = CAPEXForm(request.POST, LOM=yearCount)
		if form.is_valid():
			# mineMatch = tblMine.objects.get(mineID=int(mineID))
			# dateAdded = timezone.localtime(timezone.now())

			cleanData = form.cleaned_data
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

			negatives = [-3, -2, -1]
			allYears = negatives + list(range(1, yearCount+1))

			for year in allYears:
				preStrip.append(float(cleanData["year{0}PreStripping".format(year)]))
				mineEquipInitial.append(float(cleanData["year{0}MiningEquipmentInitial".format(year)]))
				mineEquipSustain.append(float(cleanData["year{0}MiningEquipmentSustaining".format(year)]))
				infraDirectCost.append(float(cleanData["year{0}InfrastructureDirectCosts".format(year)]))
				infraIndirectCost.append(float(cleanData["year{0}InfrastructureIndirectCosts".format(year)]))
				contingency.append(float(cleanData["year{0}Contingency".format(year)]))
				railcars.append(float(cleanData["year{0}Railcars".format(year)]))
				otherMobEquip.append(float(cleanData["year{0}OtherMobileEquipment".format(year)]))
				closureRehabAssure.append(float(cleanData["year{0}ClosureAndRehabAssurancePayment".format(year)]))
				depoProvisionPay.append(float(cleanData["year{0}DepositsProvisionPayment".format(year)]))
				workCapCurrentProd.append(float(cleanData["year{0}WorkingCapCurrentProd".format(year)]))
				workCapCostsLG.append(float(cleanData["year{0}WorkingCapCostsOfLG".format(year)]))
				EPCM.append(float(cleanData["year{0}EPCM".format(year)]))
				ownerCost.append(float(cleanData["year{0}OwnersCosts".format(year)]))

			# for year in range(1, yearCount+1):
			# 	preStrip.append(float(cleanData["year{0}PreStripping".format(year)]))
			# 	mineEquipInitial.append(float(cleanData["year{0}MiningEquipmentInitial".format(year)]))
			# 	mineEquipSustain.append(float(cleanData["year{0}MiningEquipmentSustaining".format(year)]))
			# 	infraDirectCost.append(float(cleanData["year{0}InfrastructureDirectCosts".format(year)]))
			# 	infraIndirectCost.append(float(cleanData["year{0}InfrastructureIndirectCosts".format(year)]))
			# 	contingency.append(float(cleanData["year{0}Contingency".format(year)]))
			# 	railcars.append(float(cleanData["year{0}Railcars".format(year)]))
			# 	otherMobEquip.append(float(cleanData["year{0}OtherMobileEquipment".format(year)]))
			# 	closureRehabAssure.append(float(cleanData["year{0}ClosureAndRehabAssurancePayment".format(year)]))
			# 	depoProvisionPay.append(float(cleanData["year{0}DepositsProvisionPayment".format(year)]))
			# 	workCapCurrentProd.append(float(cleanData["year{0}WorkingCapCurrentProd".format(year)]))
			# 	workCapCostsLG.append(float(cleanData["year{0}WorkingCapCostsOfLG".format(year)]))
			# 	EPCM.append(float(cleanData["year{0}EPCM".format(year)]))
			# 	ownerCost.append(float(cleanData["year{0}OwnersCosts".format(year)]))

			request.session["preStrip"] = [x*1000000.0 for x in preStrip]
			request.session["mineEquipInitial"] = [x*1000000.0 for x in mineEquipInitial]
			request.session["mineEquipSustain"] = [x*1000000.0 for x in mineEquipSustain]
			request.session["infraDirectCost"] = [x*1000000.0 for x in infraDirectCost]
			request.session["infraIndirectCost"] = [x*1000000.0 for x in infraIndirectCost]
			request.session["contingency"] = [x*1000000.0 for x in contingency]
			request.session["railcars"] = [x*1000000.0 for x in railcars]
			request.session["otherMobEquip"] = [x*1000000.0 for x in otherMobEquip]
			request.session["closureRehabAssure"] = [x*1000000.0 for x in closureRehabAssure]
			request.session["depoProvisionPay"] = [x*1000000.0 for x in depoProvisionPay]
			request.session["workCapCurrentProd"] = [x*1000000.0 for x in workCapCurrentProd]
			request.session["workCapCostsLG"] = [x*1000000.0 for x in workCapCostsLG]
			request.session["EPCM"] = [x*1000000.0 for x in EPCM]
			request.session["ownerCost"] = [x*1000000.0 for x in ownerCost]

			# Pass LOM to next form (OPEX)
			next_form = OPEXForm(LOM=yearCount)
			return render(request, 'setup/opex.html', {'form': next_form,
				'CAPEXRegistered': True, 'LOM': yearCount})

	return render(request, 'setup/capex.html', {'form': form_class })


# Function index5 handles OPEX declarations
def index6(request):
	if request.method == 'POST':
		# mineID = request.session["mineID"]
		# LOM = projectMatch.LOM
		# latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-projectID')[0]
		# yearCount = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
		yearCount = int(request.POST.get("LOM", ''))
		form = OPEXForm(request.POST, LOM=yearCount)
		if form.is_valid():
			# mineMatch = tblMine.objects.get(mineID=int(mineID))
			# dateAdded = timezone.localtime(timezone.now())

			cleanData = form.cleaned_data
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
			for year in range(1, yearCount+1):
				mining.append(float(cleanData["year{0}Mining".format(year)]))
				infrastructure.append(float(cleanData["year{0}Infrastructure".format(year)]))
				stockpileLG.append(float(cleanData["year{0}StockpileLG".format(year)]))
				dewatering.append(float(cleanData["year{0}Dewatering".format(year)]))
				processing.append(float(cleanData["year{0}Processing".format(year)]))
				hauling.append(float(cleanData["year{0}ProductHauling".format(year)]))
				loadOutRailLoop.append(float(cleanData["year{0}LoadoutRailLoop".format(year)]))
				GASite.append(float(cleanData["year{0}GASite".format(year)]))
				GARoomBoardFIFO.append(float(cleanData["year{0}GARoomBoardFIFO".format(year)]))
				railTransport.append(float(cleanData["year{0}RailTransportation".format(year)]))
				GACorp.append(float(cleanData["year{0}GACorporate".format(year)]))
				royalties.append(float(cleanData["year{0}Royalties".format(year)]))
				transportation.append(float(cleanData["year{0}Transportation".format(year)]))
				GA.append(float(cleanData["year{0}GA".format(year)]))
				shipping.append(float(cleanData["year{0}ShippingCost".format(year)]))
				opexPT.append(float(cleanData["year{0}OpexPT".format(year)]))

			request.session["mining"] = [x*1000000.0 for x in mining]
			request.session["infrastructure"] = [x*1000000.0 for x in infrastructure]
			request.session["stockpileLG"] = [x*1000000.0 for x in stockpileLG]
			request.session["dewatering"] = [x*1000000.0 for x in dewatering]
			request.session["processing"] = [x*1000000.0 for x in processing]
			request.session["hauling"] = [x*1000000.0 for x in hauling]
			request.session["loadOutRailLoop"] = [x*1000000.0 for x in loadOutRailLoop]
			request.session["GASite"] = [x*1000000.0 for x in GASite]
			request.session["GARoomBoardFIFO"] = [x*1000000.0 for x in GARoomBoardFIFO]
			request.session["railTransport"] = [x*1000000.0 for x in railTransport]
			request.session["GACorp"] = [x*1000000.0 for x in GACorp]
			request.session["royalties"] = [x*1000000.0 for x in royalties]
			request.session["transportation"] = [x*1000000.0 for x in transportation]
			request.session["GA"] = [x*1000000.0 for x in GA]
			request.session["shipping"] = [x*1000000.0 for x in shipping]
			request.session["opexPT"] = [x*1000000.0 for x in opexPT]

			# Pass list of commodities to smelterForm
			# latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
			# timestamp = latestCommodity.dateAdded
			# commodityMatches = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=timestamp)
			
			tempIDs = request.session["mainCommodities"] + request.session["delCommodities"]
			numStockpiles = request.session["numStockpiles"]

			commIDList = []
			commNameList = []
			# tempIDs = commodityMatches.values_list('commodityID', flat=True)
			for match in tempIDs:
				commIDList.append(int(match))
				nameMatch = tblCommodityList.objects.get(commodityID=int(match))
				commNameList.append(nameMatch.name)

			next_form = smelterForm(idList=commIDList, nameList=commNameList, numStockpiles=numStockpiles)
			return render(request, 'setup/smelter.html', {'form': next_form,
				'OPEXRegistered': True, 'idList': commIDList, 'nameList': commNameList,
				'numStockpiles': list(range(1, numStockpiles+1))})

	return render(request, 'setup/opex.html', {'form': form_class })


# Function index6 handles Smelter Term declarations
def index7(request):
	form_class = smelterForm

	if request.method == 'POST':
		mineID = request.session["mineID"]

		tempIDs = request.session["mainCommodities"] + request.session["delCommodities"]
		idList = []
		commNameList = []
		for match in tempIDs:
			idList.append(int(match))
			nameMatch = tblCommodityList.objects.get(commodityID=int(match))
			commNameList.append(nameMatch.name)
		numStockpiles = request.session["numStockpiles"]
		PPIDs = request.session["projectPlantProducts"]

		form = smelterForm(request.POST, idList=idList, nameList=commNameList, numStockpiles=numStockpiles)
		if form.is_valid():
			# mineMatch = tblMine.objects.get(mineID=int(mineID))
			# dateAdded = timezone.localtime(timezone.now())

			cleanData = form.cleaned_data

			for curr in range(1, numStockpiles+1):
				for i in range(len(idList)):
					request.session["Stockpile{0}MinGrade{1}".format(curr,idList[i])] = float(cleanData["Stockpile{0}MinGrade{1}".format(curr,idList[i])])
					request.session["Stockpile{0}MaxGrade{1}".format(curr,idList[i])] = float(cleanData["Stockpile{0}MaxGrade{1}".format(curr,idList[i])])
					request.session["Stockpile{0}MinPenalty{1}".format(curr,idList[i])] = float(cleanData["Stockpile{0}MinPenalty{1}".format(curr,idList[i])])
					request.session["Stockpile{0}MaxPenalty{1}".format(curr,idList[i])] = float(cleanData["Stockpile{0}MaxPenalty{1}".format(curr,idList[i])])
					request.session["Stockpile{0}MinMaxPenalty{1}".format(curr,idList[i])] = float(cleanData["Stockpile{0}MinMaxPenalty{1}".format(curr,idList[i])])
					request.session["Stockpile{0}Premium{1}".format(curr,idList[i])] = float(cleanData["Stockpile{0}Premium{1}".format(curr,idList[i])])
					request.session["Stockpile{0}Increments{1}".format(curr,idList[i])] = float(cleanData["Stockpile{0}Increments{1}".format(curr,idList[i])])
			# for i in range(len(idList)):
				# request.session["LGMinGrade{0}".format(idList[i])] = float(cleanData["LGMinGrade{0}".format(idList[i])])
				# request.session["LGMaxGrade{0}".format(idList[i])] = float(cleanData["LGMaxGrade{0}".format(idList[i])])
				# request.session["LGMinPenalty{0}".format(idList[i])] = float(cleanData["LGMinPenalty{0}".format(idList[i])])
				# request.session["LGMaxPenalty{0}".format(idList[i])] = float(cleanData["LGMaxPenalty{0}".format(idList[i])])
				# request.session["LGMinMaxPenalty{0}".format(idList[i])] = float(cleanData["LGMinMaxPenalty{0}".format(idList[i])])
				# request.session["LGPremium{0}".format(idList[i])] = float(cleanData["LGPremium{0}".format(idList[i])])
				# request.session["HGMinGrade{0}".format(idList[i])] = float(cleanData["HGMinGrade{0}".format(idList[i])])
				# request.session["HGMaxGrade{0}".format(idList[i])] = float(cleanData["HGMaxGrade{0}".format(idList[i])])
				# request.session["HGMinPenalty{0}".format(idList[i])] = float(cleanData["HGMinPenalty{0}".format(idList[i])])
				# request.session["HGMaxPenalty{0}".format(idList[i])] = float(cleanData["HGMaxPenalty{0}".format(idList[i])])
				# request.session["HGMinMaxPenalty{0}".format(idList[i])] = float(cleanData["HGMinMaxPenalty{0}".format(idList[i])])
				# request.session["HGPremium{0}".format(idList[i])] = float(cleanData["HGPremium{0}".format(idList[i])])
				# request.session["increments{0}".format(idList[i])] = float(cleanData["increments{0}".format(idList[i])])
				
			# Load up the Financials form
			# next_form = financialsForm(mineID=int(mineID), plantProducts=request.session["projectPlantProducts"])
			next_form = financialsForm(numStockpiles=numStockpiles, plantProducts=PPIDs)
			return render(request, 'setup/financials.html', {'form': next_form,
				'smelterRegistered': True, 'numStockpiles': list(range(1, numStockpiles+1)), 'PPIDs': PPIDs})

		else:
			return render(request, 'setup/smelter.html', {'form': form_class,
				'OPEXRegistered': True, 'idList': idList, 'nameList': commNameList})

	return render(request, 'setup/smelter.html', {'form': form_class })


# Function index7 handles financials declarations
def index8(request):
	mineID = request.session["mineID"]
	numStockpiles = request.session["numStockpiles"]
	PPIDs = request.session["projectPlantProducts"]

	if request.method == 'POST':
		form = financialsForm(request.POST, numStockpiles=numStockpiles, plantProducts=PPIDs)
		if form.is_valid():
			# Get list of Plant Product IDs

			# PPIDs = request.session["projectPlantProducts"]
			cleanData = form.cleaned_data
			for curr in range(1, numStockpiles+1):
				if str(1) in PPIDs:
					request.session["Stockpile{0}Lump".format(curr)] = float(cleanData["Stockpile{0}Lump".format(curr)])
					request.session["Stockpile{0}LumpPrem".format(curr)] = float(cleanData["Stockpile{0}LumpPrem".format(curr)])
					request.session["Stockpile{0}LumpAvg".format(curr)] = float(cleanData["Stockpile{0}LumpAvg".format(curr)])
				else:
					request.session["Stockpile{0}Lump".format(curr)] = None
					request.session["Stockpile{0}LumpPrem".format(curr)] = None
					request.session["Stockpile{0}LumpAvg".format(curr)] = None
				if str(2) in PPIDs:
					request.session["Stockpile{0}Fines".format(curr)] = float(cleanData["Stockpile{0}Fines".format(curr)])
				else:
					request.session["Stockpile{0}Fines".format(curr)] = None
				if str(3) in PPIDs:
					request.session["Stockpile{0}UltraFines".format(curr)] = float(cleanData["Stockpile{0}UltraFines".format(curr)])
				else:
					request.session["Stockpile{0}UltraFines".format(curr)] = None

			# if str(1) in PPIDs:	
			# 	request.session["HGLump"] = float(cleanData["HGLump"])
			# 	request.session["HGLumpPrem"] = float(cleanData["HGLumpPrem"])
			# 	request.session["LGLump"] = float(cleanData["LGLump"])
			# 	request.session["LGLumpPrem"] = float(cleanData["LGLumpPrem"])
			# 	request.session["HGLumpAvg"] = float(cleanData["HGLumpAvg"])
			# 	request.session["LGLumpAvg"] = float(cleanData["LGLumpAvg"])
			# else:
			# 	request.session["HGLump"] = None
			# 	request.session["HGLumpPrem"] = None
			# 	request.session["LGLump"] = None
			# 	request.session["LGLumpPrem"] = None
			# 	request.session["HGLumpAvg"] = None
			# 	request.session["LGLumpAvg"] = None

			# if str(2) in PPIDs:
			# 	request.session["HGFines"] = float(cleanData["HGFines"])
			# 	request.session["LGFines"] = float(cleanData["LGFines"])
			# else:
			# 	request.session["HGFines"] = None
			# 	request.session["LGFines"] = None

			# if str(3) in PPIDs:
			# 	request.session["HGUltraFines"] = float(cleanData["HGUltraFines"])
			# 	request.session["LGUltraFines"] = float(cleanData["LGUltraFines"])
			# else:
			# 	request.session["HGUltraFines"] = None
			# 	request.session["LGUltraFines"] = None

			# projectMatch = tblProject.objects.filter(mineID=int(mineID)).order_by('-projectID')[0]
			# LOM = projectMatch.LOM
			# latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-projectID')[0]
			# yearCount = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
			next_form_class = taxesForm(LOM=request.session["yearCount"])
			return render(request, 'setup/taxes.html', {'form': next_form_class,
				'financialsRegistered':True, 'LOM': request.session["yearCount"]}) #Redirect

	form_class = financialsForm(numStockpiles=numStockpiles, plantProducts=PPIDs)
	return render(request, 'setup/financials.html', {'form': form_class })


# Function index8 handles taxes declarations
def index9(request):
	form_class = taxesForm

	if request.method == 'POST':
		yearCount = request.session["yearCount"]
		form = taxesForm(request.POST, LOM=yearCount)
		if form.is_valid():
			# mineMatch = tblMine.objects.get(mineID=int(mineID))
			# dateAdded = timezone.localtime(timezone.now())

			cleanData = form.cleaned_data
			federal = []
			provincial = []
			mining = []
			for year in range(1, yearCount+1):
				federal.append(float(cleanData["year{0}Federal".format(year)]))
				provincial.append(float(cleanData["year{0}Provincial".format(year)]))
				mining.append(float(cleanData["year{0}Mining".format(year)]))

			request.session["taxesFederal"] = [x*1000000.0 for x in federal]
			request.session["taxesProvincial"] = [x*1000000.0 for x in provincial]
			request.session["taxesMining"] = [x*1000000.0 for x in mining]

			next_form_class = inputsForm(plantProducts=request.session["projectPlantProducts"])
			return render(request, 'setup/inputs.html', {'form': next_form_class,
				'taxesRegistered':True}) #Redirect

	return render(request, 'setup/taxes.html', {'form': form_class })


# Function index9 handles inputs declarations
def index10(request):
	form_class = inputsForm(plantProducts=request.session["projectPlantProducts"])

	if request.method == 'POST':
		mineID = request.session["mineID"]
		form = inputsForm(request.POST, plantProducts=request.session["projectPlantProducts"])
		if form.is_valid():
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			dateAdded = timezone.localtime(timezone.now())

			# Get list of Mine Product IDs
			# latestMineProduct = tblMineProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
			# MPtimestamp = latestMineProduct.dateAdded
			# mineProductMatches = tblMineProduct.objects.filter(mineID=int(mineID), dateAdded=MPtimestamp)
			# MPIDs = mineProductMatches.values_list('mineProductID', flat=True)

			# Get list of Plant Product IDs
			# latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
			# PPTimestamp = latestPlantProduct.dateAdded
			# PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
			# PPIDs = PPMatches.values_list('plantProductID', flat=True)

			PPIDs = request.session["projectPlantProducts"]

			# commodityMatches = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=timestamp)
			# tempIDs = commodityMatches.values_list('commodityID', flat=True)

			# Insert into tblProject
			projectTypeID = request.session['projectType']
			startDate = datetime.date(request.session["projectStartYear"], 
				request.session["projectStartMonth"], request.session["projectStartDay"])
			projectTypeMatch = tblProjectTypeList.objects.get(projectTypeID=int(projectTypeID))
			numStockpiles = request.session["numStockpiles"]
			tblProjectObj = tblProject(mineID=mineMatch, projectTypeID=projectTypeMatch,
				LOM=int(request.session["LOM"]), numStockpiles=numStockpiles, startDate=startDate, dateAdded=dateAdded)
			tblProjectObj.save()

			# Insert into tblCommodity
			mainCommodities = request.session["mainCommodities"]
			delCommodities = request.session["delCommodities"]
			for commodity in mainCommodities:
				commodityMatch = tblCommodityList.objects.get(commodityID=int(commodity))
				tblCommodityObj = tblCommodity(commodityID=commodityMatch,
					mineID=mineMatch, projectID=tblProjectObj, dateAdded=dateAdded)
				tblCommodityObj.save()

			for commodity in delCommodities:
				commodityMatch = tblCommodityList.objects.get(commodityID=int(commodity))
				tblCommodityObj = tblCommodity(commodityID=commodityMatch,
					mineID=mineMatch, projectID=tblProjectObj, dateAdded=dateAdded)
				tblCommodityObj.save()

			# # Insert into tblProjectPeriods
			start = datetime.date(request.session["projectStartYear"], 
				request.session["projectStartMonth"], request.session["projectStartDay"])
			if (start.month == 1) and (start.day == 1):
				endYear = int(request.session["LOM"])
			else:
				endYear = int(request.session["LOM"]) + 1

			tblProjectPeriodsObj = tblProjectPeriods(mineID=mineMatch, projectID=tblProjectObj, year=1,
				startDate=start, endDate=datetime.date(start.year, 12, 31), dateAdded=dateAdded)
			tblProjectPeriodsObj.save()
			currYear = 2
			while currYear <= endYear:
				currStartDate = datetime.date(start.year+currYear-1, 1, 1)
				currEndDate = datetime.date(start.year+currYear-1, 12, 31)
				tblProjectPeriodsObj = tblProjectPeriods(mineID=mineMatch, projectID=tblProjectObj, year=currYear,
					startDate=currStartDate, endDate=currEndDate, dateAdded=dateAdded)
				tblProjectPeriodsObj.save()
				currYear += 1

			# # Insert into tblMineProduct
			# mineProducts = request.session["projectMineProducts"]
			# for product in mineProducts:
			# 	mineProductMatch = tblMineProductList.objects.get(mineProductID=int(product))
			# 	tblMineProductObj = tblMineProduct(mineProductID=mineProductMatch, mineID=mineMatch, projectID=tblProjectObj, 
			# 		dateAdded=dateAdded)
			# 	tblMineProductObj.save()

			# Insert into tblPlantProduct
			plantProducts = request.session["projectPlantProducts"]
			for product in plantProducts:
				plantProductMatch = tblPlantProductList.objects.get(plantProductID=int(product))
				tblPlantProductObj = tblPlantProduct(plantProductID=plantProductMatch, mineID=mineMatch, projectID=tblProjectObj,
					recovery=None, moisture=None, dateAdded=dateAdded)
				tblPlantProductObj.save()

			# Insert into tblMineProductTonnage and tblMineProductGrade
			commNameList = request.session["commNameList"]
			idList = request.session["idList"]
			yearCount = request.session["yearCount"]
			numStockpiles = request.session["numStockpiles"]
			minePlanTonnages = request.session["minePlanTonnages"]
			minePlanGrades = request.session["minePlanGrades"]
			for curr in range(1, numStockpiles+1):
				currMPTonnages = minePlanTonnages[str(curr)]
				currMPGrades = minePlanGrades[str(curr)]
				for i in range(len(currMPTonnages)):
					tblMineProductTonnageObj = tblMineProductTonnage(mineID=mineMatch, projectID=tblProjectObj, stockpileID=curr,
						year=i+1, tonnage=currMPTonnages[i], dateAdded=dateAdded)
					tblMineProductTonnageObj.save()

				for i in range(len(commNameList)):
					currGrades = currMPGrades[commNameList[i]]
					commMatch = tblCommodityList.objects.get(commodityID=idList[i])
					for year in range(len(currGrades)):
						tblMineProductGradeObj = tblMineProductGrade(mineID=mineMatch, projectID=tblProjectObj, stockpileID=curr,
							commodityID=commMatch, year=year+1, grade=currGrades[year], dateAdded=dateAdded)
						tblMineProductGradeObj.save()

			# commNameList = request.session["commNameList"]
			# idList = request.session["idList"]
			# yearCount = request.session["yearCount"]
			# if str(1) in mineProducts:
			# 	minePlanHGTonnages = request.session["minePlanHGTonnages"]
			# 	mineProductMatch = tblMineProductList.objects.get(mineProductID=1)
			# 	for i in range(len(minePlanHGTonnages)):
			# 		tblMineProductTonnageObj = tblMineProductTonnage(mineID=mineMatch, projectID=tblProjectObj, mineProductID=mineProductMatch,
			# 			year=i+1, tonnage=minePlanHGTonnages[i], dateAdded=dateAdded)
			# 		tblMineProductTonnageObj.save()

			# 	minePlanHGGrades = request.session["minePlanHGGrades"]
			# 	for i in range(len(commNameList)):
			# 		currGrades = minePlanHGGrades[commNameList[i]]
			# 		commMatch = tblCommodityList.objects.get(commodityID=idList[i])
			# 		for year in range(len(currGrades)):
			# 			tblMineProductGradeObj = tblMineProductGrade(mineID=mineMatch, projectID=tblProjectObj, mineProductID=mineProductMatch,
			# 				commodityID=commMatch, year=year+1, grade=currGrades[year], dateAdded=dateAdded)
			# 			tblMineProductGradeObj.save()

			# if str(2) in mineProducts:
			# 	minePlanLGTonnages = request.session["minePlanLGTonnages"]
			# 	mineProductMatch = tblMineProductList.objects.get(mineProductID=2)
			# 	for i in range(len(minePlanLGTonnages)):
			# 		tblMineProductTonnageObj = tblMineProductTonnage(mineID=mineMatch, projectID=tblProjectObj, mineProductID=mineProductMatch,
			# 			year=i+1, tonnage=minePlanLGTonnages[i], dateAdded=dateAdded)
			# 		tblMineProductTonnageObj.save()

			# 	minePlanLGGrades = request.session["minePlanLGGrades"]
			# 	for i in range(len(commNameList)):
			# 		currGrades = minePlanLGGrades[commNameList[i]]
			# 		commMatch = tblCommodityList.objects.get(commodityID=idList[i])
			# 		for year in range(len(currGrades)):
			# 			tblMineProductGradeObj = tblMineProductGrade(mineID=mineMatch, projectID=tblProjectObj, mineProductID=mineProductMatch,
			# 				commodityID=commMatch, year=year+1, grade=currGrades[year], dateAdded=dateAdded)
			# 			tblMineProductGradeObj.save()

			# if str(3) in mineProducts:
			# 	minePlanWasteTonnages = request.session["minePlanWasteTonnages"]
			# 	mineProductMatch = tblMineProductList.objects.get(mineProductID=3)
			# 	for i in range(len(minePlanWasteTonnages)):
			# 		tblMineProductTonnageObj = tblMineProductTonnage(mineID=mineMatch, projectID=tblProjectObj, mineProductID=mineProductMatch,
			# 			year=i+1, tonnage=minePlanWasteTonnages[i], dateAdded=dateAdded)
			# 		tblMineProductTonnageObj.save()

			# if str(4) in mineProducts:
			# 	minePlanOverburdenTonnages = request.session["minePlanOverburdenTonnages"]
			# 	mineProductMatch = tblMineProductList.objects.get(mineProductID=4)
			# 	for i in range(len(minePlanOverburdenTonnages)):
			# 		tblMineProductTonnageObj = tblMineProductTonnage(mineID=mineMatch, projectID=tblProjectObj, mineProductID=mineProductMatch,
			# 			year=i+1, tonnage=minePlanOverburdenTonnages[i], dateAdded=dateAdded)
			# 		tblMineProductTonnageObj.save()


			# Insert into tblCAPEX
			preStrip = request.session["preStrip"]
			mineEquipInitial = request.session["mineEquipInitial"]
			mineEquipSustain = request.session["mineEquipSustain"]
			infraDirectCost = request.session["infraDirectCost"]
			infraIndirectCost = request.session["infraIndirectCost"]
			contingency = request.session["contingency"]
			railcars = request.session["railcars"]
			otherMobEquip = request.session["otherMobEquip"]
			closureRehabAssure = request.session["closureRehabAssure"]
			depoProvisionPay = request.session["depoProvisionPay"]
			workCapCurrentProd = request.session["workCapCurrentProd"]
			workCapCostsLG = request.session["workCapCostsLG"]
			EPCM = request.session["EPCM"]
			ownerCost = request.session["ownerCost"]

			negatives = [-3, -2, -1]
			allYears = negatives + list(range(1, len(preStrip) - 3 + 1))

			for i in range(len(allYears)):
				tblCAPEXObj = tblCAPEX(mineID=mineMatch, year=allYears[i], preStrip=preStrip[i],
					mineEquipInitial=mineEquipInitial[i], mineEquipSustain=mineEquipSustain[i],
					infraDirectCost=infraDirectCost[i], infraIndirectCost=infraIndirectCost[i],
					contingency=contingency[i], railcars=railcars[i], otherMobEquip=otherMobEquip[i],
					closureRehabAssure=closureRehabAssure[i], depoProvisionPay=depoProvisionPay[i],
					workCapCurrentProd=workCapCurrentProd[i], workCapCostsLG=workCapCostsLG[i],
					EPCM=EPCM[i], ownerCost=ownerCost[i], dateAdded=dateAdded)
				tblCAPEXObj.save()

			# for year in range(endYear):
			# 	tblCAPEXObj = tblCAPEX(mineID=mineMatch, year=year+1, preStrip=preStrip[year],
			# 		mineEquipInitial=mineEquipInitial[year], mineEquipSustain=mineEquipSustain[year],
			# 		infraDirectCost=infraDirectCost[year], infraIndirectCost=infraIndirectCost[year],
			# 		contingency=contingency[year], railcars=railcars[year], otherMobEquip=otherMobEquip[year],
			# 		closureRehabAssure=closureRehabAssure[year], depoProvisionPay=depoProvisionPay[year],
			# 		workCapCurrentProd=workCapCurrentProd[year], workCapCostsLG=workCapCostsLG[year],
			# 		EPCM=EPCM[year], ownerCost=ownerCost[year], dateAdded=dateAdded)
			# 	tblCAPEXObj.save()

			# Insert into tblOPEX
			mining = request.session["mining"]
			infrastructure = request.session["infrastructure"]
			stockpileLG = request.session["stockpileLG"]
			dewatering = request.session["dewatering"]
			processing = request.session["processing"]
			hauling = request.session["hauling"]
			loadOutRailLoop = request.session["loadOutRailLoop"]
			GASite = request.session["GASite"]
			GARoomBoardFIFO = request.session["GARoomBoardFIFO"]
			railTransport = request.session["railTransport"]
			GACorp = request.session["GACorp"]
			royalties = request.session["royalties"]
			transportation = request.session["transportation"]
			GA = request.session["GA"]
			shipping = request.session["shipping"]
			opexPT = request.session["opexPT"]
			for year in range(endYear):
				tblOPEXObj = tblOPEX(mineID=mineMatch, year=year+1, mining=mining[year],
					infrastructure=infrastructure[year], stockpileLG=stockpileLG[year],
					dewatering=dewatering[year], processing=processing[year], hauling=hauling[year],
					loadOutRailLoop=loadOutRailLoop[year], GASite=GASite[year],
					GARoomBoardFIFO=GARoomBoardFIFO[year], railTransport=railTransport[year],
					GACorp=GACorp[year], royalties=royalties[year], transportation=transportation[year],
					GA=GA[year], shipping=shipping[year], opexPT=opexPT[year], dateAdded=dateAdded)
				tblOPEXObj.save()

			# Insert into tblSmelterTerms
			# commodityMatches = tblCommodity.objects.filter(projectID=tblProjectObj.projectID)
			# tempIDs = commodityMatches.values_list('commodityID', flat=True)
			# for ID in tempIDs:
			# 	commMatch = tblCommodityList.objects.get(commodityID=ID)
			# 	tblSmelterTermsObj = tblSmelterTerms(mineID=mineMatch, commodityID=commMatch,
			# 		LGMinGrade=request.session["LGMinGrade{0}".format(ID)], LGMaxGrade=request.session["LGMaxGrade{0}".format(ID)],
			# 		LGMinPenalty=request.session["LGMinPenalty{0}".format(ID)], LGMaxPenalty=request.session["LGMaxPenalty{0}".format(ID)], 
			# 		LGMinMaxPenalty=request.session["LGMinMaxPenalty{0}".format(ID)], LGPremium=request.session["LGPremium{0}".format(ID)], 
			# 		HGMinGrade=request.session["HGMinGrade{0}".format(ID)], HGMaxGrade=request.session["HGMaxGrade{0}".format(ID)],
			# 		HGMinPenalty=request.session["HGMinPenalty{0}".format(ID)], HGMaxPenalty=request.session["HGMaxPenalty{0}".format(ID)], 
			# 		HGMinMaxPenalty=request.session["HGMinMaxPenalty{0}".format(ID)], HGPremium=request.session["HGPremium{0}".format(ID)], 
			# 		increments=request.session["increments{0}".format(ID)], dateAdded=dateAdded)
			# 	tblSmelterTermsObj.save()

			for curr in range(1, numStockpiles+1):
				for ID in idList:
					commMatch = tblCommodityList.objects.get(commodityID=ID)
					tblSmelterTermsObj = tblSmelterTerms(mineID=mineMatch, projectID=tblProjectObj, commodityID=commMatch, stockpileID=curr,
						minGrade=request.session["Stockpile{0}MinGrade{1}".format(curr,ID)], maxGrade=request.session["Stockpile{0}MaxGrade{1}".format(curr,ID)],
						minPenalty=request.session["Stockpile{0}MinPenalty{1}".format(curr,ID)], maxPenalty=request.session["Stockpile{0}MaxPenalty{1}".format(curr,ID)], 
						minMaxPenalty=request.session["Stockpile{0}MinMaxPenalty{1}".format(curr,ID)], premium=request.session["Stockpile{0}Premium{1}".format(curr,ID)], 
						increments=request.session["Stockpile{0}Increments{1}".format(curr,ID)], dateAdded=dateAdded)
					tblSmelterTermsObj.save()

			# Insert into tblPrice
			for curr in range(1, numStockpiles+1):
				tblPriceObj = tblPrice(mineID=mineMatch, projectID=tblProjectObj, stockpileID=curr,
					lump=request.session["Stockpile{0}Lump".format(curr)],
					lumpPrem=request.session["Stockpile{0}LumpPrem".format(curr)],
					fines=request.session["Stockpile{0}Fines".format(curr)],
					ultraFines=request.session["Stockpile{0}UltraFines".format(curr)],
					lumpAvg=request.session["Stockpile{0}LumpAvg".format(curr)],
					dateAdded=dateAdded)
				tblPriceObj.save()
			# tblPriceObj = tblPrice(mineID=mineMatch,
			# 	HGLump=request.session["HGLump"], HGLumpPrem=request.session["HGLumpPrem"], 
			# 	HGFines=request.session["HGFines"], HGUltraFines=request.session["HGUltraFines"], 
			# 	LGLump=request.session["LGLump"], LGLumpPrem=request.session["LGLumpPrem"],
			# 	LGFines=request.session["LGFines"], LGUltraFines=request.session["LGUltraFines"],
			# 	HGLumpAvg=request.session["HGLumpAvg"], LGLumpAvg=request.session["LGLumpAvg"], 
			# 	dateAdded=dateAdded)
			# tblPriceObj.save()

			# Insert into tblTaxes
			yearCount = tblProjectPeriods.objects.filter(projectID=tblProjectObj.projectID).count()
			federal = request.session["taxesFederal"]
			provincial = request.session["taxesProvincial"]
			mining = request.session["taxesMining"]
			for year in range(yearCount):
				tblTaxesObj = tblTaxes(mineID=mineMatch, year=year+1, federal=federal[year],
					provincial=provincial[year], mining=mining[year], dateAdded=dateAdded)
				tblTaxesObj.save()

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

			if str(1) in PPIDs:
				lumpRecovery = request.POST.get('lumpRecovery', '')
				lumpGrade = request.POST.get('lumpGrade', '')
				lumpMoisture = request.POST.get('lumpMoisture', '')
			else:
				lumpRecovery = None
				lumpGrade = None
				lumpMoisture = None

			if str(2) in PPIDs:
				finesRecovery = request.POST.get('finesRecovery', '')
				finesGrade = request.POST.get('finesGrade', '')
				finesMoisture = request.POST.get('finesMoisture', '')
			else:
				finesRecovery = None
				finesGrade = None
				finesMoisture = None

			if str(3) in PPIDs:
				ultraFinesRecovery = request.POST.get('ultraFinesRecovery', '')
				ultraFinesGrade = request.POST.get('ultraFinesGrade', '')
				ultraFinesMoisture = request.POST.get('ultraFinesMoisture', '')
			else:
				ultraFinesRecovery = None
				ultraFinesGrade = None
				ultraFinesMoisture = None

			if str(4) in PPIDs:
				rejectsRecovery = request.POST.get('rejectsRecovery', '')
				rejectsGrade = request.POST.get('rejectsGrade', '')
				rejectsMoisture = request.POST.get('rejectsMoisture', '')
			else:
				rejectsRecovery = None
				rejectsGrade = None
				rejectsMoisture = None

			tblInputsObj = tblInputs(mineID=mineMatch, Fe2O3Iron=Fe2O3Iron, 
				totalGrade=totalGrade, avgCommodity1Grade=avgCommodity1Grade,
				lumpRecovery=lumpRecovery, finesRecovery=finesRecovery,
				lumpGrade=lumpGrade, finesGrade=finesGrade,
				feedMoisture=feedMoisture, lumpMoisture=lumpMoisture,
				finesMoisture=finesMoisture, ultraFinesMoisture=ultraFinesMoisture,
				rejectsMoisture=rejectsMoisture, mineOpsDays=mineOpsDays,
				plantOpsDays=plantOpsDays, mineCapacity=mineCapacity,
				plantCapacity=plantCapacity, discountRate1=Decimal(discountRate1),
				discountRate2=Decimal(discountRate2), discountRate3=Decimal(discountRate3),
				discountRate4=Decimal(discountRate4), discountRate5=Decimal(discountRate5),
				discountRate6=Decimal(discountRate6), exchangeRate=exchangeRate, dateAdded=dateAdded,
				ultraFinesRecovery=ultraFinesRecovery, ultraFinesGrade=ultraFinesGrade,
				rejectsRecovery=rejectsRecovery, rejectsGrade=rejectsGrade)
			tblInputsObj.save()

			tempUser = request.session['username']
			tempFN = request.session['firstname']
			tempUserID = request.session['userID'] 
			tempMineID = request.session['mineID']
			request.session.flush()
			request.session['username'] = tempUser
			request.session['firstname'] = tempFN
			request.session['userID'] = tempUserID
			request.session['mineID'] = tempMineID
			request.session.set_expiry(0)

			return render(request, 'setup/success.html', { }) #Redirect

	return render(request, 'setup/inputs.html', {'form': form_class })
