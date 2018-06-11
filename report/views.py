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
from math import pow
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
	# HGTonnageVals = None
	# HGTonnageTotal = None
	# HGGradeVals = None
	# HGMoistures = None

	# LGTonnageVals = None
	# LGTonnageTotal = None
	# LGGradeVals = None
	# LGMoistures = None

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

	yearCount = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).count()
	fullYearVals = list(range(1, yearCount+1))
	for i in range(yearCount):
		i += 1
		currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=i)
		currStart = currPeriod.startDate
		currEnd = currPeriod.endDate
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

	for year in range(1, yearCount+1):
		currOPEX = tblOPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
		mining.append(round(Decimal(currOPEX.mining)*1000,2))
		infrastructure.append(round(Decimal(currOPEX.infrastructure)*1000,2))
		stockpileLG.append(round(Decimal(currOPEX.stockpileLG)*1000,2))
		dewatering.append(round(Decimal(currOPEX.dewatering)*1000,2))
		processing.append(round(Decimal(currOPEX.processing)*1000,2))
		hauling.append(round(Decimal(currOPEX.hauling)*1000,2))
		loadOutRailLoop.append(round(Decimal(currOPEX.loadOutRailLoop)*1000,2))
		GASite.append(round(Decimal(currOPEX.GASite)*1000,2))
		GARoom.append(round(Decimal(currOPEX.GARoomBoardFIFO)*1000,2))
		railTransport.append(round(Decimal(currOPEX.railTransport)*1000,2))
		GACorp.append(round(Decimal(currOPEX.GACorp)*1000,2))
		royalties.append(round(Decimal(currOPEX.royalties)*1000,2))
		transportation.append(round(Decimal(currOPEX.transportation)*1000,2))
		GA.append(round(Decimal(currOPEX.GA)*1000,2))
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

	for year in range(1, yearCount+1):
		currCAPEX = tblCAPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
		preStrip.append(round(Decimal(currCAPEX.preStrip)*1000,2))
		mineEquipInitial.append(round(Decimal(currCAPEX.mineEquipInitial)*1000,2))
		mineEquipSustain.append(round(Decimal(currCAPEX.mineEquipSustain)*1000,2))
		infraDirectCost.append(round(Decimal(currCAPEX.infraDirectCost)*1000,2))
		infraIndirectCost.append(round(Decimal(currCAPEX.infraIndirectCost)*1000,2))
		contingency.append(round(Decimal(currCAPEX.contingency)*1000,2))
		railcars.append(round(Decimal(currCAPEX.railcars)*1000,2))
		otherMobEquip.append(round(Decimal(currCAPEX.otherMobEquip)*1000,2))
		closureRehabAssure.append(round(Decimal(currCAPEX.closureRehabAssure)*1000,2))
		depoProvisionPay.append(round(Decimal(currCAPEX.depoProvisionPay)*1000,2))
		workCapCurrentProd.append(round(Decimal(currCAPEX.workCapCurrentProd)*1000,2))
		workCapCostsLG.append(round(Decimal(currCAPEX.workCapCostsLG)*1000,2))
		EPCM.append(round(Decimal(currCAPEX.EPCM)*1000,2))
		ownerCost.append(round(Decimal(currCAPEX.ownerCost)*1000,2))
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

	for year in range(1, yearCount+1):
		currTaxes = tblTaxes.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
		federalTaxes.append(round(Decimal(currTaxes.federal),2))
		provincialTaxes.append(round(Decimal(currTaxes.provincial),2))
		miningTaxes.append(round(Decimal(currTaxes.mining),2))
	sumFederalTaxes = sum(federalTaxes)
	sumProvincialTaxes = sum(provincialTaxes)
	sumMiningTaxes = sum(miningTaxes)
	totalTaxes = [sum(x) for x in zip(federalTaxes, provincialTaxes, miningTaxes)]
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
		filter_form = filterForm(mineID=mineID)
		report_form = reportForm(mineID=mineID, reportData=reportData)

		# Create DL Form Data
		# reportRowCount = 1

		# currDataRow = []
		# currDataRow.append('Item')
		# for year in range(1, yearCount+1):
		# 	currDataRow.append('Year{0}'.format(year))
		# currDataRow.append('Total')
		# request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining']

		# for curr in range(1, numStockpiles+1):
		# 	reportRowCount += 1
		# 	currDataRow = ["Stockpile {0} Ore (kt)".format(curr)] + [*[str(round(x,2)) for x in minePlanTonnageVals[curr]]]
		# 	# currDataRow += [*[str(round(x,2)) for x in minePlanTonnageVals[curr]]]
		# 	currDataRow.append(str(round(sumMinePlanTonnages[curr],2)))
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Processing']

		# for curr in range(1, numStockpiles+1):
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ["Stockpile {0} Ore".format(curr)]
		# 	reportRowCount += 1
		# 	currDataRow = ['Tonnage (kt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]
		# 	currDataRow.append(tonnageTotals[curr])
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]
		# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Plant Product']

		# if 1 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump']
		# 	reportRowCount += 1
		# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]
		# 	currDataRow.append(lumpTonnageTotal)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]
		# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# if 2 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines']
		# 	reportRowCount += 1
		# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]
		# 	currDataRow.append(finesTonnageTotal)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]
		# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# if 3 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines']
		# 	reportRowCount += 1
		# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]
		# 	currDataRow.append(ultraFinesTonnageTotal)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]
		# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# reportRowCount += 1
		# currDataRow = ['Total Product (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]
		# currDataRow.append(sumTotalProducts)
		# request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# if 4 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Rejects']
		# 	reportRowCount += 1
		# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]
		# 	currDataRow.append(str(round(rejectsTonnageTotal,2)))
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]
		# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Products Selling Price']

		# if 1 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump Selling Price (USD/dmt)']
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump Base (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		request.session['reportRow{0}'.format(reportRowCount)] = ['Lump {0} Penalty (USD/t)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Lump Selling Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]
		# 	currDataRow.append('Avg: ' + avgLumpSellingPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Shipping (USD/dmt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Net Lump Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]
		# 	currDataRow.append('Avg: ' + avgNetLumpPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Exchange Rate (USD to CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Net Lump Price (CAD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]
		# 	currDataRow.append('Avg: ' + avgExchangeNetLumpPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# if 2 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines Selling Price (USD/dmt)']
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines Base (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		request.session['reportRow{0}'.format(reportRowCount)] = ['Fines {0} Penalty (USD/t)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Fines Selling Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]
		# 	currDataRow.append('Avg: ' + avgFinesSellingPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Shipping (USD/dmt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Net Fines Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]
		# 	currDataRow.append('Avg: ' + avgNetFinesPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Exchange Rate (USD to CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Net Fines Price (CAD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]
		# 	currDataRow.append('Avg: ' + avgExchangeNetFinesPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# if 3 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines Selling Price (USD/dmt)']
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines Base (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]
		# 	for i in range(len(commIDs)):
		# 		reportRowCount += 1
		# 		request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines {0} Penalty (USD/t)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Ultra Fines Selling Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]
		# 	currDataRow.append('Avg: ' + avgUltraFinesSellingPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Shipping (USD/dmt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Net Ultra Fines Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]
		# 	currDataRow.append('Avg: ' + avgNetUltraFinesPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Exchange Rate (USD to CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]
		# 	reportRowCount += 1
		# 	currDataRow = ['Net Ultra Fines Price (CAD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]
		# 	currDataRow.append('Avg: ' + avgExchangeNetUltraFinesPrice)
		# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Revenues']

		# if 1 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump Revenue'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]] + [sumLumpRevenues]
		# if 2 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines Revenue'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]] + [sumFinesRevenues]
		# if 3 in PPIDs:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines Revenue'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]] + [sumUltraFinesRevenues]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL REVENUE'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]] + [sumTotalRevenues]

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['COSTS']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['OPEX (millions CAD)']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in mining]] + [str(round(sumMining,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Stockpile LG Reclaiming'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]] + [str(round(sumStockpileLG,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Pit Dewatering'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]] + [str(round(sumDewatering,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Processing'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in processing]] + [str(round(sumProcessing,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Product Hauling'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]] + [str(round(sumHauling,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Load-out and Rail Loop'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]] + [str(round(sumLoadOutRailLoop,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['G&A (Site)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]] + [str(round(sumGASite,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['G&A (Room & Board / FIFO)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]] + [str(round(sumGARoom,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Rail Transportation, Port and Shiploading'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]] + [str(round(sumRailTransport,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Corporate G&A'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]] + [str(round(sumGACorp,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL OPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]] + [str(round(sumTotalOPEX,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['ROYALTIES (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]] + [str(round(sumRoyalties,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['CAPEX (millions CAD)']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Pre-Stripping'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]] + [str(round(sumPreStrip,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining Equipment Initial'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]] + [str(round(sumMineEquipInitial,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining Equipment Sustaining'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]] + [str(round(sumMineEquipSustain,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Project Infrastructure Direct Costs'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]] + [str(round(sumInfraDirectCost,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Project Infrastructure Indirect Costs'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]] + [str(round(sumInfraIndirectCost,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Project Infrastructure Contingency'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]] + [str(round(sumContingency,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Railcars'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]] + [str(round(sumRailcars,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Other Mobile Equipment'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]] + [str(round(sumOtherMobEquip,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Closure and Rehab Assurance Payments'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]] + [str(round(sumClosureRehabAssure,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Deposits Provision Payments'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]] + [str(round(sumDepoProvisionPay,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL CAPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]] + [str(round(sumTotalCAPEX,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['TAXES (millions CAD)']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Federal Corporate Taxes'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]] + [str(round(sumFederalTaxes,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Provincial Corporate Taxes'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]] + [str(round(sumProvincialTaxes,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining Taxes'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]] + [str(round(sumMiningTaxes,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]] + [str(round(sumTotalTaxes,2))]

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['SUMMARY']

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Revenues (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]] + [sumTotalRevenues]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['OPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]] + [str(round(sumTotalOPEX,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Royalties (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]] + [str(round(sumRoyalties,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['CAPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]] + [str(round(sumTotalCAPEX,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Working Capital (Current Production) (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]] + [str(round(sumWorkCapCurrentProd,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Working Capital (Costs of LG Stockpile) (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]] + [str(round(sumWorkCapCostsLG,2))]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Taxes (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]] + [str(round(sumTotalTaxes,2))]

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['PRE-TAX CASH FLOW']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]] + [sumCashFlowPreTax]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Cumulative Undiscounted Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]] + [sumCashFlowPreTax]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Payback Period (year)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]] + [sumPaybackPreTax]
		# for rate in discountRates:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['PRE-TAX NPV @ {0}%'.format(int(round(rate*100)))] + [*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]] + [sumPreTaxNPV[int(round(rate*100))]]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['INTERNAL RATE OF RETURN (IRR)'] + [preTaxIRR]

		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['POST-TAX CASH FLOW']
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]] + [sumCashFlowPostTax]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Cumulative Undiscounted Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]] + [sumCashFlowPostTax]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['Payback Period (year)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]] + [sumPaybackPostTax]
		# for rate in discountRates:
		# 	reportRowCount += 1
		# 	request.session['reportRow{0}'.format(reportRowCount)] = ['POST-TAX NPV @ {0}%'.format(int(round(rate*100)))] + [*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]] + [sumPostTaxNPV[int(round(rate*100))]]
		# reportRowCount += 1
		# request.session['reportRow{0}'.format(reportRowCount)] = ['INTERNAL RATE OF RETURN (IRR)'] + [postTaxIRR]

		# request.session['reportRowCount'] = reportRowCount

		return render(request, 'report/report.html', {'filterForm': filter_form, 'reportForm': report_form,
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
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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

	# # High Grade Ore data if declared
	# if 1 in MPIDs:
	# 	HGTonnageVals = []
	# 	HGGradeVals = {}
	# 	for year in yearVals:
	# 		# TO FIX: After Year column has been added to tblMineProductTonnageOptimized
	# 		currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
	# 		# HGTonnageEntry = tblMineProductTonnageOptimized.objects.filter(mineID=mineID, mineProductID=1).order_by('-dateAdded')[0]
	# 		HGTonnageEntries = tblMineProductTonnageOptimized.objects.filter(projectID=latestProject.projectID, mineProductID=1,
	# 			date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
	# 		sumTonnage = HGTonnageEntries.aggregate(sumTonnage=Sum('tonnage'))
	# 		HGTonnageVals.append(sumTonnage['sumTonnage'])
	# 		# HGTonnageVals.append(HGTonnageEntry.tonnage)
	# 	HGTonnageTotal = sum(HGTonnageVals)

	# 	for i in range(len(commIDs)):
	# 	# for ID in commIDs:
	# 		tempGrades = []
	# 		for year in yearVals:
	# 			# TO FIX: After Year column has been added to tblMineProduct
	# 			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
	# 			# MPEntry = tblMineProduct.objects.filter(mineID=mineID, mineProductID=1, commodityID=commIDs[i]).order_by('-dateAdded')[0]
	# 			MPEntries = tblMineProductGradeOptimized.objects.filter(projectID=latestProject.projectID, mineProductID=1, commodityID=commIDs[i],
	# 				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
	# 			avgGrade = MPEntries.aggregate(avgGrade=Avg('grade'))
	# 			tempGrades.append(round(avgGrade['avgGrade'],2))
	# 		HGGradeVals[commNameList[i]] = tempGrades

	# 	HGMoistures = [round(latestInput.feedMoisture,2)]*yearCount

	# # Low Grade Ore data if declared
	# if 2 in MPIDs:
	# 	LGTonnageVals = []
	# 	LGGradeVals = {}
	# 	for year in yearVals:
	# 		# TO FIX: After Year column has been added to tblMineProductTonnageOptimized
	# 		# LGTonnageEntry = tblMineProductTonnageOptimized.objects.filter(mineID=mineID, mineProductID=2).order_by('-dateAdded')[0]
	# 		# LGTonnageVals.append(LGTonnageEntry.tonnage)
	# 		currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
	# 		LGTonnageEntries = tblMineProductTonnageOptimized.objects.filter(projectID=latestProject.projectID, mineProductID=2,
	# 			date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
	# 		sumTonnage = LGTonnageEntries.aggregate(sumTonnage=Sum('tonnage'))
	# 		LGTonnageVals.append(sumTonnage['sumTonnage'])
	# 	LGTonnageTotal = sum(LGTonnageVals)

	# 	for i in range(len(commIDs)):
	# 	# for ID in commIDs:
	# 		tempGrades = []
	# 		for year in yearVals:
	# 			# TO FIX: After Year column has been added to tblMineProduct
	# 			# MPEntry = tblMineProduct.objects.filter(mineID=mineID, mineProductID=2, commodityID=commIDs[i]).order_by('-dateAdded')[0]
	# 			# tempGrades.append(round(MPEntry.grade,2))
	# 			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
	# 			MPEntries = tblMineProductGradeOptimized.objects.filter(projectID=latestProject.projectID, mineProductID=2, commodityID=commIDs[i],
	# 				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
	# 			avgGrade = MPEntries.aggregate(avgGrade=Avg('grade'))
	# 			tempGrades.append(round(avgGrade['avgGrade'],2))
	# 		LGGradeVals[commNameList[i]] = tempGrades

	# 	LGMoistures = [round(latestInput.feedMoisture,2)]*yearCount

	# Lump data if declared
	if 1 in PPIDs:
		lumpTonnageVals = []
		lumpGradeVals = {}
		lumpDailyTonnages = {}

		for year in yearVals:
			# TO FIX: After Year column has been added to tblMineProductTonnageOptimized
			# lumpTonnageEntry = tblPlantProductTonnage.objects.filter(mineID=mineID, plantProductID=1).order_by('-dateAdded')[0]
			# lumpTonnageVals.append(round(Decimal(lumpTonnageEntry.tonnageDMT),2))
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
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
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=3,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
			sumPPRevenue = revenueEntries.aggregate(sumPPRevenue=Sum('plantProductRevenue'))
			currRevenue = round(Decimal(sumPPRevenue['sumPPRevenue']),2)
			ultraFinesRevenues.append(currRevenue)
			sumUltraFinesRevenues += currRevenue
		totalRevenues = list(map(operator.add, totalRevenues, ultraFinesRevenues))

	sumTotalRevenues = sum(totalRevenues)

	# # Handle Costs Section (OPEX)
	# mining = []
	# infrastructure = []
	# stockpileLG = []
	# dewatering = []
	# processing = []
	# hauling = []
	# loadOutRailLoop = []
	# GASite = []
	# GARoom = []
	# railTransport = []
	# GACorp = []
	# royalties = []
	# transportation = []
	# GA = []

	# for year in yearVals:
	# 	currOPEX = tblOPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
	# 	mining.append(round(Decimal(currOPEX.mining)*1000,2))
	# 	infrastructure.append(round(Decimal(currOPEX.infrastructure)*1000,2))
	# 	stockpileLG.append(round(Decimal(currOPEX.stockpileLG)*1000,2))
	# 	dewatering.append(round(Decimal(currOPEX.dewatering)*1000,2))
	# 	processing.append(round(Decimal(currOPEX.processing)*1000,2))
	# 	hauling.append(round(Decimal(currOPEX.hauling)*1000,2))
	# 	loadOutRailLoop.append(round(Decimal(currOPEX.loadOutRailLoop)*1000,2))
	# 	GASite.append(round(Decimal(currOPEX.GASite)*1000,2))
	# 	GARoom.append(round(Decimal(currOPEX.GARoomBoardFIFO)*1000,2))
	# 	railTransport.append(round(Decimal(currOPEX.railTransport)*1000,2))
	# 	GACorp.append(round(Decimal(currOPEX.GACorp)*1000,2))
	# 	royalties.append(round(Decimal(currOPEX.royalties)*1000,2))
	# 	transportation.append(round(Decimal(currOPEX.transportation)*1000,2))
	# 	GA.append(round(Decimal(currOPEX.GA)*1000,2))
	# sumMining = sum(mining)
	# sumStockpileLG = sum(stockpileLG)
	# sumDewatering = sum(dewatering)
	# sumProcessing = sum(processing)
	# sumHauling = sum(hauling)
	# sumLoadOutRailLoop = sum(loadOutRailLoop)
	# sumGASite = sum(GASite)
	# sumGARoom = sum(GARoom)
	# sumRailTransport = sum(railTransport)
	# sumGACorp = sum(GACorp)
	# sumRoyalties = sum(royalties)
	# totalOPEX = [sum(x) for x in zip(mining, stockpileLG, dewatering, processing, hauling,
	# 	loadOutRailLoop, GASite, GARoom, railTransport, GACorp)]
	# cashFlowOPEX = [sum(x) for x in zip(mining, infrastructure, stockpileLG, dewatering, processing, hauling,
	# 	loadOutRailLoop, GASite, GARoom, railTransport, GACorp, royalties, transportation, GA)]
	# sumTotalOPEX = sum(totalOPEX)


	# # Handle Costs Section (CAPEX)
	# preStrip = []
	# mineEquipInitial = []
	# mineEquipSustain = []
	# infraDirectCost = []
	# infraIndirectCost = []
	# contingency = []
	# railcars = []
	# otherMobEquip = []
	# closureRehabAssure = []
	# depoProvisionPay = []
	# workCapCurrentProd = []
	# workCapCostsLG = []
	# EPCM = []
	# ownerCost = []

	# for year in yearVals:
	# 	currCAPEX = tblCAPEX.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
	# 	preStrip.append(round(Decimal(currCAPEX.preStrip)*1000,2))
	# 	mineEquipInitial.append(round(Decimal(currCAPEX.mineEquipInitial)*1000,2))
	# 	mineEquipSustain.append(round(Decimal(currCAPEX.mineEquipSustain)*1000,2))
	# 	infraDirectCost.append(round(Decimal(currCAPEX.infraDirectCost)*1000,2))
	# 	infraIndirectCost.append(round(Decimal(currCAPEX.infraIndirectCost)*1000,2))
	# 	contingency.append(round(Decimal(currCAPEX.contingency)*1000,2))
	# 	railcars.append(round(Decimal(currCAPEX.railcars)*1000,2))
	# 	otherMobEquip.append(round(Decimal(currCAPEX.otherMobEquip)*1000,2))
	# 	closureRehabAssure.append(round(Decimal(currCAPEX.closureRehabAssure)*1000,2))
	# 	depoProvisionPay.append(round(Decimal(currCAPEX.depoProvisionPay)*1000,2))
	# 	workCapCurrentProd.append(round(Decimal(currCAPEX.workCapCurrentProd)*1000,2))
	# 	workCapCostsLG.append(round(Decimal(currCAPEX.workCapCostsLG)*1000,2))
	# 	EPCM.append(round(Decimal(currCAPEX.EPCM)*1000,2))
	# 	ownerCost.append(round(Decimal(currCAPEX.ownerCost)*1000,2))
	# sumPreStrip = sum(preStrip)
	# sumMineEquipInitial = sum(mineEquipInitial)
	# sumMineEquipSustain = sum(mineEquipSustain)
	# sumInfraDirectCost = sum(infraDirectCost)
	# sumInfraIndirectCost = sum(infraIndirectCost)
	# sumContingency = sum(contingency)
	# sumRailcars = sum(railcars)
	# sumOtherMobEquip = sum(otherMobEquip)
	# sumClosureRehabAssure = sum(closureRehabAssure)
	# sumDepoProvisionPay = sum(depoProvisionPay)
	# sumWorkCapCurrentProd = sum(workCapCurrentProd)
	# sumWorkCapCostsLG = sum(workCapCostsLG)
	# totalCAPEX = [sum(x) for x in zip(preStrip, mineEquipInitial, mineEquipSustain, infraDirectCost, infraIndirectCost,
	# 	contingency, railcars, otherMobEquip, closureRehabAssure, depoProvisionPay)]
	# cashFlowCAPEX = [sum(x) for x in zip(totalCAPEX, workCapCurrentProd, workCapCostsLG, EPCM, ownerCost)]
	# sumTotalCAPEX = sum(totalCAPEX)


	# # Handle Taxes Section
	# federalTaxes = []
	# provincialTaxes = []
	# miningTaxes = []

	# for year in yearVals:
	# 	currTaxes = tblTaxes.objects.filter(mineID=mineID, year=year).order_by('-dateAdded')[0]
	# 	federalTaxes.append(round(Decimal(currTaxes.federal),2))
	# 	provincialTaxes.append(round(Decimal(currTaxes.provincial),2))
	# 	miningTaxes.append(round(Decimal(currTaxes.mining),2))
	# sumFederalTaxes = sum(federalTaxes)
	# sumProvincialTaxes = sum(provincialTaxes)
	# sumMiningTaxes = sum(miningTaxes)
	# totalTaxes = [sum(x) for x in zip(federalTaxes, provincialTaxes, miningTaxes)]
	# sumTotalTaxes = sum(totalTaxes)

	# # tblCashFlow and tblFinancials Data Processing
	# # 1. Find the earliest (processed=FALSE) entry
	# notProcessed = tblCashFlow.objects.filter(projectID=latestProject.projectID, processed=False).order_by('date')
	# if notProcessed:
	# 	toProcess = notProcessed[0]

	# 	dailyOPEXPlusCAPEX = {}
	# 	dailyTaxes = {}
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
	# 		currOPEXPlusCAPEX = round((Decimal(currCAPEX) + Decimal(currOPEX))*1000,2)

	# 		currTaxes = round(Decimal(taxesRow.federal + taxesRow.provincial + taxesRow.mining),2)

	# 		if calendar.isleap(latestProject.startDate.year + i):
	# 			dailyOPEXPlusCAPEX[i+1] = currOPEXPlusCAPEX / Decimal(366.0)
	# 			dailyTaxes[i+1] = currTaxes / Decimal(366.0)
	# 		else:
	# 			dailyOPEXPlusCAPEX[i+1] = currOPEXPlusCAPEX / Decimal(365.0)
	# 			dailyTaxes[i+1] = currTaxes / Decimal(365.0)

	# 	earlyEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__lt=toProcess.date).order_by('-date')
	# 	if earlyEntries:
	# 		lastCashFlowEntry = earlyEntries[0]
	# 		currCumCashFlowPreTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPreTax)
	# 		currCumCashFlowPostTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPostTax)

	# 	else:
	# 		currCumCashFlowPreTax = Decimal(0.0)
	# 		currCumCashFlowPostTax = Decimal(0.0)

	# 	toUpdate = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=toProcess.date).order_by('date')
	# 	for entry in toUpdate:
	# 		currLumpPlusFines = Decimal(0.0)
	# 		if 1 in PPIDs:
	# 			currRev = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=1, date=entry.date)
	# 			currLumpPlusFines += Decimal(currRev.plantProductRevenue)
	# 		if 2 in PPIDs:
	# 			currRev = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=2, date=entry.date)
	# 			currLumpPlusFines += Decimal(currRev.plantProductRevenue)
	# 		entry.cashFlowPreTax = currDailyCashFlowPreTax = currLumpPlusFines - dailyOPEXPlusCAPEX[entry.date.year - latestProject.startDate.year + 1]
	# 		entry.cashFlowPostTax = currDailyCashFlowPostTax = currDailyCashFlowPreTax - dailyTaxes[entry.date.year - latestProject.startDate.year + 1]

	# 		currCumCashFlowPreTax += currDailyCashFlowPreTax
	# 		currCumCashFlowPostTax += currDailyCashFlowPostTax
	# 		entry.cumulativeCashFlowPreTax = currCumCashFlowPreTax
	# 		entry.cumulativeCashFlowPostTax = currCumCashFlowPostTax
	# 		entry.processed = True
	# 		entry.save()

	# 		# After updating Cash Flow data for the day, update the Financials data for the day as well.
	# 		tblFinancials.objects.filter(projectID=latestProject.projectID, date=entry.date).delete()
	# 		discountRates = [0.06, 0.08, 0.10, 0.12, 0.15, 0.20]
	# 		currTime = timezone.localtime(timezone.now())
	# 		for rate in discountRates:
	# 			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, startDate__lte=entry.date,
	# 				endDate__gte=entry.date)
	# 			currNPVPreTax = round(entry.cashFlowPreTax / Decimal(pow((1+rate),currPeriod.year)),2)
	# 			currNPVPostTax = round(entry.cashFlowPostTax / Decimal(pow((1+rate),currPeriod.year)),2)
	# 			financialsEntry = tblFinancials(projectID=latestProject, mineID=mineMatch, date=entry.date,
	# 				discountRate=rate, NPVPreTax=currNPVPreTax, NPVPostTax=currNPVPostTax, IRRPreTax=None, IRRPostTax=None, dateAdded=currTime)
	# 			financialsEntry.save()

	# tblCashFlow and tblFinancials Data Processing (VERSION 2)
	# No Pro-ration of Costs
	# Annual Costs and Expenses charged on the last calculated day of the corresponding year
	notProcessed = tblCashFlow.objects.filter(projectID=latestProject.projectID, processed=False).order_by('date')
	if notProcessed:
		toProcess = notProcessed[0]

		annualOPEXPlusCAPEX = {}
		annualTaxes = {}

		latestOPEX = tblOPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
		latestCAPEX = tblCAPEX.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
		latestTaxes = tblTaxes.objects.filter(mineID=mineID).order_by('-dateAdded')[0]
		OPEXEntries = tblOPEX.objects.filter(mineID=mineID, dateAdded=latestOPEX.dateAdded).order_by('year')
		CAPEXEntries = tblCAPEX.objects.filter(mineID=mineID, dateAdded=latestCAPEX.dateAdded).order_by('year')
		taxesEntries = tblTaxes.objects.filter(mineID=mineID, dateAdded=latestTaxes.dateAdded).order_by('year')
		for i in range(len(OPEXEntries)):
			OPEXrow = OPEXEntries[i]
			CAPEXrow = CAPEXEntries[i]
			taxesRow = taxesEntries[i]
			currOPEX = (OPEXrow.mining+OPEXrow.infrastructure+OPEXrow.stockpileLG+OPEXrow.dewatering+OPEXrow.processing+
				OPEXrow.hauling+OPEXrow.loadOutRailLoop+OPEXrow.GASite+OPEXrow.GARoomBoardFIFO+OPEXrow.railTransport+OPEXrow.GACorp+
				OPEXrow.royalties+OPEXrow.transportation+OPEXrow.GA)
			currCAPEX = (CAPEXrow.preStrip+CAPEXrow.mineEquipInitial+CAPEXrow.mineEquipSustain+CAPEXrow.infraDirectCost+
				CAPEXrow.infraIndirectCost+CAPEXrow.contingency+CAPEXrow.railcars+CAPEXrow.otherMobEquip+CAPEXrow.closureRehabAssure+
				CAPEXrow.depoProvisionPay+CAPEXrow.workCapCurrentProd+CAPEXrow.workCapCostsLG+CAPEXrow.EPCM+CAPEXrow.ownerCost)
			currOPEXPlusCAPEX = round((Decimal(currCAPEX) + Decimal(currOPEX))*1000,2)
			currTaxes = round(Decimal(taxesRow.federal + taxesRow.provincial + taxesRow.mining)*1000,2)

			annualOPEXPlusCAPEX[i+1] = currOPEXPlusCAPEX
			annualTaxes[i+1] = currTaxes

		projectPeriods = tblProjectPeriods.objects.filter(projectID=latestProject.projectID).order_by('year')
		toProcessPeriod = projectPeriods.filter(startDate__lte=toProcess.date, endDate__gte=toProcess.date)[0]
		toProcessYears = yearVals[yearVals.index(toProcessPeriod.year):]

		earlyEntries = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__lt=toProcess.date).order_by('-date')
		if earlyEntries:
			lastCashFlowEntry = earlyEntries[0]
			currCumCashFlowPreTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPreTax)
			currCumCashFlowPostTax = Decimal(lastCashFlowEntry.cumulativeCashFlowPostTax)
		else:
			currCumCashFlowPreTax = Decimal(0.0)
			currCumCashFlowPostTax = Decimal(0.0)

		for year in toProcessYears:
			currPeriod = projectPeriods.filter(year=year)[0]
			if year == toProcessPeriod.year:
				toUpdate = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=toProcess.date, 
					date__lte=currPeriod.endDate).order_by('date')
			else:
				toUpdate = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=currPeriod.startDate, 
					date__lte=currPeriod.endDate).order_by('date')

			for i in range(len(toUpdate)):
				currLumpPlusFines = Decimal(0.0)
				if 1 in PPIDs:
					currRev = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=1, date=toUpdate[i].date)
					currLumpPlusFines += Decimal(currRev.plantProductRevenue)
				if 2 in PPIDs:
					currRev = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=2, date=toUpdate[i].date)
					currLumpPlusFines += Decimal(currRev.plantProductRevenue)

				if i != (len(toUpdate)-1):
					toUpdate[i].cashFlowPreTax = currDailyCashFlowPreTax = currLumpPlusFines
					toUpdate[i].cashFlowPostTax = currDailyCashFlowPostTax = currLumpPlusFines
				else:
					toUpdate[i].cashFlowPreTax = currDailyCashFlowPreTax = currLumpPlusFines - annualOPEXPlusCAPEX[currPeriod.year]
					toUpdate[i].cashFlowPostTax = currDailyCashFlowPostTax = currDailyCashFlowPreTax - annualTaxes[currPeriod.year]

				currCumCashFlowPreTax += currDailyCashFlowPreTax
				currCumCashFlowPostTax += currDailyCashFlowPostTax
				toUpdate[i].cumulativeCashFlowPreTax = currCumCashFlowPreTax
				toUpdate[i].cumulativeCashFlowPostTax = currCumCashFlowPostTax
				toUpdate[i].processed = True
				toUpdate[i].save()

				# After updating Cash Flow data for the day, update the Financials data for the day as well.
				tblFinancials.objects.filter(projectID=latestProject.projectID, date=toUpdate[i].date).delete()
				discountRates = [Decimal(0.06), Decimal(0.08), Decimal(0.10), Decimal(0.12), Decimal(0.15), Decimal(0.20)]
				currTime = timezone.localtime(timezone.now())
				for rate in discountRates:
					currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, startDate__lte=toUpdate[i].date,
						endDate__gte=toUpdate[i].date)
					currNPVPreTax = round(toUpdate[i].cashFlowPreTax / Decimal(pow((1+rate),currPeriod.year)),2)
					currNPVPostTax = round(toUpdate[i].cashFlowPostTax / Decimal(pow((1+rate),currPeriod.year)),2)
					financialsEntry = tblFinancials(projectID=latestProject, mineID=mineMatch, date=toUpdate[i].date,
						discountRate=int(round(rate*100)), NPVPreTax=currNPVPreTax, NPVPostTax=currNPVPostTax, IRRPreTax=None, IRRPostTax=None, dateAdded=currTime)
					financialsEntry.save()


	cashFlowPreTax = []
	cashFlowPostTax = []
	cumCashFlowPreTax = []
	cumCashFlowPostTax = []
	# Beginning populating tblCashFlow data for HTML report here
	currCumCashFlowPreTax = Decimal(0.0)
	currCumCashFlowPostTax = Decimal(0.0)
	for year in yearVals:
		currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
		currStart = currPeriod.startDate
		currEnd = currPeriod.endDate
		lastCashFlow = tblCashFlow.objects.filter(projectID=latestProject.projectID, date__gte=currStart, date__lte=currEnd).order_by('-date')[0]
		cumCashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax),2))
		cumCashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax),2))
		cashFlowPreTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPreTax) - currCumCashFlowPreTax,2))
		cashFlowPostTax.append(round(Decimal(lastCashFlow.cumulativeCashFlowPostTax) - currCumCashFlowPostTax,2))
		currCumCashFlowPreTax = cumCashFlowPreTax[-1]
		currCumCashFlowPostTax = cumCashFlowPostTax[-1]
	sumCashFlowPreTax = cumCashFlowPreTax[-1]
	sumCashFlowPostTax = cumCashFlowPostTax[-1]

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
	NPVCashFlowPreTax = [0] + cashFlowPreTax
	NPVCashFlowPostTax = [0] + cashFlowPostTax
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
	for rate in discountRates:
		rate = int(round(rate*100))
		preTaxPVs[rate] = []
		postTaxPVs[rate] = []
		for year in yearVals:
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			currStart = currPeriod.startDate
			currEnd = currPeriod.endDate
			currPVs = tblFinancials.objects.filter(projectID=latestProject.projectID, discountRate=rate,
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

		cashFlowPreTax = padList(yearVals, yearCount, cashFlowPreTax, filler)
		cashFlowPostTax = padList(yearVals, yearCount, cashFlowPostTax, filler)
		cumCashFlowPreTax = padList(yearVals, yearCount, cumCashFlowPreTax, filler)
		cumCashFlowPostTax = padList(yearVals, yearCount, cumCashFlowPostTax, filler)
		paybackPreTax = padList(yearVals, yearCount, paybackPreTax, filler)
		paybackPostTax = padList(yearVals, yearCount, paybackPostTax, filler)
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

	# currDataRow = []
	# currDataRow.append('Item')
	# for year in range(1, yearCount+1):
	# 	currDataRow.append('Year{0}'.format(year))
	# currDataRow.append('Total')
	# request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	reportData += ";Mining;"
	for curr in range(1, numStockpiles+1):
		currRow = "Stockpile {0} Ore (kt),".format(curr) + ''.join([*[str(round(x,2))+',' for x in minePlanTonnageVals[curr]]]) + str(round(sumMinePlanTonnages[curr],2)) + ";"
		reportData += currRow

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining']

	# for curr in range(1, numStockpiles+1):
	# 	reportRowCount += 1
	# 	currDataRow = ["Stockpile {0} Ore (kt)".format(curr)] + [*[str(round(x,2)) for x in minePlanTonnageVals[curr]]]
	# 	# currDataRow += [*[str(round(x,2)) for x in minePlanTonnageVals[curr]]]
	# 	currDataRow.append(str(round(sumMinePlanTonnages[curr],2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	reportData += ";Processing;"
	for curr in range(1, numStockpiles+1):
		reportData += "Stockpile {0} Ore;".format(curr)
		currRow = 'Tonnage (kt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]) + ',' + str(round(tonnageTotals[curr],2)) + ";"
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]) + ';'

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Processing']

	# for curr in range(1, numStockpiles+1):
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ["Stockpile {0} Ore".format(curr)]
	# 	reportRowCount += 1
	# 	currDataRow = ['Tonnage (kt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in tonnageVals[curr]]]
	# 	currDataRow.append(str(round(tonnageTotals[curr],2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in gradeVals[curr][commNameList[i]]]]
	# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in moistures[curr]]]
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	reportData += ";Plant Product;"

	if 1 in PPIDs:
		reportData += "Lump;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]) + ',' + str(round(lumpTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]) + ';'

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Plant Product']

	# if 1 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump']
	# 	reportRowCount += 1
	# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpTonnageVals]]
	# 	currDataRow.append(str(round(lumpTonnageTotal,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpGradeVals[commNameList[i]]]]
	# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpMoistures]]
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	if 2 in PPIDs:
		reportData += "Fines;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]) + ',' + str(round(finesTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]) + ';'

	# if 2 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines']
	# 	reportRowCount += 1
	# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesTonnageVals]]
	# 	currDataRow.append(str(round(finesTonnageTotal,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesGradeVals[commNameList[i]]]]
	# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesMoistures]]
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	if 3 in PPIDs:
		reportData += "Ultra Fines;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]) + ',' + str(round(ultraFinesTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]) + ';'

	# if 3 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines']
	# 	reportRowCount += 1
	# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesTonnageVals]]
	# 	currDataRow.append(str(round(ultraFinesTonnageTotal,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesGradeVals[commNameList[i]]]]
	# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesMoistures]]
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	reportData += 'Total Product (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]) + ',' + str(round(sumTotalProducts,2)) + ';'

	# reportRowCount += 1
	# currDataRow = ['Total Product (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalProducts]]
	# currDataRow.append(str(round(sumTotalProducts,2)))
	# request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	if 4 in PPIDs:
		reportData += "Rejects;"
		currRow = 'Tonnage (dkt),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]) + ',' + str(round(rejectsTonnageTotal,2)) + ';'
		reportData += currRow
		for i in range(len(commIDs)):
			currRow = '{0} Grade (%),'.format(commNameList[i]) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]) + ';'
			reportData += currRow
		reportData += 'Moisture (%),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]) + ';'

	# if 4 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Rejects']
	# 	reportRowCount += 1
	# 	currDataRow = ['Tonnage (dkt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsTonnageVals]]
	# 	currDataRow.append(str(round(rejectsTonnageTotal,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		currDataRow = ['{0} Grade (%)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsGradeVals[commNameList[i]]]]
	# 		request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	currDataRow = ['Moisture (%)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in rejectsMoistures]]
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	reportData += ";Products Selling Price;"

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Products Selling Price']

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

	# if 1 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump Selling Price (USD/dmt)']
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump Base (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in HGLumps]]
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		request.session['reportRow{0}'.format(reportRowCount)] = ['Lump {0} Penalty (USD/t)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpPenaltyVals[commNameList[i]]]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Lump Selling Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpSellingPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgLumpSellingPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Shipping (USD/dmt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Net Lump Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in netLumpPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgNetLumpPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Exchange Rate (USD to CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Net Lump Price (CAD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetLumpPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgExchangeNetLumpPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

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

	# if 2 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines Selling Price (USD/dmt)']
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines Base (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in HGFines]]
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		request.session['reportRow{0}'.format(reportRowCount)] = ['Fines {0} Penalty (USD/t)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesPenaltyVals[commNameList[i]]]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Fines Selling Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesSellingPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgFinesSellingPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Shipping (USD/dmt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Net Fines Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in netFinesPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgNetFinesPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Exchange Rate (USD to CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Net Fines Price (CAD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetFinesPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgExchangeNetFinesPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

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

	# if 3 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines Selling Price (USD/dmt)']
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines Base (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in HGUltraFines]]
	# 	for i in range(len(commIDs)):
	# 		reportRowCount += 1
	# 		request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines {0} Penalty (USD/t)'.format(commNameList[i])] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesPenaltyVals[commNameList[i]]]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Ultra Fines Selling Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesSellingPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgUltraFinesSellingPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Shipping (USD/dmt)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullShippingCosts]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Net Ultra Fines Price (USD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in netUltraFinesPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgNetUltraFinesPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Exchange Rate (USD to CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in fullExchangeRates]]
	# 	reportRowCount += 1
	# 	currDataRow = ['Net Ultra Fines Price (CAD/t)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in exchangeNetUltraFinesPrices]]
	# 	currDataRow.append('Avg: ' + str(round(avgExchangeNetUltraFinesPrice,2)))
	# 	request.session['reportRow{0}'.format(reportRowCount)] = currDataRow

	reportData += ';Revenues;'
	if 1 in PPIDs:
		reportData += 'Lump Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]]) + ',' + str(round(sumLumpRevenues,2)) + ';'
	if 2 in PPIDs:
		reportData += 'Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]]) + ',' + str(round(sumFinesRevenues,2)) + ';'
	if 3 in PPIDs:
		reportData += 'Ultra Fines Revenue,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]]) + ',' + str(round(sumUltraFinesRevenues,2)) + ';'
	reportData += 'TOTAL REVENUE,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Revenues']

	# if 1 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Lump Revenue'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in lumpRevenues]] + [str(round(sumLumpRevenues,2))]
	# if 2 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Fines Revenue'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in finesRevenues]] + [str(round(sumFinesRevenues,2))]
	# if 3 in PPIDs:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['Ultra Fines Revenue'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in ultraFinesRevenues]] + [str(round(sumUltraFinesRevenues,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL REVENUE'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]] + [str(round(sumTotalRevenues,2))]


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

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['COSTS']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['OPEX (millions CAD)']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in mining]] + [str(round(sumMining,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Stockpile LG Reclaiming'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in stockpileLG]] + [str(round(sumStockpileLG,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Pit Dewatering'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in dewatering]] + [str(round(sumDewatering,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Processing'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in processing]] + [str(round(sumProcessing,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Product Hauling'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in hauling]] + [str(round(sumHauling,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Load-out and Rail Loop'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in loadOutRailLoop]] + [str(round(sumLoadOutRailLoop,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['G&A (Site)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in GASite]] + [str(round(sumGASite,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['G&A (Room & Board / FIFO)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in GARoom]] + [str(round(sumGARoom,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Rail Transportation, Port and Shiploading'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in railTransport]] + [str(round(sumRailTransport,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Corporate G&A'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in GACorp]] + [str(round(sumGACorp,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL OPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]] + [str(round(sumTotalOPEX,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['ROYALTIES (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]] + [str(round(sumRoyalties,2))]

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

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['CAPEX (millions CAD)']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Pre-Stripping'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in preStrip]] + [str(round(sumPreStrip,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining Equipment Initial'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipInitial]] + [str(round(sumMineEquipInitial,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining Equipment Sustaining'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in mineEquipSustain]] + [str(round(sumMineEquipSustain,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Project Infrastructure Direct Costs'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in infraDirectCost]] + [str(round(sumInfraDirectCost,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Project Infrastructure Indirect Costs'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in infraIndirectCost]] + [str(round(sumInfraIndirectCost,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Project Infrastructure Contingency'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in contingency]] + [str(round(sumContingency,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Railcars'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in railcars]] + [str(round(sumRailcars,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Other Mobile Equipment'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in otherMobEquip]] + [str(round(sumOtherMobEquip,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Closure and Rehab Assurance Payments'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in closureRehabAssure]] + [str(round(sumClosureRehabAssure,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Deposits Provision Payments'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in depoProvisionPay]] + [str(round(sumDepoProvisionPay,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL CAPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]] + [str(round(sumTotalCAPEX,2))]

	reportData += 'TAXES (millions CAD);'
	reportData += 'Federal Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]]) + ',' + str(round(sumFederalTaxes,2)) + ';'
	reportData += 'Provincial Corporate Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]]) + ',' + str(round(sumProvincialTaxes,2)) + ';'
	reportData += 'Mining Taxes,' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]]) + ',' + str(round(sumMiningTaxes,2)) + ';'
	reportData += 'TOTAL (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['TAXES (millions CAD)']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Federal Corporate Taxes'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in federalTaxes]] + [str(round(sumFederalTaxes,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Provincial Corporate Taxes'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in provincialTaxes]] + [str(round(sumProvincialTaxes,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Mining Taxes'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in miningTaxes]] + [str(round(sumMiningTaxes,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['TOTAL (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]] + [str(round(sumTotalTaxes,2))]

	reportData += ';SUMMARY;'
	reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'
	reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
	reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
	reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
	reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
	reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
	reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['SUMMARY']

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Revenues (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]] + [str(round(sumTotalRevenues,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['OPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]] + [str(round(sumTotalOPEX,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Royalties (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]] + [str(round(sumRoyalties,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['CAPEX (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]] + [str(round(sumTotalCAPEX,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Working Capital (Current Production) (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]] + [str(round(sumWorkCapCurrentProd,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Working Capital (Costs of LG Stockpile) (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]] + [str(round(sumWorkCapCostsLG,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Taxes (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]] + [str(round(sumTotalTaxes,2))]

	reportData += ';PRE-TAX CASH FLOW;'
	reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + str(round(sumCashFlowPreTax,2)) + ';'
	reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ',' + str(round(sumCashFlowPreTax,2)) + ';'
	reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + str(round(sumPaybackPreTax,2)) + ';'
	for rate in discountRates:
		reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPreTaxNPV[int(round(rate*100))],2)) + ';'
	reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(preTaxIRR,2)) + ';'

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['PRE-TAX CASH FLOW']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]] + [str(round(sumCashFlowPreTax,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Cumulative Undiscounted Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]] + [str(round(sumCashFlowPreTax,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Payback Period (year)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]] + [str(round(sumPaybackPreTax,2))]
	# for rate in discountRates:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['PRE-TAX NPV @ {0}%'.format(int(round(rate*100)))] + [*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]] + [str(round(sumPreTaxNPV[int(round(rate*100))],2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['INTERNAL RATE OF RETURN (IRR)'] + [str(round(preTaxIRR,2))]

	reportData += ';POST-TAX CASH FLOW;'
	reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + str(round(sumCashFlowPostTax,2)) + ';'
	reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ',' + str(round(sumCashFlowPostTax,2)) + ';'
	reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + str(round(sumPaybackPostTax,2)) + ';'
	for rate in discountRates:
		reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPostTaxNPV[int(round(rate*100))],2)) + ';'
	reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(postTaxIRR,2)) + ';'

	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['POST-TAX CASH FLOW']
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]] + [str(round(sumCashFlowPostTax,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Cumulative Undiscounted Cash Flow (millions CAD)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]] + [str(round(sumCashFlowPostTax,2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['Payback Period (year)'] + [*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]] + [str(round(sumPaybackPostTax,2))]
	# for rate in discountRates:
	# 	reportRowCount += 1
	# 	request.session['reportRow{0}'.format(reportRowCount)] = ['POST-TAX NPV @ {0}%'.format(int(round(rate*100)))] + [*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]] + [str(round(sumPostTaxNPV[int(round(rate*100))],2))]
	# reportRowCount += 1
	# request.session['reportRow{0}'.format(reportRowCount)] = ['INTERNAL RATE OF RETURN (IRR)'] + [str(round(postTaxIRR,2))]

	# request.session['reportRowCount'] = reportRowCount

	# request.session['reportData'] = reportData

	filter_form = filterForm(mineID=mineID)
	report_form = reportForm(mineID=mineID, reportData=reportData)

	return render(request, 'report/report.html', {'filterForm': filter_form, 'reportForm': report_form,
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

			form = filterForm(request.POST, mineID=mineID)
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
						lumpTonnageVals.append(Decimal(entry.tonnageDMT))
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
						finesTonnageVals.append(Decimal(entry.tonnageDMT))
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
						ultraFinesTonnageVals.append(Decimal(entry.tonnageDMT))
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
						rejectsTonnageVals.append(Decimal(entry.tonnageDMT))
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

				# reportData += ';SUMMARY;'
				# reportData += 'Revenues (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalRevenues]]) + ',' + str(round(sumTotalRevenues,2)) + ';'
				# reportData += 'OPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalOPEX]]) + ',' + str(round(sumTotalOPEX,2)) + ';'
				# reportData += 'Royalties (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in royalties]]) + ',' + str(round(sumRoyalties,2)) + ';'
				# reportData += 'CAPEX (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalCAPEX]]) + ',' + str(round(sumTotalCAPEX,2)) + ';'
				# reportData += 'Working Capital (Current Production) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCurrentProd]]) + ',' + str(round(sumWorkCapCurrentProd,2)) + ';'
				# reportData += 'Working Capital (Costs of LG Stockpile) (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in workCapCostsLG]]) + ',' + str(round(sumWorkCapCostsLG,2)) + ';'
				# reportData += 'Taxes (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in totalTaxes]]) + ',' + str(round(sumTotalTaxes,2)) + ';'

				# reportData += ';PRE-TAX CASH FLOW;'
				# reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPreTax]]) + ',' + str(round(sumCashFlowPreTax,2)) + ';'
				# reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPreTax]]) + ',' + str(round(sumCashFlowPreTax,2)) + ';'
				# reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPreTax]]) + ',' + str(round(sumPaybackPreTax,2)) + ';'
				# for rate in discountRates:
				# 	reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in preTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPreTaxNPV[int(round(rate*100))],2)) + ';'
				# reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(preTaxIRR,2)) + ';'

				# reportData += ';POST-TAX CASH FLOW;'
				# reportData += 'Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cashFlowPostTax]]) + ',' + str(round(sumCashFlowPostTax,2)) + ';'
				# reportData += 'Cumulative Undiscounted Cash Flow (millions CAD),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in cumCashFlowPostTax]]) + ',' + str(round(sumCashFlowPostTax,2)) + ';'
				# reportData += 'Payback Period (year),' + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in paybackPostTax]]) + ',' + str(round(sumPaybackPostTax,2)) + ';'
				# for rate in discountRates:
				# 	reportData += 'PRE-TAX NPV @ {0}%,'.format(int(round(rate*100))) + ','.join([*[x if isinstance(x,str) else str(round(x,2)) for x in postTaxPVs[int(round(rate*100))]]]) + ',' + str(round(sumPostTaxNPV[int(round(rate*100))],2)) + ';'
				# reportData += 'INTERNAL RATE OF RETURN (IRR),' + str(round(postTaxIRR,2)) + ';'


				filter_form = filterForm(mineID=mineID)
				report_form = reportForm(mineID=mineID, reportData=reportData)

				return render(request, 'report/report2.html', {'filterForm': filter_form, 'reportForm': report_form,
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
					'sumWorkCapCurrentProd': sumWorkCapCurrentProd, 'sumWorkCapCostsLG': sumWorkCapCostsLG})
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
