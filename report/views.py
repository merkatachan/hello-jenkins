from django.shortcuts import render
from django.db.models import Sum, Avg
from django.utils import timezone
from setup.models import *
from decimal import *
from functools import reduce
import numpy as np
import operator
import calendar
from math import pow

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
	totalRevenues = [Decimal(0.0)]*len(yearVals)
	lumpPlusFinesRevenues = [Decimal(0.0)]*len(yearVals)

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

	# if 1 in MPIDs:
	# 	minePlanHGTonnageVals = []
	# 	minePlanHGTonnageEntries = tblMineProductTonnage.objects.filter(projectID=latestProject.projectID, mineProductID=1).order_by('year')
	# 	for entry in minePlanHGTonnageEntries:
	# 		minePlanHGTonnageVals.append(entry.tonnage)
	# 	sumMinePlanHGTonnage = sum(minePlanHGTonnageVals)
	# else:
	# 	minePlanHGTonnageVals = None
	# 	sumMinePlanHGTonnage = None

	# if 2 in MPIDs:
	# 	minePlanLGTonnageVals = []
	# 	minePlanLGTonnageEntries = tblMineProductTonnage.objects.filter(projectID=latestProject.projectID, mineProductID=2).order_by('year')
	# 	for entry in minePlanLGTonnageEntries:
	# 		minePlanLGTonnageVals.append(entry.tonnage)
	# 	sumMinePlanLGTonnage = sum(minePlanLGTonnageVals)
	# else:
	# 	minePlanLGTonnageVals = None
	# 	sumMinePlanLGTonnage = None

	# if 3 in MPIDs:
	# 	minePlanWasteTonnageVals = []
	# 	minePlanWasteTonnageEntries = tblMineProductTonnage.objects.filter(projectID=latestProject.projectID, mineProductID=3).order_by('year')
	# 	for entry in minePlanWasteTonnageEntries:
	# 		minePlanWasteTonnageVals.append(entry.tonnage)
	# 	sumMinePlanWasteTonnage = sum(minePlanWasteTonnageVals)
	# else:
	# 	minePlanWasteTonnageVals = None
	# 	sumMinePlanWasteTonnage = None

	# if 4 in MPIDs:
	# 	minePlanOverburdenTonnageVals = []
	# 	minePlanOverburdenTonnageEntries = tblMineProductTonnage.objects.filter(projectID=latestProject.projectID, mineProductID=4).order_by('year')
	# 	for entry in minePlanOverburdenTonnageEntries:
	# 		minePlanOverburdenTonnageVals.append(entry.tonnage)
	# 	sumMinePlanOverburdenTonnage = sum(minePlanOverburdenTonnageVals)
	# else:
	# 	minePlanOverburdenTonnageVals = None
	# 	sumMinePlanOverburdenTonnage = None

	if not yearVals:
		totalProducts = ['N/A']*yearCount
		sumTotalProducts = 'N/A'

		tonnageVals = {}
		tonnageTotals = {}
		gradeVals = {}
		moistures = {}
		for curr in range(1, numStockpiles+1):
			tonnageVals[curr] = padList(yearVals, yearCount, [], 'N/A')
			tonnageTotals[curr] = 'N/A'
			currGrades = {}
			for i in range(len(commIDs)):
				currGrades[commNameList[i]] = ['N/A']*yearCount
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
			lumpTonnageVals = padList(yearVals, yearCount, [], 'N/A')
			lumpTonnageTotal = 'N/A'
			lumpGradeVals = {}
			for i in range(len(commIDs)):
				lumpGradeVals[commNameList[i]] = ['N/A']*yearCount
			# lumpGradeVals = padList(yearVals, yearCount, [], "N/A")
			lumpMoistures = padList(yearVals, yearCount, [], round(latestInput.lumpMoisture,2))
		
		if 2 in PPIDs:
			finesTonnageVals = padList(yearVals, yearCount, [], 'N/A')
			finesTonnageTotal = 'N/A'
			finesGradeVals = {}
			for i in range(len(commIDs)):
				finesGradeVals[commNameList[i]] = ['N/A']*yearCount
			# finesGradeVals = padList(yearVals, yearCount, [], "N/A")
			finesMoistures = padList(yearVals, yearCount, [], round(latestInput.finesMoisture,2))

		if 3 in PPIDs:
			ultraFinesTonnageVals = padList(yearVals, yearCount, [], 'N/A')
			ultraFinesTonnageTotal = 'N/A'
			ultraFinesGradeVals = {}
			for i in range(len(commIDs)):
				ultraFinesGradeVals[commNameList[i]] = ['N/A']*yearCount
			ultraFinesMoistures = padList(yearVals, yearCount, [], round(latestInput.ultraFinesMoisture,2))

		sumTotalProducts = 'N/A'

		if 4 in PPIDs:
			rejectsTonnageVals = padList(yearVals, yearCount, [], 'N/A')
			rejectsTonnageTotal = 'N/A'
			rejectsGradeVals = {}
			for i in range(len(commIDs)):
				rejectsGradeVals[commNameList[i]] = ['N/A']*yearCount
			rejectsMoistures = padList(yearVals, yearCount, [], round(latestInput.rejectsMoisture,2))

		if 1 in PPIDs:
			# HGLumps = [round(Decimal(priceEntry.HGLump),2)]*yearCount
			HGLumps = [round(Decimal(priceEntry.lump),2)]*yearCount
			lumpPenaltyVals = {}
			for i in range(len(commIDs)):
				lumpPenaltyVals[commNameList[i]] = ['N/A']*yearCount
			lumpSellingPrices = ['N/A']*yearCount
			avgLumpSellingPrice = 'N/A'
			netLumpPrices = ['N/A']*yearCount
			avgNetLumpPrice = 'N/A'
			exchangeNetLumpPrices = ['N/A']*yearCount
			avgExchangeNetLumpPrice = 'N/A'
			lumpRevenues = ['N/A']*yearCount
			sumLumpRevenues = 'N/A'

		if 2 in PPIDs:
			# HGFines = [round(Decimal(priceEntry.HGFines),2)]*yearCount
			HGFines = [round(Decimal(priceEntry.fines),2)]*yearCount
			finesPenaltyVals = {}
			for i in range(len(commIDs)):
				finesPenaltyVals[commNameList[i]] = ['N/A']*yearCount
			finesSellingPrices = ['N/A']*yearCount
			avgFinesSellingPrice = 'N/A'
			netFinesPrices = ['N/A']*yearCount
			avgNetFinesPrice = 'N/A'
			exchangeNetFinesPrices = ['N/A']*yearCount
			avgExchangeNetFinesPrice = 'N/A'
			finesRevenues = ['N/A']*yearCount
			sumFinesRevenues = 'N/A'

		if 3 in PPIDs:
			# HGUltraFines = [round(Decimal(priceEntry.HGUltraFines),2)]*yearCount
			HGUltraFines = [round(Decimal(priceEntry.ultraFines),2)]*yearCount
			ultraFinesPenaltyVals = {}
			for i in range(len(commIDs)):
				ultraFinesPenaltyVals[commNameList[i]] = ['N/A']*yearCount
			ultraFinesSellingPrices = ['N/A']*yearCount
			avgUltraFinesSellingPrice = 'N/A'
			netUltraFinesPrices = ['N/A']*yearCount
			avgNetUltraFinesPrice = 'N/A'
			exchangeNetUltraFinesPrices = ['N/A']*yearCount
			avgExchangeNetUltraFinesPrice = 'N/A'
			ultraFinesRevenues = ['N/A']*yearCount
			sumUltraFinesRevenues = 'N/A'

		totalRevenues = ['N/A']*yearCount
		sumTotalRevenues = 'N/A'

		cashFlowPreTax = cashFlowPostTax = cumCashFlowPreTax = cumCashFlowPostTax = ['N/A']*yearCount
		sumCashFlowPreTax = sumCashFlowPostTax = 'N/A'
		paybackPreTax = paybackPostTax = ['N/A']*yearCount
		sumPaybackPreTax = sumPaybackPostTax = 'N/A'
		preTaxNPVs = postTaxNPVs = ['N/A']*yearCount
		preTaxIRR = postTaxIRR = 'N/A'


		preTaxPVs = {}
		postTaxPVs = {}
		sumPreTaxNPV = {}
		sumPostTaxNPV = {}
		for rate in discountRates:
			rate = int(round(rate*100))
			preTaxPVs[rate] = ['N/A']*yearCount
			postTaxPVs[rate] = ['N/A']*yearCount
			sumPreTaxNPV[rate] = 'N/A'
			sumPostTaxNPV[rate] = 'N/A'

		return render(request, 'report/report.html', {'yearVals': yearVals, 'fullYearVals': fullYearVals, 'commIDs': commIDs, 'commNameList': commNameList,
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
				sumPenalty = penaltyEntries.aggregate(sumPenalty=Sum('penalty'))
				tempPenalties.append(round(Decimal(sumPenalty['sumPenalty']),2))
				# tempPenalties.append(round(Decimal(penaltyEntry.penalty),2))
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
						discountRate=int(rate*100), NPVPreTax=currNPVPreTax, NPVPostTax=currNPVPostTax, IRRPreTax=None, IRRPostTax=None, dateAdded=currTime)
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
		totalProducts = padList(yearVals, yearCount, totalProducts, 'N/A')

		for curr in range(1, numStockpiles+1):
			tonnageVals[curr] = padList(yearVals, yearCount, tonnageVals[curr], 'N/A')
			for i in range(len(commIDs)):
				gradeVals[curr][commNameList[i]] = padList(yearVals, yearCount, gradeVals[curr][commNameList[i]], 'N/A')

		# if 1 in MPIDs:
		# 	HGTonnageVals = padList(yearVals, yearCount, HGTonnageVals, 'N/A')
		# 	for i in range(len(commIDs)):
		# 		HGGradeVals[commNameList[i]] = padList(yearVals, yearCount, HGGradeVals[commNameList[i]], 'N/A')

		# if 2 in MPIDs:
		# 	LGTonnageVals = padList(yearVals, yearCount, LGTonnageVals, 'N/A')
		# 	for i in range(len(commIDs)):
		# 		LGGradeVals[commNameList[i]] = padList(yearVals, yearCount, LGGradeVals[commNameList[i]], 'N/A')

		if 1 in PPIDs:
			lumpTonnageVals = padList(yearVals, yearCount, lumpTonnageVals, 'N/A')
			for i in range(len(commIDs)):
				lumpGradeVals[commNameList[i]] = padList(yearVals, yearCount, lumpGradeVals[commNameList[i]], 'N/A')

			HGLumps = [round(Decimal(priceEntry.lump),2)]*yearCount
			for i in range(len(commIDs)):
				lumpPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, lumpPenaltyVals[commNameList[i]], 'N/A')
			lumpSellingPrices = padList(yearVals, yearCount, lumpSellingPrices, 'N/A')
			netLumpPrices = padList(yearVals, yearCount, netLumpPrices, 'N/A')
			exchangeNetLumpPrices = padList(yearVals, yearCount, exchangeNetLumpPrices, 'N/A')

			lumpRevenues = padList(yearVals, yearCount, lumpRevenues, 'N/A')

		if 2 in PPIDs:
			finesTonnageVals = padList(yearVals, yearCount, finesTonnageVals, 'N/A')
			for i in range(len(commIDs)):
				finesGradeVals[commNameList[i]] = padList(yearVals, yearCount, finesGradeVals[commNameList[i]], 'N/A')

			HGFines = [round(Decimal(priceEntry.fines),2)]*yearCount
			for i in range(len(commIDs)):
				finesPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, finesPenaltyVals[commNameList[i]], 'N/A')
			finesSellingPrices = padList(yearVals, yearCount, finesSellingPrices, 'N/A')
			netFinesPrices = padList(yearVals, yearCount, netFinesPrices, 'N/A')
			exchangeNetFinesPrices = padList(yearVals, yearCount, exchangeNetFinesPrices, 'N/A')

			finesRevenues = padList(yearVals, yearCount, finesRevenues, 'N/A')

		if 3 in PPIDs:
			ultraFinesTonnageVals = padList(yearVals, yearCount, ultraFinesTonnageVals, "N/A")
			for i in range(len(commIDs)):
				ultraFinesGradeVals[commNameList[i]] = padList(yearVals, yearCount, ultraFinesGradeVals[commNameList[i]], 'N/A')

			HGUltraFines = [round(Decimal(priceEntry.ultraFines),2)]*yearCount
			for i in range(len(commIDs)):
				ultraFinesPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, ultraFinesPenaltyVals[commNameList[i]], 'N/A')
			ultraFinesSellingPrices = padList(yearVals, yearCount, ultraFinesSellingPrices, 'N/A')
			netUltraFinesPrices = padList(yearVals, yearCount, netUltraFinesPrices, 'N/A')
			exchangeNetUltraFinesPrices = padList(yearVals, yearCount, exchangeNetUltraFinesPrices, 'N/A')

			ultraFinesRevenues = padList(yearVals, yearCount, ultraFinesRevenues, 'N/A')

		if 4 in PPIDs:
			rejectsTonnageVals = padList(yearVals, yearCount, [], 'N/A')
			for i in range(len(commIDs)):
				rejectsGradeVals[commNameList[i]] = padList(yearVals, yearCount, rejectsGradeVals[commNameList[i]], 'N/A')
		
		totalRevenues = padList(yearVals, yearCount, totalRevenues, 'N/A')

		cashFlowPreTax = padList(yearVals, yearCount, cashFlowPreTax, 'N/A')
		cashFlowPostTax = padList(yearVals, yearCount, cashFlowPostTax, 'N/A')
		cumCashFlowPreTax = padList(yearVals, yearCount, cumCashFlowPreTax, 'N/A')
		cumCashFlowPostTax = padList(yearVals, yearCount, cumCashFlowPostTax, 'N/A')
		paybackPreTax = padList(yearVals, yearCount, paybackPreTax, 'N/A')
		paybackPostTax = padList(yearVals, yearCount, paybackPostTax, 'N/A')
		preTaxNPVs = padList(yearVals, yearCount, preTaxNPVs, 'N/A')
		postTaxNPVs = padList(yearVals, yearCount, postTaxNPVs, 'N/A')

		for rate in discountRates:
			rate = int(round(rate*100))
			preTaxPVs[rate] = padList(yearVals, yearCount, preTaxPVs[rate], 'N/A')
			postTaxPVs[rate] = padList(yearVals, yearCount, postTaxPVs[rate], 'N/A')

	return render(request, 'report/report.html', {'yearVals': yearVals, 'fullYearVals': fullYearVals, 'commIDs': commIDs, 'commNameList': commNameList,
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
	# 	'preTaxNPVs': preTaxNPVs, 'postTaxNPVs': postTaxNPVs, 'preTaxIRR': preTaxIRR, 'postTaxIRR': postTaxIRR})