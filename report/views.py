from django.shortcuts import render
from django.db.models import Sum, Avg
from django.utils import timezone
from setup.models import *
from decimal import *
from functools import reduce
import numpy as np
import operator
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from math import pow
from math import ceil
import csv
import calendar
from django.http import HttpResponse
from .forms import *

def padList(yearVals, yearCount, toPad, marker):
	if not yearVals:
		toPad += [marker]*yearCount
		return toPad

	for i in range(1, yearCount+1):
		if i not in yearVals:
			toPad.insert(i-1, marker)
	return toPad

# Create your views here.
def index(request):
	filler = ""
	# tempUser = request.session['username']
	# tempFN = request.session['firstname']
	# tempUserID = request.session['userID'] 
	# tempMineID = request.session['mineID']
	# request.session.flush()
	# request.session['username'] = tempUser
	# request.session['firstname'] = tempFN
	# request.session['userID'] = tempUserID
	# request.session['mineID'] = tempMineID
	# request.session.set_expiry(0)

	mineID = request.session["mineID"]
	mineMatch = tblMine.objects.get(mineID=int(mineID))

	# Check project exists
	projectsList  = tblProject.objects.filter(mineID=mineID)
	if not projectsList:
		return render(request, "report/noProjects.html", {})

	# # Get LOM of the mine's most recent project
	latestProject = projectsList.order_by('-dateAdded')[0]
	LOM = int(latestProject.LOM)
	numStockpiles = latestProject.numStockpiles
	# For now we use LOM=1
	# LOM = 1

	# # Get list of Mine Product IDs
	# latestMineProduct = tblMineProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	# MPTimestamp = latestMineProduct.dateAdded
	# mineProductMatches = tblMineProduct.objects.filter(mineID=int(mineID), dateAdded=MPTimestamp)
	# MPIDs = mineProductMatches.values_list('mineProductID', flat=True)

	# Get list of Commodity IDs
	commodities = tblCommodity.objects.filter(projectID=latestProject.projectID)
	commIDs = commodities.values_list('commodityID', flat=True)
	# latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	# commtimestamp = latestCommodity.dateAdded
	# commodities = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=commtimestamp)
	# commIDs = commodities.values_list('commodityID', flat=True)

	# Get list of Commodity Names
	commNameList = []
	for ID in commIDs:
		nameMatch = tblCommodityList.objects.get(commodityID=ID)
		commNameList.append(nameMatch.name)

	# Get list of Plant Product IDs
	PPMatches = tblPlantProduct.objects.filter(projectID=latestProject.projectID)
	PPIDs = PPMatches.values_list('plantProductID', flat=True)
	# latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	# PPTimestamp = latestPlantProduct.dateAdded
	# PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
	# PPIDs = PPMatches.values_list('plantProductID', flat=True)

	# Get most recent tblInputs entry
	latestInput = tblInputs.objects.filter(mineID=mineID).order_by('-dateAdded')[0]

	yearVals = []
	tonnageVals = None
	tonnageTotals = None
	gradeVals = None
	moistures = None

	lumpTonnageVals = None
	lumpTonnageTotal = None
	lumpGradeVals = None
	lumpMoistures = None

	finesTonnageVals = None
	finesTonnageTotal = None
	finesGradeVals = None
	finesMoistures = None

	ultraFinesTonnageVals = None
	ultraFinesTonnageTotal = None
	ultraFinesGradeVals = None
	ultraFinesMoistures = None

	rejectsTonnageVals = None
	rejectsTonnageTotal = None
	rejectsGradeVals = None
	rejectsMoistures = None


	HGLumps = None
	lumpPenaltyVals = None
	lumpSellingPrices = None
	avgLumpSellingPrice = None
	netLumpPrices = None
	avgNetLumpPrice = None
	exchangeNetLumpPrices = None
	avgExchangeNetLumpPrice = None

	HGFines = None
	finesPenaltyVals = None
	finesSellingPrices = None
	avgFinesSellingPrice = None
	netFinesPrices = None
	avgNetFinesPrice = None
	exchangeNetFinesPrices = None
	avgExchangeNetFinesPrice = None

	HGUltraFines = None
	ultraFinesPenaltyVals = None
	ultraFinesSellingPrices = None
	avgUltraFinesSellingPrice = None
	netUltraFinesPrices = None
	avgNetUltraFinesPrice = None
	exchangeNetUltraFinesPrices = None
	avgExchangeNetUltraFinesPrice = None


	lumpRevenues = None
	sumLumpRevenues = None
	finesRevenues = None
	sumFinesRevenues = None
	ultraFinesRevenues = None
	sumUltraFinesRevenues = None
	# totalRevenues = [Decimal(0.0)]*len(yearVals)
	# lumpPlusFinesRevenues = [Decimal(0.0)]*len(yearVals)

	discountRates = [Decimal(0.06), Decimal(0.08), Decimal(0.10), Decimal(0.12), Decimal(0.15), Decimal(0.20)]

	projectPeriods = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).order_by('year')
	# yearCount = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
	yearCount = projectPeriods.count()

	projectStartDate = projectPeriods[0].startDate
	projectEndDate = projectPeriods[yearCount-1].endDate

	# Check if default filter options are available
	# Check "This year", "Last year", "This quarter", and "Last quarter"
	# 1. This year
	today = datetime.date.today()
	if (today.year >= projectStartDate.year) and (today.year <= projectEndDate.year):
		# thisYear = True
		thisYearStartDate = datetime.date(today.year, 1, 1)
		thisYearEndDate = datetime.date(today.year, 12, 31)
	else:
		# thisYear = False
		thisYearStartDate = None
		thisYearEndDate = None

	# 2. Last year
	if (today.year-1 >= projectStartDate.year) and (today.year-1 <= projectEndDate.year):
		# lastYear = True
		lastYearStartDate = datetime.date(today.year-1, 1, 1)
		lastYearEndDate = datetime.date(today.year-1, 12, 31)
	else:
		# lastYear = False
		lastYearStartDate = None
		lastYearEndDate = None

	# 3. This quarter
	if thisYearStartDate:
		todayQ = ceil(today.month/3.0)
		if today.year == projectStartDate.year:
			startDateQ = ceil(projectStartDate.month/3.0)
			quarters = list(range(startDateQ, 5))			
			if todayQ in quarters:
				# thisQuarter = True
				thisQuarterStartDate = datetime.date(today.year, 3*(todayQ - 1) + 1, 1)
				thisQuarterEndDate = thisQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
			else:
				# thisQuarter = False
				thisQuarterStartDate = None
				thisQuarterEndDate = None
		else:
			# thisQuarter = True
			thisQuarterStartDate = datetime.date(today.year, 3*(todayQ - 1) + 1, 1)
			thisQuarterEndDate = thisQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
	else:
		# thisQuarter = False
		thisQuarterStartDate = None
		thisQuarterEndDate = None

	# 4. Last quarter
	threeMonthsAgo = today - relativedelta(months=+3)
	if (threeMonthsAgo >= projectStartDate) and (threeMonthsAgo <= projectEndDate):
		threeMonthsAgoQ = ceil(threeMonthsAgo.month/3.0)
		# lastQuarter = True
		lastQuarterStartDate = datetime.date(threeMonthsAgo.year, 3*(threeMonthsAgoQ - 1) + 1, 1)
		lastQuarterEndDate = lastQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
	else:
		# lastQuarter = False
		lastQuarterStartDate = None
		lastQuarterEndDate = None


	fullYearVals = list(range(1, yearCount+1))
	fullYearVals = [x+latestProject.startDate.year-1 for x in fullYearVals]
	fullYears = []

	for i in range(yearCount):
		i += 1
		currPeriod = projectPeriods.get(year=i)
		# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=i)
		currStart = currPeriod.startDate
		currEnd = currPeriod.endDate
		fullYears.append(currPeriod.startDate.year)
		calculated = tblRevenue.objects.filter(projectID=latestProject.projectID, date__gte=currStart, date__lte=currEnd)
		if calculated:
			yearVals.append(i)

	totalRevenues = [Decimal(0.0)]*len(yearVals)
	lumpPlusFinesRevenues = [Decimal(0.0)]*len(yearVals)

	# Handle Products Selling Price section
	# priceEntry = tblPrice.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
	priceEntry = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=1)

	# Handle OPEX Shipping Cost by Year
	shippingCosts = []
	fullShippingCosts = []
	for year in range(1, yearCount+1):
		currOPEX = tblOPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
		fullShippingCosts.append(round(Decimal(currOPEX.shipping),2))
		if year in yearVals:
			shippingCosts.append(round(Decimal(currOPEX.shipping),2))

	# Obtain Exchange Rate
	exchangeRates = [round(Decimal(latestInput.exchangeRate),2)]*len(yearVals)
	fullExchangeRates = [round(Decimal(latestInput.exchangeRate),2)]*yearCount
	xRate = round(Decimal(latestInput.exchangeRate),2)

	# Handle Costs Section (OPEX)
	mining = []
	infrastructure = []
	stockpileLG = []
	dewatering = []
	processing = []
	hauling = []
	loadOutRailLoop = []
	GASite = []
	GARoom = []
	railTransport = []
	GACorp = []
	royalties = []
	transportation = []
	GA = []

	dailyMining = {}
	dailyInfrastructure = {}
	dailyStockpileLG = {}
	dailyDewatering = {}
	dailyProcessing = {}
	dailyHauling = {}
	dailyLoadOutRailLoop = {}
	dailyGASite = {}
	dailyGARoom = {}
	dailyRailTransport = {}
	dailyGACorp = {}
	dailyRoyalties = {}
	dailyTransportation = {}
	dailyGA = {}

	for year in range(1, yearCount+1):
		currOPEX = tblOPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
		mining.append(round(Decimal(currOPEX.mining),2))
		infrastructure.append(round(Decimal(currOPEX.infrastructure),2))
		stockpileLG.append(round(Decimal(currOPEX.stockpileLG),2))
		dewatering.append(round(Decimal(currOPEX.dewatering),2))
		processing.append(round(Decimal(currOPEX.processing),2))
		hauling.append(round(Decimal(currOPEX.hauling),2))
		loadOutRailLoop.append(round(Decimal(currOPEX.loadOutRailLoop),2))
		GASite.append(round(Decimal(currOPEX.GASite),2))
		GARoom.append(round(Decimal(currOPEX.GARoomBoardFIFO),2))
		railTransport.append(round(Decimal(currOPEX.railTransport),2))
		GACorp.append(round(Decimal(currOPEX.GACorp),2))
		royalties.append(round(Decimal(currOPEX.royalties),2))
		transportation.append(round(Decimal(currOPEX.transportation),2))
		GA.append(round(Decimal(currOPEX.GA),2))
	sumMining = sum(mining)
	sumStockpileLG = sum(stockpileLG)
	sumDewatering = sum(dewatering)
	sumProcessing = sum(processing)
	sumHauling = sum(hauling)
	sumLoadOutRailLoop = sum(loadOutRailLoop)
	sumGASite = sum(GASite)
	sumGARoom = sum(GARoom)
	sumRailTransport = sum(railTransport)
	sumGACorp = sum(GACorp)
	sumRoyalties = sum(royalties)
	totalOPEX = [sum(x) for x in zip(mining, stockpileLG, dewatering, processing, hauling,
		loadOutRailLoop, GASite, GARoom, railTransport, GACorp)]
	cashFlowOPEX = [sum(x) for x in zip(mining, infrastructure, stockpileLG, dewatering, processing, hauling,
		loadOutRailLoop, GASite, GARoom, railTransport, GACorp, royalties, transportation, GA)]
	sumTotalOPEX = sum(totalOPEX)


	# Handle Costs Section (CAPEX)
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

	latestCAPEX = tblCAPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	timestamp = latestCAPEX.dateAdded
	CAPEXEntries = tblCAPEX.objects.filter(mineID=int(mineID), dateAdded=timestamp)

	negCAPEX = []
	for year in [-3,-2,-1]:
		currCAPEX = CAPEXEntries.filter(year=year)
		if currCAPEX:
			row = currCAPEX[0]
			negCAPEX.append(round(Decimal(row.preStrip + row.mineEquipInitial + row.mineEquipSustain + 
				row.infraDirectCost + row.infraIndirectCost + row.contingency + row.railcars + 
				row.otherMobEquip + row.closureRehabAssure + row.depoProvisionPay + 
				row.workCapCurrentProd + row.workCapCostsLG + row.EPCM + row.ownerCost),2))
		else:
			negCAPEX.append(Decimal(0.0))
	sumNegCAPEX = sum(negCAPEX)

	for year in range(1, yearCount+1):
		currCAPEX = CAPEXEntries.filter(year=year)[0]
		preStrip.append(round(Decimal(currCAPEX.preStrip),2))
		mineEquipInitial.append(round(Decimal(currCAPEX.mineEquipInitial),2))
		mineEquipSustain.append(round(Decimal(currCAPEX.mineEquipSustain),2))
		infraDirectCost.append(round(Decimal(currCAPEX.infraDirectCost),2))
		infraIndirectCost.append(round(Decimal(currCAPEX.infraIndirectCost),2))
		contingency.append(round(Decimal(currCAPEX.contingency),2))
		railcars.append(round(Decimal(currCAPEX.railcars),2))
		otherMobEquip.append(round(Decimal(currCAPEX.otherMobEquip),2))
		closureRehabAssure.append(round(Decimal(currCAPEX.closureRehabAssure),2))
		depoProvisionPay.append(round(Decimal(currCAPEX.depoProvisionPay),2))
		workCapCurrentProd.append(round(Decimal(currCAPEX.workCapCurrentProd),2))
		workCapCostsLG.append(round(Decimal(currCAPEX.workCapCostsLG),2))
		EPCM.append(round(Decimal(currCAPEX.EPCM),2))
		ownerCost.append(round(Decimal(currCAPEX.ownerCost),2))
	sumPreStrip = sum(preStrip)
	sumMineEquipInitial = sum(mineEquipInitial)
	sumMineEquipSustain = sum(mineEquipSustain)
	sumInfraDirectCost = sum(infraDirectCost)
	sumInfraIndirectCost = sum(infraIndirectCost)
	sumContingency = sum(contingency)
	sumRailcars = sum(railcars)
	sumOtherMobEquip = sum(otherMobEquip)
	sumClosureRehabAssure = sum(closureRehabAssure)
	sumDepoProvisionPay = sum(depoProvisionPay)
	sumWorkCapCurrentProd = sum(workCapCurrentProd)
	sumWorkCapCostsLG = sum(workCapCostsLG)
	totalCAPEX = [sum(x) for x in zip(preStrip, mineEquipInitial, mineEquipSustain, infraDirectCost, infraIndirectCost,
		contingency, railcars, otherMobEquip, closureRehabAssure, depoProvisionPay)]
	cashFlowCAPEX = [sum(x) for x in zip(totalCAPEX, workCapCurrentProd, workCapCostsLG, EPCM, ownerCost)]
	sumTotalCAPEX = sum(totalCAPEX)


	# Handle Taxes Section
	federalTaxes = []
	provincialTaxes = []
	miningTaxes = []
	proratedTaxes = {}

	for year in range(1, yearCount+1):
		currTaxes = tblTaxes.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
		federalTaxes.append(round(Decimal(currTaxes.federal),2))
		provincialTaxes.append(round(Decimal(currTaxes.provincial),2))
		miningTaxes.append(round(Decimal(currTaxes.mining),2))
	sumFederalTaxes = sum(federalTaxes)
	sumProvincialTaxes = sum(provincialTaxes)
	sumMiningTaxes = sum(miningTaxes)
	totalTaxes = [sum(x) for x in zip(federalTaxes, provincialTaxes, miningTaxes)]
	for i in range(len(totalTaxes)):
		currYear = projectStartDate.year + i
		proratedTaxes[currYear] = totalTaxes[i]/Decimal(366.0) if calendar.isleap(currYear) else totalTaxes[i]/Decimal(365.0)
	sumTotalTaxes = sum(totalTaxes)


	# Handle Mine Plan Tonnages Section
	sumMinePlanTonnages = {}
	minePlanTonnageVals = {}
	for curr in range(1, numStockpiles+1):
		currTonnageVals = []
		currTonnageEntries = tblMineProductTonnage.objects.filter(projectID=latestProject.projectID, stockpileID=curr).order_by('year')
		for entry in currTonnageEntries:
			currTonnageVals.append(round(Decimal(entry.tonnage),2))
		minePlanTonnageVals[curr] = currTonnageVals
		sumMinePlanTonnages[curr] = (sum(currTonnageVals))

	if not yearVals:
		filler = " - "
		totalProducts = [filler]*yearCount
		sumTotalProducts = filler

		tonnageVals = {}
		tonnageTotals = {}
		gradeVals = {}
		moistures = {}
		for curr in range(1, numStockpiles+1):
			tonnageVals[curr] = padList(yearVals, yearCount, [], filler)
			tonnageTotals[curr] = filler
			currGrades = {}
			for i in range(len(commIDs)):
				currGrades[commNameList[i]] = [filler]*yearCount
			gradeVals[curr] = currGrades
			moistures[curr] = padList(yearVals, yearCount, [], round(latestInput.feedMoisture,2))

		# if 1 in MPIDs:
		# 	HGTonnageVals = padList(yearVals, yearCount, [], 'N/A')
		# 	HGTonnageTotal = 'N/A'
		# 	HGGradeVals = {}
		# 	for i in range(len(commIDs)):
		# 		HGGradeVals[commNameList[i]] = ['N/A']*yearCount
		# 	# HGGradeVals = padList(yearVals, yearCount, [], "N/A")
		# 	HGMoistures = padList(yearVals, yearCount, [], round(latestInput.feedMoisture,2))

		# if 2 in MPIDs:
		# 	LGTonnageVals = padList(yearVals, yearCount, [], 'N/A')
		# 	LGTonnageTotal = 'N/A'
		# 	LGGradeVals = {}
		# 	for i in range(len(commIDs)):
		# 		LGGradeVals[commNameList[i]] = ['N/A']*yearCount
		# 	# LGGradeVals = padList(yearVals, yearCount, [], "N/A")
		# 	LGMoistures = padList(yearVals, yearCount, [], round(latestInput.feedMoisture,2))

		if 1 in PPIDs:
			lumpTonnageVals = padList(yearVals, yearCount, [], filler)
			lumpTonnageTotal = filler
			lumpGradeVals = {}
			for i in range(len(commIDs)):
				lumpGradeVals[commNameList[i]] = [filler]*yearCount
			# lumpGradeVals = padList(yearVals, yearCount, [], "N/A")
			lumpMoistures = padList(yearVals, yearCount, [], round(latestInput.lumpMoisture,2))
		
		if 2 in PPIDs:
			finesTonnageVals = padList(yearVals, yearCount, [], filler)
			finesTonnageTotal = filler
			finesGradeVals = {}
			for i in range(len(commIDs)):
				finesGradeVals[commNameList[i]] = [filler]*yearCount
			# finesGradeVals = padList(yearVals, yearCount, [], "N/A")
			finesMoistures = padList(yearVals, yearCount, [], round(latestInput.finesMoisture,2))

		if 3 in PPIDs:
			ultraFinesTonnageVals = padList(yearVals, yearCount, [], filler)
			ultraFinesTonnageTotal = filler
			ultraFinesGradeVals = {}
			for i in range(len(commIDs)):
				ultraFinesGradeVals[commNameList[i]] = [filler]*yearCount
			ultraFinesMoistures = padList(yearVals, yearCount, [], round(latestInput.ultraFinesMoisture,2))

		sumTotalProducts = filler

		if 4 in PPIDs:
			rejectsTonnageVals = padList(yearVals, yearCount, [], filler)
			rejectsTonnageTotal = filler
			rejectsGradeVals = {}
			for i in range(len(commIDs)):
				rejectsGradeVals[commNameList[i]] = [filler]*yearCount
			rejectsMoistures = padList(yearVals, yearCount, [], round(latestInput.rejectsMoisture,2))

		if 1 in PPIDs:
			# HGLumps = [round(Decimal(priceEntry.HGLump),2)]*yearCount
			HGLumps = [round(Decimal(priceEntry.lump),2)]*yearCount
			lumpPenaltyVals = {}
			for i in range(len(commIDs)):
				lumpPenaltyVals[commNameList[i]] = [filler]*yearCount
			lumpSellingPrices = [filler]*yearCount
			avgLumpSellingPrice = filler
			netLumpPrices = [filler]*yearCount
			avgNetLumpPrice = filler
			exchangeNetLumpPrices = [filler]*yearCount
			avgExchangeNetLumpPrice = filler
			lumpRevenues = [filler]*yearCount
			sumLumpRevenues = filler

		if 2 in PPIDs:
			# HGFines = [round(Decimal(priceEntry.HGFines),2)]*yearCount
			HGFines = [round(Decimal(priceEntry.fines),2)]*yearCount
			finesPenaltyVals = {}
			for i in range(len(commIDs)):
				finesPenaltyVals[commNameList[i]] = [filler]*yearCount
			finesSellingPrices = [filler]*yearCount
			avgFinesSellingPrice = filler
			netFinesPrices = [filler]*yearCount
			avgNetFinesPrice = filler
			exchangeNetFinesPrices = [filler]*yearCount
			avgExchangeNetFinesPrice = filler
			finesRevenues = [filler]*yearCount
			sumFinesRevenues = filler

		if 3 in PPIDs:
			# HGUltraFines = [round(Decimal(priceEntry.HGUltraFines),2)]*yearCount
			HGUltraFines = [round(Decimal(priceEntry.ultraFines),2)]*yearCount
			ultraFinesPenaltyVals = {}
			for i in range(len(commIDs)):
				ultraFinesPenaltyVals[commNameList[i]] = [filler]*yearCount
			ultraFinesSellingPrices = [filler]*yearCount
			avgUltraFinesSellingPrice = filler
			netUltraFinesPrices = [filler]*yearCount
			avgNetUltraFinesPrice = filler
			exchangeNetUltraFinesPrices = [filler]*yearCount
			avgExchangeNetUltraFinesPrice = filler
			ultraFinesRevenues = [filler]*yearCount
			sumUltraFinesRevenues = filler

		totalRevenues = [filler]*yearCount
		sumTotalRevenues = filler

		cashFlowPreTax = cashFlowPostTax = cumCashFlowPreTax = cumCashFlowPostTax = [filler]*yearCount
		sumCashFlowPreTax = sumCashFlowPostTax = filler
		paybackPreTax = paybackPostTax = [filler]*yearCount
		sumPaybackPreTax = sumPaybackPostTax = filler
		preTaxNPVs = postTaxNPVs = [filler]*yearCount
		preTaxIRR = postTaxIRR = filler


		preTaxPVs = {}
		postTaxPVs = {}
		sumPreTaxNPV = {}
		sumPostTaxNPV = {}
		for rate in discountRates:
			rate = int(round(rate*100))
			preTaxPVs[rate] = [filler]*yearCount
			postTaxPVs[rate] = [filler]*yearCount
			sumPreTaxNPV[rate] = filler
			sumPostTaxNPV[rate] = filler

		# reportRowCount = 1
		reportData = ""

		currRow = 'Item,'
		for year in range(1, yearCount+1):
			currRow += 'Year{0},'.format(year)
		currRow += 'Total;'
		reportData += currRow

		reportData += ";Mining;"
		for curr in range(1, numStockpiles+1):
			currRow = "Stockpile {0} Ore (kt),".format(curr) + ''.join([*[str(round(x,2))+',' for x in minePlanTonnageVals[curr]]]) + str(round(sumMinePlanTonnages[curr],2)) + ";"
			reportData += currRow

		reportData += ";Processing;"
		for curr in range(1, numStockpiles+1):
			reportData += "Stockpile {0} Ore;".format(curr)
			currRow = 'Tonnage (kt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]) + ',' + filler + ";"
			reportData += currRow
			for i in range(len(commIDs)):
				currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]) + ';'
				reportData += currRow
			reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]) + ';'

		reportData += ";Plant Product;"

		if 1 in PPIDs:
			reportData += "Lump;"
			currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]) + ',' + filler + ';'
			reportData += currRow
			for i in range(len(commIDs)):
				currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]) + ';'
				reportData += currRow
			reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]) + ';'

		if 2 in PPIDs:
			reportData += "Fines;"
			currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]) + ',' + filler + ';'
			reportData += currRow
			for i in range(len(commIDs)):
				currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]) + ';'
				reportData += currRow
			reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]) + ';'

		if 3 in PPIDs:
			reportData += "Ultra Fines;"
			currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]) + ',' + filler + ';'
			reportData += currRow
			for i in range(len(commIDs)):
				currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]) + ';'
				reportData += currRow
			reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]) + ';'

		reportData += 'Total Product (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]) + ',' + filler + ';'

		if 4 in PPIDs:
			reportData += "Rejects;"
			currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]) + ',' + filler + ';'
			reportData += currRow
			for i in range(len(commIDs)):
				currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]) + ';'
				reportData += currRow
			reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]) + ';'

		reportData += ";Products Selling Price;"

		if 1 in PPIDs:
			reportData += 'Lump Selling Price (USD/dmt);'
			reportData += 'Lump Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]) + ';'
			for i in range(len(commIDs)):
				reportData += 'Lump {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]) + ';'
			reportData += 'Lump Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]) + ',' + 'Avg: ' + filler + ';'
			reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
			reportData += 'Net Lump Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]) + ',' + 'Avg: ' + filler + ';'
			reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
			reportData += 'Net Lump Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]) + ',' + 'Avg: ' + filler + ';'

		if 2 in PPIDs:
			reportData += 'Fines Selling Price (USD/dmt);'
			reportData += 'Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]) + ';'
			for i in range(len(commIDs)):
				reportData += 'Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]) + ';'
			reportData += 'Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]) + ',' + 'Avg: ' + filler + ';'
			reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
			reportData += 'Net Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]) + ',' + 'Avg: ' + filler + ';'
			reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
			reportData += 'Net Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]) + ',' + 'Avg: ' + filler + ';'

		if 3 in PPIDs:
			reportData += 'Ultra Fines Selling Price (USD/dmt);'
			reportData += 'Ultra Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]) + ';'
			for i in range(len(commIDs)):
				reportData += 'Ultra Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]) + ';'
			reportData += 'Ultra Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]) + ',' + 'Avg: ' + filler + ';'
			reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
			reportData += 'Net Ultra Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]) + ',' + 'Avg: ' + filler + ';'
			reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
			reportData += 'Net Ultra Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]) + ',' + 'Avg: ' + filler + ';'

		reportData += ';Revenues;'
		if 1 in PPIDs:
			reportData += 'Lump Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]]) + ',' + filler + ';'
		if 2 in PPIDs:
			reportData += 'Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]]) + ',' + filler + ';'
		if 3 in PPIDs:
			reportData += 'Ultra Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]]) + ',' + filler + ';'
		reportData += 'TOTAL REVENUE,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + filler + ';'

		reportData += ';COSTS;'
		reportData += 'OPEX (millions CAD);'
		reportData += 'Mining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mining]]) + ',' + str(round(sumMining,2)) + ';'
		reportData += 'Stockpile LG Reclaiming,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]]) + ',' + str(round(sumStockpileLG,2)) + ';'
		reportData += 'Pit Dewatering,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]]) + ',' + str(round(sumDewatering,2)) + ';'
		reportData += 'Processing,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in processing]]) + ',' + str(round(sumProcessing,2)) + ';'
		reportData += 'Product Hauling,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]]) + ',' + str(round(sumHauling,2)) + ';'
		reportData += 'Load-out and Rail Loop,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]]) + ',' + str(round(sumLoadOutRailLoop,2)) + ';'
		reportData += 'G&A (Site),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]]) + ',' + str(round(sumGASite,2)) + ';'
		reportData += 'G&A (Room & Board / FIFO),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]]) + ',' + str(round(sumGARoom,2)) + ';'
		reportData += 'Rail Transportation Port and Shiploading,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]]) + ',' + str(round(sumRailTransport,2)) + ';'
		reportData += 'Corporate G&A,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]]) + ',' + str(round(sumGACorp,2)) + ';'
		reportData += 'TOTAL OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
		reportData += 'ROYALTIES (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'

		reportData += 'CAPEX (millions CAD);'
		reportData += 'Pre-Stripping,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]]) + ',' + str(round(sumPreStrip,2)) + ';'
		reportData += 'Mining Equipment Initial,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]]) + ',' + str(round(sumMineEquipInitial,2)) + ';'
		reportData += 'Mining Equipment Sustaining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]]) + ',' + str(round(sumMineEquipSustain,2)) + ';'
		reportData += 'Project Infrastructure Direct Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]]) + ',' + str(round(sumInfraDirectCost,2)) + ';'
		reportData += 'Project Infrastructure Indirect Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]]) + ',' + str(round(sumInfraIndirectCost,2)) + ';'
		reportData += 'Project Infrastructure Contingency,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]]) + ',' + str(round(sumContingency,2)) + ';'
		reportData += 'Railcars,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]]) + ',' + str(round(sumRailcars,2)) + ';'
		reportData += 'Other Mobile Equipment,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]]) + ',' + str(round(sumOtherMobEquip,2)) + ';'
		reportData += 'Closure and Rehab Assurance Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]]) + ',' + str(round(sumClosureRehabAssure,2)) + ';'
		reportData += 'Deposits Provision Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]]) + ',' + str(round(sumDepoProvisionPay,2)) + ';'
		reportData += 'TOTAL CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'

		reportData += 'TAXES (millions CAD);'
		reportData += 'Federal Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]]) + ',' + str(round(sumFederalTaxes,2)) + ';'
		reportData += 'Provincial Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]]) + ',' + str(round(sumProvincialTaxes,2)) + ';'
		reportData += 'Mining Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]]) + ',' + str(round(sumMiningTaxes,2)) + ';'
		reportData += 'TOTAL (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

		reportData += ';SUMMARY;'
		reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + filler + ';'
		reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
		reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
		reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
		reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
		reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
		reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

		reportData += ';PRE-TAX CASH FLOW;'
		reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + filler + ';'
		reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ',' + filler + ';'
		reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + filler + ';'
		for rate in discountRates:
			reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + filler + ';'
		reportData += 'INTERNAL RATE OF RETURN (IRR),' + 'N/A' + ';'

		reportData += ';POST-TAX CASH FLOW;'
		reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + filler + ';'
		reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ',' + filler + ';'
		reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + filler + ';'
		for rate in discountRates:
			reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + filler + ';'
		reportData += 'INTERNAL RATE OF RETURN (IRR),' + 'N/A' + ';'

		# form_class = filterForm(mineID=mineID, reportData=reportData)
		# filter_form = filterForm(mineID=mineID, reportData=reportData)
		filter_form = filterForm(mineID=mineID, startDate=projectStartDate, endDate=projectEndDate)
		default_filter_form = defaultFilterForm(mineID=mineID, thisYearStartDate=thisYearStartDate, thisYearEndDate=thisYearEndDate,
			lastYearStartDate=lastYearStartDate, lastYearEndDate=lastYearEndDate,
			thisQuarterStartDate=thisQuarterStartDate, thisQuarterEndDate=thisQuarterEndDate,
			lastQuarterStartDate=lastQuarterStartDate, lastQuarterEndDate=lastQuarterEndDate)
		report_form = reportForm(mineID=mineID, reportData=reportData)

		return render(request, 'report/report.html', {'filterForm': filter_form, 'reportForm': report_form,
			'defaultFilterForm': default_filter_form,
			'yearVals': yearVals, 'fullYearVals': fullYearVals, 'commIDs': commIDs, 'commNameList': commNameList,
			'numStockpiles': list(range(1, numStockpiles+1)),
			'minePlanTonnageVals': minePlanTonnageVals, 'sumMinePlanTonnages': sumMinePlanTonnages,
			# 'minePlanHGTonnageVals': minePlanHGTonnageVals, 'minePlanLGTonnageVals': minePlanLGTonnageVals,
			# 'minePlanWasteTonnageVals': minePlanWasteTonnageVals, 'minePlanOverburdenTonnageVals': minePlanOverburdenTonnageVals,
			# 'sumMinePlanHGTonnage': sumMinePlanHGTonnage, 'sumMinePlanLGTonnage': sumMinePlanLGTonnage,
			# 'sumMinePlanWasteTonnage': sumMinePlanWasteTonnage, 'sumMinePlanOverburdenTonnage': sumMinePlanOverburdenTonnage,
			'tonnageVals': tonnageVals, 'tonnageTotals': tonnageTotals, 'gradeVals': gradeVals, 'moistures': moistures,
			# 'HGTonnageVals': HGTonnageVals, 'HGTonnageTotal': HGTonnageTotal, 'HGGradeVals': HGGradeVals, 'HGMoistures': HGMoistures,
			# 'LGTonnageVals': LGTonnageVals, 'LGTonnageTotal': LGTonnageTotal, 'LGGradeVals': LGGradeVals, 'LGMoistures': LGMoistures,
			'lumpTonnageVals': lumpTonnageVals, 'lumpTonnageTotal': lumpTonnageTotal, 'lumpGradeVals': lumpGradeVals, 'lumpMoistures': lumpMoistures,
			'finesTonnageVals': finesTonnageVals, 'finesTonnageTotal': finesTonnageTotal, 'finesGradeVals': finesGradeVals, 'finesMoistures': finesMoistures,
			'ultraFinesTonnageVals': ultraFinesTonnageVals, 'ultraFinesTonnageTotal': ultraFinesTonnageTotal, 'ultraFinesGradeVals': ultraFinesGradeVals, 'ultraFinesMoistures': ultraFinesMoistures,
			'totalProducts': totalProducts, 'sumTotalProducts': sumTotalProducts,
			'rejectsTonnageVals': rejectsTonnageVals, 'rejectsTonnageTotal': rejectsTonnageTotal, 'rejectsGradeVals': rejectsGradeVals, 'rejectsMoistures': rejectsMoistures,
			'fullShippingCosts': fullShippingCosts, 'fullExchangeRates': fullExchangeRates,
			'HGLumps': HGLumps, 'lumpPenaltyVals': lumpPenaltyVals, 'lumpSellingPrices': lumpSellingPrices, 'avgLumpSellingPrice': avgLumpSellingPrice,
			'netLumpPrices': netLumpPrices, 'avgNetLumpPrice': avgNetLumpPrice, 'exchangeNetLumpPrices': exchangeNetLumpPrices,
			'avgExchangeNetLumpPrice': avgExchangeNetLumpPrice,
			'HGFines': HGFines, 'finesPenaltyVals': finesPenaltyVals, 'finesSellingPrices': finesSellingPrices, 'avgFinesSellingPrice': avgFinesSellingPrice,
			'netFinesPrices': netFinesPrices, 'avgNetFinesPrice': avgNetFinesPrice, 'exchangeNetFinesPrices': exchangeNetFinesPrices,
			'avgExchangeNetFinesPrice': avgExchangeNetFinesPrice,
			'HGUltraFines': HGUltraFines, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals, 'ultraFinesSellingPrices': ultraFinesSellingPrices,
			'avgUltraFinesSellingPrice': avgUltraFinesSellingPrice,
			'netUltraFinesPrices': netUltraFinesPrices, 'exchangeNetUltraFinesPrices': exchangeNetUltraFinesPrices,
			'avgExchangeNetUltraFinesPrice': avgExchangeNetUltraFinesPrice,
			'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
			'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
			'totalRevenues': totalRevenues, 'sumTotalRevenues': sumTotalRevenues,
			'mining': mining, 'stockpileLG': stockpileLG, 'dewatering': dewatering, 'processing': processing, 'hauling': hauling,
			'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite, 'GARoom': GARoom, 'railTransport': railTransport, 'GACorp': GACorp,
			'sumMining': sumMining, 'sumStockpileLG': sumStockpileLG, 'sumDewatering': sumDewatering, 'sumProcessing': sumProcessing,
			'sumHauling': sumHauling, 'sumLoadOutRailLoop': sumLoadOutRailLoop, 'sumGASite': sumGASite, 'sumGARoom': sumGARoom,
			'sumRailTransport': sumRailTransport, 'sumGACorp': sumGACorp,
			'totalOPEX': totalOPEX, 'sumTotalOPEX':sumTotalOPEX, 'royalties': royalties, 'sumRoyalties': sumRoyalties,
			'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial, 'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
			'infraIndirectCost': infraIndirectCost, 'contingency': contingency, 'railcars': railcars, 'otherMobEquip': otherMobEquip,
			'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay, 'sumPreStrip': sumPreStrip,
			'sumMineEquipInitial': sumMineEquipInitial, 'sumMineEquipSustain': sumMineEquipSustain, 'sumInfraDirectCost': sumInfraDirectCost,
			'sumInfraIndirectCost': sumInfraIndirectCost, 'sumContingency': sumContingency, 'sumRailcars': sumRailcars,
			'sumOtherMobEquip': sumOtherMobEquip, 'sumClosureRehabAssure': sumClosureRehabAssure, 'sumDepoProvisionPay': sumDepoProvisionPay,
			'totalCAPEX': totalCAPEX, 'sumTotalCAPEX': sumTotalCAPEX,
			'federalTaxes': federalTaxes, 'provincialTaxes': provincialTaxes, 'miningTaxes': miningTaxes,
			'sumFederalTaxes': sumFederalTaxes, 'sumProvincialTaxes': sumProvincialTaxes, 'sumMiningTaxes': sumMiningTaxes,
			'totalTaxes': totalTaxes, 'sumTotalTaxes': sumTotalTaxes,
			'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
			'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG,
			'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
			'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
			'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
			'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
			'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
			'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
			'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})

	# for i in range(LOM):
	# 	i += 1
	# 	currRevenue = tblRevenue.objects.filter(mineID=mineID, year=i, plantProductID=PPIDs[0]).order_by('-dateAdded')[0]
	# 	if currRevenue.sellingPrice:
	# 		yearVals.append(i)
		# Check if that year has been calculated. If so, append to yearVals
		# For now, assume every year has been calculated
		# yearVals.append(i)
	totalProducts = [Decimal(0.0)]*len(yearVals)

	tonnageVals = {}
	gradeVals = {}
	tonnageTotals = {}
	moistures = {}
	dailyTonnages = {}
	for curr in range(1, numStockpiles+1):
		gradeVals[curr] = {}
		dailyTonnages[curr] = {}
		currTonnageVals = []
		currGrades = {}
		for year in yearVals:
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			currTonnageEntries = tblMineProductTonnageOptimized.objects.filter(projectID=latestProject.projectID, stockpileID=curr,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate).order_by("date")

			currDailyTonnages = []
			for entry in currTonnageEntries:
				currDailyTonnages.append(entry.tonnage)
			dailyTonnages[curr][year] = currDailyTonnages
			sumTonnage = currTonnageEntries.aggregate(sumTonnage=Sum('tonnage'))
			currTonnageVals.append(sumTonnage['sumTonnage'])
		tonnageVals[curr] = currTonnageVals
		tonnageTotals[curr] = sum(currTonnageVals)

		for i in range(len(commIDs)):
			tempGradesByYear = []
			for year in yearVals:
				currPeriod = projectPeriods.get(year=year)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				currGradeEntries = tblMineProductGradeOptimized.objects.filter(projectID=latestProject.projectID, stockpileID=curr, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate).order_by("date")

				dailyGrades = []
				for entry in currGradeEntries:
					dailyGrades.append(entry.grade)
				# if len(dailyGrades) == 1:
				# 	tempGradesByYear.append(round())
				# else:
				tempGradesByYear.append(round(np.average(dailyGrades, weights=dailyTonnages[curr][year]),2))
			gradeVals[curr][commNameList[i]] = tempGradesByYear

		moistures[curr] = [round(latestInput.feedMoisture,2)]*yearCount

	# Lump data if declared
	if 1 in PPIDs:
		lumpTonnageVals = []
		lumpGradeVals = {}
		lumpDailyTonnages = {}

		for year in yearVals:
			# TO FIX: After Year column has been added to tblMineProductTonnageOptimized
			# lumpTonnageEntry = tblPlantProductTonnage.objects.filter(mineID=mineID, plantProductID=1).order_by('-dateAdded')[0]
			# lumpTonnageVals.append(round(Decimal(lumpTonnageEntry.tonnageDMT),2))
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			lumpTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=1,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

			currDailyTonnages = []
			for entry in lumpTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			lumpDailyTonnages[year] = currDailyTonnages

			sumTonnageDMT = lumpTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			lumpTonnageVals.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		lumpTonnageTotal = sum(lumpTonnageVals)
		totalProducts = [x+y for x,y in zip(totalProducts, lumpTonnageVals)]

		for i in range(len(commIDs)):
		# for ID in commIDs:
			tempGradesByYear = []
			for year in yearVals:
				# TO FIX: After Year column has been added to tblMineProduct
				# lumpEntry = tblPlantProduct.objects.filter(mineID=mineID, plantProductID=1, commodityID=commIDs[i]).order_by('-dateAdded')[0]
				# tempGrades.append(round(lumpEntry.grade,2))
				currPeriod = projectPeriods.get(year=year)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				lumpEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				# avgGrade = lumpEntries.aggregate(avgGrade=Avg('grade'))
				# tempGrades.append(round(avgGrade['avgGrade'],2))
				dailyGrades = []
				for entry in lumpEntries:
					dailyGrades.append(entry.grade)
				tempGradesByYear.append(round(np.average(dailyGrades, weights=lumpDailyTonnages[year]),2))
			lumpGradeVals[commNameList[i]] = tempGradesByYear

		lumpMoistures = [round(latestInput.lumpMoisture,2)]*yearCount

	# Fines data if declared
	if 2 in PPIDs:
		finesTonnageVals = []
		finesGradeVals = {}
		finesDailyTonnages = {}

		for year in yearVals:
			# TO FIX: After Year column has been added to tblMineProductTonnageOptimized
			# finesTonnageEntry = tblPlantProductTonnage.objects.filter(mineID=mineID, plantProductID=2).order_by('-dateAdded')[0]
			# finesTonnageVals.append(round(Decimal(finesTonnageEntry.tonnageDMT),2))
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			finesTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=2,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

			currDailyTonnages = []
			for entry in finesTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			finesDailyTonnages[year] = currDailyTonnages

			sumTonnageDMT = finesTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			finesTonnageVals.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		finesTonnageTotal = sum(finesTonnageVals)
		totalProducts = [x+y for x,y in zip(totalProducts, finesTonnageVals)]

		for i in range(len(commIDs)):
		# for ID in commIDs:
			tempGradesByYear = []
			for year in yearVals:
				# TO FIX: After Year column has been added to tblMineProduct
				# finesEntry = tblPlantProduct.objects.filter(mineID=mineID, plantProductID=2, commodityID=commIDs[i]).order_by('-dateAdded')[0]
				# tempGrades.append(round(finesEntry.grade,2))
				currPeriod = projectPeriods.get(year=year)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				finesEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				# avgGrade = finesEntries.aggregate(avgGrade=Avg('grade'))
				# tempGrades.append(round(avgGrade['avgGrade'],2))

				dailyGrades = []
				for entry in finesEntries:
					dailyGrades.append(entry.grade)
				tempGradesByYear.append(round(np.average(dailyGrades, weights=finesDailyTonnages[year]),2))
			finesGradeVals[commNameList[i]] = tempGradesByYear

		finesMoistures = [round(latestInput.finesMoisture,2)]*yearCount

	# Ultra Fines data if declared
	if 3 in PPIDs:
		ultraFinesTonnageVals = []
		ultraFinesGradeVals = {}
		ultraFinesDailyTonnages = {}

		for year in yearVals:
			# TO FIX: After Year column has been added to tblMineProductTonnageOptimized
			# ultraFinesTonnageEntry = tblPlantProductTonnage.objects.filter(mineID=mineID, plantProductID=3).order_by('-dateAdded')[0]
			# ultraFinesTonnageVals.append(round(Decimal(ultraFinesTonnageEntry.tonnageDMT),2))
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			ultraFinesTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=3,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

			currDailyTonnages = []
			for entry in ultraFinesTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			ultraFinesDailyTonnages[year] = currDailyTonnages

			sumTonnageDMT = ultraFinesTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			ultraFinesTonnageVals.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		ultraFinesTonnageTotal = sum(ultraFinesTonnageVals)
		totalProducts = [x+y for x,y in zip(totalProducts, ultraFinesTonnageVals)]

		for i in range(len(commIDs)):
		# for ID in commIDs:
			tempGradesByYear = []
			for year in yearVals:
				# TO FIX: After Year column has been added to tblMineProduct
				# ultraFinesEntry = tblPlantProduct.objects.filter(mineID=mineID, plantProductID=3, commodityID=commIDs[i]).order_by('-dateAdded')[0]
				# tempGrades.append(round(ultraFinesEntry.grade,2))
				# testVal = MPEntry.grade
				currPeriod = projectPeriods.get(year=year)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				ultraFinesEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				# avgGrade = ultraFinesEntries.aggregate(avgGrade=Avg('grade'))
				# tempGrades.append(round(avgGrade['avgGrade'],2))

				dailyGrades = []
				for entry in ultraFinesEntries:
					dailyGrades.append(entry.grade)
				tempGradesByYear.append(round(np.average(dailyGrades, weights=ultraFinesDailyTonnages[year]),2))
			ultraFinesGradeVals[commNameList[i]] = tempGradesByYear

		ultraFinesMoistures = [round(latestInput.ultraFinesMoisture,2)]*yearCount
	
	sumTotalProducts = sum(totalProducts)

	# Rejects data if declared
	if 4 in PPIDs:
		rejectsTonnageVals = []
		rejectsGradeVals = {}

		for year in yearVals:
			# TO FIX: After Year column has been added to tblMineProductTonnageOptimized
			# rejectsTonnageEntry = tblPlantProductTonnage.objects.filter(mineID=mineID, plantProductID=4).order_by('-dateAdded')[0]
			# rejectsTonnageVals.append(rejectsTonnageEntry.tonnageDMT)
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			rejectsTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=4,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
			sumTonnageDMT = rejectsTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			rejectsTonnageVals.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		rejectsTonnageTotal = sum(rejectsTonnageVals)

		for i in range(len(commIDs)):
		# for ID in commIDs:
			tempGrades = []
			for year in yearVals:
				# TO FIX: After Year column has been added to tblMineProduct
				# rejectsEntry = tblPlantProduct.objects.filter(mineID=mineID, plantProductID=4, commodityID=commIDs[i]).order_by('-dateAdded')[0]
				# tempGrades.append(round(rejectsEntry.grade,2))
				currPeriod = projectPeriods.get(year=year)				
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				rejectsEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=4, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				avgGrade = rejectsEntries.aggregate(avgGrade=Avg('grade'))
				tempGrades.append(round(avgGrade['avgGrade'],2))
			rejectsGradeVals[commNameList[i]] = tempGrades

		rejectsMoistures = [round(latestInput.rejectsMoisture,2)]*yearCount

	# # Handle Products Selling Price section
	# priceEntry = tblPrice.objects.filter(mineID=mineID).order_by('-dateAdded')[0]

	# # Handle OPEX Shipping Cost by Year
	# shippingCosts = []
	# for year in yearVals:
	# 	currOPEX = tblOPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
	# 	shippingCosts.append(round(Decimal(currOPEX.shipping),2))

	# # Obtain Exchange Rate
	# exchangeRates = [round(Decimal(latestInput.exchangeRate),2)]*len(yearVals)
	# xRate = round(Decimal(latestInput.exchangeRate),2)

	if 1 in PPIDs:
		HGLumps = [round(Decimal(priceEntry.lump),2)]*len(yearVals)
		lumpPenaltyVals = {}
		penaltiesByYear = []
		for i in range(len(commIDs)):
			tempPenalties = []
			for year in yearVals:
				# TO FIX: After Year column has been added to tblSmelterTermsOptimized
				# penaltyEntry = tblSmelterTermsOptimized.objects.filter(mineID=mineID, commodityID=commIDs[i], plantProductID=1).order_by('-dateAdded')[0]
				currPeriod = projectPeriods.get(year=year)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				# sumPenalty = penaltyEntries.aggregate(sumPenalty=Sum('penalty'))
				# tempPenalties.append(round(Decimal(sumPenalty['sumPenalty']),2))
				# tempPenalties.append(round(Decimal(penaltyEntry.penalty),2))

				dailyPens = []
				for entry in penaltyEntries:
					dailyPens.append(entry.penalty)
				tempPenalties.append(round(Decimal(np.average(dailyPens, weights=lumpDailyTonnages[year])),2))

			lumpPenaltyVals[commNameList[i]] = tempPenalties
			penaltiesByYear.append(tempPenalties)

		sumPenalties = [sum(x) for x in zip(*penaltiesByYear)]
		lumpSellingPrices = list(map(operator.sub, HGLumps, sumPenalties))
		avgLumpSellingPrice = round(sum(lumpSellingPrices) / len(lumpSellingPrices), 2)
		netLumpPrices = list(map(operator.sub, lumpSellingPrices, shippingCosts))
		avgNetLumpPrice = round(sum(netLumpPrices) / len(netLumpPrices), 2)
		# exchangeNetLumpPrices = [round(x*exchangeRate,2) for x in netLumpPrices]
		exchangeNetLumpPrices = list(map(operator.mul, exchangeRates, netLumpPrices))
		exchangeNetLumpPrices = [round(x,2) for x in exchangeNetLumpPrices]
		avgExchangeNetLumpPrice = round(avgNetLumpPrice*exchangeRates[0], 2)

	if 2 in PPIDs:
		HGFines = [round(Decimal(priceEntry.fines),2)]*len(yearVals)
		finesPenaltyVals = {}
		finesPenaltiesByYear = []
		for i in range(len(commIDs)):
			tempPenalties = []
			for year in yearVals:
				# TO FIX: After Year column has been added to tblSmelterTermsOptimized
				# penaltyEntry = tblSmelterTermsOptimized.objects.filter(mineID=mineID, commodityID=commIDs[i], plantProductID=2).order_by('-dateAdded')[0]
				# tempPenalties.append(round(Decimal(penaltyEntry.penalty),2))
				currPeriod = projectPeriods.get(year=year)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				sumPenalty = penaltyEntries.aggregate(sumPenalty=Sum('penalty'))
				tempPenalties.append(round(Decimal(sumPenalty['sumPenalty']),2))
			finesPenaltyVals[commNameList[i]] = tempPenalties
			finesPenaltiesByYear.append(tempPenalties)

		sumPenalties = [sum(x) for x in zip(*finesPenaltiesByYear)]
		finesSellingPrices = list(map(operator.sub, HGFines, sumPenalties))
		avgFinesSellingPrice = round(sum(finesSellingPrices) / len(finesSellingPrices), 2)
		netFinesPrices = list(map(operator.sub, finesSellingPrices, shippingCosts))
		avgNetFinesPrice = round(sum(netFinesPrices) / len(netFinesPrices), 2)
		# exchangeNetFinesPrices = [round(x*exchangeRate,2) for x in netFinesPrices]
		exchangeNetFinesPrices = list(map(operator.mul, exchangeRates, netFinesPrices))
		exchangeNetFinesPrices = [round(x,2) for x in exchangeNetFinesPrices]
		avgExchangeNetFinesPrice = round(avgNetFinesPrice*exchangeRates[0], 2)

	if 3 in PPIDs:
		HGUltraFines = [round(Decimal(priceEntry.ultraFines),2)]*len(yearVals)
		ultraFinesPenaltyVals = {}
		ultraFinesPenaltiesByYear = []
		for i in range(len(commIDs)):
			tempPenalties = []
			for year in yearVals:
				# TO FIX: After Year column has been added to tblSmelterTermsOptimized
				# penaltyEntry = tblSmelterTermsOptimized.objects.filter(mineID=mineID, commodityID=commIDs[i], plantProductID=3).order_by('-dateAdded')[0]
				# tempPenalties.append(round(Decimal(penaltyEntry.penalty),2))
				currPeriod = projectPeriods.get(year=year)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				sumPenalty = penaltyEntries.aggregate(sumPenalty=Sum('penalty'))
				tempPenalties.append(round(Decimal(sumPenalty['sumPenalty']),2))
			ultraFinesPenaltyVals[commNameList[i]] = tempPenalties
			ultraFinesPenaltiesByYear.append(tempPenalties)

		sumPenalties = [sum(x) for x in zip(*ultraFinesPenaltiesByYear)]
		ultraFinesSellingPrices = list(map(operator.sub, HGUltraFines, sumPenalties))
		avgUltraFinesSellingPrice = round(sum(ultraFinesSellingPrices) / len(ultraFinesSellingPrices), 2)
		netUltraFinesPrices = list(map(operator.sub, ultraFinesSellingPrices, shippingCosts))
		avgNetUltraFinesPrice = round(sum(netUltraFinesPrices) / len(netUltraFinesPrices), 2)
		# exchangeNetUltraFinesPrices = [round(x*exchangeRate,2) for x in netUltraFinesPrices]
		exchangeNetUltraFinesPrices = list(map(operator.mul, exchangeRates, netUltraFinesPrices))
		exchangeNetUltraFinesPrices = [round(x,2) for x in exchangeNetUltraFinesPrices]
		avgExchangeNetUltraFinesPrice = round(avgNetUltraFinesPrice*exchangeRates[0], 2)


	# Handle Revenues Section
	if 1 in PPIDs:
		lumpRevenues = []
		sumLumpRevenues = 0
		for year in yearVals:
			# revenueEntry = tblRevenue.objects.filter(mineID=mineID, year=year, plantProductID=1).order_by('-dateAdded')[0]
			# currRevenue = round(Decimal(revenueEntry.plantProductRevenue),2)
			# lumpRevenues.append(currRevenue)
			# sumLumpRevenues += currRevenue
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=1,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
			sumPPRevenue = revenueEntries.aggregate(sumPPRevenue=Sum('plantProductRevenue'))
			currRevenue = round(Decimal(sumPPRevenue['sumPPRevenue']),2)
			lumpRevenues.append(currRevenue)
			sumLumpRevenues += currRevenue

		totalRevenues = list(map(operator.add, totalRevenues, lumpRevenues))
		lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, lumpRevenues))

	if 2 in PPIDs:
		finesRevenues = []
		sumFinesRevenues = 0
		for year in yearVals:
			# revenueEntry = tblRevenue.objects.filter(mineID=mineID, year=year, plantProductID=2).order_by('-dateAdded')[0]
			# currRevenue = round(Decimal(revenueEntry.plantProductRevenue),2)
			# finesRevenues.append(currRevenue)
			# sumFinesRevenues += currRevenue
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=2,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
			sumPPRevenue = revenueEntries.aggregate(sumPPRevenue=Sum('plantProductRevenue'))
			currRevenue = round(Decimal(sumPPRevenue['sumPPRevenue']),2)
			finesRevenues.append(currRevenue)
			sumFinesRevenues += currRevenue
		totalRevenues = list(map(operator.add, totalRevenues, finesRevenues))
		lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, finesRevenues))

	if 3 in PPIDs:
		ultraFinesRevenues = []
		sumUltraFinesRevenues = 0
		for year in yearVals:
			# revenueEntry = tblRevenue.objects.filter(mineID=mineID, year=year, plantProductID=3).order_by('-dateAdded')[0]
			# currRevenue = round(Decimal(revenueEntry.plantProductRevenue),2)
			# ultraFinesRevenues.append(currRevenue)
			# sumUltraFinesRevenues += currRevenue
			currPeriod = projectPeriods.get(year=year)
			# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=3,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
			sumPPRevenue = revenueEntries.aggregate(sumPPRevenue=Sum('plantProductRevenue'))
			currRevenue = round(Decimal(sumPPRevenue['sumPPRevenue']),2)
			ultraFinesRevenues.append(currRevenue)
			sumUltraFinesRevenues += currRevenue
		totalRevenues = list(map(operator.add, totalRevenues, ultraFinesRevenues))

	sumTotalRevenues = sum(totalRevenues)

	# Find first not processed entry
	notProcessed = tblCashFlow.objects.filter(projectID=latestProject.projectID, processed=False).order_by('date')
	if notProcessed:
		toProcess = notProcessed[0]

		# Build annual CAPEX+OPEX+Taxes values here (Pro-rationed daily)
		totalCAPEXOPEX = [sum(x) for x in zip(cashFlowCAPEX, cashFlowOPEX)]
		totalCAPEXOPEXTaxes = [sum(x) for x in zip(totalCAPEXOPEX, totalTaxes)]
		dailyTotalCAPEXOPEX = [x/Decimal(366.0) if calendar.isleap(y) else x/Decimal(365.0) for x,y in zip(totalCAPEXOPEX, fullYears)]
		dailyTotalCAPEXOPEXTaxes = [x/Decimal(366.0) if calendar.isleap(y) else x/Decimal(365.0) for x,y in zip(totalCAPEXOPEXTaxes, fullYears)]

		if projectStartDate.month != 1 or projectStartDate.day != 1:
			tempEnd = datetime.date(projectStartDate.year, 12, 31)
			dailyTotalCAPEXOPEX[0] = totalCAPEXOPEX[0]/Decimal((tempEnd - projectStartDate).days)
			dailyTotalCAPEXOPEXTaxes[0] = totalCAPEXOPEXTaxes[0]/Decimal((tempEnd - projectStartDate).days)

		earlyEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__lt=toProcess.date).order_by('-date')
		if earlyEntries:
			lastCashFlowEntry = earlyEntries[0]
			currCumCashFlowPreTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPreTax)
			currCumCashFlowPostTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPostTax)
		else:
			# If there are no earlier entries, then initialize with negative CAPEX values
			currCumCashFlowPreTax = (-1)*sumNegCAPEX
			currCumCashFlowPostTax = (-1)*sumNegCAPEX

		toUpdate = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=toProcess.date).order_by('date')
		toUpdateRevenue = tblRevenue.objects.filter(projectID=latestProject.projectID, date__gte=toProcess.date).order_by('date')
		toUpdateFinancials = tblFinancials.objects.filter(projectID=latestProject.projectID, date__gte=toProcess.date).order_by('date')

		if earlyEntries:
			lastDate = earlyEntries[0].date
		else:
			lastDate = projectStartDate			
		for entry in toUpdate:
			currLumpPlusFines = Decimal(0.0)
			if 1 in PPIDs:
				currRev = toUpdateRevenue.get(plantProductID=1, date=entry.date)
				currLumpPlusFines += Decimal(currRev.plantProductRevenue)
			if 2 in PPIDs:
				currRev = toUpdateRevenue.get(plantProductID=2, date=entry.date)
				currLumpPlusFines += Decimal(currRev.plantProductRevenue)

			if lastDate.year == entry.date.year:
				multiplier = (entry.date - lastDate).days
				entry.cashFlowPreTax = currDailyCashFlowPreTax = currLumpPlusFines - dailyTotalCAPEXOPEX[entry.date.year - projectStartDate.year]*multiplier
				entry.cashFlowPostTax = currDailyCashFlowPostTax = currLumpPlusFines - dailyTotalCAPEXOPEXTaxes[entry.date.year - projectStartDate.year]*multiplier
			else:
				multiplier1 = (datetime.date(lastDate.year, 12, 31) - lastDate).days
				multiplier2 = (entry.date - datetime.date(entry.date.year, 1, 1)).days
				entry.cashFlowPreTax = currDailyCashFlowPreTax = currLumpPlusFines - dailyTotalCAPEXOPEX[lastDate.year - projectStartDate.year]*multiplier1 - dailyTotalCAPEXOPEX[entry.date.year - projectStartDate.year]*multiplier2
				entry.cashFlowPostTax = currDailyCashFlowPostTax = currLumpPlusFines - dailyTotalCAPEXOPEXTaxes[lastDate.year - projectStartDate.year]*multiplier1 - dailyTotalCAPEXOPEXTaxes[entry.date.year - projectStartDate.year]*multiplier2

			lastDate = entry.date

			currCumCashFlowPreTax += currDailyCashFlowPreTax
			currCumCashFlowPostTax += currDailyCashFlowPostTax
			entry.cumulativeCashFlowPreTax = currCumCashFlowPreTax
			entry.cumulativeCashFlowPostTax = currCumCashFlowPostTax
			entry.processed = True
			entry.save()
			
			# After updating Cash Flow data for the day, update the Financials data for the day as well.
			toUpdateFinancials.filter(date=entry.date).delete()
			# tblFinancials.objects.filter(projectID=latestProject.projectID, date=entry.date).delete()
			discountRates = [Decimal(0.06), Decimal(0.08), Decimal(0.10), Decimal(0.12), Decimal(0.15), Decimal(0.20)]
			currTime = timezone.localtime(timezone.now())
			for rate in discountRates:
				currPeriod = projectPeriods.get(startDate__lte=entry.date, endDate__gte=entry.date)
				# currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, startDate__lte=entry.date,
				# 	endDate__gte=entry.date)
				currNPVPreTax = round(entry.cashFlowPreTax / Decimal(pow((1+rate),currPeriod.year)),2)
				currNPVPostTax = round(entry.cashFlowPostTax / Decimal(pow((1+rate),currPeriod.year)),2)
				financialsEntry = tblFinancials(projectID=latestProject, mineID=mineMatch, date=entry.date,
					discountRate=int(round(rate*100)), NPVPreTax=currNPVPreTax, NPVPostTax=currNPVPostTax, IRRPreTax=None, IRRPostTax=None, dateAdded=currTime)
				financialsEntry.save()

	# # tblCashFlow and tblFinancials Data Processing (VERSION 2)
	# # No Pro-ration of Costs
	# # Annual Costs and Expenses charged on the last calculated day of the corresponding year
	# notProcessed = tblCashFlow.objects.filter(projectID=latestProject.projectID, processed=False).order_by('date')
	# if notProcessed:
	# 	toProcess = notProcessed[0]

	# 	# Form dictionaries of annual OPEX+CAPEX and Taxes
	# 	annualOPEXPlusCAPEX = {}
	# 	annualTaxes = {}

	# 	latestOPEX = tblOPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
	# 	latestCAPEX = tblCAPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
	# 	latestTaxes = tblTaxes.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
	# 	OPEXEntries = tblOPEX.objects.filter(mineID=mineID, dateAdded=latestOPEX.dateAdded).order_by('year')
	# 	CAPEXEntries = tblCAPEX.objects.filter(mineID=mineID, dateAdded=latestCAPEX.dateAdded).order_by('year')
	# 	taxesEntries = tblTaxes.objects.filter(mineID=mineID, dateAdded=latestTaxes.dateAdded).order_by('year')
	# 	for i in range(len(OPEXEntries)):
	# 		OPEXrow = OPEXEntries[i]
	# 		CAPEXrow = CAPEXEntries[i]
	# 		taxesRow = taxesEntries[i]
	# 		currOPEX = (OPEXrow.mining+OPEXrow.infrastructure+OPEXrow.stockpileLG+OPEXrow.dewatering+OPEXrow.processing+
	# 			OPEXrow.hauling+OPEXrow.loadOutRailLoop+OPEXrow.GASite+OPEXrow.GARoomBoardFIFO+OPEXrow.railTransport+OPEXrow.GACorp+
	# 			OPEXrow.royalties+OPEXrow.transportation+OPEXrow.GA)
	# 		currCAPEX = (CAPEXrow.preStrip+CAPEXrow.mineEquipInitial+CAPEXrow.mineEquipSustain+CAPEXrow.infraDirectCost+
	# 			CAPEXrow.infraIndirectCost+CAPEXrow.contingency+CAPEXrow.railcars+CAPEXrow.otherMobEquip+CAPEXrow.closureRehabAssure+
	# 			CAPEXrow.depoProvisionPay+CAPEXrow.workCapCurrentProd+CAPEXrow.workCapCostsLG+CAPEXrow.EPCM+CAPEXrow.ownerCost)
	# 		currOPEXPlusCAPEX = round((Decimal(currCAPEX) + Decimal(currOPEX)),2)
	# 		currTaxes = round(Decimal(taxesRow.federal + taxesRow.provincial + taxesRow.mining),2)

	# 		annualOPEXPlusCAPEX[i+1] = currOPEXPlusCAPEX
	# 		annualTaxes[i+1] = currTaxes

	# 	projectPeriods = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).order_by('year')
	# 	toProcessPeriod = projectPeriods.filter(startDate__lte=toProcess.date, endDate__gte=toProcess.date)[0]
	# 	toProcessYears = yearVals[yearVals.index(toProcessPeriod.year):]

	# 	earlyEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__lt=toProcess.date).order_by('-date')
	# 	if earlyEntries:
	# 		lastCashFlowEntry = earlyEntries[0]
	# 		currCumCashFlowPreTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPreTax)
	# 		currCumCashFlowPostTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPostTax)
	# 	else:
	# 		currCumCashFlowPreTax = Decimal(0.0)
	# 		currCumCashFlowPostTax = Decimal(0.0)

	# 	for year in toProcessYears:
	# 		currPeriod = projectPeriods.filter(year=year)[0]
	# 		if year == toProcessPeriod.year:
	# 			toUpdate = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=toProcess.date, 
	# 				date__lte=currPeriod.endDate).order_by('date')
	# 		else:
	# 			toUpdate = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=currPeriod.startDate, 
	# 				date__lte=currPeriod.endDate).order_by('date')

			
	# 		for i in range(len(toUpdate)):
	# 			currLumpPlusFines = Decimal(0.0)
	# 			if 1 in PPIDs:
	# 				currRev = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=1, date=toUpdate[i].date)
	# 				currLumpPlusFines += Decimal(currRev.plantProductRevenue)
	# 			if 2 in PPIDs:
	# 				currRev = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=2, date=toUpdate[i].date)
	# 				currLumpPlusFines += Decimal(currRev.plantProductRevenue)

	# 			if i != (len(toUpdate)-1):
	# 				toUpdate[i].cashFlowPreTax = currDailyCashFlowPreTax = currLumpPlusFines
	# 				toUpdate[i].cashFlowPostTax = currDailyCashFlowPostTax = currLumpPlusFines
	# 			else:
	# 				toUpdate[i].cashFlowPreTax = currDailyCashFlowPreTax = currLumpPlusFines - annualOPEXPlusCAPEX[currPeriod.year]
	# 				toUpdate[i].cashFlowPostTax = currDailyCashFlowPostTax = currDailyCashFlowPreTax - annualTaxes[currPeriod.year]

	# 			currCumCashFlowPreTax += currDailyCashFlowPreTax
	# 			currCumCashFlowPostTax += currDailyCashFlowPostTax
	# 			toUpdate[i].cumulativeCashFlowPreTax = currCumCashFlowPreTax
	# 			toUpdate[i].cumulativeCashFlowPostTax = currCumCashFlowPostTax
	# 			toUpdate[i].processed = True
	# 			toUpdate[i].save()

	# 			# After updating Cash Flow data for the day, update the Financials data for the day as well.
	# 			tblFinancials.objects.filter(projectID=latestProject.projectID, date=toUpdate[i].date).delete()
	# 			discountRates = [Decimal(0.06), Decimal(0.08), Decimal(0.10), Decimal(0.12), Decimal(0.15), Decimal(0.20)]
	# 			currTime = timezone.localtime(timezone.now())
	# 			for rate in discountRates:
	# 				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, startDate__lte=toUpdate[i].date,
	# 					endDate__gte=toUpdate[i].date)
	# 				currNPVPreTax = round(toUpdate[i].cashFlowPreTax / Decimal(pow((1+rate),currPeriod.year)),2)
	# 				currNPVPostTax = round(toUpdate[i].cashFlowPostTax / Decimal(pow((1+rate),currPeriod.year)),2)
	# 				financialsEntry = tblFinancials(projectID=latestProject, mineID=mineMatch, date=toUpdate[i].date,
	# 					discountRate=int(round(rate*100)), NPVPreTax=currNPVPreTax, NPVPostTax=currNPVPostTax, IRRPreTax=None, IRRPostTax=None, dateAdded=currTime)
	# 				financialsEntry.save()


	cashFlowPreTax = []
	cashFlowPostTax = []
	cumCashFlowPreTax = []
	cumCashFlowPostTax = []
	# Beginning populating tblCashFlow data for HTML report here
	currCumCashFlowPreTax = (-1)*sumNegCAPEX
	currCumCashFlowPostTax = (-1)*sumNegCAPEX

	# currCumCashFlowPreTax = Decimal(0.0)
	# currCumCashFlowPostTax = Decimal(0.0)
	cashFlowEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID)
	for year in yearVals:
		currPeriod = projectPeriods.get(year=year)
		currStart = currPeriod.startDate
		currEnd = currPeriod.endDate
		currCashFlows = cashFlowEntries.filter(date__gte=currStart, date__lte=currEnd).order_by('-date')
		if not currCashFlows:
			cumCashFlowPreTax.append(currCumCashFlowPreTax)
			cumCashFlowPostTax.append(currCumCashFlowPostTax)
			cashFlowPreTax.append(Decimal(0.0))
			cashFlowPostTax.append(Decimal(0.0))
		else:
			lastCashFlow = currCashFlows[0]
			cumCashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax),2))
			cumCashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax),2))
			cashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax) - currCumCashFlowPreTax,2))
			cashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax) - currCumCashFlowPostTax,2))
			currCumCashFlowPreTax = cumCashFlowPreTax[-1]
			currCumCashFlowPostTax = cumCashFlowPostTax[-1]
	sumCashFlowPreTax = sum(cashFlowPreTax)
	sumCashFlowPostTax = sum(cashFlowPostTax)

	# New: Append extra values for blank years here
	if len(yearVals) != yearCount:
		cashFlowPreTax = padList(yearVals, yearCount, cashFlowPreTax, Decimal(0.0))
		cashFlowPostTax = padList(yearVals, yearCount, cashFlowPostTax, Decimal(0.0))

		for i in range(1, yearCount+1):
			if i not in yearVals:
				cumCashFlowPreTax.insert(i-1, (-1)*sumNegCAPEX if i==1 else cumCashFlowPreTax[i-2])
				cumCashFlowPostTax.insert(i-1, (-1)*sumNegCAPEX if i==1 else cumCashFlowPostTax[i-2])

		# preTaxNPVs = padList(yearVals, yearCount, preTaxNPVs, filler)
		# postTaxNPVs = padList(yearVals, yearCount, postTaxNPVs, filler)

		# for rate in discountRates:
		# 	rate = int(round(rate*100))
		# 	preTaxPVs[rate] = padList(yearVals, yearCount, preTaxPVs[rate], filler)
		# 	postTaxPVs[rate] = padList(yearVals, yearCount, postTaxPVs[rate], filler)

	positiveFlow = False
	paybackPreTax = []
	for i in range(len(cumCashFlowPreTax)):
		if positiveFlow:
			paybackPreTax.append(Decimal(0.0))
		else:
			if cumCashFlowPreTax[i] > 0:
				if i == 0:
					paybackPreTax.append(Decimal(0.0))
				else:
					paybackPreTax.append(abs(round(cumCashFlowPreTax[i-1] / cashFlowPreTax[i],4)))
				positiveFlow = True
			else:
				paybackPreTax.append(Decimal(1.0))
	sumPaybackPreTax = sum(paybackPreTax)

	positiveFlow = False
	paybackPostTax = []
	for i in range(len(cumCashFlowPostTax)):
		if positiveFlow:
			paybackPostTax.append(Decimal(0.0))
		else:
			if cumCashFlowPostTax[i] > 0:
				if i == 0:
					paybackPostTax.append(Decimal(0.0))
				else:
					paybackPostTax.append(abs(round(cumCashFlowPostTax[i-1] / cashFlowPostTax[i],4)))
				positiveFlow = True
			else:
				paybackPostTax.append(Decimal(1.0))
	sumPaybackPostTax = sum(paybackPostTax)

	# Calculate and Update NPVs and IRRs
	preTaxNPVs = []
	postTaxNPVs = []
	NPVCashFlowPreTax = [(-1)*sumNegCAPEX] + cashFlowPreTax
	NPVCashFlowPostTax = [(-1)*sumNegCAPEX] + cashFlowPostTax
	preTaxIRR = round(np.irr(NPVCashFlowPreTax)*100,2)
	postTaxIRR = round(np.irr(NPVCashFlowPostTax)*100,2)
	for rate in discountRates:
		preTaxNPVs.append(round(np.npv(rate, NPVCashFlowPreTax),2))
		postTaxNPVs.append(round(np.npv(rate, NPVCashFlowPostTax),2))
		# preTaxIRRs.append(round(np.irr(cashFlowPreTax),4))
		# postTaxIRRs.append(round(np.irr(cashFlowPostTax),4))

	preTaxPVs = {}
	postTaxPVs = {}
	sumPreTaxNPV = {}
	sumPostTaxNPV = {}
	financialsEntries = tblFinancials.objects.filter(projectID=latestProject.projectID)
	for rate in discountRates:
		rate = int(round(rate*100))
		preTaxPVs[rate] = []
		postTaxPVs[rate] = []
		for year in yearVals:
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			currStart = currPeriod.startDate
			currEnd = currPeriod.endDate
			currPVs = financialsEntries.filter(discountRate=rate,
				date__lte=currEnd, date__gte=currStart)
			sumPVPreTax = currPVs.aggregate(sumPVPreTax=Sum('NPVPreTax'))
			sumPVPostTax = currPVs.aggregate(sumPVPostTax=Sum('NPVPostTax'))
			preTaxPVs[rate].append(round(sumPVPreTax['sumPVPreTax'],2))
			postTaxPVs[rate].append(round(sumPVPostTax['sumPVPostTax'],2))
		sumPreTaxNPV[rate] = sum(preTaxPVs[rate])
		sumPostTaxNPV[rate] = sum(postTaxPVs[rate])


	if len(yearVals) != yearCount:
		filler = ""
		totalProducts = padList(yearVals, yearCount, totalProducts, filler)

		for curr in range(1, numStockpiles+1):
			tonnageVals[curr] = padList(yearVals, yearCount, tonnageVals[curr], filler)
			for i in range(len(commIDs)):
				gradeVals[curr][commNameList[i]] = padList(yearVals, yearCount, gradeVals[curr][commNameList[i]], filler)

		# if 1 in MPIDs:
		# 	HGTonnageVals = padList(yearVals, yearCount, HGTonnageVals, 'N/A')
		# 	for i in range(len(commIDs)):
		# 		HGGradeVals[commNameList[i]] = padList(yearVals, yearCount, HGGradeVals[commNameList[i]], 'N/A')

		# if 2 in MPIDs:
		# 	LGTonnageVals = padList(yearVals, yearCount, LGTonnageVals, 'N/A')
		# 	for i in range(len(commIDs)):
		# 		LGGradeVals[commNameList[i]] = padList(yearVals, yearCount, LGGradeVals[commNameList[i]], 'N/A')

		if 1 in PPIDs:
			lumpTonnageVals = padList(yearVals, yearCount, lumpTonnageVals, filler)
			for i in range(len(commIDs)):
				lumpGradeVals[commNameList[i]] = padList(yearVals, yearCount, lumpGradeVals[commNameList[i]], filler)

			HGLumps = [round(Decimal(priceEntry.lump),2)]*yearCount
			for i in range(len(commIDs)):
				lumpPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, lumpPenaltyVals[commNameList[i]], filler)
			lumpSellingPrices = padList(yearVals, yearCount, lumpSellingPrices, filler)
			netLumpPrices = padList(yearVals, yearCount, netLumpPrices, filler)
			exchangeNetLumpPrices = padList(yearVals, yearCount, exchangeNetLumpPrices, filler)

			lumpRevenues = padList(yearVals, yearCount, lumpRevenues, filler)

		if 2 in PPIDs:
			finesTonnageVals = padList(yearVals, yearCount, finesTonnageVals, filler)
			for i in range(len(commIDs)):
				finesGradeVals[commNameList[i]] = padList(yearVals, yearCount, finesGradeVals[commNameList[i]], filler)

			HGFines = [round(Decimal(priceEntry.fines),2)]*yearCount
			for i in range(len(commIDs)):
				finesPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, finesPenaltyVals[commNameList[i]], filler)
			finesSellingPrices = padList(yearVals, yearCount, finesSellingPrices, filler)
			netFinesPrices = padList(yearVals, yearCount, netFinesPrices, filler)
			exchangeNetFinesPrices = padList(yearVals, yearCount, exchangeNetFinesPrices, filler)

			finesRevenues = padList(yearVals, yearCount, finesRevenues, filler)

		if 3 in PPIDs:
			ultraFinesTonnageVals = padList(yearVals, yearCount, ultraFinesTonnageVals, filler)
			for i in range(len(commIDs)):
				ultraFinesGradeVals[commNameList[i]] = padList(yearVals, yearCount, ultraFinesGradeVals[commNameList[i]], filler)

			HGUltraFines = [round(Decimal(priceEntry.ultraFines),2)]*yearCount
			for i in range(len(commIDs)):
				ultraFinesPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, ultraFinesPenaltyVals[commNameList[i]], filler)
			ultraFinesSellingPrices = padList(yearVals, yearCount, ultraFinesSellingPrices, filler)
			netUltraFinesPrices = padList(yearVals, yearCount, netUltraFinesPrices, filler)
			exchangeNetUltraFinesPrices = padList(yearVals, yearCount, exchangeNetUltraFinesPrices, filler)

			ultraFinesRevenues = padList(yearVals, yearCount, ultraFinesRevenues, filler)

		if 4 in PPIDs:
			rejectsTonnageVals = padList(yearVals, yearCount, [], filler)
			for i in range(len(commIDs)):
				rejectsGradeVals[commNameList[i]] = padList(yearVals, yearCount, rejectsGradeVals[commNameList[i]], filler)
		
		totalRevenues = padList(yearVals, yearCount, totalRevenues, filler)

		# cashFlowPreTax = padList(yearVals, yearCount, cashFlowPreTax, filler)
		# cashFlowPostTax = padList(yearVals, yearCount, cashFlowPostTax, filler)
		# cumCashFlowPreTax = padList(yearVals, yearCount, cumCashFlowPreTax, filler)
		# cumCashFlowPostTax = padList(yearVals, yearCount, cumCashFlowPostTax, filler)
		# paybackPreTax = padList(yearVals, yearCount, paybackPreTax, filler)
		# paybackPostTax = padList(yearVals, yearCount, paybackPostTax, filler)
		preTaxNPVs = padList(yearVals, yearCount, preTaxNPVs, filler)
		postTaxNPVs = padList(yearVals, yearCount, postTaxNPVs, filler)

		for rate in discountRates:
			rate = int(round(rate*100))
			preTaxPVs[rate] = padList(yearVals, yearCount, preTaxPVs[rate], filler)
			postTaxPVs[rate] = padList(yearVals, yearCount, postTaxPVs[rate], filler)

	# Create DL Form Data
	reportRowCount = 1

	reportData = ""

	currRow = 'Item,'
	for year in range(1, yearCount+1):
		currRow += 'Year{0},'.format(year)
	currRow += 'Total;'
	reportData += currRow

	reportData += ";Mining;"
	for curr in range(1, numStockpiles+1):
		currRow = "Stockpile {0} Ore (kt),".format(curr) + ''.join([*[str(round(x,2))+',' for x in minePlanTonnageVals[curr]]]) + str(round(sumMinePlanTonnages[curr],2)) + ";"
		reportData += currRow

	reportData += ";Processing;"
	for curr in range(1, numStockpiles+1):
		reportData += "Stockpile {0} Ore;".format(curr)
		currRow = 'Tonnage (kt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]) + ',' + str(round(tonnageTotals[curr],2)) + ";"
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]) + ';'

	reportData += ";Plant Product;"

	if 1 in PPIDs:
		reportData += "Lump;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]) + ',' + str(round(lumpTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]) + ';'

	if 2 in PPIDs:
		reportData += "Fines;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]) + ',' + str(round(finesTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]) + ';'

	if 3 in PPIDs:
		reportData += "Ultra Fines;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]) + ',' + str(round(ultraFinesTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]) + ';'

	reportData += 'Total Product (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]) + ',' + str(round(sumTotalProducts,2)) + ';'

	if 4 in PPIDs:
		reportData += "Rejects;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]) + ',' + str(round(rejectsTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]) + ';'

	reportData += ";Products Selling Price;"

	if 1 in PPIDs:
		reportData += 'Lump Selling Price (USD/dmt);'
		reportData += 'Lump Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]) + ';'
		for i in range(len(commIDs)):
			reportData += 'Lump {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]) + ';'
		reportData += 'Lump Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]) + ',' + 'Avg: ' + str(round(avgLumpSellingPrice,2)) + ';'
		reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
		reportData += 'Net Lump Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]) + ',' + 'Avg: ' + str(round(avgNetLumpPrice,2)) + ';'
		reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
		reportData += 'Net Lump Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetLumpPrice,2)) + ';'

	if 2 in PPIDs:
		reportData += 'Fines Selling Price (USD/dmt);'
		reportData += 'Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]) + ';'
		for i in range(len(commIDs)):
			reportData += 'Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]) + ';'
		reportData += 'Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]) + ',' + 'Avg: ' + str(round(avgFinesSellingPrice,2)) + ';'
		reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
		reportData += 'Net Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]) + ',' + 'Avg: ' + str(round(avgNetFinesPrice,2)) + ';'
		reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
		reportData += 'Net Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetFinesPrice,2)) + ';'

	if 3 in PPIDs:
		reportData += 'Ultra Fines Selling Price (USD/dmt);'
		reportData += 'Ultra Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]) + ';'
		for i in range(len(commIDs)):
			reportData += 'Ultra Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]) + ';'
		reportData += 'Ultra Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]) + ',' + 'Avg: ' + str(round(avgUltraFinesSellingPrice,2)) + ';'
		reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
		reportData += 'Net Ultra Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]) + ',' + 'Avg: ' + str(round(avgNetUltraFinesPrice,2)) + ';'
		reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
		reportData += 'Net Ultra Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetUltraFinesPrice,2)) + ';'

	reportData += ';Revenues;'
	if 1 in PPIDs:
		reportData += 'Lump Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]]) + ',' + str(round(sumLumpRevenues,2)) + ';'
	if 2 in PPIDs:
		reportData += 'Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]]) + ',' + str(round(sumFinesRevenues,2)) + ';'
	if 3 in PPIDs:
		reportData += 'Ultra Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]]) + ',' + str(round(sumUltraFinesRevenues,2)) + ';'
	reportData += 'TOTAL REVENUE,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'

	reportData += ';COSTS;'
	reportData += 'OPEX (millions CAD);'
	reportData += 'Mining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mining]]) + ',' + str(round(sumMining,2)) + ';'
	reportData += 'Stockpile LG Reclaiming,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]]) + ',' + str(round(sumStockpileLG,2)) + ';'
	reportData += 'Pit Dewatering,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]]) + ',' + str(round(sumDewatering,2)) + ';'
	reportData += 'Processing,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in processing]]) + ',' + str(round(sumProcessing,2)) + ';'
	reportData += 'Product Hauling,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]]) + ',' + str(round(sumHauling,2)) + ';'
	reportData += 'Load-out and Rail Loop,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]]) + ',' + str(round(sumLoadOutRailLoop,2)) + ';'
	reportData += 'G&A (Site),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]]) + ',' + str(round(sumGASite,2)) + ';'
	reportData += 'G&A (Room & Board / FIFO),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]]) + ',' + str(round(sumGARoom,2)) + ';'
	reportData += 'Rail Transportation Port and Shiploading,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]]) + ',' + str(round(sumRailTransport,2)) + ';'
	reportData += 'Corporate G&A,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]]) + ',' + str(round(sumGACorp,2)) + ';'
	reportData += 'TOTAL OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
	reportData += 'ROYALTIES (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'

	reportData += 'CAPEX (millions CAD);'
	reportData += 'Pre-Stripping,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]]) + ',' + str(round(sumPreStrip,2)) + ';'
	reportData += 'Mining Equipment Initial,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]]) + ',' + str(round(sumMineEquipInitial,2)) + ';'
	reportData += 'Mining Equipment Sustaining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]]) + ',' + str(round(sumMineEquipSustain,2)) + ';'
	reportData += 'Project Infrastructure Direct Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]]) + ',' + str(round(sumInfraDirectCost,2)) + ';'
	reportData += 'Project Infrastructure Indirect Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]]) + ',' + str(round(sumInfraIndirectCost,2)) + ';'
	reportData += 'Project Infrastructure Contingency,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]]) + ',' + str(round(sumContingency,2)) + ';'
	reportData += 'Railcars,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]]) + ',' + str(round(sumRailcars,2)) + ';'
	reportData += 'Other Mobile Equipment,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]]) + ',' + str(round(sumOtherMobEquip,2)) + ';'
	reportData += 'Closure and Rehab Assurance Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]]) + ',' + str(round(sumClosureRehabAssure,2)) + ';'
	reportData += 'Deposits Provision Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]]) + ',' + str(round(sumDepoProvisionPay,2)) + ';'
	reportData += 'TOTAL CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'

	reportData += 'TAXES (millions CAD);'
	reportData += 'Federal Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]]) + ',' + str(round(sumFederalTaxes,2)) + ';'
	reportData += 'Provincial Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]]) + ',' + str(round(sumProvincialTaxes,2)) + ';'
	reportData += 'Mining Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]]) + ',' + str(round(sumMiningTaxes,2)) + ';'
	reportData += 'TOTAL (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

	reportData += ';SUMMARY;'
	reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'
	reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
	reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
	reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
	reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
	reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
	reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

	reportData += ';PRE-TAX CASH FLOW;'
	reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + str(round(sumCashFlowPreTax,2)) + ';'
	reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ';'
	reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + str(round(sumPaybackPreTax,2)) + ';'
	for rate in discountRates:
		reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPreTaxNPV[int(round(rate*100))],2)) + ';'
	reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(preTaxIRR,2)) + ';'

	reportData += ';POST-TAX CASH FLOW;'
	reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + str(round(sumCashFlowPostTax,2)) + ';'
	reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ';'
	reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + str(round(sumPaybackPostTax,2)) + ';'
	for rate in discountRates:
		reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPostTaxNPV[int(round(rate*100))],2)) + ';'
	reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(postTaxIRR,2)) + ';'

	filter_form = filterForm(mineID=mineID, startDate=projectStartDate, endDate=projectEndDate)
	default_filter_form = defaultFilterForm(mineID=mineID, thisYearStartDate=thisYearStartDate, thisYearEndDate=thisYearEndDate,
			lastYearStartDate=lastYearStartDate, lastYearEndDate=lastYearEndDate,
			thisQuarterStartDate=thisQuarterStartDate, thisQuarterEndDate=thisQuarterEndDate,
			lastQuarterStartDate=lastQuarterStartDate, lastQuarterEndDate=lastQuarterEndDate)
	report_form = reportForm(mineID=mineID, reportData=reportData)

	return render(request, 'report/report.html', {'filterForm': filter_form, 'reportForm': report_form,
		'defaultFilterForm': default_filter_form,
		'yearVals': yearVals, 'fullYearVals': fullYearVals, 'commIDs': commIDs, 'commNameList': commNameList,
		'numStockpiles': list(range(1, numStockpiles+1)),
		'minePlanTonnageVals': minePlanTonnageVals, 'sumMinePlanTonnages': sumMinePlanTonnages,
		# 'minePlanHGTonnageVals': minePlanHGTonnageVals, 'minePlanLGTonnageVals': minePlanLGTonnageVals,
		# 'minePlanWasteTonnageVals': minePlanWasteTonnageVals, 'minePlanOverburdenTonnageVals': minePlanOverburdenTonnageVals,
		# 'sumMinePlanHGTonnage': sumMinePlanHGTonnage, 'sumMinePlanLGTonnage': sumMinePlanLGTonnage,
		# 'sumMinePlanWasteTonnage': sumMinePlanWasteTonnage, 'sumMinePlanOverburdenTonnage': sumMinePlanOverburdenTonnage,
		'tonnageVals': tonnageVals, 'tonnageTotals': tonnageTotals, 'gradeVals': gradeVals, 'moistures': moistures,
		# 'HGTonnageVals': HGTonnageVals, 'HGTonnageTotal': HGTonnageTotal, 'HGGradeVals': HGGradeVals, 'HGMoistures': HGMoistures,
		# 'LGTonnageVals': LGTonnageVals, 'LGTonnageTotal': LGTonnageTotal, 'LGGradeVals': LGGradeVals, 'LGMoistures': LGMoistures,
		'lumpTonnageVals': lumpTonnageVals, 'lumpTonnageTotal': lumpTonnageTotal, 'lumpGradeVals': lumpGradeVals, 'lumpMoistures': lumpMoistures,
		'finesTonnageVals': finesTonnageVals, 'finesTonnageTotal': finesTonnageTotal, 'finesGradeVals': finesGradeVals, 'finesMoistures': finesMoistures,
		'ultraFinesTonnageVals': ultraFinesTonnageVals, 'ultraFinesTonnageTotal': ultraFinesTonnageTotal, 'ultraFinesGradeVals': ultraFinesGradeVals, 'ultraFinesMoistures': ultraFinesMoistures,
		'totalProducts': totalProducts, 'sumTotalProducts': sumTotalProducts,
		'rejectsTonnageVals': rejectsTonnageVals, 'rejectsTonnageTotal': rejectsTonnageTotal, 'rejectsGradeVals': rejectsGradeVals, 'rejectsMoistures': rejectsMoistures,
		'fullShippingCosts': fullShippingCosts, 'fullExchangeRates': fullExchangeRates,
		'HGLumps': HGLumps, 'lumpPenaltyVals': lumpPenaltyVals, 'lumpSellingPrices': lumpSellingPrices, 'avgLumpSellingPrice': avgLumpSellingPrice,
		'netLumpPrices': netLumpPrices, 'avgNetLumpPrice': avgNetLumpPrice, 'exchangeNetLumpPrices': exchangeNetLumpPrices,
		'avgExchangeNetLumpPrice': avgExchangeNetLumpPrice,
		'HGFines': HGFines, 'finesPenaltyVals': finesPenaltyVals, 'finesSellingPrices': finesSellingPrices, 'avgFinesSellingPrice': avgFinesSellingPrice,
		'netFinesPrices': netFinesPrices, 'avgNetFinesPrice': avgNetFinesPrice, 'exchangeNetFinesPrices': exchangeNetFinesPrices,
		'avgExchangeNetFinesPrice': avgExchangeNetFinesPrice,
		'HGUltraFines': HGUltraFines, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals, 'ultraFinesSellingPrices': ultraFinesSellingPrices,
		'avgUltraFinesSellingPrice': avgUltraFinesSellingPrice,
		'netUltraFinesPrices': netUltraFinesPrices, 'exchangeNetUltraFinesPrices': exchangeNetUltraFinesPrices,
		'avgExchangeNetUltraFinesPrice': avgExchangeNetUltraFinesPrice,
		'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
		'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
		'totalRevenues': totalRevenues, 'sumTotalRevenues': sumTotalRevenues,
		'mining': mining, 'stockpileLG': stockpileLG, 'dewatering': dewatering, 'processing': processing, 'hauling': hauling,
		'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite, 'GARoom': GARoom, 'railTransport': railTransport, 'GACorp': GACorp,
		'sumMining': sumMining, 'sumStockpileLG': sumStockpileLG, 'sumDewatering': sumDewatering, 'sumProcessing': sumProcessing,
		'sumHauling': sumHauling, 'sumLoadOutRailLoop': sumLoadOutRailLoop, 'sumGASite': sumGASite, 'sumGARoom': sumGARoom,
		'sumRailTransport': sumRailTransport, 'sumGACorp': sumGACorp,
		'totalOPEX': totalOPEX, 'sumTotalOPEX':sumTotalOPEX, 'royalties': royalties, 'sumRoyalties': sumRoyalties,
		'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial, 'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
		'infraIndirectCost': infraIndirectCost, 'contingency': contingency, 'railcars': railcars, 'otherMobEquip': otherMobEquip,
		'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay, 'sumPreStrip': sumPreStrip,
		'sumMineEquipInitial': sumMineEquipInitial, 'sumMineEquipSustain': sumMineEquipSustain, 'sumInfraDirectCost': sumInfraDirectCost,
		'sumInfraIndirectCost': sumInfraIndirectCost, 'sumContingency': sumContingency, 'sumRailcars': sumRailcars,
		'sumOtherMobEquip': sumOtherMobEquip, 'sumClosureRehabAssure': sumClosureRehabAssure, 'sumDepoProvisionPay': sumDepoProvisionPay,
		'totalCAPEX': totalCAPEX, 'sumTotalCAPEX': sumTotalCAPEX,
		'federalTaxes': federalTaxes, 'provincialTaxes': provincialTaxes, 'miningTaxes': miningTaxes,
		'sumFederalTaxes': sumFederalTaxes, 'sumProvincialTaxes': sumProvincialTaxes, 'sumMiningTaxes': sumMiningTaxes,
		'totalTaxes': totalTaxes, 'sumTotalTaxes': sumTotalTaxes,
		'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
		'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG,
		'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
		'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
		'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
		'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
		'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
		'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
		'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})

	# # Handle Cash Flow Section
	# # Calculate Cash Flow PreTax first
	# OPEXPlusCAPEX = [sum(x) for x in zip(cashFlowOPEX, cashFlowCAPEX)]
	# cashFlowPreTax = list(map(operator.sub, lumpPlusFinesRevenues, OPEXPlusCAPEX))
	# cumCashFlowPreTax = reduce(lambda c, x:c + [c[-1] + x], cashFlowPreTax, [0])[1:]
	# cashFlowPostTax = list(map(operator.sub, cashFlowPreTax, totalTaxes))
	# cumCashFlowPostTax = reduce(lambda c, x:c + [c[-1] + x], cashFlowPostTax, [0])[1:]
	# sumCashFlowPreTax = sum(cashFlowPreTax)
	# sumCashFlowPostTax = sum(cashFlowPostTax)

	# positiveFlow = False
	# paybackPreTax = []
	# for i in range(len(cumCashFlowPreTax)):
	# 	if positiveFlow:
	# 		paybackPreTax.append(0.0)
	# 	else:
	# 		if cumCashFlowPreTax[i] > 0:
	# 			if i == 0:
	# 				paybackPreTax.append(0.0)
	# 			else:
	# 				paybackPreTax.append(cumCashFlowPreTax[i-1] / cashFlowPreTax[i])
	# 			positiveFlow = True
	# 		else:
	# 			paybackPreTax.append(1.0)
	# sumPaybackPreTax = sum(paybackPreTax)

	# positiveFlow = False
	# paybackPostTax = []
	# for i in range(len(cumCashFlowPostTax)):
	# 	if positiveFlow:
	# 		paybackPostTax.append(0.0)
	# 	else:
	# 		if cumCashFlowPostTax[i] > 0:
	# 			if i == 0:
	# 				paybackPostTax.append(0.0)
	# 			else:
	# 				paybackPostTax.append(cumCashFlowPostTax[i-1] / cashFlowPostTax[i])
	# 			positiveFlow = True
	# 		else:
	# 			paybackPostTax.append(1.0)
	# sumPaybackPostTax = sum(paybackPostTax)

	# # Save entries to tblCashFlow
	# currTime = timezone.localtime(timezone.now())
	# for i in range(len(yearVals)):
	# 	currCashFlow = tblCashFlow.objects.filter(mineID=mineID, year=yearVals[i]).order_by('-dateAdded')[0]
	# 	currCashFlow.cashFlowPreTax = cashFlowPreTax[i]
	# 	currCashFlow.cashFlowPostTax = cashFlowPostTax[i]
	# 	currCashFlow.cumulativeCashFlowPreTax = cumCashFlowPreTax[i]
	# 	currCashFlow.cumulativeCashFlowPostTax = cumCashFlowPostTax[i]
	# 	currCashFlow.paybackPreTax = paybackPreTax[i]
	# 	currCashFlow.paybackPostTax = paybackPostTax[i]
	# 	currCashFlow.dateAdded = currTime
	# 	currCashFlow.save()

	# # Calculate and Update NPVs and IRRs
	# discountRates = [Decimal(0.06), Decimal(0.08), Decimal(0.10), Decimal(0.12), Decimal(0.15), Decimal(0.20)]
	# preTaxNPVs = []
	# postTaxNPVs = []
	# NPVCashFlowPreTax = [0] + cashFlowPreTax
	# NPVCashFlowPostTax = [0] + cashFlowPostTax
	# preTaxIRR = round(np.irr(NPVCashFlowPreTax),4)
	# postTaxIRR = round(np.irr(NPVCashFlowPostTax),4)
	# for rate in discountRates:
	# 	preTaxNPVs.append(round(np.npv(rate, NPVCashFlowPreTax),2))
	# 	postTaxNPVs.append(round(np.npv(rate, NPVCashFlowPostTax),2))
	# 	# preTaxIRRs.append(round(np.irr(cashFlowPreTax),4))
	# 	# postTaxIRRs.append(round(np.irr(cashFlowPostTax),4))


	# return render(request, 'report/report.html', {'yearVals': yearVals, 'commIDs': commIDs, 'commNameList': commNameList,
	# 	'HGTonnageVals': HGTonnageVals, 'HGTonnageTotal': HGTonnageTotal, 'HGGradeVals': HGGradeVals, 'HGMoistures': HGMoistures,
	# 	'LGTonnageVals': LGTonnageVals, 'LGTonnageTotal': LGTonnageTotal, 'LGGradeVals': LGGradeVals, 'LGMoistures': LGMoistures,
	# 	'lumpTonnageVals': lumpTonnageVals, 'lumpTonnageTotal': lumpTonnageTotal, 'lumpGradeVals': lumpGradeVals, 'lumpMoistures': lumpMoistures,
	# 	'finesTonnageVals': finesTonnageVals, 'finesTonnageTotal': finesTonnageTotal, 'finesGradeVals': finesGradeVals, 'finesMoistures': finesMoistures,
	# 	'ultraFinesTonnageVals': ultraFinesTonnageVals, 'ultraFinesTonnageTotal': ultraFinesTonnageTotal, 'ultraFinesGradeVals': ultraFinesGradeVals, 'ultraFinesMoistures': ultraFinesMoistures,
	# 	'totalProducts': totalProducts, 'sumTotalProducts': sumTotalProducts,
	# 	'rejectsTonnageVals': rejectsTonnageVals, 'rejectsGradeVals': rejectsGradeVals, 'rejectsMoistures': rejectsMoistures,
	# 	'shippingCosts': shippingCosts, 'exchangeRates': exchangeRates,
	# 	'HGLumps': HGLumps, 'lumpPenaltyVals': lumpPenaltyVals, 'lumpSellingPrices': lumpSellingPrices, 'avgLumpSellingPrice': avgLumpSellingPrice,
	# 	'netLumpPrices': netLumpPrices, 'avgNetLumpPrice': avgNetLumpPrice, 'exchangeNetLumpPrices': exchangeNetLumpPrices,
	# 	'avgExchangeNetLumpPrice': avgExchangeNetLumpPrice,
	# 	'HGFines': HGFines, 'finesPenaltyVals': finesPenaltyVals, 'finesSellingPrices': finesSellingPrices, 'avgFinesSellingPrice': avgFinesSellingPrice,
	# 	'netFinesPrices': netFinesPrices, 'avgNetFinesPrice': avgNetFinesPrice, 'exchangeNetFinesPrices': exchangeNetFinesPrices,
	# 	'avgExchangeNetFinesPrice': avgExchangeNetFinesPrice,
	# 	'HGUltraFines': HGUltraFines, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals, 'ultraFinesSellingPrices': ultraFinesSellingPrices,
	# 	'netUltraFinesPrices': netUltraFinesPrices, 'exchangeNetUltraFinesPrices': exchangeNetUltraFinesPrices,
	# 	'avgExchangeNetUltraFinesPrice': avgExchangeNetUltraFinesPrice,
	# 	'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
	# 	'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
	# 	'totalRevenues': totalRevenues, 'sumTotalRevenues': sumTotalRevenues,
	# 	'mining': mining, 'stockpileLG': stockpileLG, 'dewatering': dewatering, 'processing': processing, 'hauling': hauling,
	# 	'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite, 'GARoom': GARoom, 'railTransport': railTransport, 'GACorp': GACorp,
	# 	'sumMining': sumMining, 'sumStockpileLG': sumStockpileLG, 'sumDewatering': sumDewatering, 'sumProcessing': sumProcessing,
	# 	'sumHauling': sumHauling, 'sumLoadOutRailLoop': sumLoadOutRailLoop, 'sumGASite': sumGASite, 'sumGARoom': sumGARoom,
	# 	'sumRailTransport': sumRailTransport, 'sumGACorp': sumGACorp,
	# 	'totalOPEX': totalOPEX, 'sumTotalOPEX':sumTotalOPEX, 'royalties': royalties, 'sumRoyalties': sumRoyalties,
	# 	'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial, 'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
	# 	'infraIndirectCost': infraIndirectCost, 'contingency': contingency, 'railcars': railcars, 'otherMobEquip': otherMobEquip,
	# 	'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay, 'sumPreStrip': sumPreStrip,
	# 	'sumMineEquipInitial': sumMineEquipInitial, 'sumMineEquipSustain': sumMineEquipSustain, 'sumInfraDirectCost': sumInfraDirectCost,
	# 	'sumInfraIndirectCost': sumInfraIndirectCost, 'sumContingency': sumContingency, 'sumRailcars': sumRailcars,
	# 	'sumOtherMobEquip': sumOtherMobEquip, 'sumClosureRehabAssure': sumClosureRehabAssure, 'sumDepoProvisionPay': sumDepoProvisionPay,
	# 	'totalCAPEX': totalCAPEX, 'sumTotalCAPEX': sumTotalCAPEX,
	# 	'federalTaxes': federalTaxes, 'provincialTaxes': provincialTaxes, 'miningTaxes': miningTaxes,
	# 	'sumFederalTaxes': sumFederalTaxes, 'sumProvincialTaxes': sumProvincialTaxes, 'sumMiningTaxes': sumMiningTaxes,
	# 	'totalTaxes': totalTaxes, 'sumTotalTaxes': sumTotalTaxes,
	# 	'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
	# 	'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG,
	# 	'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
	# 	'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
	# 	'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
	# 	'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
	# 	'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
	# 	'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR}

def reportDL(request):
	if request.method == 'POST':
		if "reportDownload" in request.POST:
			mineID = request.session["mineID"]
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="report.csv"; newline=""'

			writer = csv.writer(response)

			form = reportForm(request.POST, mineID=mineID, reportData=None)
			if form.is_valid():
				cleanData = form.cleaned_data
				reportData = cleanData["reportData"]

				reportRows = reportData.split(';')
				for row in reportRows:
					writer.writerow(row.split(','))

				return response

		elif "applyDefaultFilter" in request.POST:
			filler = ""
			mineID = request.session["mineID"]
			mineMatch = tblMine.objects.get(mineID=int(mineID))

			# Check project exists
			projectsList  = tblProject.objects.filter(mineID=mineID)
			if not projectsList:
				return render(request, "report/noProjects.html", {})

			# # Get LOM of the mine's most recent project
			latestProject = projectsList.order_by('-dateAdded')[0]
			LOM = int(latestProject.LOM)
			numStockpiles = latestProject.numStockpiles

			projectPeriods = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).order_by('year')
			projectStartDate = projectPeriods[0].startDate
			projectEndDate = projectPeriods[projectPeriods.count()-1].endDate

			# Check if default filter options are available
			# Check "This year", "Last year", "This quarter", and "Last quarter"
			# 1. This year
			today = datetime.date.today()
			if (today.year >= projectStartDate.year) and (today.year <= projectEndDate.year):
				# thisYear = True
				thisYearStartDate = datetime.date(today.year, 1, 1)
				thisYearEndDate = datetime.date(today.year, 12, 31)
			else:
				# thisYear = False
				thisYearStartDate = None
				thisYearEndDate = None

			# 2. Last year
			if (today.year-1 >= projectStartDate.year) and (today.year-1 <= projectEndDate.year):
				# lastYear = True
				lastYearStartDate = datetime.date(today.year-1, 1, 1)
				lastYearEndDate = datetime.date(today.year-1, 12, 31)
			else:
				# lastYear = False
				lastYearStartDate = None
				lastYearEndDate = None

			# 3. This quarter
			if thisYearStartDate:
				todayQ = ceil(today.month/3.0)
				if today.year == projectStartDate.year:
					startDateQ = ceil(projectStartDate.month/3.0)
					quarters = list(range(startDateQ, 5))			
					if todayQ in quarters:
						# thisQuarter = True
						thisQuarterStartDate = datetime.date(today.year, 3*(todayQ - 1) + 1, 1)
						thisQuarterEndDate = thisQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
					else:
						# thisQuarter = False
						thisQuarterStartDate = None
						thisQuarterEndDate = None
				else:
					# thisQuarter = True
					thisQuarterStartDate = datetime.date(today.year, 3*(todayQ - 1) + 1, 1)
					thisQuarterEndDate = thisQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
			else:
				# thisQuarter = False
				thisQuarterStartDate = None
				thisQuarterEndDate = None

			# 4. Last quarter
			threeMonthsAgo = today - relativedelta(months=+3)
			if (threeMonthsAgo >= projectStartDate) and (threeMonthsAgo <= projectEndDate):
				threeMonthsAgoQ = ceil(threeMonthsAgo.month/3.0)
				# lastQuarter = True
				lastQuarterStartDate = datetime.date(threeMonthsAgo.year, 3*(threeMonthsAgoQ - 1) + 1, 1)
				lastQuarterEndDate = lastQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
			else:
				# lastQuarter = False
				lastQuarterStartDate = None
				lastQuarterEndDate = None

			# Get list of Commodity IDs
			commodities = tblCommodity.objects.filter(projectID=latestProject.projectID)
			commIDs = commodities.values_list('commodityID', flat=True)

			# Get list of Commodity Names
			commNameList = []
			for ID in commIDs:
				nameMatch = tblCommodityList.objects.get(commodityID=ID)
				commNameList.append(nameMatch.name)

			# Get list of Plant Product IDs
			PPMatches = tblPlantProduct.objects.filter(projectID=latestProject.projectID)
			PPIDs = PPMatches.values_list('plantProductID', flat=True)

			# Get most recent tblInputs entry
			latestInput = tblInputs.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
			# Price entry
			priceEntry = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=1)

			# Handle OPEX Shipping Cost by Year
			# shippingCosts = []
			fullShippingCosts = []

			# for year in range(1, yearCount+1):
			# 	currOPEX = tblOPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
			# 	fullShippingCosts.append(round(currOPEX.shipping,2))
			# 	if year in yearVals:
			# 		shippingCosts.append(round(currOPEX.shipping,2))

			tonnageVals = None
			tonnageTotals = None
			gradeVals = None
			moistures = None

			lumpTonnageVals = None
			lumpTonnageTotal = None
			lumpGradeVals = None
			lumpMoistures = None

			finesTonnageVals = None
			finesTonnageTotal = None
			finesGradeVals = None
			finesMoistures = None

			ultraFinesTonnageVals = None
			ultraFinesTonnageTotal = None
			ultraFinesGradeVals = None
			ultraFinesMoistures = None

			rejectsTonnageVals = None
			rejectsTonnageTotal = None
			rejectsGradeVals = None
			rejectsMoistures = None


			HGLumps = None
			lumpPenaltyVals = None
			lumpSellingPrices = None
			avgLumpSellingPrice = None
			netLumpPrices = None
			avgNetLumpPrice = None
			exchangeNetLumpPrices = None
			avgExchangeNetLumpPrice = None

			HGFines = None
			finesPenaltyVals = None
			finesSellingPrices = None
			avgFinesSellingPrice = None
			netFinesPrices = None
			avgNetFinesPrice = None
			exchangeNetFinesPrices = None
			avgExchangeNetFinesPrice = None

			HGUltraFines = None
			ultraFinesPenaltyVals = None
			ultraFinesSellingPrices = None
			avgUltraFinesSellingPrice = None
			netUltraFinesPrices = None
			avgNetUltraFinesPrice = None
			exchangeNetUltraFinesPrices = None
			avgExchangeNetUltraFinesPrice = None

			lumpRevenues = None
			sumLumpRevenues = None
			finesRevenues = None
			sumFinesRevenues = None
			ultraFinesRevenues = None
			sumUltraFinesRevenues = None

			discountRates = [Decimal(0.06), Decimal(0.08), Decimal(0.10), Decimal(0.12), Decimal(0.15), Decimal(0.20)]

			# form = filterForm(request.POST, mineID=mineID)
			form = defaultFilterForm(request.POST, mineID=mineID, thisYearStartDate=thisYearStartDate, thisYearEndDate=thisYearEndDate,
				lastYearStartDate=lastYearStartDate, lastYearEndDate=lastYearEndDate,
				thisQuarterStartDate=thisQuarterStartDate, thisQuarterEndDate=thisQuarterEndDate,
				lastQuarterStartDate=lastQuarterStartDate, lastQuarterEndDate=lastQuarterEndDate)
			if form.is_valid():
				cleanData = form.cleaned_data
				defaultFilter = cleanData["defaultFilter"]

				divisor = 12.0
				if defaultFilter == "thisYear":
					startDate = cleanData["thisYearStartDate"]
					endDate = cleanData["thisYearEndDate"]
				elif defaultFilter == "lastYear":
					startDate = cleanData["lastYearStartDate"]
					endDate = cleanData["lastYearEndDate"]
				elif defaultFilter == "thisQuarter":
					startDate = cleanData["thisQuarterStartDate"]
					endDate = cleanData["thisQuarterEndDate"]
				elif defaultFilter == "lastQuarter":
					startDate = cleanData["lastQuarterStartDate"]
					endDate = cleanData["lastQuarterEndDate"]

				startDateVals = []
				endDateVals = []
				dateVals = []
				currDate = startDate
				while currDate <= endDate:
					startDateVals.append(currDate)
					dateVals.append(currDate.strftime("%b-%Y"))
					endDateVals.append(currDate + relativedelta(months=+1) - relativedelta(days=+1))
					currDate = currDate + relativedelta(months=+1)

				yearNum = startDate.year - projectPeriods[0].startDate.year + 1

				totalRevenues = [Decimal(0.0)]*len(startDateVals)
				lumpPlusFinesRevenues = [Decimal(0.0)]*len(startDateVals)

				# Obtain Exchange Rate
				fullExchangeRates = [round(Decimal(latestInput.exchangeRate),2)]*len(startDateVals)
				xRate = round(Decimal(latestInput.exchangeRate),2)

				totalProducts = [Decimal(0.0)]*len(startDateVals)

				# Handle Mine Plan Tonnages Section
				sumMinePlanTonnages = {}
				minePlanTonnageVals = {}

				# minePlanTonnagesByYear = {}
				# dailyMinePlanTonnageVals = {}
				for curr in range(1, numStockpiles+1):
					MPTonnageEntries = tblMineProductTonnage.objects.filter(projectID=latestProject.projectID, stockpileID=curr, year=yearNum)
					minePlanTonnageVals[curr] = [round(Decimal(MPTonnageEntries[0].tonnage/divisor), 2)]*len(startDateVals)
					# minePlanTonnageVals[curr] = []
					# minePlanTonnagesByYear[curr] = {}
					# for year,yearNum in yearRanges.items():
					# 	if calendar.isleap(year):
					# 		minePlanTonnagesByYear[curr][year] = round(Decimal(MPTonnageEntries[yearNum-1].tonnage/366.0), 2)
					# 	else:
					# 		minePlanTonnagesByYear[curr][year] = round(Decimal(MPTonnageEntries[yearNum-1].tonnage/365.0), 2)

					# currDate = startDate
					# while currDate <= endDate:
					# 	minePlanTonnageVals[curr].append(minePlanTonnagesByYear[curr][currDate.year])
					# 	currDate += datetime.timedelta(days=1)
					sumMinePlanTonnages[curr] = sum(minePlanTonnageVals[curr])

				latestOPEX = tblOPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
				latestCAPEX = tblCAPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
				# OPEXByYear = tblOPEX.objects.filter(mineID=mineID, dateAdded=latestOPEX.dateAdded).order_by('year')
				# CAPEXByYear = tblCAPEX.objects.filter(mineID=mineID, dateAdded=latestCAPEX.dateAdded).order_by('year')
				OPEXEntry = tblOPEX.objects.get(mineID=mineID, year=yearNum, dateAdded=latestOPEX.dateAdded)
				CAPEXEntry = tblCAPEX.objects.get(mineID=mineID, year=yearNum, dateAdded=latestCAPEX.dateAdded)

				fullShippingCosts = [round(OPEXEntry.shipping/Decimal(divisor), 2)]*len(startDateVals)

				mining = [round(OPEXEntry.mining/Decimal(divisor), 2)]*len(startDateVals)
				infrastructure = [round(OPEXEntry.infrastructure/Decimal(divisor), 2)]*len(startDateVals)
				stockpileLG = [round(OPEXEntry.stockpileLG/Decimal(divisor), 2)]*len(startDateVals)
				dewatering = [round(OPEXEntry.dewatering/Decimal(divisor), 2)]*len(startDateVals)
				processing = [round(OPEXEntry.processing/Decimal(divisor), 2)]*len(startDateVals)
				hauling = [round(OPEXEntry.hauling/Decimal(divisor), 2)]*len(startDateVals)
				loadOutRailLoop = [round(OPEXEntry.loadOutRailLoop/Decimal(divisor), 2)]*len(startDateVals)
				GASite = [round(OPEXEntry.GASite/Decimal(divisor), 2)]*len(startDateVals)
				GARoom = [round(OPEXEntry.GARoomBoardFIFO/Decimal(divisor), 2)]*len(startDateVals)
				railTransport = [round(OPEXEntry.railTransport/Decimal(divisor), 2)]*len(startDateVals)
				GACorp = [round(OPEXEntry.GACorp/Decimal(divisor), 2)]*len(startDateVals)
				royalties = [round(OPEXEntry.royalties/Decimal(divisor), 2)]*len(startDateVals)
				transportation = [round(OPEXEntry.transportation/Decimal(divisor), 2)]*len(startDateVals)
				GA = [round(OPEXEntry.GA/Decimal(divisor), 2)]*len(startDateVals)

				preStrip = [round(CAPEXEntry.preStrip/Decimal(divisor), 2)]*len(startDateVals)
				mineEquipInitial = [round(CAPEXEntry.mineEquipInitial/Decimal(divisor), 2)]*len(startDateVals)
				mineEquipSustain = [round(CAPEXEntry.mineEquipSustain/Decimal(divisor), 2)]*len(startDateVals)
				infraDirectCost = [round(CAPEXEntry.infraDirectCost/Decimal(divisor), 2)]*len(startDateVals)
				infraIndirectCost = [round(CAPEXEntry.infraIndirectCost/Decimal(divisor), 2)]*len(startDateVals)
				contingency = [round(CAPEXEntry.contingency/Decimal(divisor), 2)]*len(startDateVals)
				railcars = [round(CAPEXEntry.railcars/Decimal(divisor), 2)]*len(startDateVals)
				otherMobEquip = [round(CAPEXEntry.otherMobEquip/Decimal(divisor), 2)]*len(startDateVals)
				closureRehabAssure = [round(CAPEXEntry.closureRehabAssure/Decimal(divisor), 2)]*len(startDateVals)
				depoProvisionPay = [round(CAPEXEntry.depoProvisionPay/Decimal(divisor), 2)]*len(startDateVals)
				workCapCurrentProd = [round(CAPEXEntry.workCapCurrentProd/Decimal(divisor), 2)]*len(startDateVals)
				workCapCostsLG = [round(CAPEXEntry.workCapCostsLG/Decimal(divisor), 2)]*len(startDateVals)
				EPCM = [round(CAPEXEntry.EPCM/Decimal(divisor), 2)]*len(startDateVals)
				ownerCost = [round(CAPEXEntry.ownerCost/Decimal(divisor), 2)]*len(startDateVals)

				sumMining = sum(mining)
				sumStockpileLG = sum(stockpileLG)
				sumDewatering = sum(dewatering)
				sumProcessing = sum(processing)
				sumHauling = sum(hauling)
				sumLoadOutRailLoop = sum(loadOutRailLoop)
				sumGASite = sum(GASite)
				sumGARoom = sum(GARoom)
				sumRailTransport = sum(railTransport)
				sumGACorp = sum(GACorp)
				sumRoyalties = sum(royalties)

				totalOPEX = [sum(x) for x in zip(mining, stockpileLG, dewatering, processing, hauling,
					loadOutRailLoop, GASite, GARoom, railTransport, GACorp)]
				sumTotalOPEX = sum(totalOPEX)

				sumPreStrip = sum(preStrip)
				sumMineEquipInitial = sum(mineEquipInitial)
				sumMineEquipSustain = sum(mineEquipSustain)
				sumInfraDirectCost = sum(infraDirectCost)
				sumInfraIndirectCost = sum(infraIndirectCost)
				sumContingency = sum(contingency)
				sumRailcars = sum(railcars)
				sumOtherMobEquip = sum(otherMobEquip)
				sumClosureRehabAssure = sum(closureRehabAssure)
				sumDepoProvisionPay = sum(depoProvisionPay)
				sumWorkCapCurrentProd = sum(workCapCurrentProd)
				sumWorkCapCostsLG = sum(workCapCostsLG)

				totalCAPEX = [sum(x) for x in zip(preStrip, mineEquipInitial, mineEquipSustain, infraDirectCost, infraIndirectCost,
					contingency, railcars, otherMobEquip, closureRehabAssure, depoProvisionPay)]
				sumTotalCAPEX = sum(totalCAPEX)

				latestTaxes = tblTaxes.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
				taxesEntry = tblTaxes.objects.get(mineID=mineID, year=yearNum, dateAdded=latestTaxes.dateAdded)

				federalTaxes = [round(Decimal(taxesEntry.federal/divisor), 2)]*len(startDateVals)
				provincialTaxes = [round(Decimal(taxesEntry.provincial/divisor), 2)]*len(startDateVals)
				miningTaxes = [round(Decimal(taxesEntry.mining/divisor), 2)]*len(startDateVals)

				sumFederalTaxes = sum(federalTaxes)
				sumProvincialTaxes = sum(provincialTaxes)
				sumMiningTaxes = sum(miningTaxes)
				totalTaxes = [sum(x) for x in zip(federalTaxes, provincialTaxes, miningTaxes)]
				sumTotalTaxes = sum(totalTaxes)


				# Handle values if no calculations have been run during selected range of dates
				cashFlowEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=startDate, date__lte=endDate)
				if not cashFlowEntries:
					tonnageVals = {}
					tonnageTotals = {}
					gradeVals = {}
					moistures = {}
					for curr in range(1, numStockpiles+1):
						tonnageVals[curr] = [filler]*len(startDateVals)
						tonnageTotals[curr] = filler
						gradeVals[curr] = {}
						for i in range(len(commIDs)):
							gradeVals[curr][commNameList[i]] = [filler]*len(startDateVals)
						moistures[curr] = [round(latestInput.feedMoisture,2)]*len(startDateVals)

					if 1 in PPIDs:
						lumpTonnageVals = [filler]*len(startDateVals)
						lumpTonnageTotal = filler
						lumpGradeVals = {}
						for i in range(len(commIDs)):
							lumpGradeVals[commNameList[i]] = [filler]*len(startDateVals)
						lumpMoistures = [round(latestInput.lumpMoisture,2)]*len(startDateVals)

					if 2 in PPIDs:
						finesTonnageVals = [filler]*len(startDateVals)
						finesTonnageTotal = filler
						finesGradeVals = {}
						for i in range(len(commIDs)):
							finesGradeVals[commNameList[i]] = [filler]*len(startDateVals)
						finesMoistures = [round(latestInput.finesMoisture,2)]*len(startDateVals)

					if 3 in PPIDs:
						ultraFinesTonnageVals = [filler]*len(startDateVals)
						ultraFinesTonnageTotal = filler
						ultraFinesGradeVals = {}
						for i in range(len(commIDs)):
							ultraFinesGradeVals[commNameList[i]] = [filler]*len(startDateVals)
						ultraFinesMoistures = [round(latestInput.ultraFinesMoisture,2)]*len(startDateVals)

					if 4 in PPIDs:
						rejectsTonnageVals = [filler]*len(startDateVals)
						rejectsTonnageTotal = filler
						rejectsGradeVals = {}
						for i in range(len(commIDs)):
							rejectsGradeVals[commNameList[i]] = [filler]*len(startDateVals)
						rejectsMoistures = [round(latestInput.rejectsMoisture,2)]*len(startDateVals)

					totalProducts = [filler]*len(startDateVals)
					sumTotalProducts = filler

					if 1 in PPIDs:
						HGLumps = [Decimal(priceEntry.lump)]*len(startDateVals)
						lumpPenaltyVals = {}
						for i in range(len(commIDs)):
							lumpPenaltyVals[commNameList[i]] = [filler]*len(startDateVals)
						lumpSellingPrices = [filler]*len(startDateVals)
						avgLumpSellingPrice = filler
						netLumpPrices = [filler]*len(startDateVals)
						avgNetLumpPrice = filler
						exchangeNetLumpPrices = [filler]*len(startDateVals)
						avgExchangeNetLumpPrice = filler

					if 2 in PPIDs:
						HGFines = [Decimal(priceEntry.fines)]*len(startDateVals)
						finesPenaltyVals = {}
						for i in range(len(commIDs)):
							finesPenaltyVals[commNameList[i]] = [filler]*len(startDateVals)
						finesSellingPrices = [filler]*len(startDateVals)
						avgFinesSellingPrice = filler
						netFinesPrices = [filler]*len(startDateVals)
						avgNetFinesPrice = filler
						exchangeNetFinesPrices = [filler]*len(startDateVals)
						avgExchangeNetFinesPrice = filler

					if 3 in PPIDs:
						HGUltraFines = [Decimal(priceEntry.ultraFines)]*len(startDateVals)
						ultraFinesPenaltyVals = {}
						for i in range(len(commIDs)):
							ultraFinesPenaltyVals[commNameList[i]] = [filler]*len(startDateVals)
						ultraFinesSellingPrices = [filler]*len(startDateVals)
						avgUltraFinesSellingPrice = filler
						netUltraFinesPrices = [filler]*len(startDateVals)
						avgNetUltraFinesPrice = filler
						exchangeNetUltraFinesPrices = [filler]*len(startDateVals)
						avgExchangeNetUltraFinesPrice = filler

					if 1 in PPIDs:
						lumpRevenues = [filler]*len(startDateVals)
						sumLumpRevenues = filler

					if 2 in PPIDs:
						finesRevenues = [filler]*len(startDateVals)
						sumFinesRevenues = filler

					if 3 in PPIDs:
						ultraFinesRevenues = [filler]*len(startDateVals)
						sumUltraFinesRevenues = filler

					totalRevenues = [filler]*len(startDateVals)
					sumTotalRevenues = filler

					cashFlowPreTax = [filler]*len(startDateVals)
					cashFlowPostTax = [filler]*len(startDateVals)
					cumCashFlowPreTax = [filler]*len(startDateVals)
					cumCashFlowPostTax = [filler]*len(startDateVals)
					sumCashFlowPreTax = filler
					sumCashFlowPostTax = filler
					paybackPreTax = [filler]*len(startDateVals)
					paybackPostTax = [filler]*len(startDateVals)
					sumPaybackPreTax = filler
					sumPaybackPostTax = filler
					preTaxIRR = filler
					postTaxIRR = filler
					# preTaxPVs = [filler]*len(startDateVals)
					# postTaxPVs = [filler]*len(startDateVals)
					# sumPreTaxNPV = filler
					# sumPostTaxNPV = filler

					preTaxPVs = {}
					postTaxPVs = {}
					sumPreTaxNPV = {}
					sumPostTaxNPV = {}
					for rate in discountRates:
						rate = int(round(rate*100))
						preTaxPVs[rate] = [filler]*len(startDateVals)
						postTaxPVs[rate] = [filler]*len(startDateVals)
						sumPreTaxNPV[rate] = filler
						sumPostTaxNPV[rate] = filler

					# Create DL Form Data
					reportRowCount = 1

					reportData = ""

					currRow = 'Item,'
					for date in dateVals:
						# currRow += 'Year{0},'.format(year)
						currRow += date + ','
					currRow += 'Total;'
					reportData += currRow

					reportData += ";Mining;"
					for curr in range(1, numStockpiles+1):
						currRow = "Stockpile {0} Ore (kt),".format(curr) + ''.join([*[str(round(x,2))+',' for x in minePlanTonnageVals[curr]]]) + str(round(sumMinePlanTonnages[curr],2)) + ";"
						reportData += currRow

					reportData += ";Processing;"
					for curr in range(1, numStockpiles+1):
						reportData += "Stockpile {0} Ore;".format(curr)
						currRow = 'Tonnage (kt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]) + ',' + tonnageTotals[curr] + ";"
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]) + ';'

					reportData += ";Plant Product;"

					if 1 in PPIDs:
						reportData += "Lump;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]) + ',' + lumpTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]) + ';'

					if 2 in PPIDs:
						reportData += "Fines;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]) + ',' + finesTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]) + ';'

					if 3 in PPIDs:
						reportData += "Ultra Fines;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]) + ',' + ultraFinesTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]) + ';'

					reportData += 'Total Product (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]) + ',' + sumTotalProducts + ';'

					if 4 in PPIDs:
						reportData += "Rejects;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]) + ',' + rejectsTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]) + ';'

					reportData += ";Products Selling Price;"

					if 1 in PPIDs:
						reportData += 'Lump Selling Price (USD/dmt);'
						reportData += 'Lump Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]) + ';'
						for i in range(len(commIDs)):
							reportData += 'Lump {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]) + ';'
						reportData += 'Lump Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]) + ',' + 'Avg: ' + avgLumpSellingPrice + ';'
						reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
						reportData += 'Net Lump Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]) + ',' + 'Avg: ' + avgNetLumpPrice + ';'
						reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
						reportData += 'Net Lump Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]) + ',' + 'Avg: ' + avgExchangeNetLumpPrice + ';'

					if 2 in PPIDs:
						reportData += 'Fines Selling Price (USD/dmt);'
						reportData += 'Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]) + ';'
						for i in range(len(commIDs)):
							reportData += 'Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]) + ';'
						reportData += 'Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]) + ',' + 'Avg: ' + avgFinesSellingPrice + ';'
						reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
						reportData += 'Net Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]) + ',' + 'Avg: ' + avgNetFinesPrice + ';'
						reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
						reportData += 'Net Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]) + ',' + 'Avg: ' + avgExchangeNetFinesPrice + ';'

					if 3 in PPIDs:
						reportData += 'Ultra Fines Selling Price (USD/dmt);'
						reportData += 'Ultra Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]) + ';'
						for i in range(len(commIDs)):
							reportData += 'Ultra Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]) + ';'
						reportData += 'Ultra Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]) + ',' + 'Avg: ' + avgUltraFinesSellingPrice + ';'
						reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
						reportData += 'Net Ultra Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]) + ',' + 'Avg: ' + avgNetUltraFinesPrice + ';'
						reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
						reportData += 'Net Ultra Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]) + ',' + 'Avg: ' + avgExchangeNetUltraFinesPrice+ ';'

					reportData += ';Revenues;'
					if 1 in PPIDs:
						reportData += 'Lump Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]]) + ',' + sumLumpRevenues + ';'
					if 2 in PPIDs:
						reportData += 'Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]]) + ',' + sumFinesRevenues + ';'
					if 3 in PPIDs:
						reportData += 'Ultra Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]]) + ',' + sumUltraFinesRevenues + ';'
					reportData += 'TOTAL REVENUE,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + sumTotalRevenues + ';'

					reportData += ';COSTS;'
					reportData += 'OPEX (millions CAD);'
					reportData += 'Mining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mining]]) + ',' + str(round(sumMining,2)) + ';'
					reportData += 'Stockpile LG Reclaiming,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]]) + ',' + str(round(sumStockpileLG,2)) + ';'
					reportData += 'Pit Dewatering,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]]) + ',' + str(round(sumDewatering,2)) + ';'
					reportData += 'Processing,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in processing]]) + ',' + str(round(sumProcessing,2)) + ';'
					reportData += 'Product Hauling,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]]) + ',' + str(round(sumHauling,2)) + ';'
					reportData += 'Load-out and Rail Loop,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]]) + ',' + str(round(sumLoadOutRailLoop,2)) + ';'
					reportData += 'G&A (Site),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]]) + ',' + str(round(sumGASite,2)) + ';'
					reportData += 'G&A (Room & Board / FIFO),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]]) + ',' + str(round(sumGARoom,2)) + ';'
					reportData += 'Rail Transportation Port and Shiploading,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]]) + ',' + str(round(sumRailTransport,2)) + ';'
					reportData += 'Corporate G&A,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]]) + ',' + str(round(sumGACorp,2)) + ';'
					reportData += 'TOTAL OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
					reportData += 'ROYALTIES (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'

					reportData += 'CAPEX (millions CAD);'
					reportData += 'Pre-Stripping,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]]) + ',' + str(round(sumPreStrip,2)) + ';'
					reportData += 'Mining Equipment Initial,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]]) + ',' + str(round(sumMineEquipInitial,2)) + ';'
					reportData += 'Mining Equipment Sustaining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]]) + ',' + str(round(sumMineEquipSustain,2)) + ';'
					reportData += 'Project Infrastructure Direct Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]]) + ',' + str(round(sumInfraDirectCost,2)) + ';'
					reportData += 'Project Infrastructure Indirect Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]]) + ',' + str(round(sumInfraIndirectCost,2)) + ';'
					reportData += 'Project Infrastructure Contingency,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]]) + ',' + str(round(sumContingency,2)) + ';'
					reportData += 'Railcars,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]]) + ',' + str(round(sumRailcars,2)) + ';'
					reportData += 'Other Mobile Equipment,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]]) + ',' + str(round(sumOtherMobEquip,2)) + ';'
					reportData += 'Closure and Rehab Assurance Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]]) + ',' + str(round(sumClosureRehabAssure,2)) + ';'
					reportData += 'Deposits Provision Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]]) + ',' + str(round(sumDepoProvisionPay,2)) + ';'
					reportData += 'TOTAL CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'

					reportData += 'TAXES (millions CAD);'
					reportData += 'Federal Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]]) + ',' + str(round(sumFederalTaxes,2)) + ';'
					reportData += 'Provincial Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]]) + ',' + str(round(sumProvincialTaxes,2)) + ';'
					reportData += 'Mining Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]]) + ',' + str(round(sumMiningTaxes,2)) + ';'
					reportData += 'TOTAL (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

					reportData += ';SUMMARY;'
					reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + filler + ';'
					reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
					reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
					reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
					reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
					reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
					reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

					reportData += ';PRE-TAX CASH FLOW;'
					reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + filler + ';'
					reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ',' + filler + ';'
					reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + filler + ';'
					for rate in discountRates:
						reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + filler + ';'
					reportData += 'INTERNAL RATE OF RETURN (IRR),' + 'N/A' + ';'

					reportData += ';POST-TAX CASH FLOW;'
					reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + filler + ';'
					reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ',' + filler + ';'
					reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + filler + ';'
					for rate in discountRates:
						reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + filler + ';'
					reportData += 'INTERNAL RATE OF RETURN (IRR),' + 'N/A' + ';'

					filter_form = filterForm(mineID=mineID, startDate=projectStartDate, endDate=projectEndDate)
					default_filter_form = defaultFilterForm(mineID=mineID, thisYearStartDate=thisYearStartDate, thisYearEndDate=thisYearEndDate,
						lastYearStartDate=lastYearStartDate, lastYearEndDate=lastYearEndDate,
						thisQuarterStartDate=thisQuarterStartDate, thisQuarterEndDate=thisQuarterEndDate,
						lastQuarterStartDate=lastQuarterStartDate, lastQuarterEndDate=lastQuarterEndDate)
					report_form = reportForm(mineID=mineID, reportData=reportData)

					return render(request, 'report/report2.html', {'filterForm': filter_form, 'reportForm': report_form,
						'defaultFilterForm': default_filter_form,
						'dateVals': dateVals, 'commIDs': commIDs, 'commNameList': commNameList,
						'numStockpiles': list(range(1, numStockpiles+1)),
						'minePlanTonnageVals': minePlanTonnageVals, 'sumMinePlanTonnages': sumMinePlanTonnages,
						# 'minePlanHGTonnageVals': minePlanHGTonnageVals, 'minePlanLGTonnageVals': minePlanLGTonnageVals,
						# 'minePlanWasteTonnageVals': minePlanWasteTonnageVals, 'minePlanOverburdenTonnageVals': minePlanOverburdenTonnageVals,
						# 'sumMinePlanHGTonnage': sumMinePlanHGTonnage, 'sumMinePlanLGTonnage': sumMinePlanLGTonnage,
						# 'sumMinePlanWasteTonnage': sumMinePlanWasteTonnage, 'sumMinePlanOverburdenTonnage': sumMinePlanOverburdenTonnage,
						'tonnageVals': tonnageVals, 'tonnageTotals': tonnageTotals, 'gradeVals': gradeVals, 'moistures': moistures,
						# 'HGTonnageVals': HGTonnageVals, 'HGTonnageTotal': HGTonnageTotal, 'HGGradeVals': HGGradeVals, 'HGMoistures': HGMoistures,
						# 'LGTonnageVals': LGTonnageVals, 'LGTonnageTotal': LGTonnageTotal, 'LGGradeVals': LGGradeVals, 'LGMoistures': LGMoistures,
						'lumpTonnageVals': lumpTonnageVals, 'lumpTonnageTotal': lumpTonnageTotal, 'lumpGradeVals': lumpGradeVals, 'lumpMoistures': lumpMoistures,
						'finesTonnageVals': finesTonnageVals, 'finesTonnageTotal': finesTonnageTotal, 'finesGradeVals': finesGradeVals, 'finesMoistures': finesMoistures,
						'ultraFinesTonnageVals': ultraFinesTonnageVals, 'ultraFinesTonnageTotal': ultraFinesTonnageTotal, 'ultraFinesGradeVals': ultraFinesGradeVals, 'ultraFinesMoistures': ultraFinesMoistures,
						'totalProducts': totalProducts, 'sumTotalProducts': sumTotalProducts,
						'rejectsTonnageVals': rejectsTonnageVals, 'rejectsTonnageTotal': rejectsTonnageTotal, 'rejectsGradeVals': rejectsGradeVals, 'rejectsMoistures': rejectsMoistures,
						'fullShippingCosts': fullShippingCosts, 'fullExchangeRates': fullExchangeRates,
						'HGLumps': HGLumps, 'lumpPenaltyVals': lumpPenaltyVals, 'lumpSellingPrices': lumpSellingPrices, 'avgLumpSellingPrice': avgLumpSellingPrice,
						'netLumpPrices': netLumpPrices, 'avgNetLumpPrice': avgNetLumpPrice, 'exchangeNetLumpPrices': exchangeNetLumpPrices,
						'avgExchangeNetLumpPrice': avgExchangeNetLumpPrice,
						'HGFines': HGFines, 'finesPenaltyVals': finesPenaltyVals, 'finesSellingPrices': finesSellingPrices, 'avgFinesSellingPrice': avgFinesSellingPrice,
						'netFinesPrices': netFinesPrices, 'avgNetFinesPrice': avgNetFinesPrice, 'exchangeNetFinesPrices': exchangeNetFinesPrices,
						'avgExchangeNetFinesPrice': avgExchangeNetFinesPrice,
						'HGUltraFines': HGUltraFines, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals, 'ultraFinesSellingPrices': ultraFinesSellingPrices,
						'avgUltraFinesSellingPrice': avgUltraFinesSellingPrice,
						'netUltraFinesPrices': netUltraFinesPrices, 'exchangeNetUltraFinesPrices': exchangeNetUltraFinesPrices,
						'avgExchangeNetUltraFinesPrice': avgExchangeNetUltraFinesPrice,
						'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
						'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
						'totalRevenues': totalRevenues, 'sumTotalRevenues': sumTotalRevenues,
						'mining': mining, 'stockpileLG': stockpileLG, 'dewatering': dewatering, 'processing': processing, 'hauling': hauling,
						'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite, 'GARoom': GARoom, 'railTransport': railTransport, 'GACorp': GACorp,
						'sumMining': sumMining, 'sumStockpileLG': sumStockpileLG, 'sumDewatering': sumDewatering, 'sumProcessing': sumProcessing,
						'sumHauling': sumHauling, 'sumLoadOutRailLoop': sumLoadOutRailLoop, 'sumGASite': sumGASite, 'sumGARoom': sumGARoom,
						'sumRailTransport': sumRailTransport, 'sumGACorp': sumGACorp,
						'totalOPEX': totalOPEX, 'sumTotalOPEX':sumTotalOPEX, 'royalties': royalties, 'sumRoyalties': sumRoyalties,
						'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial, 'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
						'infraIndirectCost': infraIndirectCost, 'contingency': contingency, 'railcars': railcars, 'otherMobEquip': otherMobEquip,
						'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay, 'sumPreStrip': sumPreStrip,
						'sumMineEquipInitial': sumMineEquipInitial, 'sumMineEquipSustain': sumMineEquipSustain, 'sumInfraDirectCost': sumInfraDirectCost,
						'sumInfraIndirectCost': sumInfraIndirectCost, 'sumContingency': sumContingency, 'sumRailcars': sumRailcars,
						'sumOtherMobEquip': sumOtherMobEquip, 'sumClosureRehabAssure': sumClosureRehabAssure, 'sumDepoProvisionPay': sumDepoProvisionPay,
						'totalCAPEX': totalCAPEX, 'sumTotalCAPEX': sumTotalCAPEX,
						'federalTaxes': federalTaxes, 'provincialTaxes': provincialTaxes, 'miningTaxes': miningTaxes,
						'sumFederalTaxes': sumFederalTaxes, 'sumProvincialTaxes': sumProvincialTaxes, 'sumMiningTaxes': sumMiningTaxes,
						'totalTaxes': totalTaxes, 'sumTotalTaxes': sumTotalTaxes,
						'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
						'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG,
						'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
						'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
						'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
						'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
						'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
						'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
						'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})
						# 'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
						# 'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})

				latestCAPEX = tblCAPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				timestamp = latestCAPEX.dateAdded
				CAPEXEntries = tblCAPEX.objects.filter(mineID=int(mineID), dateAdded=timestamp)

				negCAPEX = []
				for year in [-3,-2,-1]:
					currCAPEX = CAPEXEntries.filter(year=year)
					if currCAPEX:
						row = currCAPEX[0]
						negCAPEX.append(round(Decimal(row.preStrip + row.mineEquipInitial + row.mineEquipSustain + 
							row.infraDirectCost + row.infraIndirectCost + row.contingency + row.railcars + 
							row.otherMobEquip + row.closureRehabAssure + row.depoProvisionPay + 
							row.workCapCurrentProd + row.workCapCostsLG + row.EPCM + row.ownerCost),2))
					else:
						negCAPEX.append(Decimal(0.0))
				sumNegCAPEX = sum(negCAPEX)

				tonnageVals = {}
				tonnageTotals = {}
				gradeVals = {}
				moistures = {}
				dailyTonnages = {}
				dailyGrades = {}
				for curr in range(1, numStockpiles+1):
					tonnageVals[curr] = []
					gradeVals[curr] = {}
					dailyTonnages[curr] = {}
					dailyGrades[curr] = {}

					# Tonnages
					MPTonnageEntries = tblMineProductTonnageOptimized.objects.filter(projectID=latestProject.projectID, stockpileID=curr, 
						date__gte=startDate, date__lte=endDate).order_by("date")
					cacheCheck = bool(MPTonnageEntries)

					for i in range(len(startDateVals)):
						dailyTonnages[curr][startDateVals[i]] = []
						subEntries = MPTonnageEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by("date")
						if subEntries:
							for entry in subEntries:
								dailyTonnages[curr][startDateVals[i]].append(entry.tonnage)
							subTotal = subEntries.aggregate(sumTonnage=Sum('tonnage'))
							tonnageVals[curr].append(subTotal['sumTonnage'])
						else:
							tonnageVals[curr].append(filler)
					tonnageTotals[curr] = sum([0 if x==filler else x for x in tonnageVals[curr]])

					# Grades
					for i in range(len(commIDs)):
						dailyGrades[curr][commNameList[i]] = {}
						currGrades = []
						MPGradeEntries = tblMineProductGradeOptimized.objects.filter(projectID=latestProject.projectID, stockpileID=curr,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(MPGradeEntries)

						for j in range(len(startDateVals)):
							dailyGrades[curr][commNameList[i]][startDateVals[j]] = []
							subEntries = MPGradeEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by("date")
							if subEntries:
								for entry in subEntries:
									dailyGrades[curr][commNameList[i]][startDateVals[j]].append(entry.grade)
								currGrades.append(round(np.average(dailyGrades[curr][commNameList[i]][startDateVals[j]], weights=dailyTonnages[curr][startDateVals[j]]),2))
							else:
								currGrades.append(filler)
						gradeVals[curr][commNameList[i]] = currGrades

					# Moistures
					moistures[curr] = [round(latestInput.feedMoisture,2)]*len(startDateVals)

				# Lump data if declared
				if 1 in PPIDs:
					lumpTonnageVals = []
					lumpGradeVals = {}
					lumpDailyTonnages = {}
					lumpDailyGrades = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=1,
						date__gte=startDate, date__lte=endDate).order_by("date")
					cacheCheck = bool(PPTonnageEntries)

					for i in range(len(startDateVals)):
						lumpDailyTonnages[startDateVals[i]] = []
						subEntries = PPTonnageEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by("date")
						if subEntries:
							for entry in subEntries:
								lumpDailyTonnages[startDateVals[i]].append(entry.tonnageDMT)
							subTotal = subEntries.aggregate(sumTonnage=Sum('tonnageDMT'))
							lumpTonnageVals.append(round(subTotal['sumTonnage'],2))
						else:
							lumpTonnageVals.append(filler)
					lumpTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in lumpTonnageVals])

					# currDate = startDate
					# for entry in PPTonnageEntries:
					# 	while currDate < entry.date:
					# 		lumpTonnageVals.append(filler)
					# 		currDate += datetime.timedelta(days=1)
					# 	lumpTonnageVals.append(round(Decimal(entry.tonnageDMT),2))
					# lumpTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in lumpTonnageVals])
					# lumpTonnageVals += [filler]*(endDate-currDate).days

					totalProducts = [x+y for x,y in zip(totalProducts, [Decimal(0.0) if x==filler else x for x in lumpTonnageVals])]


					# Grades
					for i in range(len(commIDs)):
						lumpDailyGrades[commNameList[i]] = {}
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(PPGradeEntries)

						for j in range(len(startDateVals)):
							lumpDailyGrades[commNameList[i]][startDateVals[j]] = []
							subEntries = PPGradeEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by("date")
							if subEntries:
								for entry in subEntries:
									lumpDailyGrades[commNameList[i]][startDateVals[j]].append(entry.grade)
								currGrades.append(round(np.average(lumpDailyGrades[commNameList[i]][startDateVals[j]], weights=lumpDailyTonnages[startDateVals[j]]),2))
							else:
								currGrades.append(filler)
						lumpGradeVals[commNameList[i]] = currGrades

					# # Grades
					# for i in range(len(commIDs)):
					# 	currGrades = []
					# 	PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1,
					# 		commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")

					# 	currDate = startDate
					# 	for entry in PPGradeEntries:
					# 		while currDate < entry.date:
					# 			currGrades.append(filler)
					# 			currDate += datetime.timedelta(days=1)
					# 		currGrades.append(round(entry.grade,2))
					# 	currGrades += [filler]*(endDate-currDate).days
					# 	lumpGradeVals[commNameList[i]] = currGrades

					# Moistures
					lumpMoistures = [round(latestInput.lumpMoisture,2)]*len(startDateVals)



				# Fines data if declared
				if 2 in PPIDs:
					finesTonnageVals = []
					finesGradeVals = {}
					finesDailyTonnages = {}
					finesDailyGrades = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=2,
						date__gte=startDate, date__lte=endDate).order_by("date")
					cacheCheck = bool(PPTonnageEntries)

					for i in range(len(startDateVals)):
						finesDailyTonnages[startDateVals[i]] = []
						subEntries = PPTonnageEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by("date")
						if subEntries:
							for entry in subEntries:
								finesDailyTonnages[startDateVals[i]].append(entry.tonnageDMT)
							subTotal = subEntries.aggregate(sumTonnage=Sum('tonnageDMT'))
							finesTonnageVals.append(round(subTotal['sumTonnage'],2))
						else:
							finesTonnageVals.append(filler)
					finesTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in finesTonnageVals])
					totalProducts = [x+y for x,y in zip(totalProducts, [Decimal(0.0) if x==filler else x for x in finesTonnageVals])]

					# Grades
					for i in range(len(commIDs)):
						finesDailyGrades[commNameList[i]] = {}
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(PPGradeEntries)

						for j in range(len(startDateVals)):
							finesDailyGrades[commNameList[i]][startDateVals[j]] = []
							subEntries = PPGradeEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by("date")
							if subEntries:
								for entry in subEntries:
									finesDailyGrades[commNameList[i]][startDateVals[j]].append(entry.grade)
								currGrades.append(round(np.average(finesDailyGrades[commNameList[i]][startDateVals[j]], weights=finesDailyTonnages[startDateVals[j]]),2))
							else:
								currGrades.append(filler)
						finesGradeVals[commNameList[i]] = currGrades

					# Moistures
					finesMoistures = [round(latestInput.finesMoisture,2)]*len(startDateVals)


				# Ultra Fines data if declared
				if 3 in PPIDs:
					ultraFinesTonnageVals = []
					ultraFinesGradeVals = {}
					ultraFinesDailyTonnages = {}
					ultraFinesDailyGrades = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=3,
						date__gte=startDate, date__lte=endDate).order_by("date")
					cacheCheck = bool(PPTonnageEntries)

					for i in range(len(startDateVals)):
						ultraFinesDailyTonnages[startDateVals[i]] = []
						subEntries = PPTonnageEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by("date")
						if subEntries:
							for entry in subEntries:
								ultraFinesDailyTonnages[startDateVals[i]].append(entry.tonnageDMT)
							subTotal = subEntries.aggregate(sumTonnage=Sum('tonnageDMT'))
							ultraFinesTonnageVals.append(round(subTotal['sumTonnage'],2))
						else:
							ultraFinesTonnageVals.append(filler)
					ultraFinesTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in ultraFinesTonnageVals])
					totalProducts = [x+y for x,y in zip(totalProducts, [Decimal(0.0) if x==filler else x for x in ultraFinesTonnageVals])]

					# Grades
					for i in range(len(commIDs)):
						ultraFinesDailyGrades[commNameList[i]] = {}
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(PPGradeEntries)

						for j in range(len(startDateVals)):
							ultraFinesDailyGrades[commNameList[i]][startDateVals[j]] = []
							subEntries = PPGradeEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by("date")
							if subEntries:
								for entry in subEntries:
									ultraFinesDailyGrades[commNameList[i]][startDateVals[j]].append(entry.grade)
								currGrades.append(round(np.average(ultraFinesDailyGrades[commNameList[i]][startDateVals[j]], weights=ultraFinesDailyTonnages[startDateVals[j]]),2))
							else:
								currGrades.append(filler)
						ultraFinesGradeVals[commNameList[i]] = currGrades

					# Moistures
					ultraFinesMoistures = [round(latestInput.ultraFinesMoisture,2)]*len(startDateVals)


				# Rejects data if declared
				if 4 in PPIDs:
					rejectsTonnageVals = []
					rejectsGradeVals = {}
					rejectsDailyTonnages = {}
					rejectsDailyGrades = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=4,
						date__gte=startDate, date__lte=endDate).order_by("date")
					cacheCheck = bool(PPTonnageEntries)

					for i in range(len(startDateVals)):
						rejectsDailyTonnages[startDateVals[i]] = []
						subEntries = PPTonnageEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by("date")
						if subEntries:
							for entry in subEntries:
								rejectsDailyTonnages[startDateVals[i]].append(entry.tonnageDMT)
							subTotal = subEntries.aggregate(sumTonnage=Sum('tonnageDMT'))
							rejectsTonnageVals.append(round(subTotal['sumTonnage'],2))
						else:
							rejectsTonnageVals.append(filler)
					rejectsTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in ultraFinesTonnageVals])
					# totalProducts = [x+y for x,y in zip(totalProducts, [Decimal(0.0) if x==filler else x for x in ultraFinesTonnageVals])]

					# Grades
					for i in range(len(commIDs)):
						rejectsDailyGrades[commNameList[i]] = {}
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=4,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(PPGradeEntries)

						for j in range(len(startDateVals)):
							rejectsDailyGrades[commNameList[i]][startDateVals[j]] = []
							subEntries = PPGradeEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by("date")
							if subEntries:
								for entry in subEntries:
									rejectsDailyGrades[commNameList[i]][startDateVals[j]].append(entry.grade)
								currGrades.append(round(np.average(rejectsDailyGrades[commNameList[i]][startDateVals[j]], weights=rejectsDailyTonnages[startDateVals[j]]),2))
							else:
								currGrades.append(filler)
						rejectsGradeVals[commNameList[i]] = currGrades

					# Moistures
					rejectsMoistures = [round(latestInput.rejectsMoisture,2)]*len(startDateVals)

				# sumTotalProducts
				sumTotalProducts = sum(totalProducts)


				# Plant Product Selling Prices
				if 1 in PPIDs:
					sumLumpPenalties = [Decimal(0.0)]*len(startDateVals)
					HGLumps = [Decimal(priceEntry.lump)]*len(startDateVals)
					lumpPenaltyVals = {}
					for i in range(len(commIDs)):
						tempPenalties = []
						penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1, commodityID=commIDs[i],
								date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(penaltyEntries)
						
						for j in range(len(startDateVals)):
							subEntries = penaltyEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by('date')								
							if subEntries:
								dailyPens = []
								for entry in subEntries:
									dailyPens.append(entry.penalty)
								tempPenalties.append(round(Decimal(np.average(dailyPens, weights=lumpDailyTonnages[startDateVals[j]])),2))
							else:
								tempPenalties.append(filler)
						lumpPenaltyVals[commNameList[i]] = tempPenalties
						sumLumpPenalties = [x+y for x,y in zip(sumLumpPenalties, [Decimal(0.0) if x==filler else x for x in tempPenalties])]

						# currDate = startDate
						# for entry in penaltyEntries:
						# 	while currDate < entry.date:
						# 		tempPenalties.append(filler)
						# 		currDate += datetime.timedelta(days=1)
						# 	tempPenalties.append(round(Decimal(entry.penalty),2))
						# tempPenalties += [filler]*(endDate-currDate).days
						# lumpPenaltyVals[commNameList[i]] = tempPenalties
						# sumLumpPenalties = [x+y for x,y in zip(sumLumpPenalties, [Decimal(0.0) if x==filler else x for x in tempPenalties])]

					lumpSellingPrices = list(map(operator.add, HGLumps, sumLumpPenalties))
					finalLumpSellingPrices = [filler if y==filler else x for x,y in zip(lumpSellingPrices,tempPenalties)]					
					avgLumpSellingPrice = round(np.average([float(x) for x in lumpSellingPrices], 
						weights=[0.0 if x==filler else float(x) for x in lumpTonnageVals]),2)
					netLumpPrices = list(map(operator.sub, lumpSellingPrices, fullShippingCosts))
					finalNetLumpPrices = [filler if y==filler else x for x,y in zip(netLumpPrices,tempPenalties)]
					avgNetLumpPrice = round(Decimal(np.average([float(x) for x in netLumpPrices], 
						weights=[0.0 if x==filler else float(x) for x in lumpTonnageVals])),2)
					exchangeNetLumpPrices = list(map(operator.mul, fullExchangeRates, netLumpPrices))
					exchangeNetLumpPrices = [round(x,2) for x in exchangeNetLumpPrices]
					finalExchangeNetLumpPrices = [filler if y==filler else x for x,y in zip(exchangeNetLumpPrices,tempPenalties)]
					avgExchangeNetLumpPrice = round(avgNetLumpPrice*fullExchangeRates[0], 2)

					lumpSellingPrices = finalLumpSellingPrices
					netLumpPrices = finalNetLumpPrices
					exchangeNetLumpPrices = finalExchangeNetLumpPrices


				if 2 in PPIDs:
					sumFinesPenalties = [Decimal(0.0)]*len(startDateVals)
					HGFines = [Decimal(priceEntry.fines)]*len(startDateVals)
					finesPenaltyVals = {}
					for i in range(len(commIDs)):
						tempPenalties = []
						penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2, commodityID=commIDs[i],
								date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(penaltyEntries)
						
						for j in range(len(startDateVals)):
							subEntries = penaltyEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by('date')								
							if subEntries:
								dailyPens = []
								for entry in subEntries:
									dailyPens.append(entry.penalty)
								tempPenalties.append(round(Decimal(np.average(dailyPens, weights=finesDailyTonnages[startDateVals[j]])),2))
							else:
								tempPenalties.append(filler)
						finesPenaltyVals[commNameList[i]] = tempPenalties
						sumFinesPenalties = [x+y for x,y in zip(sumFinesPenalties, [Decimal(0.0) if x==filler else x for x in tempPenalties])]

					finesSellingPrices = list(map(operator.add, HGFines, sumFinesPenalties))
					finalFinesSellingPrices = [filler if y==filler else x for x,y in zip(finesSellingPrices,tempPenalties)]					
					avgFinesSellingPrice = round(np.average([float(x) for x in finesSellingPrices], 
						weights=[0.0 if x==filler else float(x) for x in finesTonnageVals]),2)
					netFinesPrices = list(map(operator.sub, finesSellingPrices, fullShippingCosts))
					finalNetFinesPrices = [filler if y==filler else x for x,y in zip(netFinesPrices,tempPenalties)]
					avgNetFinesPrice = round(Decimal(np.average([float(x) for x in netFinesPrices], 
						weights=[0.0 if x==filler else float(x) for x in finesTonnageVals])),2)
					exchangeNetFinesPrices = list(map(operator.mul, fullExchangeRates, netFinesPrices))
					exchangeNetFinesPrices = [round(x,2) for x in exchangeNetFinesPrices]
					finalExchangeNetFinesPrices = [filler if y==filler else x for x,y in zip(exchangeNetFinesPrices,tempPenalties)]
					avgExchangeNetFinesPrice = round(avgNetFinesPrice*fullExchangeRates[0], 2)

					finesSellingPrices = finalFinesSellingPrices
					netFinesPrices = finalNetFinesPrices
					exchangeNetFinesPrices = finalExchangeNetFinesPrices


				if 3 in PPIDs:
					sumUltraFinesPenalties = [Decimal(0.0)]*len(startDateVals)
					HGUltraFines = [Decimal(priceEntry.ultraFines)]*len(startDateVals)
					ultraFinesPenaltyVals = {}
					for i in range(len(commIDs)):
						tempPenalties = []
						penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3, commodityID=commIDs[i],
								date__gte=startDate, date__lte=endDate).order_by("date")
						cacheCheck = bool(penaltyEntries)
						
						for j in range(len(startDateVals)):
							subEntries = penaltyEntries.filter(date__gte=startDateVals[j], date__lte=endDateVals[j]).order_by('date')								
							if subEntries:
								dailyPens = []
								for entry in subEntries:
									dailyPens.append(entry.penalty)
								tempPenalties.append(round(Decimal(np.average(dailyPens, weights=ultraFinesDailyTonnages[startDateVals[j]])),2))
							else:
								tempPenalties.append(filler)
						ultraFinesPenaltyVals[commNameList[i]] = tempPenalties
						sumUltraFinesPenalties = [x+y for x,y in zip(sumUltraFinesPenalties, [Decimal(0.0) if x==filler else x for x in tempPenalties])]

					ultraFinesSellingPrices = list(map(operator.add, HGUltraFines, sumUltraFinesPenalties))
					finalUltraFinesSellingPrices = [filler if y==filler else x for x,y in zip(ultraFinesSellingPrices,tempPenalties)]
					avgUltraFinesSellingPrice = round(np.average([float(x) for x in ultraFinesSellingPrices], 
						weights=[0.0 if x==filler else float(x) for x in ultraFinesTonnageVals]),2)
					netUltraFinesPrices = list(map(operator.sub, ultraFinesSellingPrices, fullShippingCosts))
					finalNetUltraFinesPrices = [filler if y==filler else x for x,y in zip(netUltraFinesPrices,tempPenalties)]
					avgNetUltraFinesPrice = round(Decimal(np.average([float(x) for x in netUltraFinesPrices], 
						weights=[0.0 if x==filler else float(x) for x in ultraFinesTonnageVals])),2)
					exchangeNetUltraFinesPrices = list(map(operator.mul, fullExchangeRates, netUltraFinesPrices))
					exchangeNetUltraFinesPrices = [round(x,2) for x in exchangeNetUltraFinesPrices]
					finalExchangeNetUltraFinesPrices = [filler if y==filler else x for x,y in zip(exchangeNetUltraFinesPrices,tempPenalties)]
					avgExchangeNetUltraFinesPrice = round(avgNetUltraFinesPrice*fullExchangeRates[0], 2)

					ultraFinesSellingPrices = finalUltraFinesSellingPrices
					netUltraFinesPrices = finalNetUltraFinesPrices
					exchangeNetUltraFinesPrices = finalExchangeNetUltraFinesPrices


				# Handle Revenues Section
				if 1 in PPIDs:
					lumpRevenues = []
					revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=1,
						date__gte=startDate, date__lte=endDate).order_by("date")
					cacheCheck = bool(revenueEntries)

					for i in range(len(startDateVals)):
						subEntries = revenueEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by('date')
						if subEntries:
							subTotal = subEntries.aggregate(sumRevenue=Sum('plantProductRevenue'))
							lumpRevenues.append(round(Decimal(subTotal['sumRevenue']),2))
						else:
							lumpRevenues.append(filler)

					# currDate = startDate
					# for entry in revenueEntries:
					# 	while currDate < entry.date:
					# 		lumpRevenues.append(filler)
					# 		currDate += datetime.timedelta(days=1)
					# 	lumpRevenues.append(round(Decimal(entry.plantProductRevenue),2))
					# lumpRevenues += [filler]*(endDate-currDate).days

					sumLumpRevenues = sum([Decimal(0.0) if x==filler else x for x in lumpRevenues])
					lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, [Decimal(0.0) if x==filler else x for x in lumpRevenues]))
					totalRevenues = list(map(operator.add, totalRevenues, [Decimal(0.0) if x==filler else x for x in lumpRevenues]))

				if 2 in PPIDs:
					finesRevenues = []
					revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=2,
						date__gte=startDate, date__lte=endDate).order_by("date")
					cacheCheck = bool(revenueEntries)

					for i in range(len(startDateVals)):
						subEntries = revenueEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by('date')
						if subEntries:
							subTotal = subEntries.aggregate(sumRevenue=Sum('plantProductRevenue'))
							finesRevenues.append(round(Decimal(subTotal['sumRevenue']),2))
						else:
							finesRevenues.append(filler)

					sumFinesRevenues = sum([Decimal(0.0) if x==filler else x for x in finesRevenues])
					lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, [Decimal(0.0) if x==filler else x for x in finesRevenues]))
					totalRevenues = list(map(operator.add, totalRevenues, [Decimal(0.0) if x==filler else x for x in finesRevenues]))

				if 3 in PPIDs:
					ultraFinesRevenues = []
					revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=3,
						date__gte=startDate, date__lte=endDate).order_by("date")

					for i in range(len(startDateVals)):
						subEntries = revenueEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by('date')
						if subEntries:
							subTotal = subEntries.aggregate(sumRevenue=Sum('plantProductRevenue'))
							ultraFinesRevenues.append(round(Decimal(subTotal['sumRevenue']),2))
						else:
							ultraFinesRevenues.append(filler)

					sumUltraFinesRevenues = sum([Decimal(0.0) if x==filler else x for x in ultraFinesRevenues])
					# lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, [0.0 if x==filler else x for x in finesRevenues]))
					totalRevenues = list(map(operator.add, totalRevenues, [Decimal(0.0) if x==filler else x for x in ultraFinesRevenues]))

				sumTotalRevenues = sum(totalRevenues)


				cashFlowPreTax = []
				cashFlowPostTax = []
				cumCashFlowPreTax = []
				cumCashFlowPostTax = []

				annualCashFlowPreTax = []
				annualCashFlowPostTax = []
				annualCumCashFlowPreTax = []
				annualCumCashFlowPostTax = []
				# Beginning populating tblCashFlow data for HTML report here
				currCumCashFlowPreTax = (-1)*sumNegCAPEX
				currCumCashFlowPostTax = (-1)*sumNegCAPEX

				cashFlowEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID)
				for year in range(1, projectPeriods.count()+1):
					currPeriod = projectPeriods.get(year=year)
					currStart = currPeriod.startDate
					currEnd = currPeriod.endDate
					currCashFlows = cashFlowEntries.filter(date__gte=currStart, date__lte=currEnd).order_by('-date')
					if not currCashFlows:
						annualCumCashFlowPreTax.append(currCumCashFlowPreTax)
						annualCumCashFlowPostTax.append(currCumCashFlowPostTax)
						annualCashFlowPreTax.append(Decimal(0.0))
						annualCashFlowPostTax.append(Decimal(0.0))
					else:
						lastCashFlow = currCashFlows[0]
						annualCumCashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax),2))
						annualCumCashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax),2))
						annualCashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax) - currCumCashFlowPreTax,2))
						annualCashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax) - currCumCashFlowPostTax,2))
						currCumCashFlowPreTax = annualCumCashFlowPreTax[-1]
						currCumCashFlowPostTax = annualCumCashFlowPostTax[-1]
				preTaxIRR = round(np.irr([(-1)*sumNegCAPEX] + annualCashFlowPreTax)*100,2)
				postTaxIRR = round(np.irr([(-1)*sumNegCAPEX] + annualCashFlowPostTax)*100,2)

				prevCashFlows = cashFlowEntries.filter(date__lt=startDateVals[0]).order_by('-date')
				if not prevCashFlows:
					currCumCashFlowPreTax = (-1)*sumNegCAPEX
					currCumCashFlowPostTax = (-1)*sumNegCAPEX
				else:
					currCumCashFlowPreTax = round(Decimal(prevCashFlows[0].cumulativeCashFlowPreTax),2)
					currCumCashFlowPostTax = round(Decimal(prevCashFlows[0].cumulativeCashFlowPostTax),2)
				for i in range(len(startDateVals)):
					currCashFlows = cashFlowEntries.filter(date__gte=startDateVals[i], date__lte=endDateVals[i]).order_by('-date')
					if not currCashFlows:
						cumCashFlowPreTax.append(currCumCashFlowPreTax)
						cumCashFlowPostTax.append(currCumCashFlowPostTax)
						cashFlowPreTax.append(Decimal(0.0))
						cashFlowPostTax.append(Decimal(0.0))
					else:
						lastCashFlow = currCashFlows[0]
						cumCashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax),2))
						cumCashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax),2))
						cashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax) - currCumCashFlowPreTax,2))
						cashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax) - currCumCashFlowPostTax,2))
						currCumCashFlowPreTax = cumCashFlowPreTax[-1]
						currCumCashFlowPostTax = cumCashFlowPostTax[-1]
				sumCashFlowPreTax = sum(cashFlowPreTax)
				sumCashFlowPostTax = sum(cashFlowPostTax)

				positiveFlow = False
				paybackPreTax = []
				if cumCashFlowPreTax[0] > 0:
					paybackPreTax = [Decimal(0.0)]*len(startDateVals)
				else:
					for i in range(len(cumCashFlowPreTax)):
						if positiveFlow:
							paybackPreTax.append(Decimal(0.0))
						else:
							if cumCashFlowPreTax[i] > 0:
								if i == 0:
									paybackPreTax.append(Decimal(0.0))
								else:
									paybackPreTax.append(abs(round(cumCashFlowPreTax[i-1] / cashFlowPreTax[i],4)))
								positiveFlow = True
							else:
								paybackPreTax.append(Decimal(1.0))
				sumPaybackPreTax = sum(paybackPreTax)

				positiveFlow = False
				paybackPostTax = []
				if cumCashFlowPostTax[0] > 0:
					paybackPostTax = [Decimal(0.0)]*len(startDateVals)
				else:
					for i in range(len(cumCashFlowPostTax)):
						if positiveFlow:
							paybackPostTax.append(Decimal(0.0))
						else:
							if cumCashFlowPostTax[i] > 0:
								if i == 0:
									paybackPostTax.append(Decimal(0.0))
								else:
									paybackPostTax.append(abs(round(cumCashFlowPostTax[i-1] / cashFlowPostTax[i],4)))
								positiveFlow = True
							else:
								paybackPostTax.append(Decimal(1.0))
				sumPaybackPostTax = sum(paybackPostTax)

				# Calculate and Update NPVs and IRRs
				# preTaxNPVs = []
				# postTaxNPVs = []
				# NPVCashFlowPreTax = [(-1)*sumNegCAPEX] + cashFlowPreTax
				# NPVCashFlowPostTax = [(-1)*sumNegCAPEX] + cashFlowPostTax
				# preTaxIRR = round(np.irr(NPVCashFlowPreTax)*100,2)
				# postTaxIRR = round(np.irr(NPVCashFlowPostTax)*100,2)
				# for rate in discountRates:
				# 	preTaxNPVs.append(round(np.npv(rate, NPVCashFlowPreTax),2))
				# 	postTaxNPVs.append(round(np.npv(rate, NPVCashFlowPostTax),2))

				preTaxPVs = {}
				postTaxPVs = {}
				sumPreTaxNPV = {}
				sumPostTaxNPV = {}
				financialsEntries = tblFinancials.objects.filter(projectID=latestProject.projectID)
				for rate in discountRates:
					rate = int(round(rate*100))
					preTaxPVs[rate] = []
					postTaxPVs[rate] = []

					for i in range(len(startDateVals)):
						currPVs = financialsEntries.filter(discountRate=rate,
							date__lte=endDateVals[i], date__gte=startDateVals[i])
						if not currPVs:
							preTaxPVs[rate].append(Decimal(0.0))
							postTaxPVs[rate].append(Decimal(0.0))
						else:
							sumPVPreTax = currPVs.aggregate(sumPVPreTax=Sum('NPVPreTax'))
							sumPVPostTax = currPVs.aggregate(sumPVPostTax=Sum('NPVPostTax'))
							preTaxPVs[rate].append(round(sumPVPreTax['sumPVPreTax'],2))
							postTaxPVs[rate].append(round(sumPVPostTax['sumPVPostTax'],2))
					sumPreTaxNPV[rate] = sum(preTaxPVs[rate])
					sumPostTaxNPV[rate] = sum(postTaxPVs[rate])				

				# Create DL Form Data
				reportRowCount = 1

				reportData = ""

				currRow = 'Item,'
				for date in dateVals:
					# currRow += 'Year{0},'.format(year)
					currRow += date + ','
				currRow += 'Total;'
				reportData += currRow

				reportData += ";Mining;"
				for curr in range(1, numStockpiles+1):
					currRow = "Stockpile {0} Ore (kt),".format(curr) + ''.join([*[str(round(x,2))+',' for x in minePlanTonnageVals[curr]]]) + str(round(sumMinePlanTonnages[curr],2)) + ";"
					reportData += currRow

				reportData += ";Processing;"
				for curr in range(1, numStockpiles+1):
					reportData += "Stockpile {0} Ore;".format(curr)
					currRow = 'Tonnage (kt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]) + ',' + str(round(tonnageTotals[curr],2)) + ";"
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]) + ';'

				reportData += ";Plant Product;"

				if 1 in PPIDs:
					reportData += "Lump;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]) + ',' + str(round(lumpTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]) + ';'

				if 2 in PPIDs:
					reportData += "Fines;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]) + ',' + str(round(finesTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]) + ';'

				if 3 in PPIDs:
					reportData += "Ultra Fines;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]) + ',' + str(round(ultraFinesTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]) + ';'

				reportData += 'Total Product (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]) + ',' + str(round(sumTotalProducts,2)) + ';'

				if 4 in PPIDs:
					reportData += "Rejects;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]) + ',' + str(round(rejectsTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]) + ';'

				reportData += ";Products Selling Price;"

				if 1 in PPIDs:
					reportData += 'Lump Selling Price (USD/dmt);'
					reportData += 'Lump Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]) + ';'
					for i in range(len(commIDs)):
						reportData += 'Lump {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]) + ';'
					reportData += 'Lump Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]) + ',' + 'Avg: ' + str(round(avgLumpSellingPrice,2)) + ';'
					reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
					reportData += 'Net Lump Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]) + ',' + 'Avg: ' + str(round(avgNetLumpPrice,2)) + ';'
					reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
					reportData += 'Net Lump Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetLumpPrice,2)) + ';'

				if 2 in PPIDs:
					reportData += 'Fines Selling Price (USD/dmt);'
					reportData += 'Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]) + ';'
					for i in range(len(commIDs)):
						reportData += 'Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]) + ';'
					reportData += 'Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]) + ',' + 'Avg: ' + str(round(avgFinesSellingPrice,2)) + ';'
					reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
					reportData += 'Net Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]) + ',' + 'Avg: ' + str(round(avgNetFinesPrice,2)) + ';'
					reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
					reportData += 'Net Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetFinesPrice,2)) + ';'

				if 3 in PPIDs:
					reportData += 'Ultra Fines Selling Price (USD/dmt);'
					reportData += 'Ultra Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]) + ';'
					for i in range(len(commIDs)):
						reportData += 'Ultra Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]) + ';'
					reportData += 'Ultra Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]) + ',' + 'Avg: ' + str(round(avgUltraFinesSellingPrice,2)) + ';'
					reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
					reportData += 'Net Ultra Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]) + ',' + 'Avg: ' + str(round(avgNetUltraFinesPrice,2)) + ';'
					reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
					reportData += 'Net Ultra Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetUltraFinesPrice,2)) + ';'

				reportData += ';Revenues;'
				if 1 in PPIDs:
					reportData += 'Lump Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]]) + ',' + str(round(sumLumpRevenues,2)) + ';'
				if 2 in PPIDs:
					reportData += 'Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]]) + ',' + str(round(sumFinesRevenues,2)) + ';'
				if 3 in PPIDs:
					reportData += 'Ultra Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]]) + ',' + str(round(sumUltraFinesRevenues,2)) + ';'
				reportData += 'TOTAL REVENUE,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'

				reportData += ';COSTS;'
				reportData += 'OPEX (millions CAD);'
				reportData += 'Mining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mining]]) + ',' + str(round(sumMining,2)) + ';'
				reportData += 'Stockpile LG Reclaiming,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]]) + ',' + str(round(sumStockpileLG,2)) + ';'
				reportData += 'Pit Dewatering,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]]) + ',' + str(round(sumDewatering,2)) + ';'
				reportData += 'Processing,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in processing]]) + ',' + str(round(sumProcessing,2)) + ';'
				reportData += 'Product Hauling,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]]) + ',' + str(round(sumHauling,2)) + ';'
				reportData += 'Load-out and Rail Loop,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]]) + ',' + str(round(sumLoadOutRailLoop,2)) + ';'
				reportData += 'G&A (Site),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]]) + ',' + str(round(sumGASite,2)) + ';'
				reportData += 'G&A (Room & Board / FIFO),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]]) + ',' + str(round(sumGARoom,2)) + ';'
				reportData += 'Rail Transportation Port and Shiploading,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]]) + ',' + str(round(sumRailTransport,2)) + ';'
				reportData += 'Corporate G&A,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]]) + ',' + str(round(sumGACorp,2)) + ';'
				reportData += 'TOTAL OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
				reportData += 'ROYALTIES (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'

				reportData += 'CAPEX (millions CAD);'
				reportData += 'Pre-Stripping,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]]) + ',' + str(round(sumPreStrip,2)) + ';'
				reportData += 'Mining Equipment Initial,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]]) + ',' + str(round(sumMineEquipInitial,2)) + ';'
				reportData += 'Mining Equipment Sustaining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]]) + ',' + str(round(sumMineEquipSustain,2)) + ';'
				reportData += 'Project Infrastructure Direct Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]]) + ',' + str(round(sumInfraDirectCost,2)) + ';'
				reportData += 'Project Infrastructure Indirect Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]]) + ',' + str(round(sumInfraIndirectCost,2)) + ';'
				reportData += 'Project Infrastructure Contingency,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]]) + ',' + str(round(sumContingency,2)) + ';'
				reportData += 'Railcars,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]]) + ',' + str(round(sumRailcars,2)) + ';'
				reportData += 'Other Mobile Equipment,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]]) + ',' + str(round(sumOtherMobEquip,2)) + ';'
				reportData += 'Closure and Rehab Assurance Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]]) + ',' + str(round(sumClosureRehabAssure,2)) + ';'
				reportData += 'Deposits Provision Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]]) + ',' + str(round(sumDepoProvisionPay,2)) + ';'
				reportData += 'TOTAL CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'

				reportData += 'TAXES (millions CAD);'
				reportData += 'Federal Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]]) + ',' + str(round(sumFederalTaxes,2)) + ';'
				reportData += 'Provincial Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]]) + ',' + str(round(sumProvincialTaxes,2)) + ';'
				reportData += 'Mining Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]]) + ',' + str(round(sumMiningTaxes,2)) + ';'
				reportData += 'TOTAL (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

				reportData += ';SUMMARY;'
				reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'
				reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
				reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
				reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
				reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
				reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
				reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

				reportData += ';PRE-TAX CASH FLOW;'
				reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + str(round(sumCashFlowPreTax,2)) + ';'
				reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ';'
				reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + str(round(sumPaybackPreTax,2)) + ';'
				for rate in discountRates:
					reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPreTaxNPV[int(round(rate*100))],2)) + ';'
				reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(preTaxIRR,2)) + ';'

				reportData += ';POST-TAX CASH FLOW;'
				reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + str(round(sumCashFlowPostTax,2)) + ';'
				reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ';'
				reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + str(round(sumPaybackPostTax,2)) + ';'
				for rate in discountRates:
					reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPostTaxNPV[int(round(rate*100))],2)) + ';'
				reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(postTaxIRR,2)) + ';'


				filter_form = filterForm(mineID=mineID, startDate=projectStartDate, endDate=projectEndDate)
				default_filter_form = defaultFilterForm(mineID=mineID, thisYearStartDate=thisYearStartDate, thisYearEndDate=thisYearEndDate,
					lastYearStartDate=lastYearStartDate, lastYearEndDate=lastYearEndDate,
					thisQuarterStartDate=thisQuarterStartDate, thisQuarterEndDate=thisQuarterEndDate,
					lastQuarterStartDate=lastQuarterStartDate, lastQuarterEndDate=lastQuarterEndDate)
				report_form = reportForm(mineID=mineID, reportData=reportData)

				return render(request, 'report/report2.html', {'filterForm': filter_form, 'reportForm': report_form,
					'defaultFilterForm': default_filter_form,
					'dateVals': dateVals, 'commIDs': commIDs, 'commNameList': commNameList,
					'numStockpiles': list(range(1, numStockpiles+1)),
					'minePlanTonnageVals': minePlanTonnageVals, 'sumMinePlanTonnages': sumMinePlanTonnages,
					# 'minePlanHGTonnageVals': minePlanHGTonnageVals, 'minePlanLGTonnageVals': minePlanLGTonnageVals,
					# 'minePlanWasteTonnageVals': minePlanWasteTonnageVals, 'minePlanOverburdenTonnageVals': minePlanOverburdenTonnageVals,
					# 'sumMinePlanHGTonnage': sumMinePlanHGTonnage, 'sumMinePlanLGTonnage': sumMinePlanLGTonnage,
					# 'sumMinePlanWasteTonnage': sumMinePlanWasteTonnage, 'sumMinePlanOverburdenTonnage': sumMinePlanOverburdenTonnage,
					'tonnageVals': tonnageVals, 'tonnageTotals': tonnageTotals, 'gradeVals': gradeVals, 'moistures': moistures,
					# 'HGTonnageVals': HGTonnageVals, 'HGTonnageTotal': HGTonnageTotal, 'HGGradeVals': HGGradeVals, 'HGMoistures': HGMoistures,
					# 'LGTonnageVals': LGTonnageVals, 'LGTonnageTotal': LGTonnageTotal, 'LGGradeVals': LGGradeVals, 'LGMoistures': LGMoistures,
					'lumpTonnageVals': lumpTonnageVals, 'lumpTonnageTotal': lumpTonnageTotal, 'lumpGradeVals': lumpGradeVals, 'lumpMoistures': lumpMoistures,
					'finesTonnageVals': finesTonnageVals, 'finesTonnageTotal': finesTonnageTotal, 'finesGradeVals': finesGradeVals, 'finesMoistures': finesMoistures,
					'ultraFinesTonnageVals': ultraFinesTonnageVals, 'ultraFinesTonnageTotal': ultraFinesTonnageTotal, 'ultraFinesGradeVals': ultraFinesGradeVals, 'ultraFinesMoistures': ultraFinesMoistures,
					'totalProducts': totalProducts, 'sumTotalProducts': sumTotalProducts,
					'rejectsTonnageVals': rejectsTonnageVals, 'rejectsTonnageTotal': rejectsTonnageTotal, 'rejectsGradeVals': rejectsGradeVals, 'rejectsMoistures': rejectsMoistures,
					'fullShippingCosts': fullShippingCosts, 'fullExchangeRates': fullExchangeRates,
					'HGLumps': HGLumps, 'lumpPenaltyVals': lumpPenaltyVals, 'lumpSellingPrices': lumpSellingPrices, 'avgLumpSellingPrice': avgLumpSellingPrice,
					'netLumpPrices': netLumpPrices, 'avgNetLumpPrice': avgNetLumpPrice, 'exchangeNetLumpPrices': exchangeNetLumpPrices,
					'avgExchangeNetLumpPrice': avgExchangeNetLumpPrice,
					'HGFines': HGFines, 'finesPenaltyVals': finesPenaltyVals, 'finesSellingPrices': finesSellingPrices, 'avgFinesSellingPrice': avgFinesSellingPrice,
					'netFinesPrices': netFinesPrices, 'avgNetFinesPrice': avgNetFinesPrice, 'exchangeNetFinesPrices': exchangeNetFinesPrices,
					'avgExchangeNetFinesPrice': avgExchangeNetFinesPrice,
					'HGUltraFines': HGUltraFines, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals, 'ultraFinesSellingPrices': ultraFinesSellingPrices,
					'avgUltraFinesSellingPrice': avgUltraFinesSellingPrice,
					'netUltraFinesPrices': netUltraFinesPrices, 'exchangeNetUltraFinesPrices': exchangeNetUltraFinesPrices,
					'avgExchangeNetUltraFinesPrice': avgExchangeNetUltraFinesPrice,
					'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
					'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
					'totalRevenues': totalRevenues, 'sumTotalRevenues': sumTotalRevenues,
					'mining': mining, 'stockpileLG': stockpileLG, 'dewatering': dewatering, 'processing': processing, 'hauling': hauling,
					'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite, 'GARoom': GARoom, 'railTransport': railTransport, 'GACorp': GACorp,
					'sumMining': sumMining, 'sumStockpileLG': sumStockpileLG, 'sumDewatering': sumDewatering, 'sumProcessing': sumProcessing,
					'sumHauling': sumHauling, 'sumLoadOutRailLoop': sumLoadOutRailLoop, 'sumGASite': sumGASite, 'sumGARoom': sumGARoom,
					'sumRailTransport': sumRailTransport, 'sumGACorp': sumGACorp,
					'totalOPEX': totalOPEX, 'sumTotalOPEX':sumTotalOPEX, 'royalties': royalties, 'sumRoyalties': sumRoyalties,
					'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial, 'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
					'infraIndirectCost': infraIndirectCost, 'contingency': contingency, 'railcars': railcars, 'otherMobEquip': otherMobEquip,
					'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay, 'sumPreStrip': sumPreStrip,
					'sumMineEquipInitial': sumMineEquipInitial, 'sumMineEquipSustain': sumMineEquipSustain, 'sumInfraDirectCost': sumInfraDirectCost,
					'sumInfraIndirectCost': sumInfraIndirectCost, 'sumContingency': sumContingency, 'sumRailcars': sumRailcars,
					'sumOtherMobEquip': sumOtherMobEquip, 'sumClosureRehabAssure': sumClosureRehabAssure, 'sumDepoProvisionPay': sumDepoProvisionPay,
					'totalCAPEX': totalCAPEX, 'sumTotalCAPEX': sumTotalCAPEX,
					'federalTaxes': federalTaxes, 'provincialTaxes': provincialTaxes, 'miningTaxes': miningTaxes,
					'sumFederalTaxes': sumFederalTaxes, 'sumProvincialTaxes': sumProvincialTaxes, 'sumMiningTaxes': sumMiningTaxes,
					'totalTaxes': totalTaxes, 'sumTotalTaxes': sumTotalTaxes,
					'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
					'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG,
					'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
					'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
					'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
					'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
					'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
					'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
					'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})
					# 'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
					# 'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})


		elif "applyFilter" in request.POST:
			filler = ""
			mineID = request.session["mineID"]
			mineMatch = tblMine.objects.get(mineID=int(mineID))

			# Check project exists
			projectsList  = tblProject.objects.filter(mineID=mineID)
			if not projectsList:
				return render(request, "report/noProjects.html", {})

			# # Get LOM of the mine's most recent project
			latestProject = projectsList.order_by('-dateAdded')[0]
			LOM = int(latestProject.LOM)
			numStockpiles = latestProject.numStockpiles

			projectPeriods = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).order_by('year')
			projectStartDate = projectPeriods[0].startDate
			projectEndDate = projectPeriods[projectPeriods.count()-1].endDate

			# Check if default filter options are available
			# Check "This year", "Last year", "This quarter", and "Last quarter"
			# 1. This year
			today = datetime.date.today()
			if (today.year >= projectStartDate.year) and (today.year <= projectEndDate.year):
				# thisYear = True
				thisYearStartDate = datetime.date(today.year, 1, 1)
				thisYearEndDate = datetime.date(today.year, 12, 31)
			else:
				# thisYear = False
				thisYearStartDate = None
				thisYearEndDate = None

			# 2. Last year
			if (today.year-1 >= projectStartDate.year) and (today.year-1 <= projectEndDate.year):
				# lastYear = True
				lastYearStartDate = datetime.date(today.year-1, 1, 1)
				lastYearEndDate = datetime.date(today.year-1, 12, 31)
			else:
				# lastYear = False
				lastYearStartDate = None
				lastYearEndDate = None

			# 3. This quarter
			if thisYearStartDate:
				todayQ = ceil(today.month/3.0)
				if today.year == projectStartDate.year:
					startDateQ = ceil(projectStartDate.month/3.0)
					quarters = list(range(startDateQ, 5))			
					if todayQ in quarters:
						# thisQuarter = True
						thisQuarterStartDate = datetime.date(today.year, 3*(todayQ - 1) + 1, 1)
						thisQuarterEndDate = thisQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
					else:
						# thisQuarter = False
						thisQuarterStartDate = None
						thisQuarterEndDate = None
				else:
					# thisQuarter = True
					thisQuarterStartDate = datetime.date(today.year, 3*(todayQ - 1) + 1, 1)
					thisQuarterEndDate = thisQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
			else:
				# thisQuarter = False
				thisQuarterStartDate = None
				thisQuarterEndDate = None

			# 4. Last quarter
			threeMonthsAgo = today - relativedelta(months=+3)
			if (threeMonthsAgo >= projectStartDate) and (threeMonthsAgo <= projectEndDate):
				threeMonthsAgoQ = ceil(threeMonthsAgo.month/3.0)
				# lastQuarter = True
				lastQuarterStartDate = datetime.date(threeMonthsAgo.year, 3*(threeMonthsAgoQ - 1) + 1, 1)
				lastQuarterEndDate = lastQuarterStartDate + relativedelta(months=+3) - relativedelta(days=+1)
			else:
				# lastQuarter = False
				lastQuarterStartDate = None
				lastQuarterEndDate = None

			# Get list of Commodity IDs
			commodities = tblCommodity.objects.filter(projectID=latestProject.projectID)
			commIDs = commodities.values_list('commodityID', flat=True)

			# Get list of Commodity Names
			commNameList = []
			for ID in commIDs:
				nameMatch = tblCommodityList.objects.get(commodityID=ID)
				commNameList.append(nameMatch.name)

			# Get list of Plant Product IDs
			PPMatches = tblPlantProduct.objects.filter(projectID=latestProject.projectID)
			PPIDs = PPMatches.values_list('plantProductID', flat=True)

			# Get most recent tblInputs entry
			latestInput = tblInputs.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
			# Price entry
			priceEntry = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=1)

			# Handle OPEX Shipping Cost by Year
			# shippingCosts = []
			fullShippingCosts = []

			# for year in range(1, yearCount+1):
			# 	currOPEX = tblOPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
			# 	fullShippingCosts.append(round(currOPEX.shipping,2))
			# 	if year in yearVals:
			# 		shippingCosts.append(round(currOPEX.shipping,2))

			tonnageVals = None
			tonnageTotals = None
			gradeVals = None
			moistures = None

			lumpTonnageVals = None
			lumpTonnageTotal = None
			lumpGradeVals = None
			lumpMoistures = None

			finesTonnageVals = None
			finesTonnageTotal = None
			finesGradeVals = None
			finesMoistures = None

			ultraFinesTonnageVals = None
			ultraFinesTonnageTotal = None
			ultraFinesGradeVals = None
			ultraFinesMoistures = None

			rejectsTonnageVals = None
			rejectsTonnageTotal = None
			rejectsGradeVals = None
			rejectsMoistures = None


			HGLumps = None
			lumpPenaltyVals = None
			lumpSellingPrices = None
			avgLumpSellingPrice = None
			netLumpPrices = None
			avgNetLumpPrice = None
			exchangeNetLumpPrices = None
			avgExchangeNetLumpPrice = None

			HGFines = None
			finesPenaltyVals = None
			finesSellingPrices = None
			avgFinesSellingPrice = None
			netFinesPrices = None
			avgNetFinesPrice = None
			exchangeNetFinesPrices = None
			avgExchangeNetFinesPrice = None

			HGUltraFines = None
			ultraFinesPenaltyVals = None
			ultraFinesSellingPrices = None
			avgUltraFinesSellingPrice = None
			netUltraFinesPrices = None
			avgNetUltraFinesPrice = None
			exchangeNetUltraFinesPrices = None
			avgExchangeNetUltraFinesPrice = None

			lumpRevenues = None
			sumLumpRevenues = None
			finesRevenues = None
			sumFinesRevenues = None
			ultraFinesRevenues = None
			sumUltraFinesRevenues = None

			# form = filterForm(request.POST, mineID=mineID)
			form = filterForm(request.POST, mineID=mineID, startDate=projectStartDate, endDate=projectEndDate)
			if form.is_valid():
				cleanData = form.cleaned_data
				startDate = cleanData["startDate"]
				endDate = cleanData["endDate"]

				# startDate = datetime.datetime.strptime(startDateStr, "%Y-%m-%d").date()
				# endDate = datetime.datetime.strptime(endDateStr, "%Y-%m-%d").date()
				projectPeriods = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).order_by("year")
				if projectPeriods[0].startDate > startDate:
					startDate = projectPeriods[0].startDate
				if projectPeriods.reverse()[0].endDate < endDate:
					endDate = projectPeriods.reverse()[0].endDate

				totalRevenues = [Decimal(0.0)]*((endDate - startDate).days+1)
				lumpPlusFinesRevenues = [Decimal(0.0)]*((endDate - startDate).days+1)

				# Obtain Exchange Rate
				# exchangeRates = [round(latestInput.exchangeRate,2)]*((endDate - startDate).days+1)
				fullExchangeRates = [round(Decimal(latestInput.exchangeRate),2)]*((endDate - startDate).days+1)
				xRate = round(Decimal(latestInput.exchangeRate),2)

				dateVals = []
				currDate = startDate
				while currDate <= endDate:
					dateVals.append(currDate.strftime("%b-%d-%Y"))
					currDate += datetime.timedelta(days=1)

				yearRanges = {}
				firstYear = projectPeriods[0].startDate.year
				startYear = startDate.year
				endYear = endDate.year
				currYear = 1
				while (firstYear+currYear-1) < startYear:
					currYear += 1
				yearRanges[startYear] = currYear
				while (firstYear+currYear-1) < endYear:
					currYear += 1
					yearRanges[firstYear+currYear-1] = currYear

				totalProducts = [Decimal(0.0)]*((endDate - startDate).days+1)

				# Handle Mine Plan Tonnages Section
				sumMinePlanTonnages = {}
				minePlanTonnageVals = {}

				minePlanTonnagesByYear = {}

				dailyMinePlanTonnageVals = {}
				for curr in range(1, numStockpiles+1):
					MPTonnageEntries = tblMineProductTonnage.objects.filter(projectID=latestProject.projectID, stockpileID=curr).order_by('year')
					minePlanTonnageVals[curr] = []
					minePlanTonnagesByYear[curr] = {}
					for year,yearNum in yearRanges.items():
						if calendar.isleap(year):
							minePlanTonnagesByYear[curr][year] = round(Decimal(MPTonnageEntries[yearNum-1].tonnage/366.0), 2)
						else:
							minePlanTonnagesByYear[curr][year] = round(Decimal(MPTonnageEntries[yearNum-1].tonnage/365.0), 2)

					currDate = startDate
					while currDate <= endDate:
						minePlanTonnageVals[curr].append(minePlanTonnagesByYear[curr][currDate.year])
						currDate += datetime.timedelta(days=1)

					sumMinePlanTonnages[curr] = sum(minePlanTonnageVals[curr])

				latestOPEX = tblOPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
				latestCAPEX = tblCAPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
				OPEXByYear = tblOPEX.objects.filter(mineID=mineID, dateAdded=latestOPEX.dateAdded).order_by('year')
				CAPEXByYear = tblCAPEX.objects.filter(mineID=mineID, dateAdded=latestCAPEX.dateAdded).order_by('year')

				miningVals = {}
				infrastructureVals = {}
				stockpileLGVals = {}
				dewateringVals = {}
				processingVals = {}
				haulingVals = {}
				loadOutRailLoopVals = {}
				GASiteVals = {}
				GARoomVals = {}
				railTransportVals = {}
				GACorpVals = {}
				royaltiesVals = {}
				transportationVals = {}
				GAVals = {}
				shippingVals = {}

				mining = []
				infrastructure = []
				stockpileLG = []
				dewatering = []
				processing = []
				hauling = []
				loadOutRailLoop = []
				GASite = []
				GARoom = []
				railTransport = []
				GACorp = []
				royalties = []
				transportation = []
				GA = []

				preStripVals = {}
				mineEquipInitialVals = {}
				mineEquipSustainVals = {}
				infraDirectCostVals = {}
				infraIndirectCostVals = {}
				contingencyVals = {}
				railcarsVals = {}
				otherMobEquipVals = {}
				closureRehabAssureVals = {}
				depoProvisionPayVals = {}
				workCapCurrentProdVals = {}
				workCapCostsLGVals = {}
				EPCMVals = {}
				ownerCostVals = {}

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

				for year,yearNum in yearRanges.items():
					miningVals[year] = round(OPEXByYear[yearNum-1].mining/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].mining/Decimal(365.0), 2)
					infrastructureVals[year] = round(OPEXByYear[yearNum-1].infrastructure/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].infrastructure/Decimal(365.0), 2)
					stockpileLGVals[year] = round(OPEXByYear[yearNum-1].stockpileLG/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].stockpileLG/Decimal(365.0), 2)
					dewateringVals[year] = round(OPEXByYear[yearNum-1].dewatering/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].dewatering/Decimal(365.0), 2)
					processingVals[year] = round(OPEXByYear[yearNum-1].processing/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].processing/Decimal(365.0), 2)
					haulingVals[year] = round(OPEXByYear[yearNum-1].hauling/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].hauling/Decimal(365.0), 2)
					loadOutRailLoopVals[year] = round(OPEXByYear[yearNum-1].loadOutRailLoop/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].loadOutRailLoop/Decimal(365.0), 2)
					GASiteVals[year] = round(OPEXByYear[yearNum-1].GASite/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].GASite/Decimal(365.0), 2)
					GARoomVals[year] = round(OPEXByYear[yearNum-1].GARoomBoardFIFO/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].GARoomBoardFIFO/Decimal(365.0), 2)
					railTransportVals[year] = round(OPEXByYear[yearNum-1].railTransport/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].railTransport/Decimal(365.0), 2)
					GACorpVals[year] = round(OPEXByYear[yearNum-1].GACorp/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].GACorp/Decimal(365.0), 2)
					royaltiesVals[year] = round(OPEXByYear[yearNum-1].royalties/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].royalties/Decimal(365.0), 2)
					transportationVals[year] = round(OPEXByYear[yearNum-1].transportation/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].transportation/Decimal(365.0), 2)
					GAVals[year] = round(OPEXByYear[yearNum-1].GA/Decimal(366.0), 2) if calendar.isleap(year) else round(OPEXByYear[yearNum-1].GA/Decimal(365.0), 2)
					
					shippingVals[year] = round(OPEXByYear[yearNum-1].shipping, 2)
					
					preStripVals[year] = round(CAPEXByYear[yearNum-1].preStrip/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].preStrip/Decimal(365.0), 2)
					mineEquipInitialVals[year] = round(CAPEXByYear[yearNum-1].mineEquipInitial/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].mineEquipInitial/Decimal(365.0), 2)
					mineEquipSustainVals[year] = round(CAPEXByYear[yearNum-1].mineEquipSustain/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].mineEquipSustain/Decimal(365.0), 2)
					infraDirectCostVals[year] = round(CAPEXByYear[yearNum-1].infraDirectCost/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].infraDirectCost/Decimal(365.0), 2)
					infraIndirectCostVals[year] = round(CAPEXByYear[yearNum-1].infraIndirectCost/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].infraIndirectCost/Decimal(365.0), 2)
					contingencyVals[year] = round(CAPEXByYear[yearNum-1].contingency/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].contingency/Decimal(365.0), 2)
					railcarsVals[year] = round(CAPEXByYear[yearNum-1].railcars/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].railcars/Decimal(365.0), 2)
					otherMobEquipVals[year] = round(CAPEXByYear[yearNum-1].otherMobEquip/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].otherMobEquip/Decimal(365.0), 2)
					closureRehabAssureVals[year] = round(CAPEXByYear[yearNum-1].closureRehabAssure/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].closureRehabAssure/Decimal(365.0), 2)
					depoProvisionPayVals[year] = round(CAPEXByYear[yearNum-1].depoProvisionPay/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].depoProvisionPay/Decimal(365.0), 2)
					workCapCurrentProdVals[year] = round(CAPEXByYear[yearNum-1].workCapCurrentProd/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].workCapCurrentProd/Decimal(365.0), 2)
					workCapCostsLGVals[year] = round(CAPEXByYear[yearNum-1].workCapCostsLG/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].workCapCostsLG/Decimal(365.0), 2)
					EPCMVals[year] = round(CAPEXByYear[yearNum-1].EPCM/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].EPCM/Decimal(365.0), 2)
					ownerCostVals[year] = round(CAPEXByYear[yearNum-1].ownerCost/Decimal(366.0), 2) if calendar.isleap(year) else round(CAPEXByYear[yearNum-1].ownerCost/Decimal(365.0), 2)

				currDate = startDate
				while currDate <= endDate:
					fullShippingCosts.append(shippingVals[currDate.year])

					mining.append(miningVals[currDate.year])
					infrastructure.append(infrastructureVals[currDate.year])
					stockpileLG.append(stockpileLGVals[currDate.year])
					dewatering.append(dewateringVals[currDate.year])
					processing.append(processingVals[currDate.year])
					hauling.append(haulingVals[currDate.year])
					loadOutRailLoop.append(loadOutRailLoopVals[currDate.year])
					GASite.append(GASiteVals[currDate.year])
					GARoom.append(GARoomVals[currDate.year])
					railTransport.append(railTransportVals[currDate.year])
					GACorp.append(GACorpVals[currDate.year])
					royalties.append(royaltiesVals[currDate.year])
					transportation.append(transportationVals[currDate.year])
					GA.append(GAVals[currDate.year])

					preStrip.append(preStripVals[currDate.year])
					mineEquipInitial.append(mineEquipInitialVals[currDate.year])
					mineEquipSustain.append(mineEquipSustainVals[currDate.year])
					infraDirectCost.append(infraDirectCostVals[currDate.year])
					infraIndirectCost.append(infraIndirectCostVals[currDate.year])
					contingency.append(contingencyVals[currDate.year])
					railcars.append(railcarsVals[currDate.year])
					otherMobEquip.append(otherMobEquipVals[currDate.year])
					closureRehabAssure.append(closureRehabAssureVals[currDate.year])
					depoProvisionPay.append(depoProvisionPayVals[currDate.year])
					workCapCurrentProd.append(workCapCurrentProdVals[currDate.year])
					workCapCostsLG.append(workCapCostsLGVals[currDate.year])
					EPCM.append(EPCMVals[currDate.year])
					ownerCost.append(ownerCostVals[currDate.year])

					currDate += datetime.timedelta(days=1)

				sumMining = sum(mining)
				sumStockpileLG = sum(stockpileLG)
				sumDewatering = sum(dewatering)
				sumProcessing = sum(processing)
				sumHauling = sum(hauling)
				sumLoadOutRailLoop = sum(loadOutRailLoop)
				sumGASite = sum(GASite)
				sumGARoom = sum(GARoom)
				sumRailTransport = sum(railTransport)
				sumGACorp = sum(GACorp)
				sumRoyalties = sum(royalties)

				totalOPEX = [sum(x) for x in zip(mining, stockpileLG, dewatering, processing, hauling,
					loadOutRailLoop, GASite, GARoom, railTransport, GACorp)]
				# cashFlowOPEX = [sum(x) for x in zip(mining, infrastructure, stockpileLG, dewatering, processing, hauling,
				# 	loadOutRailLoop, GASite, GARoom, railTransport, GACorp, royalties, transportation, GA)]
				sumTotalOPEX = sum(totalOPEX)

				sumPreStrip = sum(preStrip)
				sumMineEquipInitial = sum(mineEquipInitial)
				sumMineEquipSustain = sum(mineEquipSustain)
				sumInfraDirectCost = sum(infraDirectCost)
				sumInfraIndirectCost = sum(infraIndirectCost)
				sumContingency = sum(contingency)
				sumRailcars = sum(railcars)
				sumOtherMobEquip = sum(otherMobEquip)
				sumClosureRehabAssure = sum(closureRehabAssure)
				sumDepoProvisionPay = sum(depoProvisionPay)
				sumWorkCapCurrentProd = sum(workCapCurrentProd)
				sumWorkCapCostsLG = sum(workCapCostsLG)

				totalCAPEX = [sum(x) for x in zip(preStrip, mineEquipInitial, mineEquipSustain, infraDirectCost, infraIndirectCost,
					contingency, railcars, otherMobEquip, closureRehabAssure, depoProvisionPay)]
				# cashFlowCAPEX = [sum(x) for x in zip(totalCAPEX, workCapCurrentProd, workCapCostsLG, EPCM, ownerCost)]
				sumTotalCAPEX = sum(totalCAPEX)

				latestTaxes = tblTaxes.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
				taxesByYear = tblTaxes.objects.filter(mineID=mineID, dateAdded=latestTaxes.dateAdded).order_by('year')

				federalTaxesVals = {}
				provincialTaxesVals = {}
				miningTaxesVals = {}

				federalTaxes = []
				provincialTaxes = []
				miningTaxes = []

				for year,yearNum in yearRanges.items():
					federalTaxesVals[year] = round(Decimal(taxesByYear[yearNum-1].federal/366.0), 2) if calendar.isleap(year) else round(Decimal(taxesByYear[yearNum-1].federal/365.0), 2)
					provincialTaxesVals[year] = round(Decimal(taxesByYear[yearNum-1].provincial/366.0), 2) if calendar.isleap(year) else round(Decimal(taxesByYear[yearNum-1].provincial/365.0), 2)
					miningTaxesVals[year] = round(Decimal(taxesByYear[yearNum-1].mining/366.0), 2) if calendar.isleap(year) else round(Decimal(taxesByYear[yearNum-1].mining/365.0), 2)
					# totalTaxes[yearNum] = federalTaxes[yearNum] + provincialTaxes[yearNum] + miningTaxes[yearNum]

				currDate = startDate
				while currDate <= endDate:
					federalTaxes.append(federalTaxesVals[currDate.year])
					provincialTaxes.append(federalTaxesVals[currDate.year])
					miningTaxes.append(federalTaxesVals[currDate.year])

					currDate += datetime.timedelta(days=1)

				sumFederalTaxes = sum(federalTaxes)
				sumProvincialTaxes = sum(provincialTaxes)
				sumMiningTaxes = sum(miningTaxes)
				totalTaxes = [sum(x) for x in zip(federalTaxes, provincialTaxes, miningTaxes)]
				sumTotalTaxes = sum(totalTaxes)

				discountRates = [Decimal(0.06), Decimal(0.08), Decimal(0.10), Decimal(0.12), Decimal(0.15), Decimal(0.20)]

				# Handle values if no calculations have been run during selected range of dates
				cashFlowEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=startDate, date__lte=endDate)
				if not cashFlowEntries:
					tonnageVals = {}
					tonnageTotals = {}
					gradeVals = {}
					moistures = {}
					for curr in range(1, numStockpiles+1):
						tonnageVals[curr] = [filler]*((endDate-startDate).days+1)
						tonnageTotals[curr] = filler
						gradeVals[curr] = {}
						for i in range(len(commIDs)):
							gradeVals[curr][commNameList[i]] = [filler]*((endDate-startDate).days+1)
						moistures[curr] = [round(latestInput.feedMoisture,2)]*((endDate-startDate).days+1)

					if 1 in PPIDs:
						lumpTonnageVals = [filler]*((endDate-startDate).days+1)
						lumpTonnageTotal = filler
						lumpGradeVals = {}
						for i in range(len(commIDs)):
							lumpGradeVals[commNameList[i]] = [filler]*((endDate-startDate).days+1)
						lumpMoistures = [round(latestInput.lumpMoisture,2)]*((endDate-startDate).days+1)

					if 2 in PPIDs:
						finesTonnageVals = [filler]*((endDate-startDate).days+1)
						finesTonnageTotal = filler
						finesGradeVals = {}
						for i in range(len(commIDs)):
							finesGradeVals[commNameList[i]] = [filler]*((endDate-startDate).days+1)
						finesMoistures = [round(latestInput.finesMoisture,2)]*((endDate-startDate).days+1)

					if 3 in PPIDs:
						ultraFinesTonnageVals = [filler]*((endDate-startDate).days+1)
						ultraFinesTonnageTotal = filler
						ultraFinesGradeVals = {}
						for i in range(len(commIDs)):
							ultraFinesGradeVals[commNameList[i]] = [filler]*((endDate-startDate).days+1)
						ultraFinesMoistures = [round(latestInput.ultraFinesMoisture,2)]*((endDate-startDate).days+1)

					if 4 in PPIDs:
						rejectsTonnageVals = [filler]*((endDate-startDate).days+1)
						rejectsTonnageTotal = filler
						rejectsGradeVals = {}
						for i in range(len(commIDs)):
							rejectsGradeVals[commNameList[i]] = [filler]*((endDate-startDate).days+1)
						rejectsMoistures = [round(latestInput.rejectsMoisture,2)]*((endDate-startDate).days+1)

					totalProducts = [filler]*((endDate-startDate).days+1)
					sumTotalProducts = filler

					if 1 in PPIDs:
						HGLumps = [Decimal(priceEntry.lump)]*((endDate - startDate).days+1)
						lumpPenaltyVals = {}
						for i in range(len(commIDs)):
							lumpPenaltyVals[commNameList[i]] = [filler]*((endDate - startDate).days+1)
						lumpSellingPrices = [filler]*((endDate - startDate).days+1)
						avgLumpSellingPrice = filler
						netLumpPrices = [filler]*((endDate - startDate).days+1)
						avgNetLumpPrice = filler
						exchangeNetLumpPrices = [filler]*((endDate - startDate).days+1)
						avgExchangeNetLumpPrice = filler

					if 2 in PPIDs:
						HGFines = [Decimal(priceEntry.fines)]*((endDate - startDate).days+1)
						finesPenaltyVals = {}
						for i in range(len(commIDs)):
							finesPenaltyVals[commNameList[i]] = [filler]*((endDate - startDate).days+1)
						finesSellingPrices = [filler]*((endDate - startDate).days+1)
						avgFinesSellingPrice = filler
						netFinesPrices = [filler]*((endDate - startDate).days+1)
						avgNetFinesPrice = filler
						exchangeNetFinesPrices = [filler]*((endDate - startDate).days+1)
						avgExchangeNetFinesPrice = filler

					if 3 in PPIDs:
						HGUltraFines = [Decimal(priceEntry.ultraFines)]*((endDate - startDate).days+1)
						ultraFinesPenaltyVals = {}
						for i in range(len(commIDs)):
							ultraFinesPenaltyVals[commNameList[i]] = [filler]*((endDate - startDate).days+1)
						ultraFinesSellingPrices = [filler]*((endDate - startDate).days+1)
						avgUltraFinesSellingPrice = filler
						netUltraFinesPrices = [filler]*((endDate - startDate).days+1)
						avgNetUltraFinesPrice = filler
						exchangeNetUltraFinesPrices = [filler]*((endDate - startDate).days+1)
						avgExchangeNetUltraFinesPrice = filler

					if 1 in PPIDs:
						lumpRevenues = [filler]*((endDate - startDate).days+1)
						sumLumpRevenues = filler

					if 2 in PPIDs:
						finesRevenues = [filler]*((endDate - startDate).days+1)
						sumFinesRevenues = filler

					if 3 in PPIDs:
						ultraFinesRevenues = [filler]*((endDate - startDate).days+1)
						sumUltraFinesRevenues = filler

					totalRevenues = [filler]*((endDate - startDate).days+1)
					sumTotalRevenues = filler

					cashFlowPreTax = [filler]*len(startDateVals)
					cashFlowPostTax = [filler]*len(startDateVals)
					cumCashFlowPreTax = [filler]*len(startDateVals)
					cumCashFlowPostTax = [filler]*len(startDateVals)
					sumCashFlowPreTax = filler
					sumCashFlowPostTax = filler
					paybackPreTax = [filler]*len(startDateVals)
					paybackPostTax = [filler]*len(startDateVals)
					sumPaybackPreTax = filler
					sumPaybackPostTax = filler
					preTaxIRR = filler
					postTaxIRR = filler

					preTaxPVs = {}
					postTaxPVs = {}
					sumPreTaxNPV = {}
					sumPostTaxNPV = {}
					for rate in discountRates:
						rate = int(round(rate*100))
						preTaxPVs[rate] = [filler]*len(startDateVals)
						postTaxPVs[rate] = [filler]*len(startDateVals)
						sumPreTaxNPV[rate] = filler
						sumPostTaxNPV[rate] = filler

					# Create DL Form Data
					reportRowCount = 1

					reportData = ""

					currRow = 'Item,'
					for date in dateVals:
						# currRow += 'Year{0},'.format(year)
						currRow += date + ','
					currRow += 'Total;'
					reportData += currRow

					reportData += ";Mining;"
					for curr in range(1, numStockpiles+1):
						currRow = "Stockpile {0} Ore (kt),".format(curr) + ''.join([*[str(round(x,2))+',' for x in minePlanTonnageVals[curr]]]) + str(round(sumMinePlanTonnages[curr],2)) + ";"
						reportData += currRow

					reportData += ";Processing;"
					for curr in range(1, numStockpiles+1):
						reportData += "Stockpile {0} Ore;".format(curr)
						currRow = 'Tonnage (kt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]) + ',' + tonnageTotals[curr] + ";"
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]) + ';'

					reportData += ";Plant Product;"

					if 1 in PPIDs:
						reportData += "Lump;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]) + ',' + lumpTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]) + ';'

					if 2 in PPIDs:
						reportData += "Fines;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]) + ',' + finesTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]) + ';'

					if 3 in PPIDs:
						reportData += "Ultra Fines;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]) + ',' + ultraFinesTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]) + ';'

					reportData += 'Total Product (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]) + ',' + sumTotalProducts + ';'

					if 4 in PPIDs:
						reportData += "Rejects;"
						currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]) + ',' + rejectsTonnageTotal + ';'
						reportData += currRow
						for i in range(len(commIDs)):
							currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]) + ';'
							reportData += currRow
						reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]) + ';'

					reportData += ";Products Selling Price;"

					if 1 in PPIDs:
						reportData += 'Lump Selling Price (USD/dmt);'
						reportData += 'Lump Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]) + ';'
						for i in range(len(commIDs)):
							reportData += 'Lump {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]) + ';'
						reportData += 'Lump Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]) + ',' + 'Avg: ' + avgLumpSellingPrice + ';'
						reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
						reportData += 'Net Lump Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]) + ',' + 'Avg: ' + avgNetLumpPrice + ';'
						reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
						reportData += 'Net Lump Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]) + ',' + 'Avg: ' + avgExchangeNetLumpPrice + ';'

					if 2 in PPIDs:
						reportData += 'Fines Selling Price (USD/dmt);'
						reportData += 'Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]) + ';'
						for i in range(len(commIDs)):
							reportData += 'Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]) + ';'
						reportData += 'Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]) + ',' + 'Avg: ' + avgFinesSellingPrice + ';'
						reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
						reportData += 'Net Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]) + ',' + 'Avg: ' + avgNetFinesPrice + ';'
						reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
						reportData += 'Net Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]) + ',' + 'Avg: ' + avgExchangeNetFinesPrice + ';'

					if 3 in PPIDs:
						reportData += 'Ultra Fines Selling Price (USD/dmt);'
						reportData += 'Ultra Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]) + ';'
						for i in range(len(commIDs)):
							reportData += 'Ultra Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]) + ';'
						reportData += 'Ultra Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]) + ',' + 'Avg: ' + avgUltraFinesSellingPrice + ';'
						reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
						reportData += 'Net Ultra Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]) + ',' + 'Avg: ' + avgNetUltraFinesPrice + ';'
						reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
						reportData += 'Net Ultra Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]) + ',' + 'Avg: ' + avgExchangeNetUltraFinesPrice+ ';'

					reportData += ';Revenues;'
					if 1 in PPIDs:
						reportData += 'Lump Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]]) + ',' + sumLumpRevenues + ';'
					if 2 in PPIDs:
						reportData += 'Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]]) + ',' + sumFinesRevenues + ';'
					if 3 in PPIDs:
						reportData += 'Ultra Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]]) + ',' + sumUltraFinesRevenues + ';'
					reportData += 'TOTAL REVENUE,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + sumTotalRevenues + ';'

					reportData += ';COSTS;'
					reportData += 'OPEX (millions CAD);'
					reportData += 'Mining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mining]]) + ',' + str(round(sumMining,2)) + ';'
					reportData += 'Stockpile LG Reclaiming,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]]) + ',' + str(round(sumStockpileLG,2)) + ';'
					reportData += 'Pit Dewatering,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]]) + ',' + str(round(sumDewatering,2)) + ';'
					reportData += 'Processing,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in processing]]) + ',' + str(round(sumProcessing,2)) + ';'
					reportData += 'Product Hauling,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]]) + ',' + str(round(sumHauling,2)) + ';'
					reportData += 'Load-out and Rail Loop,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]]) + ',' + str(round(sumLoadOutRailLoop,2)) + ';'
					reportData += 'G&A (Site),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]]) + ',' + str(round(sumGASite,2)) + ';'
					reportData += 'G&A (Room & Board / FIFO),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]]) + ',' + str(round(sumGARoom,2)) + ';'
					reportData += 'Rail Transportation Port and Shiploading,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]]) + ',' + str(round(sumRailTransport,2)) + ';'
					reportData += 'Corporate G&A,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]]) + ',' + str(round(sumGACorp,2)) + ';'
					reportData += 'TOTAL OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
					reportData += 'ROYALTIES (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'

					reportData += 'CAPEX (millions CAD);'
					reportData += 'Pre-Stripping,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]]) + ',' + str(round(sumPreStrip,2)) + ';'
					reportData += 'Mining Equipment Initial,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]]) + ',' + str(round(sumMineEquipInitial,2)) + ';'
					reportData += 'Mining Equipment Sustaining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]]) + ',' + str(round(sumMineEquipSustain,2)) + ';'
					reportData += 'Project Infrastructure Direct Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]]) + ',' + str(round(sumInfraDirectCost,2)) + ';'
					reportData += 'Project Infrastructure Indirect Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]]) + ',' + str(round(sumInfraIndirectCost,2)) + ';'
					reportData += 'Project Infrastructure Contingency,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]]) + ',' + str(round(sumContingency,2)) + ';'
					reportData += 'Railcars,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]]) + ',' + str(round(sumRailcars,2)) + ';'
					reportData += 'Other Mobile Equipment,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]]) + ',' + str(round(sumOtherMobEquip,2)) + ';'
					reportData += 'Closure and Rehab Assurance Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]]) + ',' + str(round(sumClosureRehabAssure,2)) + ';'
					reportData += 'Deposits Provision Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]]) + ',' + str(round(sumDepoProvisionPay,2)) + ';'
					reportData += 'TOTAL CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'

					reportData += 'TAXES (millions CAD);'
					reportData += 'Federal Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]]) + ',' + str(round(sumFederalTaxes,2)) + ';'
					reportData += 'Provincial Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]]) + ',' + str(round(sumProvincialTaxes,2)) + ';'
					reportData += 'Mining Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]]) + ',' + str(round(sumMiningTaxes,2)) + ';'
					reportData += 'TOTAL (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

					reportData += ';SUMMARY;'
					reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + filler + ';'
					reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
					reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
					reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
					reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
					reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
					reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

					reportData += ';PRE-TAX CASH FLOW;'
					reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + filler + ';'
					reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ',' + filler + ';'
					reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + filler + ';'
					for rate in discountRates:
						reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + filler + ';'
					reportData += 'INTERNAL RATE OF RETURN (IRR),' + 'N/A' + ';'

					reportData += ';POST-TAX CASH FLOW;'
					reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + filler + ';'
					reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ',' + filler + ';'
					reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + filler + ';'
					for rate in discountRates:
						reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + filler + ';'
					reportData += 'INTERNAL RATE OF RETURN (IRR),' + 'N/A' + ';'

					filter_form = filterForm(mineID=mineID, startDate=projectStartDate, endDate=projectEndDate)
					default_filter_form = defaultFilterForm(mineID=mineID, thisYearStartDate=thisYearStartDate, thisYearEndDate=thisYearEndDate,
						lastYearStartDate=lastYearStartDate, lastYearEndDate=lastYearEndDate,
						thisQuarterStartDate=thisQuarterStartDate, thisQuarterEndDate=thisQuarterEndDate,
						lastQuarterStartDate=lastQuarterStartDate, lastQuarterEndDate=lastQuarterEndDate)
					report_form = reportForm(mineID=mineID, reportData=reportData)

					return render(request, 'report/report2.html', {'filterForm': filter_form, 'reportForm': report_form,
						'defaultFilterForm': default_filter_form,
						'dateVals': dateVals, 'commIDs': commIDs, 'commNameList': commNameList,
						'numStockpiles': list(range(1, numStockpiles+1)),
						'minePlanTonnageVals': minePlanTonnageVals, 'sumMinePlanTonnages': sumMinePlanTonnages,
						# 'minePlanHGTonnageVals': minePlanHGTonnageVals, 'minePlanLGTonnageVals': minePlanLGTonnageVals,
						# 'minePlanWasteTonnageVals': minePlanWasteTonnageVals, 'minePlanOverburdenTonnageVals': minePlanOverburdenTonnageVals,
						# 'sumMinePlanHGTonnage': sumMinePlanHGTonnage, 'sumMinePlanLGTonnage': sumMinePlanLGTonnage,
						# 'sumMinePlanWasteTonnage': sumMinePlanWasteTonnage, 'sumMinePlanOverburdenTonnage': sumMinePlanOverburdenTonnage,
						'tonnageVals': tonnageVals, 'tonnageTotals': tonnageTotals, 'gradeVals': gradeVals, 'moistures': moistures,
						# 'HGTonnageVals': HGTonnageVals, 'HGTonnageTotal': HGTonnageTotal, 'HGGradeVals': HGGradeVals, 'HGMoistures': HGMoistures,
						# 'LGTonnageVals': LGTonnageVals, 'LGTonnageTotal': LGTonnageTotal, 'LGGradeVals': LGGradeVals, 'LGMoistures': LGMoistures,
						'lumpTonnageVals': lumpTonnageVals, 'lumpTonnageTotal': lumpTonnageTotal, 'lumpGradeVals': lumpGradeVals, 'lumpMoistures': lumpMoistures,
						'finesTonnageVals': finesTonnageVals, 'finesTonnageTotal': finesTonnageTotal, 'finesGradeVals': finesGradeVals, 'finesMoistures': finesMoistures,
						'ultraFinesTonnageVals': ultraFinesTonnageVals, 'ultraFinesTonnageTotal': ultraFinesTonnageTotal, 'ultraFinesGradeVals': ultraFinesGradeVals, 'ultraFinesMoistures': ultraFinesMoistures,
						'totalProducts': totalProducts, 'sumTotalProducts': sumTotalProducts,
						'rejectsTonnageVals': rejectsTonnageVals, 'rejectsTonnageTotal': rejectsTonnageTotal, 'rejectsGradeVals': rejectsGradeVals, 'rejectsMoistures': rejectsMoistures,
						'fullShippingCosts': fullShippingCosts, 'fullExchangeRates': fullExchangeRates,
						'HGLumps': HGLumps, 'lumpPenaltyVals': lumpPenaltyVals, 'lumpSellingPrices': lumpSellingPrices, 'avgLumpSellingPrice': avgLumpSellingPrice,
						'netLumpPrices': netLumpPrices, 'avgNetLumpPrice': avgNetLumpPrice, 'exchangeNetLumpPrices': exchangeNetLumpPrices,
						'avgExchangeNetLumpPrice': avgExchangeNetLumpPrice,
						'HGFines': HGFines, 'finesPenaltyVals': finesPenaltyVals, 'finesSellingPrices': finesSellingPrices, 'avgFinesSellingPrice': avgFinesSellingPrice,
						'netFinesPrices': netFinesPrices, 'avgNetFinesPrice': avgNetFinesPrice, 'exchangeNetFinesPrices': exchangeNetFinesPrices,
						'avgExchangeNetFinesPrice': avgExchangeNetFinesPrice,
						'HGUltraFines': HGUltraFines, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals, 'ultraFinesSellingPrices': ultraFinesSellingPrices,
						'avgUltraFinesSellingPrice': avgUltraFinesSellingPrice,
						'netUltraFinesPrices': netUltraFinesPrices, 'exchangeNetUltraFinesPrices': exchangeNetUltraFinesPrices,
						'avgExchangeNetUltraFinesPrice': avgExchangeNetUltraFinesPrice,
						'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
						'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
						'totalRevenues': totalRevenues, 'sumTotalRevenues': sumTotalRevenues,
						'mining': mining, 'stockpileLG': stockpileLG, 'dewatering': dewatering, 'processing': processing, 'hauling': hauling,
						'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite, 'GARoom': GARoom, 'railTransport': railTransport, 'GACorp': GACorp,
						'sumMining': sumMining, 'sumStockpileLG': sumStockpileLG, 'sumDewatering': sumDewatering, 'sumProcessing': sumProcessing,
						'sumHauling': sumHauling, 'sumLoadOutRailLoop': sumLoadOutRailLoop, 'sumGASite': sumGASite, 'sumGARoom': sumGARoom,
						'sumRailTransport': sumRailTransport, 'sumGACorp': sumGACorp,
						'totalOPEX': totalOPEX, 'sumTotalOPEX':sumTotalOPEX, 'royalties': royalties, 'sumRoyalties': sumRoyalties,
						'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial, 'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
						'infraIndirectCost': infraIndirectCost, 'contingency': contingency, 'railcars': railcars, 'otherMobEquip': otherMobEquip,
						'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay, 'sumPreStrip': sumPreStrip,
						'sumMineEquipInitial': sumMineEquipInitial, 'sumMineEquipSustain': sumMineEquipSustain, 'sumInfraDirectCost': sumInfraDirectCost,
						'sumInfraIndirectCost': sumInfraIndirectCost, 'sumContingency': sumContingency, 'sumRailcars': sumRailcars,
						'sumOtherMobEquip': sumOtherMobEquip, 'sumClosureRehabAssure': sumClosureRehabAssure, 'sumDepoProvisionPay': sumDepoProvisionPay,
						'totalCAPEX': totalCAPEX, 'sumTotalCAPEX': sumTotalCAPEX,
						'federalTaxes': federalTaxes, 'provincialTaxes': provincialTaxes, 'miningTaxes': miningTaxes,
						'sumFederalTaxes': sumFederalTaxes, 'sumProvincialTaxes': sumProvincialTaxes, 'sumMiningTaxes': sumMiningTaxes,
						'totalTaxes': totalTaxes, 'sumTotalTaxes': sumTotalTaxes,
						'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
						'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG,
						'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
						'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
						'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
						'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
						'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
						'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
						'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})
						# 'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
						# 'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
						# 'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
						# 'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
						# 'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
						# 'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
						# 'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})

				latestCAPEX = tblCAPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				timestamp = latestCAPEX.dateAdded
				CAPEXEntries = tblCAPEX.objects.filter(mineID=int(mineID), dateAdded=timestamp)

				negCAPEX = []
				for year in [-3,-2,-1]:
					currCAPEX = CAPEXEntries.filter(year=year)
					if currCAPEX:
						row = currCAPEX[0]
						negCAPEX.append(round(Decimal(row.preStrip + row.mineEquipInitial + row.mineEquipSustain + 
							row.infraDirectCost + row.infraIndirectCost + row.contingency + row.railcars + 
							row.otherMobEquip + row.closureRehabAssure + row.depoProvisionPay + 
							row.workCapCurrentProd + row.workCapCostsLG + row.EPCM + row.ownerCost),2))
					else:
						negCAPEX.append(Decimal(0.0))
				sumNegCAPEX = sum(negCAPEX)

				tonnageVals = {}
				tonnageTotals = {}
				gradeVals = {}
				moistures = {}
				for curr in range(1, numStockpiles+1):
					tonnageVals[curr] = []
					gradeVals[curr] = {}

					# Tonnages
					MPTonnageEntries = tblMineProductTonnageOptimized.objects.filter(projectID=latestProject.projectID, stockpileID=curr, 
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in MPTonnageEntries:
						while currDate < entry.date:
							tonnageVals[curr].append(filler)
							currDate += datetime.timedelta(days=1)
						tonnageVals[curr].append(entry.tonnage)
					tonnageTotals[curr] = sum([0 if x==filler else x for x in tonnageVals[curr]])
					tonnageVals[curr] += [filler]*(endDate-currDate).days

					# Grades
					for i in range(len(commIDs)):
						currGrades = []
						MPGradeEntries = tblMineProductGradeOptimized.objects.filter(projectID=latestProject.projectID, stockpileID=curr,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")

						currDate = startDate
						for entry in MPGradeEntries:
							while currDate < entry.date:
								currGrades.append(filler)
								currDate += datetime.timedelta(days=1)
							currGrades.append(round(entry.grade,2))
						currGrades += [filler]*(endDate-currDate).days
						gradeVals[curr][commNameList[i]] = currGrades

					# Moistures
					diff = endDate - startDate
					moistures[curr] = [round(latestInput.feedMoisture,2)]*(diff.days+1)


				# Lump data if declared
				if 1 in PPIDs:
					lumpTonnageVals = []
					lumpGradeVals = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=1,
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in PPTonnageEntries:
						while currDate < entry.date:
							lumpTonnageVals.append(filler)
							currDate += datetime.timedelta(days=1)
						lumpTonnageVals.append(round(Decimal(entry.tonnageDMT),2))
					lumpTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in lumpTonnageVals])
					lumpTonnageVals += [filler]*(endDate-currDate).days

					totalProducts = [x+y for x,y in zip(totalProducts, [Decimal(0.0) if x==filler else x for x in lumpTonnageVals])]

					# Grades
					for i in range(len(commIDs)):
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")

						currDate = startDate
						for entry in PPGradeEntries:
							while currDate < entry.date:
								currGrades.append(filler)
								currDate += datetime.timedelta(days=1)
							currGrades.append(round(entry.grade,2))
						currGrades += [filler]*(endDate-currDate).days
						lumpGradeVals[commNameList[i]] = currGrades

					# Moistures
					diff = endDate - startDate
					lumpMoistures = [round(latestInput.lumpMoisture,2)]*(diff.days+1)


				# Fines data if declared
				if 2 in PPIDs:
					finesTonnageVals = []
					finesGradeVals = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=2,
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in PPTonnageEntries:
						while currDate < entry.date:
							finesTonnageVals.append(filler)
							currDate += datetime.timedelta(days=1)
						finesTonnageVals.append(round(Decimal(entry.tonnageDMT),2))
					finesTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in finesTonnageVals])
					finesTonnageVals += [filler]*(endDate-currDate).days

					totalProducts = [x+y for x,y in zip(totalProducts, [Decimal(0.0) if x==filler else x for x in finesTonnageVals])]

					# Grades
					for i in range(len(commIDs)):
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")

						currDate = startDate
						for entry in PPGradeEntries:
							while currDate < entry.date:
								currGrades.append(filler)
								currDate += datetime.timedelta(days=1)
							currGrades.append(round(entry.grade,2))
						currGrades += [filler]*(endDate-currDate).days
						finesGradeVals[commNameList[i]] = currGrades

					# Moistures
					diff = endDate - startDate
					finesMoistures = [round(latestInput.finesMoisture,2)]*(diff.days+1)


				# Ultra Fines data if declared
				if 3 in PPIDs:
					ultraFinesTonnageVals = []
					ultraFinesGradeVals = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=3,
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in PPTonnageEntries:
						while currDate < entry.date:
							ultraFinesTonnageVals.append(filler)
							currDate += datetime.timedelta(days=1)
						ultraFinesTonnageVals.append(round(Decimal(entry.tonnageDMT),2))
					ultraFinesTonnageTotal = sum([Decimal(0.0) if x==filler else x for x in ultraFinesTonnageVals])
					ultraFinesTonnageVals += [filler]*(endDate-currDate).days

					totalProducts = [x+y for x,y in zip(totalProducts, [Decimal(0.0) if x==filler else x for x in ultraFinesTonnageVals])]

					# Grades
					for i in range(len(commIDs)):
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")

						currDate = startDate
						for entry in PPGradeEntries:
							while currDate < entry.date:
								currGrades.append(filler)
								currDate += datetime.timedelta(days=1)
							currGrades.append(round(entry.grade,2))
						currGrades += [filler]*(endDate-currDate).days
						ultraFinesGradeVals[commNameList[i]] = currGrades

					# Moistures
					diff = endDate - startDate
					ultraFinesMoistures = [round(latestInput.ultraFinesMoisture,2)]*(diff.days+1)

				# sumTotalProducts
				sumTotalProducts = sum(totalProducts)

				# Rejects data if declared
				if 4 in PPIDs:
					rejectsTonnageVals = []
					rejectsGradeVals = {}

					# Tonnages
					PPTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=4,
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in PPTonnageEntries:
						while currDate < entry.date:
							rejectsTonnageVals.append(filler)
							currDate += datetime.timedelta(days=1)
						rejectsTonnageVals.append(round(Decimal(entry.tonnageDMT),2))
					rejectsTonnageVals += [filler]*(endDate-currDate).days

					# Grades
					for i in range(len(commIDs)):
						currGrades = []
						PPGradeEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=4,
							commodityID=commIDs[i], date__gte=startDate, date__lte=endDate).order_by("date")

						currDate = startDate
						for entry in PPGradeEntries:
							while currDate < entry.date:
								currGrades.append(filler)
								currDate += datetime.timedelta(days=1)
							currGrades.append(round(entry.grade,2))
						currGrades += [filler]*(endDate-currDate).days
						rejectsGradeVals[commNameList[i]] = currGrades

					# Moistures
					diff = endDate - startDate
					rejectsMoistures = [round(latestInput.rejectsMoisture,2)]*(diff.days+1)


				# Plant Product Selling Prices
				if 1 in PPIDs:
					sumLumpPenalties = [Decimal(0.0)]*((endDate - startDate).days+1)
					HGLumps = [Decimal(priceEntry.lump)]*((endDate - startDate).days+1)
					lumpPenaltyVals = {}
					# penaltiesByYear = []
					for i in range(len(commIDs)):
						tempPenalties = []
						penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1, commodityID=commIDs[i],
								date__gte=startDate, date__lte=endDate).order_by("date")
						
						currDate = startDate
						for entry in penaltyEntries:
							while currDate < entry.date:
								tempPenalties.append(filler)
								currDate += datetime.timedelta(days=1)
							tempPenalties.append(round(Decimal(entry.penalty),2))
						tempPenalties += [filler]*(endDate-currDate).days
						lumpPenaltyVals[commNameList[i]] = tempPenalties
						sumLumpPenalties = [x+y for x,y in zip(sumLumpPenalties, [Decimal(0.0) if x==filler else x for x in tempPenalties])]

					lumpSellingPrices = list(map(operator.add, HGLumps, sumLumpPenalties))
					finalLumpSellingPrices = [filler if y==filler else x for x,y in zip(lumpSellingPrices,tempPenalties)]
					# avgLumpSellingPrice = round(sum(lumpSellingPrices) / len(lumpSellingPrices), 2)
					
					avgLumpSellingPrice = round(np.average([float(x) for x in lumpSellingPrices], 
						weights=[0.0 if x==filler else float(x) for x in lumpTonnageVals]),2)

					# avgLumpSellingPrice = round(np.average(lumpSellingPrices, 
					# 	weights=[Decimal(0.0) if x==filler else x for x in lumpTonnageVals]),2)
					netLumpPrices = list(map(operator.sub, lumpSellingPrices, fullShippingCosts))
					finalNetLumpPrices = [filler if y==filler else x for x,y in zip(netLumpPrices,tempPenalties)]
					# avgNetLumpPrice = round(sum(netLumpPrices) / len(netLumpPrices), 2)
					avgNetLumpPrice = round(Decimal(np.average([float(x) for x in netLumpPrices], 
						weights=[0.0 if x==filler else float(x) for x in lumpTonnageVals])),2)
					# exchangeNetLumpPrices = [round(x*exchangeRate,2) for x in netLumpPrices]
					exchangeNetLumpPrices = list(map(operator.mul, fullExchangeRates, netLumpPrices))
					exchangeNetLumpPrices = [round(x,2) for x in exchangeNetLumpPrices]
					finalExchangeNetLumpPrices = [filler if y==filler else x for x,y in zip(exchangeNetLumpPrices,tempPenalties)]
					avgExchangeNetLumpPrice = round(avgNetLumpPrice*fullExchangeRates[0], 2)

					lumpSellingPrices = finalLumpSellingPrices
					netLumpPrices = finalNetLumpPrices
					exchangeNetLumpPrices = finalExchangeNetLumpPrices

				if 2 in PPIDs:
					sumFinesPenalties = [Decimal(0.0)]*((endDate - startDate).days+1)
					HGFines = [Decimal(priceEntry.fines)]*((endDate - startDate).days+1)
					finesPenaltyVals = {}
					# penaltiesByYear = []
					for i in range(len(commIDs)):
						tempPenalties = []
						penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2, commodityID=commIDs[i],
								date__gte=startDate, date__lte=endDate).order_by("date")
						
						currDate = startDate
						for entry in penaltyEntries:
							while currDate < entry.date:
								tempPenalties.append(filler)
								currDate += datetime.timedelta(days=1)
							tempPenalties.append(round(Decimal(entry.penalty),2))
						tempPenalties += [filler]*(endDate-currDate).days
						finesPenaltyVals[commNameList[i]] = tempPenalties
						sumFinesPenalties = [x+y for x,y in zip(sumFinesPenalties, [Decimal(0.0) if x==filler else x for x in tempPenalties])]

					finesSellingPrices = list(map(operator.add, HGFines, sumFinesPenalties))
					finalFinesSellingPrices = [filler if y==filler else x for x,y in zip(finesSellingPrices,tempPenalties)]
					# avgLumpSellingPrice = round(sum(lumpSellingPrices) / len(lumpSellingPrices), 2)
					avgFinesSellingPrice = round(np.average([float(x) for x in finesSellingPrices], 
						weights=[0.0 if x==filler else float(x) for x in finesTonnageVals]),2)
					netFinesPrices = list(map(operator.sub, finesSellingPrices, fullShippingCosts))
					finalNetFinesPrices = [filler if y==filler else x for x,y in zip(netFinesPrices,tempPenalties)]
					# avgNetLumpPrice = round(sum(netLumpPrices) / len(netLumpPrices), 2)

					avgNetFinesPrice = round(Decimal(np.average([float(x) for x in netFinesPrices], 
						weights=[0.0 if x==filler else float(x) for x in finesTonnageVals])),2)
					# exchangeNetLumpPrices = [round(x*exchangeRate,2) for x in netLumpPrices]
					exchangeNetFinesPrices = list(map(operator.mul, fullExchangeRates, netFinesPrices))
					exchangeNetFinesPrices = [round(x,2) for x in exchangeNetFinesPrices]
					finalExchangeNetFinesPrices = [filler if y==filler else x for x,y in zip(exchangeNetFinesPrices,tempPenalties)]
					avgExchangeNetFinesPrice = round(avgNetFinesPrice*fullExchangeRates[0], 2)

					finesSellingPrices = finalFinesSellingPrices
					netFinesPrices = finalNetFinesPrices
					exchangeNetFinesPrices = finalExchangeNetFinesPrices


				if 3 in PPIDs:
					sumUltraFinesPenalties = [Decimal(0.0)]*((endDate - startDate).days+1)
					HGUltraFines = [Decimal(priceEntry.ultraFines)]*((endDate - startDate).days+1)
					ultraFinesPenaltyVals = {}
					# penaltiesByYear = []
					for i in range(len(commIDs)):
						tempPenalties = []
						penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3, commodityID=commIDs[i],
								date__gte=startDate, date__lte=endDate).order_by("date")
						
						currDate = startDate
						for entry in penaltyEntries:
							while currDate < entry.date:
								tempPenalties.append(filler)
								currDate += datetime.timedelta(days=1)
							tempPenalties.append(round(Decimal(entry.penalty),2))
						tempPenalties += [filler]*(endDate-currDate).days
						ultraFinesPenaltyVals[commNameList[i]] = tempPenalties
						sumUltraFinesPenalties = [x+y for x,y in zip(sumUltraFinesPenalties, [Decimal(0.0) if x==filler else x for x in tempPenalties])]

					ultraFinesSellingPrices = list(map(operator.add, HGUltraFines, sumUltraFinesPenalties))
					finalUltraFinesSellingPrices = [filler if y==filler else x for x,y in zip(ultraFinesSellingPrices,tempPenalties)]
					# avgLumpSellingPrice = round(sum(lumpSellingPrices) / len(lumpSellingPrices), 2)

					avgUltraFinesSellingPrice = round(np.average([float(x) for x in ultraFinesSellingPrices], 
						weights=[0.0 if x==filler else float(x) for x in ultraFinesTonnageVals]),2)

					netUltraFinesPrices = list(map(operator.sub, ultraFinesSellingPrices, fullShippingCosts))
					finalNetUltraFinesPrices = [filler if y==filler else x for x,y in zip(netUltraFinesPrices,tempPenalties)]
					# avgNetLumpPrice = round(sum(netLumpPrices) / len(netLumpPrices), 2)

					avgNetUltraFinesPrice = round(Decimal(np.average([float(x) for x in netUltraFinesPrices], 
						weights=[0.0 if x==filler else float(x) for x in ultraFinesTonnageVals])),2)
					# exchangeNetLumpPrices = [round(x*exchangeRate,2) for x in netLumpPrices]
					exchangeNetUltraFinesPrices = list(map(operator.mul, fullExchangeRates, netUltraFinesPrices))
					exchangeNetUltraFinesPrices = [round(x,2) for x in exchangeNetUltraFinesPrices]
					finalExchangeNetUltraFinesPrices = [filler if y==filler else x for x,y in zip(exchangeNetUltraFinesPrices,tempPenalties)]
					avgExchangeNetUltraFinesPrice = round(avgNetUltraFinesPrice*fullExchangeRates[0], 2)

					ultraFinesSellingPrices = finalUltraFinesSellingPrices
					netUltraFinesPrices = finalNetUltraFinesPrices
					exchangeNetUltraFinesPrices = finalExchangeNetUltraFinesPrices

				# Handle Revenues Section
				if 1 in PPIDs:
					lumpRevenues = []
					revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=1,
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in revenueEntries:
						while currDate < entry.date:
							lumpRevenues.append(filler)
							currDate += datetime.timedelta(days=1)
						lumpRevenues.append(round(Decimal(entry.plantProductRevenue),2))
					lumpRevenues += [filler]*(endDate-currDate).days

					sumLumpRevenues = sum([Decimal(0.0) if x==filler else x for x in lumpRevenues])
					lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, [Decimal(0.0) if x==filler else x for x in lumpRevenues]))
					totalRevenues = list(map(operator.add, totalRevenues, [Decimal(0.0) if x==filler else x for x in lumpRevenues]))

				if 2 in PPIDs:
					finesRevenues = []
					revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=2,
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in revenueEntries:
						while currDate < entry.date:
							finesRevenues.append(filler)
							currDate += datetime.timedelta(days=1)
						finesRevenues.append(round(Decimal(entry.plantProductRevenue),2))
					finesRevenues += [filler]*(endDate-currDate).days

					sumFinesRevenues = sum([Decimal(0.0) if x==filler else x for x in finesRevenues])
					lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, [Decimal(0.0) if x==filler else x for x in finesRevenues]))
					totalRevenues = list(map(operator.add, totalRevenues, [Decimal(0.0) if x==filler else x for x in finesRevenues]))

				if 3 in PPIDs:
					ultraFinesRevenues = []
					revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=3,
						date__gte=startDate, date__lte=endDate).order_by("date")

					currDate = startDate
					for entry in revenueEntries:
						while currDate < entry.date:
							ultraFinesRevenues.append(filler)
							currDate += datetime.timedelta(days=1)
						ultraFinesRevenues.append(round(Decimal(entry.plantProductRevenue),2))
					ultraFinesRevenues += [filler]*(endDate-currDate).days

					sumUltraFinesRevenues = sum([Decimal(0.0) if x==filler else x for x in ultraFinesRevenues])
					# lumpPlusFinesRevenues = list(map(operator.add, lumpPlusFinesRevenues, [0.0 if x==filler else x for x in finesRevenues]))
					totalRevenues = list(map(operator.add, totalRevenues, [Decimal(0.0) if x==filler else x for x in ultraFinesRevenues]))

				sumTotalRevenues = sum(totalRevenues)

				cashFlowPreTax = []
				cashFlowPostTax = []
				cumCashFlowPreTax = []
				cumCashFlowPostTax = []

				annualCashFlowPreTax = []
				annualCashFlowPostTax = []
				annualCumCashFlowPreTax = []
				annualCumCashFlowPostTax = []
				# Beginning populating tblCashFlow data for HTML report here
				currCumCashFlowPreTax = (-1)*sumNegCAPEX
				currCumCashFlowPostTax = (-1)*sumNegCAPEX

				cashFlowEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID)
				for year in range(1, projectPeriods.count()+1):
					currPeriod = projectPeriods.get(year=year)
					currStart = currPeriod.startDate
					currEnd = currPeriod.endDate
					currCashFlows = cashFlowEntries.filter(date__gte=currStart, date__lte=currEnd).order_by('-date')
					if not currCashFlows:
						annualCumCashFlowPreTax.append(currCumCashFlowPreTax)
						annualCumCashFlowPostTax.append(currCumCashFlowPostTax)
						annualCashFlowPreTax.append(Decimal(0.0))
						annualCashFlowPostTax.append(Decimal(0.0))
					else:
						lastCashFlow = currCashFlows[0]
						annualCumCashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax),2))
						annualCumCashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax),2))
						annualCashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax) - currCumCashFlowPreTax,2))
						annualCashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax) - currCumCashFlowPostTax,2))
						currCumCashFlowPreTax = annualCumCashFlowPreTax[-1]
						currCumCashFlowPostTax = annualCumCashFlowPostTax[-1]
				preTaxIRR = round(np.irr([(-1)*sumNegCAPEX] + annualCashFlowPreTax)*100,2)
				postTaxIRR = round(np.irr([(-1)*sumNegCAPEX] + annualCashFlowPostTax)*100,2)

				prevCashFlows = cashFlowEntries.filter(date__lt=startDate).order_by('-date')
				if not prevCashFlows:
					currCumCashFlowPreTax = (-1)*sumNegCAPEX
					currCumCashFlowPostTax = (-1)*sumNegCAPEX
				else:
					currCumCashFlowPreTax = round(Decimal(prevCashFlows[0].cumulativeCashFlowPreTax),2)
					currCumCashFlowPostTax = round(Decimal(prevCashFlows[0].cumulativeCashFlowPostTax),2)

				currCashFlows = cashFlowEntries.filter(date__gte=startDate, date__lte=endDate).order_by('date')
				if not currCashFlows:
					cashFlowPreTax += [Decimal(0.0)]*((endDate - startDate).days)
					cashFlowPostTax += [Decimal(0.0)]*((endDate - startDate).days)
					cumCashFlowPreTax += [currCumCashFlowPreTax]*((endDate - startDate).days)
					cumCashFlowPostTax += [currCumCashFlowPostTax]*((endDate - startDate).days)
				else:
					currDate = startDate
					for entry in currCashFlows:
						cashFlowPreTax += [Decimal(0.0)]*((entry.date - currDate).days)
						cashFlowPostTax += [Decimal(0.0)]*((entry.date - currDate).days)
						cumCashFlowPreTax += [currCumCashFlowPreTax]*((entry.date - currDate).days)
						cumCashFlowPostTax += [currCumCashFlowPostTax]*((entry.date - currDate).days)

						cumCashFlowPreTax.append(round(Decimal(entry.cumulativeCashFlowPreTax),2))
						cumCashFlowPostTax.append(round(Decimal(entry.cumulativeCashFlowPostTax),2))
						cashFlowPreTax.append(round(Decimal(entry.cashFlowPreTax),2))
						cashFlowPostTax.append(round(Decimal(entry.cashFlowPostTax),2))

						currDate = entry.date
						currCumCashFlowPreTax = cumCashFlowPreTax[-1]
						currCumCashFlowPostTax = cumCashFlowPostTax[-1]
					cashFlowPreTax += [Decimal(0.0)]*((endDate - currDate).days)
					cashFlowPostTax += [Decimal(0.0)]*((endDate - currDate).days)
					cumCashFlowPreTax += [currCumCashFlowPreTax]*((endDate - currDate).days)
					cumCashFlowPostTax += [currCumCashFlowPostTax]*((endDate - currDate).days)
				sumCashFlowPreTax = sum(cashFlowPreTax)
				sumCashFlowPostTax = sum(cashFlowPostTax)

				positiveFlow = False
				paybackPreTax = []
				if cumCashFlowPreTax[0] > 0:
					paybackPreTax = [Decimal(0.0)]*((endDate - startDate).days)
				else:
					for i in range(len(cumCashFlowPreTax)):
						if positiveFlow:
							paybackPreTax.append(Decimal(0.0))
						else:
							if cumCashFlowPreTax[i] > 0:
								if i == 0:
									paybackPreTax.append(Decimal(0.0))
								else:
									paybackPreTax.append(abs(round(cumCashFlowPreTax[i-1] / cashFlowPreTax[i],4)))
								positiveFlow = True
							else:
								paybackPreTax.append(Decimal(1.0))
				sumPaybackPreTax = sum(paybackPreTax)

				positiveFlow = False
				paybackPostTax = []
				if cumCashFlowPostTax[0] > 0:
					paybackPostTax = [Decimal(0.0)]*((endDate - startDate).days)
				else:
					for i in range(len(cumCashFlowPostTax)):
						if positiveFlow:
							paybackPostTax.append(Decimal(0.0))
						else:
							if cumCashFlowPostTax[i] > 0:
								if i == 0:
									paybackPostTax.append(Decimal(0.0))
								else:
									paybackPostTax.append(abs(round(cumCashFlowPostTax[i-1] / cashFlowPostTax[i],4)))
								positiveFlow = True
							else:
								paybackPostTax.append(Decimal(1.0))
				sumPaybackPostTax = sum(paybackPostTax)

				# Calculate and Update NPVs and IRRs
				preTaxPVs = {}
				postTaxPVs = {}
				sumPreTaxNPV = {}
				sumPostTaxNPV = {}
				financialsEntries = tblFinancials.objects.filter(projectID=latestProject.projectID)
				for rate in discountRates:
					rate = int(round(rate*100))
					preTaxPVs[rate] = []
					postTaxPVs[rate] = []

					currFinancials = financialsEntries.filter(date__gte=startDate, date__lte=endDate, 
						discountRate=rate).order_by('date')
					if not currFinancials:
						preTaxPVs[rate] += [0.0]*((endDate - startDate).days)
						postTaxPVs[rate] += [0.0]*((endDate - startDate).days)
					else:
						currDate = startDate
						for entry in currFinancials:
							preTaxPVs[rate] += [0.0]*((entry.date - currDate).days)
							postTaxPVs[rate] += [0.0]*((entry.date - currDate).days)

							preTaxPVs[rate].append(round(entry.NPVPreTax,2))
							postTaxPVs[rate].append(round(entry.NPVPostTax,2))

							currDate = entry.date
						preTaxPVs[rate] += [0.0]*((endDate - currDate).days)
						postTaxPVs[rate] += [0.0]*((endDate - currDate).days)
					sumPreTaxNPV[rate] = sum(preTaxPVs[rate])
					sumPostTaxNPV[rate] = sum(postTaxPVs[rate])

				# Create DL Form Data
				reportRowCount = 1

				reportData = ""

				currRow = 'Item,'
				for date in dateVals:
					# currRow += 'Year{0},'.format(year)
					currRow += date + ','
				currRow += 'Total;'
				reportData += currRow

				reportData += ";Mining;"
				for curr in range(1, numStockpiles+1):
					currRow = "Stockpile {0} Ore (kt),".format(curr) + ''.join([*[str(round(x,2))+',' for x in minePlanTonnageVals[curr]]]) + str(round(sumMinePlanTonnages[curr],2)) + ";"
					reportData += currRow

				reportData += ";Processing;"
				for curr in range(1, numStockpiles+1):
					reportData += "Stockpile {0} Ore;".format(curr)
					currRow = 'Tonnage (kt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]) + ',' + str(round(tonnageTotals[curr],2)) + ";"
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]) + ';'

				reportData += ";Plant Product;"

				if 1 in PPIDs:
					reportData += "Lump;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]) + ',' + str(round(lumpTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]) + ';'

				if 2 in PPIDs:
					reportData += "Fines;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]) + ',' + str(round(finesTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]) + ';'

				if 3 in PPIDs:
					reportData += "Ultra Fines;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]) + ',' + str(round(ultraFinesTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]) + ';'

				reportData += 'Total Product (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]) + ',' + str(round(sumTotalProducts,2)) + ';'

				if 4 in PPIDs:
					reportData += "Rejects;"
					currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]) + ',' + str(round(rejectsTonnageTotal,2)) + ';'
					reportData += currRow
					for i in range(len(commIDs)):
						currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]) + ';'
						reportData += currRow
					reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]) + ';'

				reportData += ";Products Selling Price;"

				if 1 in PPIDs:
					reportData += 'Lump Selling Price (USD/dmt);'
					reportData += 'Lump Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]) + ';'
					for i in range(len(commIDs)):
						reportData += 'Lump {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]) + ';'
					reportData += 'Lump Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]) + ',' + 'Avg: ' + str(round(avgLumpSellingPrice,2)) + ';'
					reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
					reportData += 'Net Lump Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]) + ',' + 'Avg: ' + str(round(avgNetLumpPrice,2)) + ';'
					reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
					reportData += 'Net Lump Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetLumpPrice,2)) + ';'

				if 2 in PPIDs:
					reportData += 'Fines Selling Price (USD/dmt);'
					reportData += 'Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]) + ';'
					for i in range(len(commIDs)):
						reportData += 'Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]) + ';'
					reportData += 'Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]) + ',' + 'Avg: ' + str(round(avgFinesSellingPrice,2)) + ';'
					reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
					reportData += 'Net Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]) + ',' + 'Avg: ' + str(round(avgNetFinesPrice,2)) + ';'
					reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
					reportData += 'Net Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetFinesPrice,2)) + ';'

				if 3 in PPIDs:
					reportData += 'Ultra Fines Selling Price (USD/dmt);'
					reportData += 'Ultra Fines Base (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]) + ';'
					for i in range(len(commIDs)):
						reportData += 'Ultra Fines {0} Penalty (USD/t),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]) + ';'
					reportData += 'Ultra Fines Selling Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]) + ',' + 'Avg: ' + str(round(avgUltraFinesSellingPrice,2)) + ';'
					reportData += 'Shipping (USD/dmt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]) + ';'
					reportData += 'Net Ultra Fines Price (USD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]) + ',' + 'Avg: ' + str(round(avgNetUltraFinesPrice,2)) + ';'
					reportData += 'Exchange Rate (USD to CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]) + ';'
					reportData += 'Net Ultra Fines Price (CAD/t),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]) + ',' + 'Avg: ' + str(round(avgExchangeNetUltraFinesPrice,2)) + ';'

				reportData += ';Revenues;'
				if 1 in PPIDs:
					reportData += 'Lump Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]]) + ',' + str(round(sumLumpRevenues,2)) + ';'
				if 2 in PPIDs:
					reportData += 'Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]]) + ',' + str(round(sumFinesRevenues,2)) + ';'
				if 3 in PPIDs:
					reportData += 'Ultra Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]]) + ',' + str(round(sumUltraFinesRevenues,2)) + ';'
				reportData += 'TOTAL REVENUE,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'

				reportData += ';COSTS;'
				reportData += 'OPEX (millions CAD);'
				reportData += 'Mining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mining]]) + ',' + str(round(sumMining,2)) + ';'
				reportData += 'Stockpile LG Reclaiming,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]]) + ',' + str(round(sumStockpileLG,2)) + ';'
				reportData += 'Pit Dewatering,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]]) + ',' + str(round(sumDewatering,2)) + ';'
				reportData += 'Processing,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in processing]]) + ',' + str(round(sumProcessing,2)) + ';'
				reportData += 'Product Hauling,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]]) + ',' + str(round(sumHauling,2)) + ';'
				reportData += 'Load-out and Rail Loop,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]]) + ',' + str(round(sumLoadOutRailLoop,2)) + ';'
				reportData += 'G&A (Site),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]]) + ',' + str(round(sumGASite,2)) + ';'
				reportData += 'G&A (Room & Board / FIFO),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]]) + ',' + str(round(sumGARoom,2)) + ';'
				reportData += 'Rail Transportation Port and Shiploading,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]]) + ',' + str(round(sumRailTransport,2)) + ';'
				reportData += 'Corporate G&A,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]]) + ',' + str(round(sumGACorp,2)) + ';'
				reportData += 'TOTAL OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
				reportData += 'ROYALTIES (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'

				reportData += 'CAPEX (millions CAD);'
				reportData += 'Pre-Stripping,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]]) + ',' + str(round(sumPreStrip,2)) + ';'
				reportData += 'Mining Equipment Initial,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]]) + ',' + str(round(sumMineEquipInitial,2)) + ';'
				reportData += 'Mining Equipment Sustaining,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]]) + ',' + str(round(sumMineEquipSustain,2)) + ';'
				reportData += 'Project Infrastructure Direct Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]]) + ',' + str(round(sumInfraDirectCost,2)) + ';'
				reportData += 'Project Infrastructure Indirect Costs,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]]) + ',' + str(round(sumInfraIndirectCost,2)) + ';'
				reportData += 'Project Infrastructure Contingency,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]]) + ',' + str(round(sumContingency,2)) + ';'
				reportData += 'Railcars,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]]) + ',' + str(round(sumRailcars,2)) + ';'
				reportData += 'Other Mobile Equipment,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]]) + ',' + str(round(sumOtherMobEquip,2)) + ';'
				reportData += 'Closure and Rehab Assurance Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]]) + ',' + str(round(sumClosureRehabAssure,2)) + ';'
				reportData += 'Deposits Provision Payments,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]]) + ',' + str(round(sumDepoProvisionPay,2)) + ';'
				reportData += 'TOTAL CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'

				reportData += 'TAXES (millions CAD);'
				reportData += 'Federal Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]]) + ',' + str(round(sumFederalTaxes,2)) + ';'
				reportData += 'Provincial Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]]) + ',' + str(round(sumProvincialTaxes,2)) + ';'
				reportData += 'Mining Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]]) + ',' + str(round(sumMiningTaxes,2)) + ';'
				reportData += 'TOTAL (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

				reportData += ';SUMMARY;'
				reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'
				reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
				reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
				reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
				reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
				reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
				reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

				reportData += ';PRE-TAX CASH FLOW;'
				reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + str(round(sumCashFlowPreTax,2)) + ';'
				reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ';'
				reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + str(round(sumPaybackPreTax,2)) + ';'
				for rate in discountRates:
					reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPreTaxNPV[int(round(rate*100))],2)) + ';'
				reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(preTaxIRR,2)) + ';'

				reportData += ';POST-TAX CASH FLOW;'
				reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + str(round(sumCashFlowPostTax,2)) + ';'
				reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ';'
				reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + str(round(sumPaybackPostTax,2)) + ';'
				for rate in discountRates:
					reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPostTaxNPV[int(round(rate*100))],2)) + ';'
				reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(postTaxIRR,2)) + ';'

				filter_form = filterForm(mineID=mineID, startDate=projectStartDate, endDate=projectEndDate)
				default_filter_form = defaultFilterForm(mineID=mineID, thisYearStartDate=thisYearStartDate, thisYearEndDate=thisYearEndDate,
					lastYearStartDate=lastYearStartDate, lastYearEndDate=lastYearEndDate,
					thisQuarterStartDate=thisQuarterStartDate, thisQuarterEndDate=thisQuarterEndDate,
					lastQuarterStartDate=lastQuarterStartDate, lastQuarterEndDate=lastQuarterEndDate)
				report_form = reportForm(mineID=mineID, reportData=reportData)

				return render(request, 'report/report2.html', {'filterForm': filter_form, 'reportForm': report_form,
					'defaultFilterForm': default_filter_form,
					'dateVals': dateVals, 'commIDs': commIDs, 'commNameList': commNameList,
					'numStockpiles': list(range(1, numStockpiles+1)),
					'minePlanTonnageVals': minePlanTonnageVals, 'sumMinePlanTonnages': sumMinePlanTonnages,
					# 'minePlanHGTonnageVals': minePlanHGTonnageVals, 'minePlanLGTonnageVals': minePlanLGTonnageVals,
					# 'minePlanWasteTonnageVals': minePlanWasteTonnageVals, 'minePlanOverburdenTonnageVals': minePlanOverburdenTonnageVals,
					# 'sumMinePlanHGTonnage': sumMinePlanHGTonnage, 'sumMinePlanLGTonnage': sumMinePlanLGTonnage,
					# 'sumMinePlanWasteTonnage': sumMinePlanWasteTonnage, 'sumMinePlanOverburdenTonnage': sumMinePlanOverburdenTonnage,
					'tonnageVals': tonnageVals, 'tonnageTotals': tonnageTotals, 'gradeVals': gradeVals, 'moistures': moistures,
					# 'HGTonnageVals': HGTonnageVals, 'HGTonnageTotal': HGTonnageTotal, 'HGGradeVals': HGGradeVals, 'HGMoistures': HGMoistures,
					# 'LGTonnageVals': LGTonnageVals, 'LGTonnageTotal': LGTonnageTotal, 'LGGradeVals': LGGradeVals, 'LGMoistures': LGMoistures,
					'lumpTonnageVals': lumpTonnageVals, 'lumpTonnageTotal': lumpTonnageTotal, 'lumpGradeVals': lumpGradeVals, 'lumpMoistures': lumpMoistures,
					'finesTonnageVals': finesTonnageVals, 'finesTonnageTotal': finesTonnageTotal, 'finesGradeVals': finesGradeVals, 'finesMoistures': finesMoistures,
					'ultraFinesTonnageVals': ultraFinesTonnageVals, 'ultraFinesTonnageTotal': ultraFinesTonnageTotal, 'ultraFinesGradeVals': ultraFinesGradeVals, 'ultraFinesMoistures': ultraFinesMoistures,
					'totalProducts': totalProducts, 'sumTotalProducts': sumTotalProducts,
					'rejectsTonnageVals': rejectsTonnageVals, 'rejectsTonnageTotal': rejectsTonnageTotal, 'rejectsGradeVals': rejectsGradeVals, 'rejectsMoistures': rejectsMoistures,
					'fullShippingCosts': fullShippingCosts, 'fullExchangeRates': fullExchangeRates,
					'HGLumps': HGLumps, 'lumpPenaltyVals': lumpPenaltyVals, 'lumpSellingPrices': lumpSellingPrices, 'avgLumpSellingPrice': avgLumpSellingPrice,
					'netLumpPrices': netLumpPrices, 'avgNetLumpPrice': avgNetLumpPrice, 'exchangeNetLumpPrices': exchangeNetLumpPrices,
					'avgExchangeNetLumpPrice': avgExchangeNetLumpPrice,
					'HGFines': HGFines, 'finesPenaltyVals': finesPenaltyVals, 'finesSellingPrices': finesSellingPrices, 'avgFinesSellingPrice': avgFinesSellingPrice,
					'netFinesPrices': netFinesPrices, 'avgNetFinesPrice': avgNetFinesPrice, 'exchangeNetFinesPrices': exchangeNetFinesPrices,
					'avgExchangeNetFinesPrice': avgExchangeNetFinesPrice,
					'HGUltraFines': HGUltraFines, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals, 'ultraFinesSellingPrices': ultraFinesSellingPrices,
					'avgUltraFinesSellingPrice': avgUltraFinesSellingPrice,
					'netUltraFinesPrices': netUltraFinesPrices, 'exchangeNetUltraFinesPrices': exchangeNetUltraFinesPrices,
					'avgExchangeNetUltraFinesPrice': avgExchangeNetUltraFinesPrice,
					'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
					'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
					'totalRevenues': totalRevenues, 'sumTotalRevenues': sumTotalRevenues,
					'mining': mining, 'stockpileLG': stockpileLG, 'dewatering': dewatering, 'processing': processing, 'hauling': hauling,
					'loadOutRailLoop': loadOutRailLoop, 'GASite': GASite, 'GARoom': GARoom, 'railTransport': railTransport, 'GACorp': GACorp,
					'sumMining': sumMining, 'sumStockpileLG': sumStockpileLG, 'sumDewatering': sumDewatering, 'sumProcessing': sumProcessing,
					'sumHauling': sumHauling, 'sumLoadOutRailLoop': sumLoadOutRailLoop, 'sumGASite': sumGASite, 'sumGARoom': sumGARoom,
					'sumRailTransport': sumRailTransport, 'sumGACorp': sumGACorp,
					'totalOPEX': totalOPEX, 'sumTotalOPEX':sumTotalOPEX, 'royalties': royalties, 'sumRoyalties': sumRoyalties,
					'preStrip': preStrip, 'mineEquipInitial': mineEquipInitial, 'mineEquipSustain': mineEquipSustain, 'infraDirectCost': infraDirectCost,
					'infraIndirectCost': infraIndirectCost, 'contingency': contingency, 'railcars': railcars, 'otherMobEquip': otherMobEquip,
					'closureRehabAssure': closureRehabAssure, 'depoProvisionPay': depoProvisionPay, 'sumPreStrip': sumPreStrip,
					'sumMineEquipInitial': sumMineEquipInitial, 'sumMineEquipSustain': sumMineEquipSustain, 'sumInfraDirectCost': sumInfraDirectCost,
					'sumInfraIndirectCost': sumInfraIndirectCost, 'sumContingency': sumContingency, 'sumRailcars': sumRailcars,
					'sumOtherMobEquip': sumOtherMobEquip, 'sumClosureRehabAssure': sumClosureRehabAssure, 'sumDepoProvisionPay': sumDepoProvisionPay,
					'totalCAPEX': totalCAPEX, 'sumTotalCAPEX': sumTotalCAPEX,
					'federalTaxes': federalTaxes, 'provincialTaxes': provincialTaxes, 'miningTaxes': miningTaxes,
					'sumFederalTaxes': sumFederalTaxes, 'sumProvincialTaxes': sumProvincialTaxes, 'sumMiningTaxes': sumMiningTaxes,
					'totalTaxes': totalTaxes, 'sumTotalTaxes': sumTotalTaxes,
					'workCapCurrentProd': workCapCurrentProd, 'workCapCostsLG': workCapCostsLG,
					'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG,
					'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
					'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
					'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
					'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
					'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
					'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
					'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})
					# 'cashFlowPreTax': cashFlowPreTax, 'cashFlowPostTax': cashFlowPostTax,
					# 'cumCashFlowPreTax': cumCashFlowPreTax, 'cumCashFlowPostTax': cumCashFlowPostTax,
					# 'sumCashFlowPreTax': sumCashFlowPreTax, 'sumCashFlowPostTax': sumCashFlowPostTax,
					# 'paybackPreTax': paybackPreTax, 'paybackPostTax': paybackPostTax,
					# 'sumPaybackPreTax': sumPaybackPreTax, 'sumPaybackPostTax': sumPaybackPostTax,
					# 'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR,
					# 'preTaxPVs': preTaxPVs, 'postTaxPVs': postTaxPVs, 'sumPreTaxNPV': sumPreTaxNPV, 'sumPostTaxNPV': sumPostTaxNPV})


def reportFilter(request):
	if request.method == 'POST':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="report.csv"'

		writer = csv.writer(response)
		writer.write("a,b,c\r\n")
		# writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
		# writer.writerow(['Second row', 'A', 'B', 234, '"Testing"', "Here's a quote"])
		# writer.writerow(['This,row,splits,by,commas'])

		# reportRowCount = request.session['reportRowCount']
		# for i in range(1, reportRowCount+1):
		# 	writer.writerow(request.session['reportRow{0}'.format(i)])

		return response
