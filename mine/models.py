from django.db import models

# Create your models here

class tblCommodityList(models.Model):
	commodityID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=5, null=False)
	commodityType = models.IntegerField(null=False)

	def __str__(self):
		return str(self.commodityID)

	class Meta:
		db_table = 'tblCommodityList'


class tblCommodity(models.Model):
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	dateAdded = models.DateTimeField()

	class Meta:
		db_table = 'tblCommodity'
		

class tblMineProductList(models.Model):
	mineProductID = models.AutoField(primary_key=True)
	mineProduct = models.CharField(max_length=30, null=False)

	class Meta:
		db_table = 'tblMineProductList'


class tblPlantProductList(models.Model):
	plantProductID = models.AutoField(primary_key=True)
	plantProduct = models.CharField(max_length=30, null=False)

	class Meta:
		db_table = 'tblPlantProductList'


class tblMine(models.Model):
	mineID = models.AutoField(primary_key=True)
	mine = models.CharField(max_length=100)
	address = models.CharField(max_length=250)
	city = models.CharField(max_length=100)
	province = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	postalCode = models.CharField(max_length=10)
	phone = models.CharField(max_length=32)
	dateAdded = models.DateTimeField(null=False)

	def __str__(self):
		return str(self.mineID)

	class Meta:
		db_table = 'tblMine'
		
		
class tblMineProduct(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	mineProductID = models.ForeignKey('tblMineProductList', db_column='mineProductID')
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	grade = models.DecimalField(max_digits=12, decimal_places=6, null=True)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblMineProduct'


class tblMineProductTonnage(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	mineProductID = models.ForeignKey('tblMineProductList', db_column='mineProductID')
	tonnage = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()
	
	class Meta:
		db_table = 'tblMineProductTonnage'

		
class tblPlantProduct(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	grade = models.DecimalField(max_digits=12, decimal_places=6, null=True)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblPlantProduct'
	
	
class tblPlantProductTonnage(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	tonnageWMT = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	tonnageDMT = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblPlantProductTonnage'


class tblSmelterTermsOptimized(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	penalty = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblSmelterTermsOptimized'
		unique_together = (("mineID", "commodityID", "plantProductID", "dateAdded"),)

		
class tblRevenue(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	dateAdded = models.DateTimeField(null=False)
	productRevenue = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	cashFlowPreTax = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	cumulativeCashFlowPreTax = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	paybackPreTax = models.DecimalField(max_digits=4, decimal_places=2, null=False)
	cashFlowAfterTax = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	cumulativeCashFlowAfterTax = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	paybackAfterTax = models.DecimalField(max_digits=4, decimal_places=2, null=False)
	optimized = models.BooleanField('tblMineProduct', db_column='optimized')
	
	class Meta:
		db_table = 'tblRevenue'


class tblFinancials(models.Model):
	financialsID = models.AutoField(primary_key=True)
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	dateAdded = models.DateTimeField(null=False)
	npvPreTax = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	npvAfterTax = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	irrPreTax = models.DecimalField(max_digits=4, decimal_places=2, null=False)
	irrAfterTax = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	optimized = models.BooleanField('tblMineProduct', db_column='optimized')
	
	class Meta:
		db_table = 'tblFinancials'


class tblPrice(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	#commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	HGLump = models.DecimalField(max_digits=12, decimal_places=2)
	HGLumpPrem = models.DecimalField(max_digits=12, decimal_places=2)
	HGFines = models.DecimalField(max_digits=12, decimal_places=2)
	HGUltraFines = models.DecimalField(max_digits=12, decimal_places=2)
	LGLump = models.DecimalField(max_digits=12, decimal_places=2)
	LGLumpPrem = models.DecimalField(max_digits=12, decimal_places=2)
	LGFines = models.DecimalField(max_digits=12, decimal_places=2)
	LGUltraFines = models.DecimalField(max_digits=12, decimal_places=2)
	HGLumpAvg = models.DecimalField(max_digits=12, decimal_places=2)
	LGLumpAvg = models.DecimalField(max_digits=12, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblPrice'
		#unique_together = (("mineID", "commodityID", "dateAdded"),)
		unique_together = (("mineID", "dateAdded"),)


class tblInputs(models.Model):
	inputID = models.AutoField(primary_key=True)
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	Fe2O3Iron = models.DecimalField(max_digits=12, decimal_places=6)
	totalGrade = models.DecimalField(max_digits=12, decimal_places=6)
	avgCommodity1Grade = models.DecimalField(max_digits=12, decimal_places=6)
	lumpRecovery = models.DecimalField(max_digits=12, decimal_places=6)
	finesRecovery = models.DecimalField(max_digits=12, decimal_places=6)
	ultraFinesRecovery = models.DecimalField(max_digits=12, decimal_places=6)
	rejectsRecovery = models.DecimalField(max_digits=12, decimal_places=6)
	lumpGrade = models.DecimalField(max_digits=12, decimal_places=6)
	finesGrade = models.DecimalField(max_digits=12, decimal_places=6)
	ultraFinesGrade = models.DecimalField(max_digits=12, decimal_places=6)
	rejectsGrade = models.DecimalField(max_digits=12, decimal_places=6)
	feedMoisture = models.DecimalField(max_digits=12, decimal_places=6)
	lumpMoisture = models.DecimalField(max_digits=12, decimal_places=6)
	finesMoisture = models.DecimalField(max_digits=12, decimal_places=6)
	ultraFinesMoisture = models.DecimalField(max_digits=12, decimal_places=6)
	rejectsMoisture = models.DecimalField(max_digits=12, decimal_places=6)
	mineOpsDays = models.IntegerField(null=False)
	plantOpsDays = models.IntegerField(null=False)
	mineCapacity = models.DecimalField(max_digits=12, decimal_places=6)
	plantCapacity = models.DecimalField(max_digits=12, decimal_places=6)
	discountRate1 = models.DecimalField(max_digits=12, decimal_places=4)
	discountRate2 = models.DecimalField(max_digits=12, decimal_places=4)
	discountRate3 = models.DecimalField(max_digits=12, decimal_places=4)
	discountRate4 = models.DecimalField(max_digits=12, decimal_places=4)
	discountRate5 = models.DecimalField(max_digits=12, decimal_places=4)
	discountRate6 = models.DecimalField(max_digits=12, decimal_places=4)
	exchangeRate = models.DecimalField(max_digits=12, decimal_places=4)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblInputs'


class tblSmelterTerms(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	LGMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
	LGMaxGrade = models.DecimalField(max_digits=20, decimal_places=2)
	LGMinPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	LGMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	LGMinMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	LGPremium = models.DecimalField(max_digits=20, decimal_places=2)
	HGMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
	HGMaxGrade = models.DecimalField(max_digits=20, decimal_places=2)
	HGMinPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	HGMinMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	HGPremium = models.DecimalField(max_digits=20, decimal_places=2)
	increments = models.DecimalField(max_digits=20, decimal_places=2)
	LGPFMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
	HGPFMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblSmelterTerms'
		unique_together = (("mineID", "commodityID", "dateAdded"),)

		
class tblRevenue(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	sellingPrice = models.DecimalField(max_digits=20, decimal_places=2)
	netPriceUSD = models.DecimalField(max_digits=20, decimal_places=2)
	netPriceCAD = models.DecimalField(max_digits=20, decimal_places=2)
	plantProductRevenue = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblRevenue'
		unique_together = (("mineID", "plantProductID", "year", "dateAdded"),)


class tblCashFlow(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	cashFlowPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	cashFlowPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	cumulativeCashFlowPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	cumulativeCashFlowPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	paybackPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	paybackPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblCashFlow'
		unique_together = (("mineID", "year", "dateAdded"),)


class tblFinancials(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	discountRate = models.IntegerField(null=False)
	NPVPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	NPVPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	IRRPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	IRRPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblFinancials'


class tblCAPEX(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	preStrip = models.DecimalField(max_digits=20, decimal_places=2)
	mineEquipInitial = models.DecimalField(max_digits=20, decimal_places=2)
	mineEquipSustain = models.DecimalField(max_digits=20, decimal_places=2)
	infraDirectCost = models.DecimalField(max_digits=20, decimal_places=2)
	infraIndirectCost = models.DecimalField(max_digits=20, decimal_places=2)
	contingency = models.DecimalField(max_digits=20, decimal_places=2)
	railcars = models.DecimalField(max_digits=20, decimal_places=2)
	otherMobEquip = models.DecimalField(max_digits=20, decimal_places=2)
	closureRehabAssure = models.DecimalField(max_digits=20, decimal_places=2)
	depoProvisionPay = models.DecimalField(max_digits=20, decimal_places=2)
	workCapCurrentProd = models.DecimalField(max_digits=20, decimal_places=2)
	workCapCostsLG = models.DecimalField(max_digits=20, decimal_places=2)
	EPCM = models.DecimalField(max_digits=20, decimal_places=2)
	ownerCost = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblCAPEX'
		unique_together = (("mineID", "year", "dateAdded"),)


class tblOPEX(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	mining = models.DecimalField(max_digits=20, decimal_places=2)
	infrastructure = models.DecimalField(max_digits=20, decimal_places=2)
	stockpileLG = models.DecimalField(max_digits=20, decimal_places=2)
	dewatering = models.DecimalField(max_digits=20, decimal_places=2)
	processing = models.DecimalField(max_digits=20, decimal_places=2)
	hauling = models.DecimalField(max_digits=20, decimal_places=2)
	loadOutRailLoop = models.DecimalField(max_digits=20, decimal_places=2)
	GASite = models.DecimalField(max_digits=20, decimal_places=2)
	GARoomBoardFIFO = models.DecimalField(max_digits=20, decimal_places=2)
	railTransport = models.DecimalField(max_digits=20, decimal_places=2)
	GACorp = models.DecimalField(max_digits=20, decimal_places=2)
	royalties = models.DecimalField(max_digits=20, decimal_places=2)
	transportation = models.DecimalField(max_digits=20, decimal_places=2)
	GA = models.DecimalField(max_digits=20, decimal_places=2)
	shipping = models.DecimalField(max_digits=20, decimal_places=2)
	opexPT = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblOPEX'
		unique_together = (("mineID", "year", "dateAdded"),)


class tblProjectTypeList(models.Model):
	projectTypeID = models.AutoField(primary_key=True)
	projectType = models.CharField(max_length=10)

	class Meta:
		db_table = 'tblProjectTypeList'


class tblProject(models.Model):
	projectID = models.AutoField(primary_key=True)
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectTypeID = models.ForeignKey('tblProjectTypeList', db_column='projectTypeID')
	LOM = models.IntegerField(null=False)
	startDate = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblProject'


class tblProjectPeriods(models.Model):
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	startDate = models.DateField(null=False)
	endDate = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblProjectPeriods'
		unique_together = (("projectID", "mineID", "year", "dateAdded"),)
