from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Avg
from setup.models import *
from decimal import *
from functools import reduce
import numpy as np
import operator
import calendar
from math import pow
from .forms import *

def padList(yearVals, yearCount, toPad, marker):
	if not yearVals:
		toPad += [marker]*yearCount
		return toPad

	for i in range(1, yearCount+1):
		if i not in yearVals:
			toPad.insert(i-1, marker)
	return toPad

def index(request):
	mineID = request.session["mineID"]

	projectsList  = tblProject.objects.filter(mineID=mineID)
	latestProject = projectsList.order_by('-dateAdded')[0]
	LOM = int(latestProject.LOM)

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

	yearVals = []

	lumpPenaltyVals = {}
	finesPenaltyVals = {}
	ultraFinesPenaltyVals = {}
	sumLumpPenaltyVals = None
	sumFinesPenaltyVals = None
	sumUltraFinesPenaltyVals = None

	lumpRevenues = None
	finesRevenues = None
	ultraFinesRevenues = None
	sumLumpRevenues = None
	sumFinesRevenues = None
	sumUltraFinesRevenues = None

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

	if not yearVals:
		if 1 in PPIDs:
			lumpRevenues = [0.0]*yearCount
			sumLumpRevenues = 0.0
			for i in range(len(commIDs)):
				lumpPenaltyVals[commNameList[i]] = [0.0]*yearCount
			sumLumpPenaltyVals = [0.0]*yearCount

		if 2 in PPIDs:
			finesRevenues = [0.0]*yearCount
			sumFinesRevenues = 0.0
			for i in range(len(commIDs)):
				finesPenaltyVals[commNameList[i]] = [0.0]*yearCount
			sumFinesPenaltyVals = [0.0]*yearCount

		if 3 in PPIDs:
			ultraFinesRevenues = [0.0]*yearCount
			sumUltraFinesRevenues = 0.0
			for i in range(len(commIDs)):
				ultraFinesPenaltyVals[commNameList[i]] = [0.0]*yearCount
			sumUltraFinesPenaltyVals = [0.0]*yearCount

		form = smelterForm(commIDs=commIDs, commNameList=commNameList, PPIDs=PPIDs,
			lumpRevenues=lumpRevenues, finesRevenues=finesRevenues, ultraFinesRevenues=ultraFinesRevenues,
			sumLumpRevenues=sumLumpRevenues, sumFinesRevenues=sumFinesRevenues, sumUltraFinesRevenues=sumUltraFinesRevenues,
			lumpPenaltyVals=lumpPenaltyVals, finesPenaltyVals=finesPenaltyVals, ultraFinesPenaltyVals=ultraFinesPenaltyVals,
			sumLumpPenaltyVals=sumLumpPenaltyVals, sumFinesPenaltyVals=sumFinesPenaltyVals, sumUltraFinesPenaltyVals=sumUltraFinesPenaltyVals)

		return render(request, 'smelter/smelter.html', {'form': form, 'yearCount': range(yearCount), 'PPIDs': PPIDs,
			'commIDs': commIDs, 'commNameList': commNameList,
			'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
			'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
			'lumpPenaltyVals': lumpPenaltyVals, 'finesPenaltyVals': finesPenaltyVals, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals,
			'sumLumpPenaltyVals': sumLumpPenaltyVals, 'sumFinesPenaltyVals': sumFinesPenaltyVals, 'sumUltraFinesPenaltyVals': sumUltraFinesPenaltyVals})

	periodDates = {}
	for year in yearVals:
		currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
		periodDates[year] = [currPeriod.startDate, currPeriod.endDate]

	if 1 in PPIDs:
		lumpDailyTonnages = {}
		lumpPenaltyVals = {}

		for year in yearVals:
			lumpTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=1,
				date__gte=periodDates[year][0], date__lte=periodDates[year][1])
			currDailyTonnages = []
			for entry in lumpTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			lumpDailyTonnages[year] = currDailyTonnages

		sumLumpPenaltyVals = [0.0]*len(yearVals)
		for i in range(len(commIDs)):
			tempPenalties = []
			for year in yearVals:
				penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1, commodityID=commIDs[i],
					date__gte=periodDates[year][0], date__lte=periodDates[year][1])

				dailyPens = []
				for entry in penaltyEntries:
					dailyPens.append(entry.penalty)
				tempPenalties.append(round(np.average(dailyPens, weights=lumpDailyTonnages[year]),2))

			lumpPenaltyVals[commNameList[i]] = tempPenalties
			sumLumpPenaltyVals = [sum(x) for x in zip(sumLumpPenaltyVals, tempPenalties)]
			
		lumpRevenues = []
		sumLumpRevenues = Decimal(0.0)
		for year in yearVals:
			revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=1,
				date__gte=periodDates[year][0], date__lte=periodDates[year][1])
			sumPPRevenue = revenueEntries.aggregate(sumPPRevenue=Sum('plantProductRevenue'))
			currRevenue = round(sumPPRevenue['sumPPRevenue'],2)
			lumpRevenues.append(currRevenue)
			sumLumpRevenues += currRevenue

	if 2 in PPIDs:
		finesDailyTonnages = {}
		finesPenaltyVals = {}

		for year in yearVals:
			finesTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=2,
				date__gte=periodDates[year][0], date__lte=periodDates[year][1])
			currDailyTonnages = []
			for entry in finesTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			finesDailyTonnages[year] = currDailyTonnages

		sumFinesPenaltyVals = [0.0]*len(yearVals)
		for i in range(len(commIDs)):
			tempPenalties = []
			for year in yearVals:
				penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2, commodityID=commIDs[i],
					date__gte=periodDates[year][0], date__lte=periodDates[year][1])

				dailyPens = []
				for entry in penaltyEntries:
					dailyPens.append(entry.penalty)
				tempPenalties.append(round(np.average(dailyPens, weights=finesDailyTonnages[year]),2))

			finesPenaltyVals[commNameList[i]] = tempPenalties
			sumFinesPenaltyVals = [sum(x) for x in zip(sumFinesPenaltyVals, tempPenalties)]
			
		finesRevenues = []
		sumFinesRevenues = Decimal(0.0)
		for year in yearVals:
			revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=2,
				date__gte=periodDates[year][0], date__lte=periodDates[year][1])
			sumPPRevenue = revenueEntries.aggregate(sumPPRevenue=Sum('plantProductRevenue'))
			currRevenue = round(sumPPRevenue['sumPPRevenue'],2)
			finesRevenues.append(currRevenue)
			sumFinesRevenues += currRevenue

	if 3 in PPIDs:
		ultraFinesDailyTonnages = {}
		ultraFinesPenaltyVals = {}

		for year in yearVals:
			ultraFinesTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=3,
				date__gte=periodDates[year][0], date__lte=periodDates[year][1])
			currDailyTonnages = []
			for entry in ultraFinesTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			ultraFinesDailyTonnages[year] = currDailyTonnages

		sumUltraFinesPenaltyVals = [0.0]*len(yearVals)
		for i in range(len(commIDs)):
			tempPenalties = []
			for year in yearVals:
				penaltyEntries = tblSmelterTermsOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3, commodityID=commIDs[i],
					date__gte=periodDates[year][0], date__lte=periodDates[year][1])

				dailyPens = []
				for entry in penaltyEntries:
					dailyPens.append(entry.penalty)
				tempPenalties.append(round(np.average(dailyPens, weights=ultraFinesDailyTonnages[year]),2))

			ultraFinesPenaltyVals[commNameList[i]] = tempPenalties
			sumUltraFinesPenaltyVals = [sum(x) for x in zip(sumUltraFinesPenaltyVals, tempPenalties)]
			
		ultraFinesRevenues = []
		sumUltraFinesRevenues = Decimal(0.0)
		for year in yearVals:
			revenueEntries = tblRevenue.objects.filter(projectID=latestProject.projectID, plantProductID=3,
				date__gte=periodDates[year][0], date__lte=periodDates[year][1])
			sumPPRevenue = revenueEntries.aggregate(sumPPRevenue=Sum('plantProductRevenue'))
			currRevenue = round(sumPPRevenue['sumPPRevenue'],2)
			ultraFinesRevenues.append(currRevenue)
			sumUltraFinesRevenues += currRevenue

	# Pad values afterwards for missing years
	if len(yearVals) != yearCount:
		if 1 in PPIDs:
			lumpRevenues = padList(yearVals, yearCount, lumpRevenues, 0.0)
			sumLumpPenaltyVals = padList(yearVals, yearCount, sumLumpPenaltyVals, 0.0)
			for i in range(len(commIDs)):
				lumpPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, lumpPenaltyVals[commNameList[i]], 0.0)
		if 2 in PPIDs:
			finesRevenues = padList(yearVals, yearCount, finesRevenues, 0.0)
			sumFinesPenaltyVals = padList(yearVals, yearCount, sumFinesPenaltyVals, 0.0)
			for i in range(len(commIDs)):
				finesPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, finesPenaltyVals[commNameList[i]], 0.0)
		if 3 in PPIDs:
			ultraFinesRevenues = padList(yearVals, yearCount, ultraFinesRevenues, 0.0)
			sumUltraFinesPenaltyVals = padList(yearVals, yearCount, sumUltraFinesPenaltyVals, 0.0)
			for i in range(len(commIDs)):
				ultraFinesPenaltyVals[commNameList[i]] = padList(yearVals, yearCount, ultraFinesPenaltyVals[commNameList[i]], 0.0)

	form = smelterForm(commIDs=commIDs, commNameList=commNameList, PPIDs=PPIDs,
			lumpRevenues=lumpRevenues, finesRevenues=finesRevenues, ultraFinesRevenues=ultraFinesRevenues,
			sumLumpRevenues=sumLumpRevenues, sumFinesRevenues=sumFinesRevenues, sumUltraFinesRevenues=sumUltraFinesRevenues,
			lumpPenaltyVals=lumpPenaltyVals, finesPenaltyVals=finesPenaltyVals, ultraFinesPenaltyVals=ultraFinesPenaltyVals,
			sumLumpPenaltyVals=sumLumpPenaltyVals, sumFinesPenaltyVals=sumFinesPenaltyVals, sumUltraFinesPenaltyVals=sumUltraFinesPenaltyVals)

	return render(request, 'smelter/smelter.html', {'form': form, 'yearCount': range(yearCount), 'PPIDs': PPIDs,
		'commIDs': commIDs, 'commNameList': commNameList,
		'lumpRevenues': lumpRevenues, 'finesRevenues': finesRevenues, 'ultraFinesRevenues': ultraFinesRevenues,
		'sumLumpRevenues': sumLumpRevenues, 'sumFinesRevenues': sumFinesRevenues, 'sumUltraFinesRevenues': sumUltraFinesRevenues,
		'lumpPenaltyVals': lumpPenaltyVals, 'finesPenaltyVals': finesPenaltyVals, 'ultraFinesPenaltyVals': ultraFinesPenaltyVals,
		'sumLumpPenaltyVals': sumLumpPenaltyVals, 'sumFinesPenaltyVals': sumFinesPenaltyVals, 'sumUltraFinesPenaltyVals': sumUltraFinesPenaltyVals})

	# if request.method == 'POST':
	# 	form = smelterForm(request.POST, idList=idList, nameList=commNameList, LOM=str(LOM))
	# 	if form.is_valid():
	# 		mineMatch = tblMine.objects.get(mineID=int(mineID))
	# 		dateAdded = timezone.localtime(timezone.now())
			
	# 		# Get list of Plant Product IDs
	# 		latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	# 		PPTimestamp = latestPlantProduct.dateAdded
	# 		PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
	# 		PPIDs = PPMatches.values_list('plantProductID', flat=True)
			
	# 		latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
	# 		timestamp = latestCommodity.dateAdded
	# 		commodityMatches = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=timestamp)
			
			
	# 		if 1 in PPIDs:	
	# 			penalty = request.POST.get('penalty', '')
				
	# 		else:
	# 			penalty = None
				

	# 		if 2 in PPIDs:
	# 			penalty = request.POST.get('penalty', '')
				
	# 		else:
	# 			penalty = None
			

	# 		if 3 in PPIDs:
	# 			penalty = request.POST.get('penalty', '')
				
	# 		else:
	# 			penalty = None
				
	# 		if 4 in PPIDs:
	# 			penalty = request.POST.get('penalty', '')
				
	# 		else:
	# 			penalty = None

	# 		for i in range(len(idList)):
	# 			commodityID = tblCommodityList.objects.get(commodityID=tempIDs[i])
	# 			penalty = request.POST.get("Penalty{0}".format(idList[i]), '')

	# 			tblSmelterTermsObj = tblSmelterTerms(mineID=mineMatch, commodityID=commodityID,
	# 				plantProductID=plantProductID, penalty=penalty,
	# 				dateAdded=dateAdded)
	# 			tblSmelterTermsObj.save()

	# 		return render (request, 'smelter/success.html', {})

	# 	return render(request, 'smelter/smelter.html', {'form': form_class, 'idList': idList, 'nameList': commNameList, 'plantProductID': plantProductID })		
	# else:
		
	# 	penalty = []
		

	# 	for ID in idList:
	# 		smelterEntry = tblSmelterTermsOptimized.objects.filter(mineID=mineID, commodityID=ID, plantProductID=plantProductID).order_by('-dateAdded')[0]
	# 		penalty.append(smelterEntry.penalty)
			
		
		
		
	# 	return render (request, "smelter/smelter.html", {'form': form_class, 'idList': idList, 'nameList': commNameList, 'LGMinGrade': LGMinGrade,
	# 			'plantProductID': plantProductID, 'penalty': penalty})
