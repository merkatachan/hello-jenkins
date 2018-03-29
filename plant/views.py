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

# Create your views here.
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

	lumpWMTs = None
	lumpDMTs = None
	lumpGradeVals = {}
	lumpWMTTotal = None
	lumpDMTTotal = None

	finesWMTs = None
	finesDMTs = None
	finesGradeVals ={}
	finesWMTTotal = None
	finesDMTTotal = None

	ultraFinesWMTs = None
	ultraFinesDMTs = None
	ultraFinesGradeVals = {}
	ultraFinesWMTTotal = None
	ultraFinesDMTTotal = None

	rejectsWMTs = None
	rejectsDMTs = None
	# rejectsGradeVals = None
	rejectsWMTTotal = None
	rejectsDMTTotal = None

	sumWMTs = None
	sumDMTs = None
	sumWMTTotal = None
	sumDMTTotal = None

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
			lumpWMTs = [0.0]*yearCount
			lumpDMTs = [0.0]*yearCount
			for i in range(len(commIDs)):
				lumpGradeVals[commNameList[i]] = [0.0]*yearCount

		if 2 in PPIDs:
			finesWMTs = [0.0]*yearCount
			finesDMTs = [0.0]*yearCount
			for i in range(len(commIDs)):
				finesGradeVals[commNameList[i]] = [0.0]*yearCount

		if 3 in PPIDs:
			ultraFinesWMTs = [0.0]*yearCount
			ultraFinesDMTs = [0.0]*yearCount
			for i in range(len(commIDs)):
				ultraFinesGradeVals[commNameList[i]] = [0.0]*yearCount

		if 4 in PPIDs:
			rejectsWMTs = [0.0]*yearCount
			rejectsDMTs = [0.0]*yearCount
			# for i in range(len(commIDs)):
			# 	rejectsGradeVals[commNameList[i]] = ['N/A']*yearCount

		sumWMTs = [0.0]*yearCount
		sumDMTs = [0.0]*yearCount

		lumpWMTTotal = 0.0
		lumpDMTTotal = 0.0
		finesWMTTotal = 0.0
		finesDMTTotal = 0.0
		ultraFinesWMTTotal = 0.0
		ultraFinesDMTTotal = 0.0
		rejectsWMTTotal = 0.0
		rejectsDMTTotal = 0.0

		sumWMTTotal = 0.0
		sumDMTTotal = 0.0

		form = plantForm(commIDs=commIDs, commNameList=commNameList, PPIDs=PPIDs,
			lumpWMTs=lumpWMTs, lumpDMTs=lumpDMTs, lumpGradeVals=lumpGradeVals,
			lumpWMTTotal=lumpWMTTotal, lumpDMTTotal=lumpDMTTotal,
			finesWMTs=finesWMTs, finesDMTs=finesDMTs, finesGradeVals=finesGradeVals,
			finesWMTTotal=finesWMTTotal, finesDMTTotal=finesDMTTotal,
			ultraFinesWMTs=ultraFinesWMTs, ultraFinesDMTs=ultraFinesDMTs, ultraFinesGradeVals=ultraFinesGradeVals,
			ultraFinesWMTTotal=ultraFinesWMTTotal, ultraFinesDMTTotal=ultraFinesDMTTotal,
			rejectsWMTs=rejectsWMTs, rejectsDMTs=rejectsDMTs,
			rejectsWMTTotal=rejectsWMTTotal, rejectsDMTTotal=rejectsDMTTotal,
			sumWMTs=sumWMTs, sumDMTs=sumDMTs, sumWMTTotal=sumWMTTotal, sumDMTTotal=sumDMTTotal)

		return render(request, 'plant/plant.html', {'form': form, 'yearCount': yearCount, 'PPIDs': PPIDs,
			'commIDs': commIDs, 'commNameList': commNameList,
			'lumpWMTs': lumpWMTs, 'lumpDMTs': lumpDMTs, 'lumpGradeVals': lumpGradeVals,
			'lumpWMTTotal': lumpWMTTotal, 'lumpDMTTotal': lumpDMTTotal,
			'finesWMTs': finesWMTs, 'finesDMTs': finesDMTs, 'finesGradeVals': finesGradeVals,
			'finesWMTTotal': finesWMTTotal, 'finesDMTTotal': finesDMTTotal,
			'ultraFinesWMTs': ultraFinesWMTs, 'ultraFinesDMTs': ultraFinesDMTs, 'ultraFinesGradeVals': ultraFinesGradeVals,
			'ultraFinesWMTTotal': ultraFinesWMTTotal, 'ultraFinesDMTTotal': ultraFinesDMTTotal,
			'rejectsWMTs': rejectsWMTs, 'rejectsDMTs': rejectsDMTs,
			'rejectsWMTTotal': rejectsWMTTotal, 'rejectsDMTTotal': rejectsDMTTotal,
			'sumWMTs': sumWMTs, 'sumDMTs': sumDMTs, 'sumWMTTotal': sumWMTTotal, 'sumDMTTotal': sumDMTTotal})

	sumWMTs = [Decimal(0.0)]*len(yearVals)
	sumDMTs = [Decimal(0.0)]*len(yearVals)

	# tblPlantProductTonnage gives tonnageDMT and tonnageWMT values
	# tblSmelterTermsOptimized gives grade values
	if 1 in PPIDs:
		lumpWMTs = []
		lumpDMTs = []
		lumpGradeVals = {}
		lumpDailyTonnages = {}

		for year in yearVals:
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			lumpTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=1,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

			currDailyTonnages = []
			for entry in lumpTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			lumpDailyTonnages[year] = currDailyTonnages

			sumTonnageWMT = lumpTonnageEntries.aggregate(sumTonnageWMT=Sum('tonnageWMT'))
			lumpWMTs.append(round(sumTonnageWMT['sumTonnageWMT'],2))
			sumTonnageDMT = lumpTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			lumpDMTs.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		lumpWMTTotal = sum(lumpWMTs)
		lumpDMTTotal = sum(lumpDMTs)
		sumWMTs = [x+y for x,y in zip(sumWMTs, lumpWMTs)]
		sumDMTs = [x+y for x,y in zip(sumDMTs, lumpDMTs)]

		for i in range(len(commIDs)):
			tempGradesByYear = []
			for year in yearVals:
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				lumpEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=1, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

				dailyGrades = []
				for entry in lumpEntries:
					dailyGrades.append(entry.grade)
				tempGradesByYear.append(round(np.average(dailyGrades, weights=lumpDailyTonnages[year]),2))
			lumpGradeVals[commNameList[i]] = tempGradesByYear

	if 2 in PPIDs:
		finesWMTs = []
		finesDMTs = []
		finesGradeVals = {}
		finesDailyTonnages = {}

		for year in yearVals:
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			finesTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=2,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

			currDailyTonnages = []
			for entry in finesTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			finesDailyTonnages[year] = currDailyTonnages

			sumTonnageWMT = finesTonnageEntries.aggregate(sumTonnageWMT=Sum('tonnageWMT'))
			finesWMTs.append(round(sumTonnageWMT['sumTonnageWMT'],2))
			sumTonnageDMT = finesTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			finesDMTs.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		finesWMTTotal = sum(finesWMTs)
		finesDMTTotal = sum(finesDMTs)
		sumWMTs = [x+y for x,y in zip(sumWMTs, finesWMTs)]
		sumDMTs = [x+y for x,y in zip(sumDMTs, finesDMTs)]

		for i in range(len(commIDs)):
			tempGradesByYear = []
			for year in yearVals:
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				finesEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=2, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				
				dailyGrades = []
				for entry in finesEntries:
					dailyGrades.append(entry.grade)
				tempGradesByYear.append(round(np.average(dailyGrades, weights=finesDailyTonnages[year]),2))
			finesGradeVals[commNameList[i]] = tempGradesByYear

	if 3 in PPIDs:
		ultraFinesWMTs = []
		ultraFinesDMTs = []
		ultraFinesGradeVals = {}
		ultraFinesDailyTonnages = {}

		for year in yearVals:
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			ultraFinesTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=3,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

			currDailyTonnages = []
			for entry in ultraFinesTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			ultraFinesDailyTonnages[year] = currDailyTonnages

			sumTonnageWMT = ultraFinesTonnageEntries.aggregate(sumTonnageWMT=Sum('tonnageWMT'))
			ultraFinesWMTs.append(round(sumTonnageWMT['sumTonnageWMT'],2))
			sumTonnageDMT = ultraFinesTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			ultraFinesDMTs.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		ultraFinesWMTTotal = sum(ultraFinesWMTs)
		ultraFinesDMTTotal = sum(ultraFinesDMTs)
		sumWMTs = [x+y for x,y in zip(sumWMTs, ultraFinesWMTs)]
		sumDMTs = [x+y for x,y in zip(sumDMTs, ultraFinesDMTs)]

		for i in range(len(commIDs)):
			tempGradesByYear = []
			for year in yearVals:
				currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
				ultraFinesEntries = tblPlantProductGradeOptimized.objects.filter(projectID=latestProject.projectID, plantProductID=3, commodityID=commIDs[i],
					date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)
				
				dailyGrades = []
				for entry in ultraFinesEntries:
					dailyGrades.append(entry.grade)
				tempGradesByYear.append(round(np.average(dailyGrades, weights=ultraFinesDailyTonnages[year]),2))
			ultraFinesGradeVals[commNameList[i]] = tempGradesByYear

	if 4 in PPIDs:
		rejectsWMTs = []
		rejectsDMTs = []
		rejectsGradeVals = {}
		rejectsDailyTonnages = {}

		for year in yearVals:
			currPeriod = tblProjectPeriods.objects.get(projectID=latestProject.projectID, year=year)
			rejectsTonnageEntries = tblPlantProductTonnage.objects.filter(projectID=latestProject.projectID, plantProductID=4,
				date__gte=currPeriod.startDate, date__lte=currPeriod.endDate)

			currDailyTonnages = []
			for entry in rejectsTonnageEntries:
				currDailyTonnages.append(entry.tonnageDMT)
			rejectsDailyTonnages[year] = currDailyTonnages

			sumTonnageWMT = rejectsTonnageEntries.aggregate(sumTonnageWMT=Sum('tonnageWMT'))
			rejectsWMTs.append(round(sumTonnageWMT['sumTonnageWMT'],2))
			sumTonnageDMT = rejectsTonnageEntries.aggregate(sumTonnageDMT=Sum('tonnageDMT'))
			rejectsDMTs.append(round(sumTonnageDMT['sumTonnageDMT'],2))
		rejectsWMTTotal = sum(rejectsWMTs)
		rejectsDMTTotal = sum(rejectsDMTs)
		sumWMTs = [x+y for x,y in zip(sumWMTs, rejectsWMTs)]
		sumDMTs = [x+y for x,y in zip(sumDMTs, rejectsDMTs)]

	sumWMTTotal = sum(sumWMTs)
	sumDMTTotal = sum(sumDMTs)

	# Pad values afterwards for missing years
	if len(yearVals) != yearCount:
		if 1 in PPIDs:
			lumpWMTs = padList(yearVals, yearCount, lumpWMTs, 0.0)
			lumpDMTs = padList(yearVals, yearCount, lumpDMTs, 0.0)
			for i in range(len(commIDs)):
				lumpGradeVals[commNameList[i]] = padList(yearVals, yearCount, lumpGradeVals[commNameList[i]], 0.0)
		if 2 in PPIDs:
			finesWMTs = padList(yearVals, yearCount, finesWMTs, 0.0)
			finesDMTs = padList(yearVals, yearCount, finesDMTs, 0.0)
			for i in range(len(commIDs)):
				finesGradeVals[commNameList[i]] = padList(yearVals, yearCount, finesGradeVals[commNameList[i]], 0.0)
		if 3 in PPIDs:
			ultraFinesWMTs = padList(yearVals, yearCount, ultraFinesWMTs, 0.0)
			ultraFinesDMTs = padList(yearVals, yearCount, ultraFinesDMTs, 0.0)
			for i in range(len(commIDs)):
				ultraFinesGradeVals[commNameList[i]] = padList(yearVals, yearCount, ultraFinesGradeVals[commNameList[i]], 0.0)
		if 4 in PPIDs:
			rejectsWMTs = padList(yearVals, yearCount, rejectsWMTs, 0.0)
			rejectsDMTs = padList(yearVals, yearCount, rejectsDMTs, 0.0)

		sumWMTs = padList(yearVals, yearCount, sumWMTs, 0.0)
		sumDMTs = padList(yearVals, yearCount, sumDMTs, 0.0)

	form = plantForm(commIDs=commIDs, commNameList=commNameList, PPIDs=PPIDs,
		lumpWMTs=lumpWMTs, lumpDMTs=lumpDMTs, lumpGradeVals=lumpGradeVals,
		lumpWMTTotal=lumpWMTTotal, lumpDMTTotal=lumpDMTTotal,
		finesWMTs=finesWMTs, finesDMTs=finesDMTs, finesGradeVals=finesGradeVals,
		finesWMTTotal=finesWMTTotal, finesDMTTotal=finesDMTTotal,
		ultraFinesWMTs=ultraFinesWMTs, ultraFinesDMTs=ultraFinesDMTs, ultraFinesGradeVals=ultraFinesGradeVals,
		ultraFinesWMTTotal=ultraFinesWMTTotal, ultraFinesDMTTotal=ultraFinesDMTTotal,
		rejectsWMTs=rejectsWMTs, rejectsDMTs=rejectsDMTs,
		rejectsWMTTotal=rejectsWMTTotal, rejectsDMTTotal=rejectsDMTTotal,
		sumWMTs=sumWMTs, sumDMTs=sumDMTs, sumWMTTotal=sumWMTTotal, sumDMTTotal=sumDMTTotal)

	return render(request, 'plant/plant.html', {'form': form, 'yearCount': yearCount, 
		'PPIDs': PPIDs, 'commIDs': commIDs, 'commNameList': commNameList,
		'lumpWMTs': lumpWMTs, 'lumpDMTs': lumpDMTs, 'lumpGradeVals': lumpGradeVals,
		'lumpWMTTotal': lumpWMTTotal, 'lumpDMTTotal': lumpDMTTotal,
		'finesWMTs': finesWMTs, 'finesDMTs': finesDMTs, 'finesGradeVals': finesGradeVals,
		'finesWMTTotal': finesWMTTotal, 'finesDMTTotal': finesDMTTotal,
		'ultraFinesWMTs': ultraFinesWMTs, 'ultraFinesDMTs': ultraFinesDMTs, 'ultraFinesGradeVals': ultraFinesGradeVals,
		'ultraFinesWMTTotal': ultraFinesWMTTotal, 'ultraFinesDMTTotal': ultraFinesDMTTotal,
		'rejectsWMTs': rejectsWMTs, 'rejectsDMTs': rejectsDMTs,
		'rejectsWMTTotal': rejectsWMTTotal, 'rejectsDMTTotal': rejectsDMTTotal,
		'sumWMTs': sumWMTs, 'sumDMTs': sumDMTs, 'sumWMTTotal': sumWMTTotal, 'sumDMTTotal': sumDMTTotal})
