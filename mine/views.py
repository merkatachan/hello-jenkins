from django.shortcuts import render
from django.utils import timezone
from .forms import *
import numpy as np
import decimal as decimal
from decimal import Decimal
import datetime
from setup.models import *

# Create your views here.
# Function index handles mine products declarations.
def index(request):
	# return render(request, 'mineproduct.html')
	#form_class = MineProductForm
	mineID = request.session["mineID"]
	mineMatch = tblMine.objects.get(mineID=int(mineID))
	if request.method == 'POST':

		form = MineProductForm(request.POST, mineID=mineID)
		# productsTonnage = request.POST.getlist('productTonnage')
		# mineProductGrade = request.POST.getlist('mineProductGrade')

		# Obtain latest projectID
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		numStockpiles = latestProject.numStockpiles

		# # Get list of Mine Product IDs
		# latestMineProduct = tblMineProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# MPTimestamp = latestMineProduct.dateAdded
		# mineProductMatches = tblMineProduct.objects.filter(mineID=int(mineID), dateAdded=MPTimestamp)
		# MPIDs = mineProductMatches.values_list('mineProductID', flat=True)

		# Get list of Commodity IDs
		latestCommodity = tblCommodity.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		commtimestamp = latestCommodity.dateAdded
		commodities = tblCommodity.objects.filter(mineID=int(mineID), dateAdded=commtimestamp)
		commIDs = commodities.values_list('commodityID', flat=True)

		# Get list of Plant Product IDs
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		PPMatches = tblPlantProduct.objects.filter(projectID=latestProject.projectID)
		# latestPlantProduct = tblPlantProduct.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		# PPTimestamp = latestPlantProduct.dateAdded
		# PPMatches = tblPlantProduct.objects.filter(mineID=int(mineID), dateAdded=PPTimestamp)
		PPIDs = PPMatches.values_list('plantProductID', flat=True)
		
		if form.is_valid():
			if "calculate" in request.POST:

				# Get latest ProjectID
				# latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				calcDateStr = request.POST.get('calcDate', '')
				calcDate = datetime.datetime.strptime(calcDateStr, "%Y-%m-%d").date()
				try:
					periodEntry = tblProjectPeriods.objects.get(projectID=latestProject.projectID, startDate__lte=calcDate, endDate__gte=calcDate)
				except tblProjectPeriods.DoesNotExist:
					periodEntry = None

				if periodEntry is None:
					errorMsg = "Your chosen date is outside of the range of this project. Try again."
					form_class = MineProductForm(mineID=mineID)
					return render(request, 'mine/mineproduct.html', {'form': form_class,
						'errorMsg': errorMsg})
				else:
					year = periodEntry.year

				# hgTonnageInit = None
				# lgTonnageInit = None
				# wasteInit = None
				# overburdenInit = None
				# hgInits = {}
				# lgInits = {}
				# wasteInits = {}

				# NEW: Instantiate and Populate tonnagesInit and gradesInit
				# tonnagesInit: list of tonnages ordered by stockpileID
				tonnagesInit = []
				# gradesInit: Key=stockpile, Value={[ID]: Grade%}
				gradesInit = {}
				for curr in range(1, numStockpiles+1):
					tonnagesInit.append(float(request.POST.get('stockpile{0}Tonnage'.format(curr), '')))

					tempGrades = {}
					for ID in commIDs:
						tempGrades[ID] = float(request.POST.get('stockpile{0}{1}'.format(curr, ID), ''))
					gradesInit[curr] = tempGrades


				# if 1 in MPIDs:
				# 	highGradeTonnage = hgTonnageInit = float(request.POST.get('highGradeTonnage', ''))
				# 	for ID in commIDs:
				# 		hgInits[ID] = float(request.POST.get('highGrade{0}'.format(ID), ''))

				# if 2 in MPIDs:
				# 	lowGradeTonnage = lgTonnageInit = float(request.POST.get('lowGradeTonnage', ''))
				# 	for ID in commIDs:
				# 		lgInits[ID] = float(request.POST.get('lowGrade{0}'.format(ID), ''))

				# if 3 in MPIDs:
				# 	waste = wasteInit = float(request.POST.get('waste', ''))
				# 	for ID in commIDs:
				# 		wasteInits[ID] = float(request.POST.get('waste{0}'.format(ID), ''))

				# if 4 in MPIDs:
				# 	overburdenInit = float(request.POST.get('overburden', ''))

				# hgEntries = int(highGradeTonnage/10)
				# lgEntries = int(lowGradeTonnage/10)


				# NEW: tonnageEntries, tonnageVectors and tonnageSpaces
				# tonnageEntries = [*[int(curr/10) for curr in tonnagesInit]]
				tonnageEntries = [*[int(curr/1) for curr in tonnagesInit]]
				# if len(tonnageEntries) > 1:
				# 	tonnageEntries[0], tonnageEntries[1] = tonnageEntries[1], tonnageEntries[0]
				tonnageVectors = [*[np.linspace(0.0, float(curr), curr+1) for curr in tonnageEntries]]
				tonnageSpaces = np.meshgrid(*tonnageVectors)



				intermediateMats = {}
				if 1 in PPIDs:
					lumpGradeMats = {}
					lumpGradePenMats = {}
				if 2 in PPIDs:
					finesGradeMats = {}
					finesGradePenMats = {}
				if 3 in PPIDs:
					ultraFinesGradeMats = {}
					ultraFinesPenMats = {}
				if 4 in PPIDs:
					rejectsGradeMats = {}
					rejectsPenMats = {}


				# NEW: IntermediateMats calculations (by commID)
				dimensions = tonnageSpaces[0].shape
				firstIndex = tuple([0]*len(dimensions))
				for ID in commIDs:
					intermediateSpaces = [*[tonnageSpaces[curr]*gradesInit[curr+1][ID] for curr in range(len(tonnageSpaces))]]
					denominator = sum(tonnageSpaces)
					sumIntermediateSpaces = sum(intermediateSpaces)
					intermediateMats[ID] = sumIntermediateSpaces/denominator
					intermediateMats[ID][firstIndex] = 0.0


				# for ID in commIDs:
				# 	intermediateMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 	if 1 in PPIDs:
				# 		lumpGradeMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 		lumpGradePenMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 	if 2 in PPIDs:
				# 		finesGradeMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 		finesGradePenMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 	if 3 in PPIDs:
				# 		ultraFinesGradeMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 		ultraFinesPenMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 	if 4 in PPIDs:
				# 		rejectsGradeMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))
				# 		rejectsPenMats[ID] = np.empty(shape=(lgEntries+1, hgEntries+1))

				# # Perform the Lump Grade % calculation here
				# # Find out the other 2 constants for the Lump Grade % calculation
				# latestInputEntry = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				# constant1 = (latestInputEntry.lumpGrade/100.0) * (latestInputEntry.lumpRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
				# constant2 = 1.0 / (latestInputEntry.lumpRecovery/100.0)
				# # Iterate through each commodity
				# for ID in commIDs:
				# 	for i in range(lgEntries+1):
				# 		for j in range(hgEntries+1):
				# 			# Add 1 to both i and j for arithmetic
				# 			if (i==0) and (j==0):
				# 				intermediateMats[ID][i][j] = 0.0
				# 			else:
				# 				# lumpGradeMats[ID][i][j] = finesGradeMats[ID][i][j] = (float((j+1)*1000)*hgEntry.grade/(float(i+j+2)*1000)) + (float((i+1)*1000)*lgEntry.grade/(float(i+j+2)*1000))
				# 				# lumpGradeMats[ID][i][j] = finesGradeMats[ID][i][j] = (float(j*100)*(hgEntry.grade/100.0)/(float(i+j)*100)) + (float(i*100)*(lgEntry.grade/100.0)/(float(i+j)*100))
				# 				# lumpGradeMats[ID][i][j] = finesGradeMats[ID][i][j] = (float(j*10)*(hgEntry.grade/100.0)/(float(i+j)*10)) + (float(i*10)*(lgEntry.grade/100.0)/(float(i+j)*10))
				# 				# lumpGradeMats[ID][i][j] = finesGradeMats[ID][i][j] = (float(j)*hgEntry.grade/(float(i+j))) + (float(i)*lgEntry.grade/(float(i+j)))
				# 				# intermediateMats[ID][i][j] = (float(j*10)*(hgEntry.grade/100.0)/(float(i+j)*10)) + (float(i*10)*(lgEntry.grade/100.0)/(float(i+j)*10))
				# 				# intermediateMats[ID][i][j] = (float(j*10)*(hgEntry.grade)/(float(i+j)*10)) + (float(i*10)*(lgEntry.grade)/(float(i+j)*10))
				# 				intermediateMats[ID][i][j] = (float(j*10)*(hgInits[ID])/(float(i+j)*10)) + (float(i*10)*(lgInits[ID])/(float(i+j)*10))

				# 	# Multiply the other 2 constant terms to the Lump Grade Matrix
				# 	if 1 in PPIDs:
				# 		lumpGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]


				# NEW: Lump, Fines, UltraFines, Rejects calculations
				latestInputEntry = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				if 1 in PPIDs:
					constant1 = (latestInputEntry.lumpGrade/100.0) * (latestInputEntry.lumpRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.lumpRecovery/100.0)
					for ID in commIDs:
						lumpGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						lumpGradePenMats[ID] = np.empty(shape=lumpGradeMats[ID].shape)
						lumpGradePenMats[ID] = np.where(lumpGradeMats[ID] >= smelterEntry.maxGrade,
							(-1)*(smelterEntry.maxGrade - lumpGradeMats[ID])*smelterEntry.premium, lumpGradePenMats[ID])
						lumpGradePenMats[ID] = np.where((lumpGradeMats[ID] < smelterEntry.maxGrade) & (lumpGradeMats[ID] >= smelterEntry.minGrade), 
							(lumpGradeMats[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty, 
							(smelterEntry.minGrade - lumpGradeMats[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty)

				if 2 in PPIDs:
					constant1 = (latestInputEntry.finesGrade/100.0) * (latestInputEntry.finesRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.finesRecovery/100.0)
					for ID in commIDs:
						finesGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						finesGradePenMats[ID] = np.empty(shape=finesGradeMats[ID].shape)
						finesGradePenMats[ID] = np.where(finesGradeMats[ID] >= smelterEntry.maxGrade,
							(-1)*(smelterEntry.maxGrade - finesGradeMats[ID])*smelterEntry.premium, finesGradePenMats[ID])
						finesGradePenMats[ID] = np.where((finesGradeMats[ID] < smelterEntry.maxGrade) & (finesGradeMats[ID] >= smelterEntry.minGrade), 
							(finesGradeMats[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty, 
							(smelterEntry.minGrade - finesGradeMats[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty)

				if 3 in PPIDs:
					constant1 = (latestInputEntry.ultraFinesGrade/100.0) * (latestInputEntry.ultraFinesRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.ultraFinesRecovery/100.0)
					for ID in commIDs:
						ultraFinesGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						ultraFinesGradePenMats[ID] = np.empty(shape=ultraFinesGradeMats[ID].shape)
						ultraFinesGradePenMats[ID] = np.where(ultraFinesGradeMats[ID] >= smelterEntry.maxGrade,
							(-1)*(smelterEntry.maxGrade - ultraFinesGradeMats[ID])*smelterEntry.premium, ultraFinesGradePenMats[ID])
						ultraFinesGradePenMats[ID] = np.where((ultraFinesGradeMats[ID] < smelterEntry.maxGrade) & (ultraFinesGradeMats[ID] >= smelterEntry.minGrade), 
							(ultraFinesGradeMats[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty, 
							(smelterEntry.minGrade - ultraFinesGradeMats[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty)

				if 4 in PPIDs:
					constant1 = (latestInputEntry.rejectsGrade/100.0) * (latestInputEntry.rejectsRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.rejectsRecovery/100.0)
					for ID in commIDs:
						rejectsGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						rejectsGradePenMats[ID] = np.empty(shape=rejectsGradeMats[ID].shape)
						rejectsGradePenMats[ID] = np.where(rejectsGradeMats[ID] >= smelterEntry.maxGrade,
							(-1)*(smelterEntry.maxGrade - rejectsGradeMats[ID])*smelterEntry.premium, rejectsGradePenMats[ID])
						rejectsGradePenMats[ID] = np.where((rejectsGradeMats[ID] < smelterEntry.maxGrade) & (rejectsGradeMats[ID] >= smelterEntry.minGrade), 
							(rejectsGradeMats[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty, 
							(smelterEntry.minGrade - rejectsGradeMats[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty)



				# # Perform the Lump Penalty calculation here
				# if 1 in PPIDs:
				# 	latestSmelterEntry = tblSmelterTerms.objects.filter(mineID=int(mineID), commodityID=ID).order_by('-dateAdded')[0]
				# 	smelterTimestamp = latestSmelterEntry.dateAdded
				# 	for ID in commIDs:
				# 		smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
				# 		for i in range(lgEntries+1):
				# 			for j in range(hgEntries+1):
				# 				# if lumpGradeMats[ID][i][j] >= (smelterEntry.HGMaxGrade/100.0):
				# 				if lumpGradeMats[ID][i][j] >= smelterEntry.HGMaxGrade:
				# 					# lumpGradePenMats[ID][i][j] = (smelterEntry.HGMaxGrade/100.0 - lumpGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 					lumpGradePenMats[ID][i][j] = (-1)*(smelterEntry.HGMaxGrade - lumpGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 				# elif lumpGradeMats[ID][i][j] > (smelterEntry.HGMinGrade/100.0):
				# 				elif lumpGradeMats[ID][i][j] >= smelterEntry.HGMinGrade:
				# 					# lumpGradePenMats[ID][i][j] = (lumpGradeMats[ID][i][j] - smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinMaxPenalty
				# 					lumpGradePenMats[ID][i][j] = (lumpGradeMats[ID][i][j] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
				# 				# elif lumpGradeMats[ID][i][j] == (smelterEntry.HGMinGrade/100.0):
				# 				# 	lumpGradePenMats[ID][i][j] = smelterEntry.HGMinPenalty + ((smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)/100.0)*smelterEntry.HGMinMaxPenalty
				# 				else:
				# 					# lumpGradePenMats[ID][i][j] = (1.0+lumpGradeMats[ID][i][j]-smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinPenalty
				# 					lumpGradePenMats[ID][i][j] = (smelterEntry.HGMinGrade - lumpGradeMats[ID][i][j])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty

				# if 2 in PPIDs:
				# 	# Perform the Fines Grade % calcuation here
				# 	constant1 = (latestInputEntry.finesGrade/100.0) * (latestInputEntry.finesRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
				# 	constant2 = 1.0 / (latestInputEntry.finesRecovery/100.0)
				# 	for ID in commIDs:
				# 		finesGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]

				# 	# Perform the Fines Penalty calculation here
				# 	for ID in commIDs:
				# 		smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
				# 		for i in range(lgEntries+1):
				# 			for j in range(hgEntries+1):
				# 				# if finesGradeMats[ID][i][j] >= (smelterEntry.HGMaxGrade/100.0):
				# 				if finesGradeMats[ID][i][j] >= smelterEntry.HGMaxGrade:
				# 					# finesGradePenMats[ID][i][j] = (smelterEntry.HGMaxGrade/100.0 - finesGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 					finesGradePenMats[ID][i][j] = (-1)*(smelterEntry.HGMaxGrade - finesGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 				# elif finesGradeMats[ID][i][j] > (smelterEntry.HGMinGrade/100.0):
				# 				elif finesGradeMats[ID][i][j] >= smelterEntry.HGMinGrade:
				# 					# finesGradePenMats[ID][i][j] = (finesGradeMats[ID][i][j] - smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinMaxPenalty
				# 					finesGradePenMats[ID][i][j] = (finesGradeMats[ID][i][j] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
				# 				# elif finesGradeMats[ID][i][j] == (smelterEntry.HGMinGrade/100.0):
				# 				# 	finesGradePenMats[ID][i][j] = smelterEntry.HGMinPenalty + ((smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)/100.0)*smelterEntry.HGMinMaxPenalty
				# 				else:
				# 					# finesGradePenMats[ID][i][j] = (1.0+finesGradeMats[ID][i][j]-smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinPenalty
				# 					finesGradePenMats[ID][i][j] = (smelterEntry.HGMinGrade - finesGradeMats[ID][i][j])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty

				# if 3 in PPIDs:
				# 	# Perform the Ultra Fines Grade % calcuation here
				# 	constant1 = (latestInputEntry.ultraFinesGrade/100.0) * (latestInputEntry.ultraFinesRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
				# 	constant2 = 1.0 / (latestInputEntry.ultraFinesRecovery/100.0)
				# 	for ID in commIDs:
				# 		ultraFinesGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]

				# 	# Perform the Ultra Fines Penalty Calculation here
				# 	for ID in commIDs:
				# 		smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
				# 		for i in range(lgEntries+1):
				# 			for j in range(hgEntries+1):
				# 				# if ultraFinesGradeMats[ID][i][j] >= (smelterEntry.HGMaxGrade/100.0):
				# 				if ultraFinesGradeMats[ID][i][j] >= smelterEntry.HGMaxGrade:
				# 					# ultraFinesPenMats[ID][i][j] = (smelterEntry.HGMaxGrade/100.0 - ultraFinesGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 					ultraFinesPenMats[ID][i][j] = (-1)*(smelterEntry.HGMaxGrade - ultraFinesGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 				# elif ultraFinesGradeMats[ID][i][j] > (smelterEntry.HGMinGrade/100.0):
				# 				elif ultraFinesGradeMats[ID][i][j] >= smelterEntry.HGMinGrade:
				# 					# ultraFinesPenMats[ID][i][j] = (ultraFinesGradeMats[ID][i][j] - smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinMaxPenalty
				# 					ultraFinesPenMats[ID][i][j] = (ultraFinesGradeMats[ID][i][j] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
				# 				# elif ultraFinesGradeMats[ID][i][j] == (smelterEntry.HGMinGrade/100.0):
				# 				# 	ultraFinesPenMats[ID][i][j] = smelterEntry.HGMinPenalty + ((smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)/100.0)*smelterEntry.HGMinMaxPenalty
				# 				else:
				# 					# ultraFinesPenMats[ID][i][j] = (1.0+ultraFinesGradeMats[ID][i][j]-smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinPenalty
				# 					ultraFinesPenMats[ID][i][j] = (smelterEntry.HGMinGrade - ultraFinesGradeMats[ID][i][j])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty

				# if 4 in PPIDs:
				# 	# Perform the Rejects Grade % calcuation here
				# 	constant1 = (latestInputEntry.rejectsGrade/100.0) * (latestInputEntry.rejectsRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
				# 	constant2 = 1.0 / (latestInputEntry.rejectsRecovery/100.0)
				# 	for ID in commIDs:
				# 		rejectsGradeMats[ID] = constant1 * constant2 * intermediateMats[ID]

				# 	# Perform the Rejects Penalty Calculation here
				# 	for ID in commIDs:
				# 		smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
				# 		for i in range(lgEntries+1):
				# 			for j in range(hgEntries+1):
				# 				# if rejectsGradeMats[ID][i][j] >= (smelterEntry.HGMaxGrade/100.0):
				# 				if rejectsGradeMats[ID][i][j] >= smelterEntry.HGMaxGrade:
				# 					# rejectsPenMats[ID][i][j] = (smelterEntry.HGMaxGrade/100.0 - rejectsGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 					rejectsPenMats[ID][i][j] = (-1)*(smelterEntry.HGMaxGrade - rejectsGradeMats[ID][i][j])*smelterEntry.HGPremium
				# 				# elif rejectsGradeMats[ID][i][j] > (smelterEntry.HGMinGrade/100.0):
				# 				elif rejectsGradeMats[ID][i][j] >= smelterEntry.HGMinGrade:
				# 					# rejectsPenMats[ID][i][j] = (rejectsGradeMats[ID][i][j] - smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinMaxPenalty
				# 					rejectsPenMats[ID][i][j] = (rejectsGradeMats[ID][i][j] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
				# 				# elif rejectsGradeMats[ID][i][j] == (smelterEntry.HGMinGrade/100.0):
				# 				# 	rejectsPenMats[ID][i][j] = smelterEntry.HGMinPenalty + ((smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)/100.0)*smelterEntry.HGMinMaxPenalty
				# 				else:
				# 					# rejectsPenMats[ID][i][j] = (1.0+rejectsGradeMats[ID][i][j]-smelterEntry.HGMinGrade/100.0)*smelterEntry.HGMinPenalty
				# 					rejectsPenMats[ID][i][j] = (smelterEntry.HGMinGrade - rejectsGradeMats[ID][i][j])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty


				# Perform the Net Price calculation here
				sumLumpPenalties = 0
				if 1 in PPIDs:
					for ID in commIDs:
						# if sumLumpPenalties == 0:
						# 	sumLumpPenalties = lumpGradePenMats[ID]
						# else:
						# 	sumLumpPenalties = sumLumpPenalties + lumpGradePenMats[ID]
						sumLumpPenalties = sumLumpPenalties + lumpGradePenMats[ID]

				sumFinesPenalties = 0
				if 2 in PPIDs:
					for ID in commIDs:
						# if sumFinesPenalties == 0:
						# 	sumFinesPenalties = finesGradePenMats[ID]
						# else:
						# 	sumFinesPenalties = sumFinesPenalties + finesGradePenMats[ID]
						sumFinesPenalties = sumFinesPenalties + finesGradePenMats[ID]

				sumUltraFinesPenalties = 0
				if 3 in PPIDs:
					for ID in commIDs:
						# if sumUltraFinesPenalties == 0:
						# 	sumUltraFinesPenalties = ultraFinesGradePenMats[ID]
						# else:
						# 	sumUltraFinesPenalties = sumUltraFinesPenalties + ultraFinesGradePenMats[ID]
						sumUltraFinesPenalties = sumUltraFinesPenalties + ultraFinesGradePenMats[ID]

				priceEntry = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=1)
				# priceEntry = tblPrice.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				opexPT = tblOPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]

				# netHG = np.tile(np.arange(hgEntries+1), (lgEntries+1,1)) * (priceEntry.HGLump - sumLumpPenalties)
				# netLG = np.tile(np.arange(lgEntries+1), (hgEntries+1,1)).transpose() * (priceEntry.HGFines - sumFinesPenalties)

				# netHG = highGradeTonnage * (priceEntry.HGLump - sumLumpPenalties)
				# netLG = lowGradeTonnage * (priceEntry.HGFines - sumFinesPenalties)
				# netPrice = highGradeTonnage * (priceEntry.HGLump - sumLumpPenalties) + lowGradeTonnage * (priceEntry.HGFines - sumFinesPenalties)
				
				# lumpSubMX = np.tile(np.arange(hgEntries+1), (lgEntries+1,1))
				# finesSubMX = np.tile(np.arange(lgEntries+1), (hgEntries+1,1)).transpose()

				# netLump = (lumpSubMX + finesSubMX) * latestInputEntry.lumpRecovery * (priceEntry.HGLump - sumLumpPenalties - opexPT.opexPT)
				# netFines = (lumpSubMX + finesSubMX) * latestInputEntry.finesRecovery * (priceEntry.HGFines - sumFinesPenalties - opexPT.opexPT)
				
				if 1 in PPIDs:
					netLump = denominator * latestInputEntry.lumpRecovery * (priceEntry.lump - opexPT.opexPT - sumLumpPenalties)
					# netLump = denominator * latestInputEntry.lumpRecovery * (priceEntry.HGLump - opexPT.opexPT - sumLumpPenalties)
				else:
					netLump = 0
				if 2 in PPIDs:
					netFines = denominator * latestInputEntry.finesRecovery * (priceEntry.fines - opexPT.opexPT - sumFinesPenalties)
					# netFines = denominator * latestInputEntry.finesRecovery * (priceEntry.HGFines - opexPT.opexPT - sumFinesPenalties)
				else:
					netFines = 0
				if 3 in PPIDs:
					netUltraFines = denominator * latestInputEntry.ultraFinesRecovery * (priceEntry.ultraFines - opexPT.opexPT - sumUltraFinesPenalties)
					# netUltraFines = denominator * latestInputEntry.ultraFinesRecovery * (priceEntry.HGUltraFines - opexPT.opexPT - sumUltraFinesPenalties)
				else:
					netUltraFines = 0
				
				netPrice = netLump + netFines + netUltraFines
				maxIndex = netPrice.argmax()
				maxEntry = np.unravel_index(maxIndex, netPrice.shape)
				
				optimizedIntermediates = {}
				optimizedLumpGrades = None
				optimizedLumpPens = None
				optimizedFinesGrades = None
				optimizedFinesPens = None
				optimizedUltraFinesGrades = None
				optimizedUltraFinesPens = None
				optimizedRejectsGrades = None
				optimizedRejectsPens = None

				if 1 in PPIDs:
					optimizedLumpGrades = {}
					optimizedLumpPens = {}
				if 2 in PPIDs:
					optimizedFinesGrades = {}
					optimizedFinesPens = {}
				if 3 in PPIDs:
					optimizedUltraFinesGrades = {}
					optimizedUltraFinesPens = {}
				if 4 in PPIDs:
					optimizedRejectsGrades = {}
					optimizedRejectsPens = {}

				# for ID in commIDs:
				# 	optimizedIntermediates[ID] = intermediateMats[ID].flatten()[maxIndex]
				# 	if 1 in PPIDs:
				# 		optimizedLumpGrades[ID] = lumpGradeMats[ID].flatten()[maxIndex]
				# 		optimizedLumpPens[ID] = lumpGradePenMats[ID].flatten()[maxIndex]
				# 	if 2 in PPIDs:
				# 		optimizedFinesGrades[ID] = finesGradeMats[ID].flatten()[maxIndex]
				# 		optimizedFinesPens[ID] = finesGradePenMats[ID].flatten()[maxIndex]	
				# 	if 3 in PPIDs:
				# 		optimizedUltraFinesGrades[ID] = ultraFinesGradeMats[ID].flatten()[maxIndex]
				# 		optimizedUltraFinesPens[ID] = ultraFinesPenMats[ID].flatten()[maxIndex]
				# 	if 4 in PPIDs:
				# 		optimizedRejectsGrades[ID] = rejectsGradeMats[ID].flatten()[maxIndex]
				# 		optimizedRejectsPens[ID] = rejectsPenMats[ID].flatten()[maxIndex]

				for ID in commIDs:
					optimizedIntermediates[ID] = intermediateMats[ID][maxEntry]
					if 1 in PPIDs:
						optimizedLumpGrades[ID] = lumpGradeMats[ID][maxEntry]
						optimizedLumpPens[ID] = lumpGradePenMats[ID][maxEntry]
					if 2 in PPIDs:
						optimizedFinesGrades[ID] = finesGradeMats[ID][maxEntry]
						optimizedFinesPens[ID] = finesGradePenMats[ID][maxEntry]
					if 3 in PPIDs:
						optimizedUltraFinesGrades[ID] = ultraFinesGradeMats[ID][maxEntry]
						optimizedUltraFinesPens[ID] = ultraFinesPenMats[ID][maxEntry]
					if 4 in PPIDs:
						optimizedRejectsGrades[ID] = rejectsGradeMats[ID][maxEntry]
						optimizedRejectsPens[ID] = rejectsPenMats[ID][maxEntry]

				# optimizedHGTonnage = (maxIndex % (hgEntries+1))*100
				# optimizedHGTonnage = (maxIndex % (hgEntries+1))*10
				# optimizedHGTonnage = maxEntry[1]*10
				# optimizedLGTonnage = int(maxIndex / (hgEntries+1))*100
				# optimizedLGTonnage = int(maxIndex / (hgEntries+1))*10
				# optimizedLGTonnage = maxEntry[0]*10

				# optimizedTonnages = [*[i*10 for i in maxEntry]]
				optimizedTonnages = [*[i*1 for i in maxEntry]]
				if len(optimizedTonnages) > 1:
					optimizedTonnages[0], optimizedTonnages[1] = optimizedTonnages[1], optimizedTonnages[0]

				# currFines = priceEntry.HGFines

				# next_form_class = MineProductOptimizedForm(mineID=mineID, lumpGrades=optimizedLumpGrades, lumpPens=optimizedLumpPens,
				# 	finesGrades=optimizedFinesGrades, finesPens=optimizedFinesPens, hgTonnage=optimizedHGTonnage, lgTonnage=optimizedLGTonnage)
				# return render(request, 'mine/mineproductoptimized.html', {'form': next_form_class,
				# 	'calculated': True})

				next_form_class = MineProductForm(mineID=mineID, calculated=True, lumpGrades=optimizedLumpGrades, lumpPens=optimizedLumpPens,
					finesGrades=optimizedFinesGrades, finesPens=optimizedFinesPens, intermediates=optimizedIntermediates,
					ultraFinesGrades=optimizedUltraFinesGrades, ultraFinesPens=optimizedUltraFinesPens,
					rejectsGrades=optimizedRejectsGrades, rejectsPens=optimizedRejectsPens,
					optimizedTonnages=optimizedTonnages,
					tonnagesInit=tonnagesInit, gradesInit=gradesInit,
					calcDateStr=calcDateStr, year=year)
				return render(request, 'mine/mineproduct.html', {'form': next_form_class,
					'calculated': True})

			# Handle "Accept optimized values" here
			elif "accept" in request.POST:
				# Get recent tblMineProductTonnageOptimized timestamp
				# latestTonnage = tblMineProductTonnageOptimized.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				# tonnageTimestamp = latestTonnage.dateAdded

				calcDateStr = request.POST.get('calcDate', '')
				calcDate = datetime.datetime.strptime(calcDateStr, "%Y-%m-%d").date()

				# latestPPTonnage = tblPlantProductTonnage.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				# PPTonnageTimestamp = latestPPTonnage.dateAdded

				# if 1 in MPIDs:
				# 	wmtHighGrade = float(request.POST.get('wmtHighGrade', ''))
				# 	HGMPMatch = tblMineProductList.objects.get(mineProductID=1)
				# if 2 in MPIDs:
				# 	wmtLowGrade = float(request.POST.get('wmtLowGrade', ''))
				# 	LGMPMatch = tblMineProductList.objects.get(mineProductID=2)
				# if 3 in MPIDs:
				# 	wasteMPMatch = tblMineProductList.objects.get(mineProductID=3)
				# if 4 in MPIDs:
				# 	overburdenMPMatch = tblMineProductList.objects.get(mineProductID=4)

				if 1 in PPIDs:
					lumpPPMatch = tblPlantProductList.objects.get(plantProductID=1)
				if 2 in PPIDs:
					finesPPMatch = tblPlantProductList.objects.get(plantProductID=2)
				if 3 in PPIDs:
					ultraFinesPPMatch = tblPlantProductList.objects.get(plantProductID=3)
				if 4 in PPIDs:
					rejectsPPMatch = tblPlantProductList.objects.get(plantProductID=4)

				commMatches = {}
				for ID in commIDs:
					commMatches[ID] = tblCommodityList.objects.get(commodityID=ID)

				currTime = timezone.localtime(timezone.now())

				calcDateExists = False
				testEntry = tblMineProductTonnageOptimized.objects.filter(projectID=latestProject.projectID, date=calcDate)
				if testEntry:
					calcDateExists = True

				# Step 29: Find the tblMineProductTonnageOptimized entries and update tonnage values
				for curr in range(1, numStockpiles+1):
					if calcDateExists:
						currEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, stockpileID=curr, date=calcDate)
						currEntry.tonnage = float(request.POST.get("wmtStockpile{0}".format(curr), ''))
						currEntry.optimized = True
						currEntry.dateAdded = currTime
					else:
						currEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, stockpileID=curr,
							tonnage=float(request.POST.get("wmtStockpile{0}".format(curr), '')), date=calcDate, optimized=True, dateAdded=currTime)
					currEntry.save()

				# if 1 in MPIDs:
				# 	if calcDateExists:
				# 		HGTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=1, date=calcDate)
				# 		HGTonnageEntry.tonnage = wmtHighGrade
				# 		HGTonnageEntry.optimized = True
				# 		HGTonnageEntry.dateAdded = currTime
				# 	else:
				# 		HGTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=HGMPMatch,
				# 			tonnage=wmtHighGrade, date=calcDate, optimized=True, dateAdded=currTime)
				# 	HGTonnageEntry.save()

				# if 2 in MPIDs:
				# 	if calcDateExists:
				# 		LGTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=2, date=calcDate)
				# 		LGTonnageEntry.tonnage = wmtLowGrade
				# 		LGTonnageEntry.optimized = True
				# 		LGTonnageEntry.dateAdded = currTime
				# 	else:
				# 		LGTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=LGMPMatch,
				# 			tonnage=wmtLowGrade, date=calcDate, optimized=True, dateAdded=currTime)
				# 	LGTonnageEntry.save()

				# if 3 in MPIDs:
				# 	if calcDateExists:
				# 		wasteTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=3, date=calcDate)
				# 		wasteTonnageEntry.optimized = True
				# 		wasteTonnageEntry.dateAdded = currTime
				# 	else:
				# 		wasteTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=wasteMPMatch,
				# 			tonnage=None, date=calcDate, optimized=True, dateAdded=currTime)
				# 	wasteTonnageEntry.save()

				# if 4 in MPIDs:
				# 	if calcDateExists:
				# 		overburdenTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=4, date=calcDate)
				# 		overburdenTonnageEntry.optimized = True
				# 		overburdenTonnageEntry.dateAdded = currTime
				# 	else:
				# 		overburdenTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=overburdenMPMatch,
				# 			tonnage=None, date=calcDate, optimized=True, dateAdded=currTime)
				# 	overburdenTonnageEntry.save()

				# Find the tblMineProduct entries and update optimized flags
				# Find the tblPlantProduct entries and update grade values
				inputsEntry = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				for curr in range(1, numStockpiles+1):
					for ID in commIDs:
						if calcDateExists:
							currEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								stockpileID=curr, date=calcDate)
							currEntry.grade = request.POST.get('stockpile{0}{1}'.format(curr,ID), '')
							currEntry.optimized = True
							currEntry.dateAdded = currTime
						else:
							currEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, stockpileID=curr,
								commodityID=commMatches[ID], grade=request.POST.get('stockpile{0}{1}'.format(curr,ID), ''),
								date=calcDate, optimized=True, dateAdded=currTime)
						currEntry.save()



				# inputsEntry = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				# for ID in commIDs:
				# 	commodityMatch = tblCommodityList.objects.get(commodityID=ID)
				# 	if 1 in MPIDs:
				# 		tempGrade = request.POST.get('highGrade{0}'.format(ID), '')
				# 		if calcDateExists:
				# 			HGMPEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
				# 				mineProductID=1, date=calcDate)
				# 			HGMPEntry.grade = tempGrade
				# 			HGMPEntry.optimized = True
				# 			HGMPEntry.dateAdded = currTime
				# 		else:
				# 			HGMPEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=HGMPMatch,
				# 				commodityID=commodityMatch, grade=tempGrade, date=calcDate, optimized=True, dateAdded=currTime)
				# 		HGMPEntry.save()

				# 	if 2 in MPIDs:
				# 		tempGrade = request.POST.get('lowGrade{0}'.format(ID), '')
				# 		if calcDateExists:
				# 			LGMPEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
				# 				mineProductID=2, date=calcDate)
				# 			LGMPEntry.grade = tempGrade
				# 			LGMPEntry.optimized = True
				# 			LGMPEntry.dateAdded = currTime
				# 		else:
				# 			LGMPEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=LGMPMatch,
				# 				commodityID=commodityMatch, grade=tempGrade, date=calcDate, optimized=True, dateAdded=currTime)
				# 		LGMPEntry.save()

				# 	if 3 in MPIDs:
				# 		tempGrade = request.POST.get('waste{0}'.format(ID), '')
				# 		if calcDateExists:
				# 			wasteMPEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
				# 				mineProductID=3, date=calcDate)
				# 			wasteMPEntry.grade = tempGrade
				# 			wasteMPEntry.optimized = True
				# 			wasteMPEntry.dateAdded = currTime
				# 		else:
				# 			wasteMPEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=wasteMPMatch,
				# 				commodityID=commodityMatch, grade=tempGrade, date=calcDate, optimized=True, dateAdded=currTime)
				# 		wasteMPEntry.save()

				for ID in commIDs:
					if 1 in PPIDs:
						lumpGrade = float(request.POST.get("lumpGrade{0}".format(ID), ''))
						if calcDateExists:
							HGPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=1, date=calcDate)
							HGPPEntry.grade = lumpGrade
							HGPPEntry.optimized = True
							HGPPEntry.dateAdded = currTime
						else:
							HGPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
								commodityID=commMatches[ID], grade=lumpGrade, date=calcDate, dateAdded=currTime, optimized=True)
						HGPPEntry.save()
					else:
						lumpGrade = 0.0

					if 2 in PPIDs:
						finesGrade = float(request.POST.get("finesGrade{0}".format(ID), ''))
						if calcDateExists:
							LGPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=2, date=calcDate)
							LGPPEntry.grade = finesGrade
							LGPPEntry.optimized = True
							LGPPEntry.dateAdded = currTime
						else:
							LGPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
								commodityID=commMatches[ID], grade=finesGrade, date=calcDate, dateAdded=currTime, optimized=True)
						LGPPEntry.save()
					else:
						finesGrade = 0.0

					# Update Ultra Fines if it has been declared
					if 3 in PPIDs:
						ultraFinesGrade = float(request.POST.get("ultraFinesGrade{0}".format(ID), ''))
						if calcDateExists:
							UFPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=3, date=calcDate)
							UFPPEntry.grade = ultraFinesGrade
							UFPPEntry.optimized = True
							UFPPEntry.dateAdded = currTime
						else:
							UFPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
								commodityID=commMatches[ID], grade=ultraFinesGrade, date=calcDate, dateAdded=currTime, optimized=True)
						UFPPEntry.save()

					# Update Rejects if it has been declared
					if 4 in PPIDs:
						rejectsGrade = float(request.POST.get("rejectsGrade{0}".format(ID), ''))
						if calcDateExists:
							RPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=4, date=calcDate)
							RPPEntry.grade = rejectsGrade
							RPPEntry.optimized = True
							RPPEntry.dateAdded = currTime
						else:
							RPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=rejectsPPMatch,
								commodityID=commMatches[ID], grade=rejectsGrade, date=calcDate, dateAdded=currTime, optimized=True)
						RPPEntry.save()


				sumTonnage = 0.0
				for curr in range(1, numStockpiles+1):
					sumTonnage += float(request.POST.get("wmtStockpile{0}".format(curr), ''))
				# Find the Plant Product Tonnage entries and update tonnage values
				if 1 in PPIDs:
					lumpTonnageWMT = sumTonnage*inputsEntry.lumpRecovery/100
					lumpTonnageDMT = sumTonnage*inputsEntry.lumpRecovery/100*(1-inputsEntry.lumpMoisture/100)
					if calcDateExists:
						PPTLumpEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=1, date=calcDate)
						PPTLumpEntry.tonnageWMT = lumpTonnageWMT
						PPTLumpEntry.tonnageDMT = lumpTonnageDMT
						PPTLumpEntry.optimized = True
						PPTLumpEntry.dateAdded = currTime
					else:
						PPTLumpEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
							dateAdded=currTime, optimized=True, tonnageWMT=lumpTonnageWMT, tonnageDMT=lumpTonnageDMT, date=calcDate)
					PPTLumpEntry.save()

				if 2 in PPIDs:
					finesTonnageWMT = sumTonnage*inputsEntry.finesRecovery/100
					finesTonnageDMT = sumTonnage*inputsEntry.finesRecovery/100*(1-inputsEntry.finesMoisture/100)
					if calcDateExists:
						PPTFinesEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=2, date=calcDate)
						PPTFinesEntry.tonnageWMT = finesTonnageWMT
						PPTFinesEntry.tonnageDMT = finesTonnageDMT
						PPTFinesEntry.optimized = True
						PPTFinesEntry.dateAdded = currTime
					else:
						PPTFinesEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
							dateAdded=currTime, optimized=True, tonnageWMT=finesTonnageWMT, tonnageDMT=finesTonnageDMT, date=calcDate)
					PPTFinesEntry.save()

				# Update Ultra Fines Tonnage if it has been declared
				if 3 in PPIDs:
					ultraFinesTonnageWMT = sumTonnage*inputsEntry.ultraFinesRecovery/100
					ultraFinesTonnageDMT = sumTonnage*inputsEntry.ultraFinesRecovery/100*(1-inputsEntry.ultraFinesMoisture/100)
					if calcDateExists:
						PPTUltraFinesEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=3, date=calcDate)
						PPTUltraFinesEntry.tonnageWMT = ultraFinesTonnageWMT
						PPTUltraFinesEntry.tonnageDMT = ultraFinesTonnageDMT
						PPTUltraFinesEntry.optimized = True
						PPTUltraFinesEntry.dateAdded = currTime
					else:
						PPTUltraFinesEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
							dateAdded=currTime, optimized=True, tonnageWMT=ultraFinesTonnageWMT, tonnageDMT=ultraFinesTonnageDMT, date=calcDate)
					PPTUltraFinesEntry.save()

				# Update Rejects Tonnage if it has been declared
				if 4 in PPIDs:
					rejectsTonnageWMT = sumTonnage*inputsEntry.rejectsRecovery/100
					rejectsTonnageDMT = sumTonnage*inputsEntry.rejectsRecovery/100*(1-inputsEntry.rejectsMoisture/100)
					if calcDateExists:
						PPTRejectsEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=4, date=calcDate)
						PPTRejectsEntry.tonnageWMT = rejectsTonnageWMT
						PPTRejectsEntry.tonnageDMT = rejectsTonnageDMT
						PPTRejectsEntry.optimized = True
						PPTRejectsEntry.dateAdded = currTime
					else:
						PPTRejectsEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=rejectsPPMatch,
							dateAdded=currTime, optimized=True, tonnageWMT=rejectsTonnageWMT, tonnageDMT=rejectsTonnageDMT, date=calcDate)
					PPTRejectsEntry.save()

				sumLumpPen = 0
				sumFinesPen = 0
				sumUltraFinesPen = 0
				# Step 34: tblSmelterTermsOptimized Updates
				for ID in commIDs:
					commodityMatch = tblCommodityList.objects.get(commodityID=ID)
					if 1 in PPIDs:
						currPen = float(request.POST.get("lumpPen{0}".format(ID), ''))
						sumLumpPen += currPen
						if calcDateExists:
							lumpPenObj = tblSmelterTermsOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=1, date=calcDate)						
							lumpPenObj.penalty = currPen
							lumpPenObj.optimized = True
							lumpPenObj.dateAdded = currTime
						else:
							lumpPenObj = tblSmelterTermsOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
								commodityID=commodityMatch, penalty=currPen, date=calcDate, optimized=True, dateAdded=currTime)
						lumpPenObj.save()                                

					if 2 in PPIDs:
						currPen = float(request.POST.get("finesPen{0}".format(ID), ''))
						sumFinesPen += currPen
						if calcDateExists:
							finesPenObj = tblSmelterTermsOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=2, date=calcDate)							
							finesPenObj.penalty = currPen
							finesPenObj.optimized = True
							finesPenObj.dateAdded = currTime
						else:
							finesPenObj = tblSmelterTermsOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
								commodityID=commodityMatch, penalty=currPen, date=calcDate, optimized=True, dateAdded=currTime)
						finesPenObj.save()

					# Update Ultra Fines Penalty values if declared
					if 3 in PPIDs:
						currPen = float(request.POST.get("ultraFinesPen{0}".format(ID), ''))
						sumUltraFinesPen += currPen
						if calcDateExists:
							ultraFinesPenObj = tblSmelterTermsOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=3, date=calcDate)							
							ultraFinesPenObj.penalty = currPen
							ultraFinesPenObj.optimized = True
							ultraFinesPenObj.dateAdded = currTime
						else:
							ultraFinesPenObj = tblSmelterTermsOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
								commodityID=commodityMatch, penalty=currPen, date=calcDate, optimized=True, dateAdded=currTime)
						ultraFinesPenObj.save()

				# Get year entry from hidden field in mine form
				year = int(request.POST.get('year', ''))
				# year = 1
				# Step 35: tblRevenue Updates
				# Obtain tblPrice entry
				# priceEntry = tblPrice.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				priceEntry = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=1)
				OPEXEntry = tblOPEX.objects.filter(mineID=int(mineID), year=year).order_by('-dateAdded')[0]
				CAPEXEntry = tblCAPEX.objects.filter(mineID=int(mineID), year=year).order_by('-dateAdded')[0]

				sumRevenue = 0
				# HGLump = priceEntry.HGLump
				if 1 in PPIDs:
					# constant2 = priceEntry.HGLump - sumLumpPen
					constant2 = priceEntry.lump - sumLumpPen
					# constant1 = (wmtHighGrade + wmtLowGrade)*inputsEntry.lumpRecovery/100*(1-inputsEntry.lumpMoisture/100)
					constant1 = sumTonnage*inputsEntry.lumpRecovery/100*(1-inputsEntry.lumpMoisture/100)
					priceUSD = Decimal(constant2) - Decimal(OPEXEntry.shipping)					
					netPriceCAD = Decimal(priceUSD) / Decimal(inputsEntry.exchangeRate)
					tempRevenue = (Decimal(lumpTonnageDMT) * (Decimal(constant2) - Decimal(OPEXEntry.shipping))) / Decimal(inputsEntry.exchangeRate)				
					sumRevenue += tempRevenue

					if calcDateExists:
						lumpRevObj = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=1, date=calcDate)
						lumpRevObj.sellingPrice = constant2
						lumpRevObj.netPriceUSD = priceUSD
						lumpRevObj.netPriceCAD = netPriceCAD
						lumpRevObj.plantProductRevenue = tempRevenue
						lumpRevObj.dateAdded = currTime
					else:
						lumpRevObj = tblRevenue(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch, sellingPrice=constant2,
							netPriceUSD=priceUSD, netPriceCAD=netPriceCAD, plantProductRevenue=tempRevenue, dateAdded=currTime, date=calcDate)
					lumpRevObj.save()

				if 2 in PPIDs:
					# constant2 = priceEntry.HGFines - sumFinesPen
					constant2 = priceEntry.fines - sumFinesPen
					# constant1 = (wmtHighGrade + wmtLowGrade)*inputsEntry.finesRecovery/100*(1-inputsEntry.finesMoisture/100)
					constant1 = sumTonnage*inputsEntry.finesRecovery/100*(1-inputsEntry.finesMoisture/100)
					priceUSD = Decimal(constant2) - Decimal(OPEXEntry.shipping)					
					netPriceCAD = Decimal(priceUSD) / Decimal(inputsEntry.exchangeRate)
					tempRevenue = (Decimal(finesTonnageDMT) * (Decimal(constant2) - Decimal(OPEXEntry.shipping))) / Decimal(inputsEntry.exchangeRate)
					sumRevenue += tempRevenue

					if calcDateExists:
						finesRevObj = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=2, date=calcDate)
						finesRevObj.sellingPrice = constant2
						finesRevObj.netPriceUSD = priceUSD
						finesRevObj.netPriceCAD = netPriceCAD
						finesRevObj.plantProductRevenue = tempRevenue
						finesRevObj.dateAdded = currTime
					else:
						finesRevObj = tblRevenue(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch, sellingPrice=constant2,
							netPriceUSD=priceUSD, netPriceCAD=netPriceCAD, plantProductRevenue=tempRevenue, dateAdded=currTime, date=calcDate)
					finesRevObj.save()

				if 3 in PPIDs:
					# constant2 = priceEntry.HGUltraFines - sumUltraFinesPen
					constant2 = priceEntry.ultraFines - sumUltraFinesPen
					# constant1 = (wmtHighGrade + wmtLowGrade)*inputsEntry.ultraFinesRecovery/100*(1-inputsEntry.ultraFinesMoisture/100)
					constant1 = sumTonnage*inputsEntry.ultraFinesRecovery/100*(1-inputsEntry.ultraFinesMoisture/100)
					priceUSD = Decimal(constant2) - Decimal(OPEXEntry.shipping)
					netPriceCAD = Decimal(priceUSD) / Decimal(inputsEntry.exchangeRate)					
					plantProductRevenue = (Decimal(ultraFinesTonnageDMT) * (Decimal(constant2) - Decimal(OPEXEntry.shipping))) / Decimal(inputsEntry.exchangeRate)
					if calcDateExists:
						ultraFinesRevObj = tblRevenue.objects.filter(mineID=int(mineID), year=year, plantProductID=3).order_by('-dateAdded')[0]
						ultraFinesRevObj.sellingPrice = constant2
						ultraFinesRevObj.netPriceUSD = priceUSD
						ultraFinesRevObj.netPriceCAD = netPriceCAD
						ultraFinesRevObj.plantProductRevenue = plantProductRevenue
					else:
						ultraFinesRevObj = tblRevenue(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch, sellingPrice=constant2,
							netPriceUSD=priceUSD, netPriceCAD=netPriceCAD, plantProductRevenue=plantProductRevenue, dateAdded=currTime, date=calcDate)
					ultraFinesRevObj.save()

				if calcDateExists:
					cashFlowEntry = tblCashFlow.objects.get(projectID=latestProject.projectID, date=calcDate)
					cashFlowEntry.processed = False
					cashFlowEntry.cashFlowPreTax = None
					cashFlowEntry.cashFlowPostTax = None
					cashFlowEntry.cumulativeCashFlowPreTax = None
					cashFlowEntry.cumulativeCashFlowPostTax = None
					cashFlowEntry.paybackPreTax = None
					cashFlowEntry.paybackPostTax = None
					cashFlowEntry.dateAdded = currTime
				else:
					cashFlowEntry = tblCashFlow(mineID=mineMatch, projectID=latestProject, cashFlowPreTax=None, cashFlowPostTax=None,
						cumulativeCashFlowPreTax=None, cumulativeCashFlowPostTax=None, paybackPreTax=None, paybackPostTax=None,
						date=calcDate, dateAdded=currTime, processed=False)
				cashFlowEntry.save()

				# if calcDateExists:
				# 	tblFinancials.objects.filter(projectID=latestProject.projectID, date=calcDate).delete()

				# discountRates = [6, 8, 10, 12, 15, 20]
				# for rate in discountRates:
				# 	financialsEntry = tblFinancials(projectID=latestProject.projectID, mineID=mineMatch, date=calcDate,
				# 		discountRate=rate, NPVPreTax=None, NPVPostTax=None, IRRPreTax=None, IRRPostTax=None, dateAdded=currTime)
				# 	financialsEntry.save()

				return render(request, 'mine/success.html', { }) #Redirect

			# Handle "Calculate Overwrite Values" here
			elif "overwrite" in request.POST:
				# hgInits = {}
				# lgInits = {}
				# wasteInits = {}
				gradesInit = {}
				# hgTonnageInit = None
				# lgTonnageInit = None
				# wasteInit = None
				# overburdenInit = None
				tonnagesInit = []
				# optimizedHGTonnage = None
				# optimizedLGTonnage = None
				optimizedTonnages = []
				optimizedIntermediates = {}
				optimizedLumpGrades = {}
				optimizedLumpPens = {}
				optimizedFinesGrades = {}
				optimizedFinesPens = {}
				optimizedUltraFinesGrades = {}
				optimizedUltraFinesPens = {}
				optimizedRejectsGrades = {}
				optimizedRejectsPens = {}
				calcDateStr = request.POST.get('calcDate', '')
				year = int(request.POST.get('year', ''))

				# if 1 in MPIDs:
				# 	hgTonnageInit = float(request.POST.get('highGradeTonnage', ''))
				# 	optimizedHGTonnage = float(request.POST.get('wmtHighGrade', ''))
				# 	for ID in commIDs:
				# 		hgInits[ID] = float(request.POST.get('highGrade{0}'.format(ID), ''))
				# if 2 in MPIDs:
				# 	lgTonnageInit = float(request.POST.get('lowGradeTonnage', ''))
				# 	optimizedLGTonnage = float(request.POST.get('wmtLowGrade', ''))
				# 	for ID in commIDs:
				# 		lgInits[ID] = float(request.POST.get('lowGrade{0}'.format(ID), ''))
				# if 3 in MPIDs:
				# 	wasteInit = float(request.POST.get('waste', ''))
				# 	for ID in commIDs:
				# 		wasteInits[ID] = float(request.POST.get('waste{0}'.format(ID), ''))
				# if 4 in MPIDs:
				# 	overburdenInit = float(request.POST.get('overburden', ''))

				for curr in range(1, numStockpiles+1):
					tonnagesInit.append(float(request.POST.get("stockpile{0}Tonnage".format(curr), '')))
					optimizedTonnages.append(float(request.POST.get("wmtStockpile{0}".format(curr), '')))

					tempGrades = {}
					for ID in commIDs:
						tempGrades[ID] = float(request.POST.get('stockpile{0}{1}'.format(curr, ID), ''))
					gradesInit[curr] = tempGrades

				for ID in commIDs:
					optimizedIntermediates[ID] = float(request.POST.get("intermediateGrade{0}".format(ID), ''))
					if 1 in PPIDs:
						optimizedLumpGrades[ID] = float(request.POST.get("lumpGrade{0}".format(ID), ''))
						optimizedLumpPens[ID] = float(request.POST.get("lumpPen{0}".format(ID), ''))
					if 2 in PPIDs:
						optimizedFinesGrades[ID] = float(request.POST.get("finesGrade{0}".format(ID), ''))
						optimizedFinesPens[ID] = float(request.POST.get("finesPen{0}".format(ID), ''))
					if 3 in PPIDs:
						optimizedUltraFinesGrades[ID] = float(request.POST.get("ultraFinesGrade{0}".format(ID), ''))
						optimizedUltraFinesPens[ID] = float(request.POST.get("ultraFinesPen{0}".format(ID), ''))
					if 4 in PPIDs:
						optimizedRejectsGrades[ID] = float(request.POST.get("rejectsGrade{0}".format(ID), ''))
						optimizedRejectsPens[ID] = float(request.POST.get("rejectsPen{0}".format(ID), ''))

				# for curr in range(1, numStockpiles+1):
				# 	tonnagesInit.append(float(request.POST.get('stockpile{0}Tonnage'.format(curr), '')))

				# 	tempGrades = {}
				# 	for ID in commIDs:
				# 		tempGrades[ID] = float(request.POST.get('stockpile{0}{1}'.format(curr, ID), ''))
				# 	gradesInit[curr] = tempGrades

				OWTonnages = []
				OWLumpGrades = {}
				OWFinesGrades = {}
				OWUltraFinesGrades = {}
				OWRejectsGrades = {}
				OWLumpPens = {}
				OWFinesPens = {}
				OWUltraFinesPens = {}
				OWRejectsPens = {}
				latestInputEntry = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				latestSmelterEntry = tblSmelterTerms.objects.filter(mineID=int(mineID), commodityID=commIDs[0]).order_by('-dateAdded')[0]
				smelterTimestamp = latestSmelterEntry.dateAdded
				
				for curr in range(1, numStockpiles+1):
					OWTonnages.append(float(request.POST.get("wmtStockpile{0}OW".format(curr), '')))

				# if 1 in MPIDs:
				# 	OWHGTonnage = float(request.POST.get('wmtHighGradeOW', ''))
				# 	for ID in commIDs:
				# 		hgInits[ID] = float(request.POST.get('highGrade{0}'.format(ID), ''))
				# else:
				# 	OWHGTonnage = 0.0

				# if 2 in MPIDs:
				# 	OWLGTonnage = float(request.POST.get('wmtLowGradeOW', ''))
				# 	for ID in commIDs:
				# 		lgInits[ID] = float(request.POST.get('lowGrade{0}'.format(ID), ''))
				# else:
				# 	OWLGTonnage = 0.0

				# Calculate the Overwrite Intermediate Grades
				OWIntermediates = {}
				for ID in commIDs:
					numerators = []
					for curr in range(1, numStockpiles+1):
						numerators.append(OWTonnages[curr-1]*gradesInit[curr][ID])
					OWIntermediates[ID] = sum(numerators) / sum(OWTonnages)

				# OWIntermediates = {}
				# for ID in commIDs:
				# 	if 1 in MPIDs:
				# 		numerator1 = OWHGTonnage*hgInits[ID]
				# 	else:
				# 		numerator1 = 0.0	

				# 	if 2 in MPIDs:
				# 		numerator2 = OWLGTonnage*lgInits[ID]
				# 	else:
				# 		numerator2 = 0.0
				# 	OWIntermediates[ID] = (numerator1 + numerator2) / (OWHGTonnage + OWLGTonnage)


				if 1 in PPIDs:
					constant1 = (latestInputEntry.lumpGrade/100.0) * (latestInputEntry.lumpRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.lumpRecovery/100.0)

					for ID in commIDs:
						OWLumpGrades[ID] = constant1 * constant2 * OWIntermediates[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						if OWLumpGrades[ID] >= smelterEntry.maxGrade:
							OWLumpPens[ID] = (-1)*(smelterEntry.maxGrade - OWLumpGrades[ID])*smelterEntry.premium
						elif OWLumpGrades[ID] >= smelterEntry.minGrade:
							OWLumpPens[ID] = (OWLumpGrades[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty
						else:
							OWLumpPens[ID] = (smelterEntry.minGrade - OWLumpGrades[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty

						# smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
						# if OWLumpGrades[ID] >= smelterEntry.HGMaxGrade:
						# 	OWLumpPens[ID] = (-1)*(smelterEntry.HGMaxGrade - OWLumpGrades[ID])*smelterEntry.HGPremium
						# elif OWLumpGrades[ID] >= smelterEntry.HGMinGrade:
						# 	OWLumpPens[ID] = (OWLumpGrades[ID] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
						# else:
						# 	OWLumpPens[ID] = (smelterEntry.HGMinGrade - OWLumpGrades[ID])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty

				if 2 in PPIDs:
					constant1 = (latestInputEntry.finesGrade/100.0) * (latestInputEntry.finesRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.finesRecovery/100.0)

					for ID in commIDs:
						OWFinesGrades[ID] = constant1 * constant2 * OWIntermediates[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						if OWFinesGrades[ID] >= smelterEntry.maxGrade:
							OWFinesPens[ID] = (-1)*(smelterEntry.maxGrade - OWFinesGrades[ID])*smelterEntry.premium
						elif OWFinesGrades[ID] >= smelterEntry.minGrade:
							OWFinesPens[ID] = (OWFinesGrades[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty
						else:
							OWFinesPens[ID] = (smelterEntry.minGrade - OWFinesGrades[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty

					# for ID in commIDs:
					# 	OWFinesGrades[ID] = constant1 * constant2 * OWIntermediates[ID]

					# 	smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
					# 	if OWFinesGrades[ID] >= smelterEntry.HGMaxGrade:
					# 		OWFinesPens[ID] = (-1)*(smelterEntry.HGMaxGrade - OWFinesGrades[ID])*smelterEntry.HGPremium
					# 	elif OWFinesGrades[ID] >= smelterEntry.HGMinGrade:
					# 		OWFinesPens[ID] = (OWFinesGrades[ID] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
					# 	else:
					# 		OWFinesPens[ID] = (smelterEntry.HGMinGrade - OWFinesGrades[ID])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty

				if 3 in PPIDs:
					constant1 = (latestInputEntry.ultraFinesGrade/100.0) * (latestInputEntry.ultraFinesRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.ultraFinesRecovery/100.0)

					for ID in commIDs:
						OWUltraFinesGrades[ID] = constant1 * constant2 * OWIntermediates[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						if OWUltraFinesGrades[ID] >= smelterEntry.maxGrade:
							OWUltraFinesPens[ID] = (-1)*(smelterEntry.maxGrade - OWUltraFinesGrades[ID])*smelterEntry.premium
						elif OWUltraFinesGrades[ID] >= smelterEntry.minGrade:
							OWUltraFinesPens[ID] = (OWUltraFinesGrades[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty
						else:
							OWUltraFinesPens[ID] = (smelterEntry.minGrade - OWUltraFinesGrades[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty

					# for ID in commIDs:
					# 	OWUltraFinesGrades[ID] = constant1 * constant2 * OWIntermediates[ID]

					# 	smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
					# 	if OWUltraFinesGrades[ID] >= smelterEntry.HGMaxGrade:
					# 		OWUltraFinesPens[ID] = (-1)*(smelterEntry.HGMaxGrade - OWUltraFinesGrades[ID])*smelterEntry.HGPremium
					# 	elif OWUltraFinesGrades[ID] >= smelterEntry.HGMinGrade:
					# 		OWUltraFinesPens[ID] = (OWUltraFinesGrades[ID] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
					# 	else:
					# 		OWUltraFinesPens[ID] = (smelterEntry.HGMinGrade - OWUltraFinesGrades[ID])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty

				if 4 in PPIDs:
					constant1 = (latestInputEntry.rejectsGrade/100.0) * (latestInputEntry.rejectsRecovery/100.0) / (latestInputEntry.avgCommodity1Grade/100.0)
					constant2 = 1.0 / (latestInputEntry.rejectsRecovery/100.0)

					for ID in commIDs:
						OWRejectsGrades[ID] = constant1 * constant2 * OWIntermediates[ID]
						smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), stockpileID=1,
							commodityID=ID, projectID=latestProject.projectID)
						if OWRejectsGrades[ID] >= smelterEntry.maxGrade:
							OWRejectsPens[ID] = (-1)*(smelterEntry.maxGrade - OWRejectsGrades[ID])*smelterEntry.premium
						elif OWRejectsGrades[ID] >= smelterEntry.minGrade:
							OWRejectsPens[ID] = (OWRejectsGrades[ID] - smelterEntry.minGrade)*smelterEntry.minMaxPenalty
						else:
							OWRejectsPens[ID] = (smelterEntry.minGrade - OWRejectsGrades[ID])*smelterEntry.minPenalty + (smelterEntry.maxGrade - smelterEntry.minGrade)*smelterEntry.minMaxPenalty

					# for ID in commIDs:
					# 	OWRejectsGrades[ID] = constant1 * constant2 * OWIntermediates[ID]

					# 	smelterEntry = tblSmelterTerms.objects.get(mineID=int(mineID), commodityID=ID, dateAdded=smelterTimestamp)
					# 	if OWRejectsGrades[ID] >= smelterEntry.HGMaxGrade:
					# 		OWRejectsPens[ID] = (-1)*(smelterEntry.HGMaxGrade - OWRejectsGrades[ID])*smelterEntry.HGPremium
					# 	elif OWRejectsGrades[ID] >= smelterEntry.HGMinGrade:
					# 		OWRejectsPens[ID] = (OWRejectsGrades[ID] - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty
					# 	else:
					# 		OWRejectsPens[ID] = (smelterEntry.HGMinGrade - OWRejectsGrades[ID])*smelterEntry.HGMinPenalty + (smelterEntry.HGMaxGrade - smelterEntry.HGMinGrade)*smelterEntry.HGMinMaxPenalty

				next_form_class = MineProductForm(mineID=mineID, calculated=True, lumpGrades=optimizedLumpGrades, lumpPens=optimizedLumpPens,
					finesGrades=optimizedFinesGrades, finesPens=optimizedFinesPens, intermediates=optimizedIntermediates,
					ultraFinesGrades=optimizedUltraFinesGrades, ultraFinesPens=optimizedUltraFinesPens,
					rejectsGrades=optimizedRejectsGrades, rejectsPens=optimizedRejectsPens,
					optimizedTonnages=optimizedTonnages, tonnagesInit=tonnagesInit,
					gradesInit=gradesInit, calcDateStr=calcDateStr, year=year,
					overwrite=True, OWTonnagesInit=OWTonnages,
					# hgTonnage=optimizedHGTonnage, lgTonnage=optimizedLGTonnage,
					# hgTonnageInit=hgTonnageInit, lgTonnageInit=lgTonnageInit,
					# wasteInit=wasteInit, overburdenInit=overburdenInit,
					# hgInits=hgInits, lgInits=lgInits, wasteInits=wasteInits, calcDateStr=calcDateStr, year=year,
					# overwrite=True, OWHGTonnageInit=OWHGTonnage, OWLGTonnageInit=OWLGTonnage,
					OWIntermediates=OWIntermediates, OWLumpGrades=OWLumpGrades, OWLumpPens=OWLumpPens,
					OWFinesGrades=OWFinesGrades, OWFinesPens=OWFinesPens,
					OWUltraFinesGrades=OWUltraFinesGrades, OWUltraFinesPens=OWUltraFinesPens,
					OWRejectsGrades=OWRejectsGrades, OWRejectsPens=OWRejectsPens)
				return render(request, 'mine/mineproduct.html', {'form': next_form_class,
					'calculated': True, 'overwrite': True})

			# Handle "Accept Overwrite Values" here
			elif "acceptOverwrite" in request.POST:
				calcDateStr = request.POST.get('calcDate', '')
				calcDate = datetime.datetime.strptime(calcDateStr, "%Y-%m-%d").date()

				# if 1 in MPIDs:
				# 	wmtHighGradeOW = float(request.POST.get('wmtHighGradeOW', ''))
				# 	HGMPMatch = tblMineProductList.objects.get(mineProductID=1)
				# if 2 in MPIDs:
				# 	wmtLowGradeOW = float(request.POST.get('wmtLowGradeOW', ''))
				# 	LGMPMatch = tblMineProductList.objects.get(mineProductID=2)
				# if 3 in MPIDs:
				# 	wasteMPMatch = tblMineProductList.objects.get(mineProductID=3)
				# if 4 in MPIDs:
				# 	overburdenMPMatch = tblMineProductList.objects.get(mineProductID=4)

				commMatches = {}
				for ID in commIDs:
					commMatches[ID] = tblCommodityList.objects.get(commodityID=ID)

				if 1 in PPIDs:
					lumpPPMatch = tblPlantProductList.objects.get(plantProductID=1)
				if 2 in PPIDs:
					finesPPMatch = tblPlantProductList.objects.get(plantProductID=2)
				if 3 in PPIDs:
					ultraFinesPPMatch = tblPlantProductList.objects.get(plantProductID=3)
				if 4 in PPIDs:
					rejectsPPMatch = tblPlantProductList.objects.get(plantProductID=4)

				currTime = timezone.localtime(timezone.now())

				calcDateExists = False
				testEntry = tblMineProductTonnageOptimized.objects.filter(projectID=latestProject.projectID, date=calcDate)
				if testEntry:
					calcDateExists = True


				# Step 29: Find the tblMineProductTonnageOptimized entries and update tonnage values
				for curr in range(1, numStockpiles+1):
					if calcDateExists:
						currEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, stockpileID=curr, date=calcDate)
						currEntry.tonnage = float(request.POST.get("wmtStockpile{0}OW".format(curr), ''))
						currEntry.optimized = False
						currEntry.dateAdded = currTime
					else:
						currEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, stockpileID=curr,
							tonnage=float(request.POST.get("wmtStockpile{0}OW".format(curr), '')), date=calcDate, optimized=False, dateAdded=currTime)
					currEntry.save()


				# # Step 29: Find the tblMineProductTonnageOptimized entries and update tonnage values
				# if 1 in MPIDs:
				# 	if calcDateExists:
				# 		HGTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=1, date=calcDate)
				# 		HGTonnageEntry.tonnage = wmtHighGradeOW
				# 		HGTonnageEntry.optimized = False
				# 		HGTonnageEntry.dateAdded = currTime
				# 	else:
				# 		HGTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=HGMPMatch,
				# 			tonnage=wmtHighGradeOW, date=calcDate, optimized=False, dateAdded=currTime)
				# 	HGTonnageEntry.save()

				# if 2 in MPIDs:
				# 	if calcDateExists:
				# 		LGTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=2, date=calcDate)
				# 		LGTonnageEntry.tonnage = wmtLowGradeOW
				# 		LGTonnageEntry.optimized = False
				# 		LGTonnageEntry.dateAdded = currTime
				# 	else:
				# 		LGTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=LGMPMatch,
				# 			tonnage=wmtLowGradeOW, date=calcDate, optimized=False, dateAdded=currTime)
				# 	LGTonnageEntry.save()

				# if 3 in MPIDs:
				# 	if calcDateExists:
				# 		wasteTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=3, date=calcDate)
				# 		wasteTonnageEntry.optimized = False
				# 		wasteTonnageEntry.dateAdded = currTime
				# 	else:
				# 		wasteTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=wasteMPMatch,
				# 			tonnage=None, date=calcDate, optimized=False, dateAdded=currTime)
				# 	wasteTonnageEntry.save()

				# if 4 in MPIDs:
				# 	if calcDateExists:
				# 		overburdenTonnageEntry = tblMineProductTonnageOptimized.objects.get(projectID=latestProject.projectID, mineProductID=4, date=calcDate)
				# 		overburdenTonnageEntry.optimized = False
				# 		overburdenTonnageEntry.dateAdded = currTime
				# 	else:
				# 		overburdenTonnageEntry = tblMineProductTonnageOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=overburdenMPMatch,
				# 			tonnage=None, date=calcDate, optimized=False, dateAdded=currTime)
				# 	overburdenTonnageEntry.save()


				# Find the tblMineProduct entries and update optimized flags
				# Find the tblPlantProduct entries and update grade values
				inputsEntry = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				for curr in range(1, numStockpiles+1):
					for ID in commIDs:
						if calcDateExists:
							currEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								stockpileID=curr, date=calcDate)
							currEntry.grade = request.POST.get('stockpile{0}{1}'.format(curr,ID), '')
							currEntry.optimized = False
							currEntry.dateAdded = currTime
						else:
							currEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, stockpileID=curr,
								commodityID=commMatches[ID], grade=request.POST.get('stockpile{0}{1}'.format(curr,ID), ''),
								date=calcDate, optimized=False, dateAdded=currTime)
						currEntry.save()

				# # Find the tblMineProduct entries and update optimized flags
				# # Find the tblPlantProduct entries and update grade values
				# inputsEntry = tblInputs.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				# for ID in commIDs:
				# 	commodityMatch = tblCommodityList.objects.get(commodityID=ID)
				# 	if 1 in MPIDs:
				# 		tempGrade = request.POST.get('highGrade{0}'.format(ID), '')
				# 		if calcDateExists:
				# 			HGMPEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
				# 				mineProductID=1, date=calcDate)
				# 			HGMPEntry.grade = tempGrade
				# 			HGMPEntry.optimized = False
				# 			HGMPEntry.dateAdded = currTime
				# 		else:
				# 			HGMPEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=HGMPMatch,
				# 				commodityID=commodityMatch, grade=tempGrade, date=calcDate, optimized=False, dateAdded=currTime)
				# 		HGMPEntry.save()

				# 	if 2 in MPIDs:
				# 		tempGrade = request.POST.get('lowGrade{0}'.format(ID), '')
				# 		if calcDateExists:
				# 			LGMPEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
				# 				mineProductID=2, date=calcDate)
				# 			LGMPEntry.grade = tempGrade
				# 			LGMPEntry.optimized = False
				# 			LGMPEntry.dateAdded = currTime
				# 		else:
				# 			LGMPEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=LGMPMatch,
				# 				commodityID=commodityMatch, grade=tempGrade, date=calcDate, optimized=False, dateAdded=currTime)
				# 		LGMPEntry.save()

				# 	if 3 in MPIDs:
				# 		tempGrade = request.POST.get('waste{0}'.format(ID), '')
				# 		if calcDateExists:
				# 			wasteMPEntry = tblMineProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
				# 				mineProductID=3, date=calcDate)
				# 			wasteMPEntry.grade = tempGrade
				# 			wasteMPEntry.optimized = False
				# 			wasteMPEntry.dateAdded = currTime
				# 		else:
				# 			wasteMPEntry = tblMineProductGradeOptimized(mineID=mineMatch, projectID=latestProject, mineProductID=wasteMPMatch,
				# 				commodityID=commodityMatch, grade=tempGrade, date=calcDate, optimized=False, dateAdded=currTime)
				# 		wasteMPEntry.save()

				for ID in commIDs:
					if 1 in PPIDs:
						lumpGrade = float(request.POST.get("OWLumpGrade{0}".format(ID), ''))
						if calcDateExists:
							HGPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=1, date=calcDate)
							HGPPEntry.grade = lumpGrade
							HGPPEntry.optimized = False
							HGPPEntry.dateAdded = currTime
						else:
							HGPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
								commodityID=commMatches[ID], grade=lumpGrade, date=calcDate, dateAdded=currTime, optimized=False)
						HGPPEntry.save()
					else:
						lumpGrade = 0.0

					if 2 in PPIDs:
						finesGrade = float(request.POST.get("OWFinesGrade{0}".format(ID), ''))
						if calcDateExists:
							LGPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=2, date=calcDate)
							LGPPEntry.grade = finesGrade
							LGPPEntry.optimized = False
							LGPPEntry.dateAdded = currTime
						else:
							LGPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
								commodityID=commMatches[ID], grade=finesGrade, date=calcDate, dateAdded=currTime, optimized=False)
						LGPPEntry.save()
					else:
						finesGrade = 0.0

					# Update Ultra Fines if it has been declared
					if 3 in PPIDs:
						ultraFinesGrade = float(request.POST.get("OWUltraFinesGrade{0}".format(ID), ''))
						if calcDateExists:
							UFPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=3, date=calcDate)
							UFPPEntry.grade = ultraFinesGrade
							UFPPEntry.optimized = False
							UFPPEntry.dateAdded = currTime
						else:
							UFPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
								commodityID=commMatches[ID], grade=ultraFinesGrade, date=calcDate, dateAdded=currTime, optimized=False)
						UFPPEntry.save()

					# Update Rejects if it has been declared
					if 4 in PPIDs:
						rejectsGrade = float(request.POST.get("OWRejectsGrade{0}".format(ID), ''))
						if calcDateExists:
							RPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=4, date=calcDate)
							RPPEntry.grade = rejectsGrade
							RPPEntry.optimized = False
							RPPEntry.dateAdded = currTime
						else:
							RPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=rejectsPPMatch,
								commodityID=commMatches[ID], grade=rejectsGrade, date=calcDate, dateAdded=currTime, optimized=False)
						RPPEntry.save()

					# if 1 in PPIDs:
					# 	lumpGrade = float(request.POST.get("OWLumpGrade{0}".format(ID), ''))
					# 	if calcDateExists:
					# 		HGPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
					# 			plantProductID=1, date=calcDate)
					# 		HGPPEntry.grade = lumpGrade
					# 		HGPPEntry.optimized = False
					# 		HGPPEntry.dateAdded = currTime
					# 	else:
					# 		HGPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
					# 			commodityID=commodityMatch, grade=lumpGrade, date=calcDate, dateAdded=currTime, optimized=False)
					# 	HGPPEntry.save()
					# else:
					# 	lumpGrade = 0.0

					# if 2 in PPIDs:
					# 	finesGrade = float(request.POST.get("OWFinesGrade{0}".format(ID), ''))
					# 	if calcDateExists:
					# 		LGPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
					# 			plantProductID=2, date=calcDate)
					# 		LGPPEntry.grade = finesGrade
					# 		LGPPEntry.optimized = False
					# 		LGPPEntry.dateAdded = currTime
					# 	else:
					# 		LGPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
					# 			commodityID=commodityMatch, grade=finesGrade, date=calcDate, dateAdded=currTime, optimized=False)
					# 	LGPPEntry.save()
					# else:
					# 	finesGrade = 0.0

					# # Update Ultra Fines if it has been declared
					# if 3 in PPIDs:
					# 	ultraFinesGrade = float(request.POST.get("OWUltraFinesGrade{0}".format(ID), ''))
					# 	if calcDateExists:
					# 		UFPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
					# 			plantProductID=3, date=calcDate)
					# 		UFPPEntry.grade = ultraFinesGrade
					# 		UFPPEntry.optimized = False
					# 		UFPPEntry.dateAdded = currTime
					# 	else:
					# 		UFPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
					# 			commodityID=commodityMatch, grade=ultraFinesGrade, date=calcDate, dateAdded=currTime, optimized=False)
					# 	UFPPEntry.save()

					# # Update Rejects if it has been declared
					# if 4 in PPIDs:
					# 	rejectsGrade = float(request.POST.get("OWRejectsGrade{0}".format(ID), ''))
					# 	if calcDateExists:
					# 		RPPEntry = tblPlantProductGradeOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
					# 			plantProductID=4, date=calcDate)
					# 		RPPEntry.grade = rejectsGrade
					# 		RPPEntry.optimized = False
					# 		RPPEntry.dateAdded = currTime
					# 	else:
					# 		RPPEntry = tblPlantProductGradeOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=rejectsPPMatch,
					# 			commodityID=commodityMatch, grade=rejectsGrade, date=calcDate, dateAdded=currTime, optimized=False)
					# 	RPPEntry.save()


				sumTonnage = 0.0
				for curr in range(1, numStockpiles+1):
					sumTonnage += float(request.POST.get("wmtStockpile{0}".format(curr), ''))
				# Find the Plant Product Tonnage entries and update tonnage values
				if 1 in PPIDs:
					lumpTonnageWMT = sumTonnage*inputsEntry.lumpRecovery/100
					lumpTonnageDMT = sumTonnage*inputsEntry.lumpRecovery/100*(1-inputsEntry.lumpMoisture/100)
					if calcDateExists:
						PPTLumpEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=1, date=calcDate)
						PPTLumpEntry.tonnageWMT = lumpTonnageWMT
						PPTLumpEntry.tonnageDMT = lumpTonnageDMT
						PPTLumpEntry.optimized = False
						PPTLumpEntry.dateAdded = currTime
					else:
						PPTLumpEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
							dateAdded=currTime, optimized=False, tonnageWMT=lumpTonnageWMT, tonnageDMT=lumpTonnageDMT, date=calcDate)
					PPTLumpEntry.save()

				if 2 in PPIDs:
					finesTonnageWMT = sumTonnage*inputsEntry.finesRecovery/100
					finesTonnageDMT = sumTonnage*inputsEntry.finesRecovery/100*(1-inputsEntry.finesMoisture/100)
					if calcDateExists:
						PPTFinesEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=2, date=calcDate)
						PPTFinesEntry.tonnageWMT = finesTonnageWMT
						PPTFinesEntry.tonnageDMT = finesTonnageDMT
						PPTFinesEntry.optimized = False
						PPTFinesEntry.dateAdded = currTime
					else:
						PPTFinesEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
							dateAdded=currTime, optimized=False, tonnageWMT=finesTonnageWMT, tonnageDMT=finesTonnageDMT, date=calcDate)
					PPTFinesEntry.save()

				# Update Ultra Fines Tonnage if it has been declared
				if 3 in PPIDs:
					ultraFinesTonnageWMT = sumTonnage*inputsEntry.ultraFinesRecovery/100
					ultraFinesTonnageDMT = sumTonnage*inputsEntry.ultraFinesRecovery/100*(1-inputsEntry.ultraFinesMoisture/100)
					if calcDateExists:
						PPTUltraFinesEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=3, date=calcDate)
						PPTUltraFinesEntry.tonnageWMT = ultraFinesTonnageWMT
						PPTUltraFinesEntry.tonnageDMT = ultraFinesTonnageDMT
						PPTUltraFinesEntry.optimized = False
						PPTUltraFinesEntry.dateAdded = currTime
					else:
						PPTUltraFinesEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
							dateAdded=currTime, optimized=False, tonnageWMT=ultraFinesTonnageWMT, tonnageDMT=ultraFinesTonnageDMT, date=calcDate)
					PPTUltraFinesEntry.save()

				# Update Rejects Tonnage if it has been declared
				if 4 in PPIDs:
					rejectsTonnageWMT = sumTonnage*inputsEntry.rejectsRecovery/100
					rejectsTonnageDMT = sumTonnage*inputsEntry.rejectsRecovery/100*(1-inputsEntry.rejectsMoisture/100)
					if calcDateExists:
						PPTRejectsEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=4, date=calcDate)
						PPTRejectsEntry.tonnageWMT = rejectsTonnageWMT
						PPTRejectsEntry.tonnageDMT = rejectsTonnageDMT
						PPTRejectsEntry.optimized = False
						PPTRejectsEntry.dateAdded = currTime
					else:
						PPTRejectsEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=rejectsPPMatch,
							dateAdded=currTime, optimized=False, tonnageWMT=rejectsTonnageWMT, tonnageDMT=rejectsTonnageDMT, date=calcDate)
					PPTRejectsEntry.save()

				# # Find the Plant Product Tonnage entries and update tonnage values
				# if 1 in PPIDs:
				# 	lumpTonnageWMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.lumpRecovery/100
				# 	lumpTonnageDMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.lumpRecovery/100*(1-inputsEntry.lumpMoisture/100)
				# 	if calcDateExists:
				# 		PPTLumpEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=1, date=calcDate)
				# 		PPTLumpEntry.tonnageWMT = lumpTonnageWMT
				# 		PPTLumpEntry.tonnageDMT = lumpTonnageDMT
				# 		PPTLumpEntry.optimized = False
				# 		PPTLumpEntry.dateAdded = currTime
				# 	else:
				# 		PPTLumpEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
				# 			dateAdded=currTime, optimized=False, tonnageWMT=lumpTonnageWMT, tonnageDMT=lumpTonnageDMT, date=calcDate)
				# 	PPTLumpEntry.save()

				# if 2 in PPIDs:
				# 	finesTonnageWMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.finesRecovery/100
				# 	finesTonnageDMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.finesRecovery/100*(1-inputsEntry.finesMoisture/100)
				# 	if calcDateExists:
				# 		PPTFinesEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=2, date=calcDate)
				# 		PPTFinesEntry.tonnageWMT = finesTonnageWMT
				# 		PPTFinesEntry.tonnageDMT = finesTonnageDMT
				# 		PPTFinesEntry.optimized = False
				# 		PPTFinesEntry.dateAdded = currTime
				# 	else:
				# 		PPTFinesEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
				# 			dateAdded=currTime, optimized=False, tonnageWMT=finesTonnageWMT, tonnageDMT=finesTonnageDMT, date=calcDate)
				# 	PPTFinesEntry.save()

				# # Update Ultra Fines Tonnage if it has been declared
				# if 3 in PPIDs:
				# 	ultraFinesTonnageWMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.ultraFinesRecovery/100
				# 	ultraFinesTonnageDMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.ultraFinesRecovery/100*(1-inputsEntry.ultraFinesMoisture/100)
				# 	if calcDateExists:
				# 		PPTUltraFinesEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=3, date=calcDate)
				# 		PPTUltraFinesEntry.tonnageWMT = ultraFinesTonnageWMT
				# 		PPTUltraFinesEntry.tonnageDMT = ultraFinesTonnageDMT
				# 		PPTUltraFinesEntry.optimized = False
				# 		PPTUltraFinesEntry.dateAdded = currTime
				# 	else:
				# 		PPTUltraFinesEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
				# 			dateAdded=currTime, optimized=False, tonnageWMT=ultraFinesTonnageWMT, tonnageDMT=ultraFinesTonnageDMT, date=calcDate)
				# 	PPTUltraFinesEntry.save()

				# # Update Rejects Tonnage if it has been declared
				# if 4 in PPIDs:
				# 	rejectsTonnageWMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.rejectsRecovery/100
				# 	rejectsTonnageDMT = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.rejectsRecovery/100*(1-inputsEntry.rejectsMoisture/100)
				# 	if calcDateExists:
				# 		PPTRejectsEntry = tblPlantProductTonnage.objects.get(projectID=latestProject.projectID, plantProductID=4, date=calcDate)
				# 		PPTRejectsEntry.tonnageWMT = rejectsTonnageWMT
				# 		PPTRejectsEntry.tonnageDMT = rejectsTonnageDMT
				# 		PPTRejectsEntry.optimized = False
				# 		PPTRejectsEntry.dateAdded = currTime
				# 	else:
				# 		PPTRejectsEntry = tblPlantProductTonnage(mineID=mineMatch, projectID=latestProject, plantProductID=rejectsPPMatch,
				# 			dateAdded=currTime, optimized=False, tonnageWMT=rejectsTonnageWMT, tonnageDMT=rejectsTonnageDMT, date=calcDate)
				# 	PPTRejectsEntry.save()


				sumLumpPen = 0
				sumFinesPen = 0
				sumUltraFinesPen = 0
				# Step 34: tblSmelterTermsOptimized Updates
				for ID in commIDs:
					commodityMatch = tblCommodityList.objects.get(commodityID=ID)
					if 1 in PPIDs:
						currPen = float(request.POST.get("OWLumpPen{0}".format(ID), ''))
						sumLumpPen += currPen
						if calcDateExists:
							lumpPenObj = tblSmelterTermsOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=1, date=calcDate)						
							lumpPenObj.penalty = currPen
							lumpPenObj.optimized = False
							lumpPenObj.dateAdded = currTime
						else:
							lumpPenObj = tblSmelterTermsOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch,
								commodityID=commodityMatch, penalty=currPen, date=calcDate, optimized=False, dateAdded=currTime)
						lumpPenObj.save()                                

					if 2 in PPIDs:
						currPen = float(request.POST.get("OWFinesPen{0}".format(ID), ''))
						sumFinesPen += currPen
						if calcDateExists:
							finesPenObj = tblSmelterTermsOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=2, date=calcDate)							
							finesPenObj.penalty = currPen
							finesPenObj.optimized = False
							finesPenObj.dateAdded = currTime
						else:
							finesPenObj = tblSmelterTermsOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch,
								commodityID=commodityMatch, penalty=currPen, date=calcDate, optimized=False, dateAdded=currTime)
						finesPenObj.save()

					# Update Ultra Fines Penalty values if declared
					if 3 in PPIDs:
						currPen = float(request.POST.get("OWUltraFinesPen{0}".format(ID), ''))
						sumUltraFinesPen += currPen
						if calcDateExists:
							ultraFinesPenObj = tblSmelterTermsOptimized.objects.get(projectID=latestProject.projectID, commodityID=ID,
								plantProductID=3, date=calcDate)							
							ultraFinesPenObj.penalty = currPen
							ultraFinesPenObj.optimized = False
							ultraFinesPenObj.dateAdded = currTime
						else:
							ultraFinesPenObj = tblSmelterTermsOptimized(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch,
								commodityID=commodityMatch, penalty=currPen, date=calcDate, optimized=False, dateAdded=currTime)
						ultraFinesPenObj.save()


				# Get year entry from hidden field in mine form
				year = int(request.POST.get('year', ''))
				# year = 1
				# Step 35: tblRevenue Updates
				# Obtain tblPrice entry
				# priceEntry = tblPrice.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
				priceEntry = tblPrice.objects.get(projectID=latestProject.projectID, stockpileID=1)
				OPEXEntry = tblOPEX.objects.filter(mineID=int(mineID), year=year).order_by('-dateAdded')[0]
				CAPEXEntry = tblCAPEX.objects.filter(mineID=int(mineID), year=year).order_by('-dateAdded')[0]

				sumRevenue = 0
				# HGLump = priceEntry.HGLump
				if 1 in PPIDs:
					# constant2 = priceEntry.HGLump - sumLumpPen
					constant2 = priceEntry.lump - sumLumpPen
					# constant1 = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.lumpRecovery/100*(1-inputsEntry.lumpMoisture/100)
					constant1 = sumTonnage*inputsEntry.lumpRecovery/100*(1-inputsEntry.lumpMoisture/100)
					priceUSD = Decimal(constant2) - Decimal(OPEXEntry.shipping)					
					netPriceCAD = Decimal(priceUSD) / Decimal(inputsEntry.exchangeRate)
					tempRevenue = (Decimal(lumpTonnageDMT) * (Decimal(constant2) - Decimal(OPEXEntry.shipping))) / Decimal(inputsEntry.exchangeRate)				
					sumRevenue += tempRevenue

					if calcDateExists:
						lumpRevObj = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=1, date=calcDate)
						lumpRevObj.sellingPrice = constant2
						lumpRevObj.netPriceUSD = priceUSD
						lumpRevObj.netPriceCAD = netPriceCAD
						lumpRevObj.plantProductRevenue = tempRevenue
						lumpRevObj.dateAdded = currTime
					else:
						lumpRevObj = tblRevenue(mineID=mineMatch, projectID=latestProject, plantProductID=lumpPPMatch, sellingPrice=constant2,
							netPriceUSD=priceUSD, netPriceCAD=netPriceCAD, plantProductRevenue=tempRevenue, dateAdded=currTime, date=calcDate)
					lumpRevObj.save()

				if 2 in PPIDs:
					# constant2 = priceEntry.HGFines - sumFinesPen
					constant2 = priceEntry.fines - sumFinesPen
					# constant1 = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.finesRecovery/100*(1-inputsEntry.finesMoisture/100)
					constant1 = sumTonnage*inputsEntry.finesRecovery/100*(1-inputsEntry.finesMoisture/100)
					priceUSD = Decimal(constant2) - Decimal(OPEXEntry.shipping)					
					netPriceCAD = Decimal(priceUSD) / Decimal(inputsEntry.exchangeRate)
					tempRevenue = (Decimal(finesTonnageDMT) * (Decimal(constant2) - Decimal(OPEXEntry.shipping))) / Decimal(inputsEntry.exchangeRate)
					sumRevenue += tempRevenue

					if calcDateExists:
						finesRevObj = tblRevenue.objects.get(projectID=latestProject.projectID, plantProductID=2, date=calcDate)
						finesRevObj.sellingPrice = constant2
						finesRevObj.netPriceUSD = priceUSD
						finesRevObj.netPriceCAD = netPriceCAD
						finesRevObj.plantProductRevenue = tempRevenue
						finesRevObj.dateAdded = currTime
					else:
						finesRevObj = tblRevenue(mineID=mineMatch, projectID=latestProject, plantProductID=finesPPMatch, sellingPrice=constant2,
							netPriceUSD=priceUSD, netPriceCAD=netPriceCAD, plantProductRevenue=tempRevenue, dateAdded=currTime, date=calcDate)
					finesRevObj.save()

				if 3 in PPIDs:
					# constant2 = priceEntry.HGUltraFines - sumUltraFinesPen
					constant2 = priceEntry.ultraFines - sumUltraFinesPen
					# constant1 = (wmtHighGradeOW + wmtLowGradeOW)*inputsEntry.ultraFinesRecovery/100*(1-inputsEntry.ultraFinesMoisture/100)
					constant1 = sumTonnage*inputsEntry.ultraFinesRecovery/100*(1-inputsEntry.ultraFinesMoisture/100)
					priceUSD = Decimal(constant2) - Decimal(OPEXEntry.shipping)
					netPriceCAD = Decimal(priceUSD) / Decimal(inputsEntry.exchangeRate)					
					plantProductRevenue = (Decimal(ultraFinesTonnageDMT) * (Decimal(constant2) - Decimal(OPEXEntry.shipping))) / Decimal(inputsEntry.exchangeRate)
					if calcDateExists:
						ultraFinesRevObj = tblRevenue.objects.filter(mineID=int(mineID), year=year, plantProductID=3).order_by('-dateAdded')[0]
						ultraFinesRevObj.sellingPrice = constant2
						ultraFinesRevObj.netPriceUSD = priceUSD
						ultraFinesRevObj.netPriceCAD = netPriceCAD
						ultraFinesRevObj.plantProductRevenue = plantProductRevenue
					else:
						ultraFinesRevObj = tblRevenue(mineID=mineMatch, projectID=latestProject, plantProductID=ultraFinesPPMatch, sellingPrice=constant2,
							netPriceUSD=priceUSD, netPriceCAD=netPriceCAD, plantProductRevenue=plantProductRevenue, dateAdded=currTime, date=calcDate)
					ultraFinesRevObj.save()

				if calcDateExists:
					cashFlowEntry = tblCashFlow.objects.get(projectID=latestProject.projectID, date=calcDate)
					cashFlowEntry.processed = False
					cashFlowEntry.cashFlowPreTax = None
					cashFlowEntry.cashFlowPostTax = None
					cashFlowEntry.cumulativeCashFlowPreTax = None
					cashFlowEntry.cumulativeCashFlowPostTax = None
					cashFlowEntry.paybackPreTax = None
					cashFlowEntry.paybackPostTax = None
					cashFlowEntry.dateAdded = currTime
				else:
					cashFlowEntry = tblCashFlow(mineID=mineMatch, projectID=latestProject, cashFlowPreTax=None, cashFlowPostTax=None,
						cumulativeCashFlowPreTax=None, cumulativeCashFlowPostTax=None, paybackPreTax=None, paybackPostTax=None,
						date=calcDate, dateAdded=currTime, processed=False)
				cashFlowEntry.save()

				return render(request, 'mine/overwritesuccess.html', { }) #Redirect			
				
		return render(request,  "mine/mineproduct.html", {'form': form_class})

	else:
		form_class = MineProductForm(mineID=mineID)
		return render(request, "mine/mineproduct.html", {'form': form_class})
