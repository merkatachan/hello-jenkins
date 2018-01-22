from django.db import models

# Create your models here.

class tblCompany(models.Model):
	companyID = models.AutoField(primary_key=True)
	company = models.CharField(max_length=250)
	address = models.CharField(max_length=250)
	city = models.CharField(max_length=100)
	province = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	postalCode = models.CharField(max_length=10)
	phone = models.CharField(max_length=32)
	# dateAdded = models.DateTimeField(auto_now_add=True)
	dateAdded = models.DateTimeField(null=False)

	def __str__(self):
		return str(self.companyID)

	class Meta:
		db_table = 'tblCompany'

class tblMine(models.Model):
	mineID = models.AutoField(primary_key=True)
	mine = models.CharField(max_length=100)
	address = models.CharField(max_length=250)
	city = models.CharField(max_length=100)
	province = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	postalCode = models.CharField(max_length=10)
	phone = models.CharField(max_length=32)
	fax = models.CharField(max_length=32)
	dateAdded = models.DateTimeField(null=False)

	def __str__(self):
		return str(self.mineID)

	class Meta:
		db_table = 'tblMine'

class tblUsers(models.Model):
	userID = models.AutoField(primary_key=True)
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	companyID = models.ForeignKey('tblCompany', db_column='companyID')
	username = models.CharField(max_length=50, unique=True)
	firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	phone = models.CharField(max_length=32)
	jobTitle = models.CharField(max_length=50)

	# Need to change userRole settings
	userRole = models.IntegerField()

	password = models.CharField(max_length=64)
	lastLogin = models.DateTimeField()
	dateAdded = models.DateTimeField(null=False)
	reset = models.CharField(max_length=6)
	resetExpiry = models.DateTimeField()

	def __str__(self):
		return str(self.userID)

	class Meta:
		db_table = 'tblUsers'


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
	projectID = models.ForeignKey('tblProject', db_column='projectID')
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


class tblMineProduct(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	mineProductID = models.ForeignKey('tblMineProductList', db_column='mineProductID')
	# commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	# grade = models.DecimalField(max_digits=12, decimal_places=6, null=True)
	dateAdded = models.DateTimeField(null=False)
	# optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblMineProduct'


class tblMineProductGrade(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	# mineProductID = models.ForeignKey('tblMineProductList', db_column='mineProductID')
	stockpileID = models.IntegerField(null=False)
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	year = models.IntegerField(null=False)
	grade = models.DecimalField(max_digits=12, decimal_places=6, null=True)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblMineProductGrade'


class tblMineProductGradeOptimized(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	# mineProductID = models.ForeignKey('tblMineProductList', db_column='mineProductID')
	stockpileID = models.IntegerField(null=False)
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	grade = models.DecimalField(max_digits=12, decimal_places=6, null=True)
	date = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblMineProductGradeOptimized'


class tblMineProductTonnage(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	# mineProductID = models.ForeignKey('tblMineProductList', db_column='mineProductID')
	stockpileID = models.IntegerField(null=False)
	year = models.IntegerField(null=False)
	tonnage = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblMineProductTonnage'


class tblMineProductTonnageOptimized(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	# mineProductID = models.ForeignKey('tblMineProductList', db_column='mineProductID')
	stockpileID = models.IntegerField(null=False)
	tonnage = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()
	date = models.DateField(null=False)

	class Meta:
		db_table = 'tblMineProductTonnageOptimized'


class tblPlantProduct(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	# commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	# grade = models.DecimalField(max_digits=12, decimal_places=6, null=True)
	dateAdded = models.DateTimeField(null=False)
	# optimized = models.NullBooleanField()
	recovery = models.DecimalField(max_digits=12, decimal_places=6)
	moisture = models.DecimalField(max_digits=12, decimal_places=6)

	class Meta:
		db_table = 'tblPlantProduct'


class tblPlantProductGradeOptimized(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	grade = models.DecimalField(max_digits=12, decimal_places=6, null=True)
	date = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblPlantProductGradeOptimized'		


class tblPlantProductTonnage(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	tonnageWMT = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	tonnageDMT = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()
	date = models.DateField(null=False)

	class Meta:
		db_table = 'tblPlantProductTonnage'


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
	numStockpiles = models.IntegerField(null=False)
	startDate = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblProject'


class tblCAPEX(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	preStrip = models.DecimalField(max_digits=20, decimal_places=8)
	mineEquipInitial = models.DecimalField(max_digits=20, decimal_places=8)
	mineEquipSustain = models.DecimalField(max_digits=20, decimal_places=8)
	infraDirectCost = models.DecimalField(max_digits=20, decimal_places=8)
	infraIndirectCost = models.DecimalField(max_digits=20, decimal_places=8)
	contingency = models.DecimalField(max_digits=20, decimal_places=8)
	railcars = models.DecimalField(max_digits=20, decimal_places=8)
	otherMobEquip = models.DecimalField(max_digits=20, decimal_places=8)
	closureRehabAssure = models.DecimalField(max_digits=20, decimal_places=8)
	depoProvisionPay = models.DecimalField(max_digits=20, decimal_places=8)
	workCapCurrentProd = models.DecimalField(max_digits=20, decimal_places=8)
	workCapCostsLG = models.DecimalField(max_digits=20, decimal_places=8)
	EPCM = models.DecimalField(max_digits=20, decimal_places=8)
	ownerCost = models.DecimalField(max_digits=20, decimal_places=8)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblCAPEX'
		unique_together = (("mineID", "year", "dateAdded"),)


class tblOPEX(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	mining = models.DecimalField(max_digits=20, decimal_places=8)
	infrastructure = models.DecimalField(max_digits=20, decimal_places=8)
	stockpileLG = models.DecimalField(max_digits=20, decimal_places=8)
	dewatering = models.DecimalField(max_digits=20, decimal_places=8)
	processing = models.DecimalField(max_digits=20, decimal_places=8)
	hauling = models.DecimalField(max_digits=20, decimal_places=8)
	loadOutRailLoop = models.DecimalField(max_digits=20, decimal_places=8)
	GASite = models.DecimalField(max_digits=20, decimal_places=8)
	GARoomBoardFIFO = models.DecimalField(max_digits=20, decimal_places=8)
	railTransport = models.DecimalField(max_digits=20, decimal_places=8)
	GACorp = models.DecimalField(max_digits=20, decimal_places=8)
	royalties = models.DecimalField(max_digits=20, decimal_places=8)
	transportation = models.DecimalField(max_digits=20, decimal_places=8)
	GA = models.DecimalField(max_digits=20, decimal_places=8)
	shipping = models.DecimalField(max_digits=20, decimal_places=8)
	opexPT = models.DecimalField(max_digits=20, decimal_places=8)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblOPEX'
		unique_together = (("mineID", "year", "dateAdded"),)


# class tblSmelterTerms(models.Model):
# 	mineID = models.ForeignKey('tblMine', db_column='mineID')
# 	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
# 	LGMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
# 	LGMaxGrade = models.DecimalField(max_digits=20, decimal_places=2)
# 	LGMinPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	LGMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	LGMinMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	LGPremium = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGMaxGrade = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGMinPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGMinMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGPremium = models.DecimalField(max_digits=20, decimal_places=2)
# 	increments = models.DecimalField(max_digits=20, decimal_places=2)
# 	LGPFMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
# 	LGPFMinPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGPFMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
# 	HGPFMinPenalty = models.DecimalField(max_digits=20, decimal_places=2)
# 	dateAdded = models.DateTimeField(null=False)

# 	class Meta:
# 		db_table = 'tblSmelterTerms'
# 		unique_together = (("mineID", "commodityID", "dateAdded"),)


class tblSmelterTerms(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	stockpileID = models.IntegerField(null=False)
	minGrade = models.DecimalField(max_digits=20, decimal_places=2)
	maxGrade = models.DecimalField(max_digits=20, decimal_places=2)
	minPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	maxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	minMaxPenalty = models.DecimalField(max_digits=20, decimal_places=2)
	premium = models.DecimalField(max_digits=20, decimal_places=2)
	increments = models.DecimalField(max_digits=20, decimal_places=2)
	PFMinGrade = models.DecimalField(max_digits=20, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblSmelterTerms'


class tblPrice(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	stockpileID = models.IntegerField(null=False)
	#commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	lump = models.DecimalField(max_digits=12, decimal_places=2)
	lumpPrem = models.DecimalField(max_digits=12, decimal_places=2)
	fines = models.DecimalField(max_digits=12, decimal_places=2)
	ultraFines = models.DecimalField(max_digits=12, decimal_places=2)
	# LGLump = models.DecimalField(max_digits=12, decimal_places=2)
	# LGLumpPrem = models.DecimalField(max_digits=12, decimal_places=2)
	# LGFines = models.DecimalField(max_digits=12, decimal_places=2)
	# LGUltraFines = models.DecimalField(max_digits=12, decimal_places=2)
	lumpAvg = models.DecimalField(max_digits=12, decimal_places=2)
	# LGLumpAvg = models.DecimalField(max_digits=12, decimal_places=2)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblPrice'
		# unique_together = (("mineID", "commodityID", "dateAdded"),)
		# unique_together = (("mineID", "dateAdded"),)


class tblTaxes(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	year = models.IntegerField(null=False)
	federal = models.DecimalField(max_digits=10, decimal_places=4)
	provincial = models.DecimalField(max_digits=10, decimal_places=4)
	mining = models.DecimalField(max_digits=10, decimal_places=4)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblTaxes'
		unique_together = (("mineID", "year", "dateAdded"),)


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
	mineCapacity = models.DecimalField(max_digits=12, decimal_places=2)
	plantCapacity = models.DecimalField(max_digits=12, decimal_places=2)
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


class tblSmelterTermsOptimized(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	commodityID = models.ForeignKey('tblCommodityList', db_column='commodityID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	penalty = models.DecimalField(max_digits=20, decimal_places=2)
	date = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)
	optimized = models.NullBooleanField()

	class Meta:
		db_table = 'tblSmelterTermsOptimized'


class tblRevenue(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	plantProductID = models.ForeignKey('tblPlantProductList', db_column='plantProductID')
	sellingPrice = models.DecimalField(max_digits=20, decimal_places=2)
	netPriceUSD = models.DecimalField(max_digits=20, decimal_places=2)
	netPriceCAD = models.DecimalField(max_digits=20, decimal_places=2)
	plantProductRevenue = models.DecimalField(max_digits=20, decimal_places=2)
	date = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblRevenue'


class tblCashFlow(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = models.ForeignKey('tblProject', db_column='projectID')
	cashFlowPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	cashFlowPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	cumulativeCashFlowPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	cumulativeCashFlowPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	paybackPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	paybackPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	date = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)
	processed = models.NullBooleanField()

	class Meta:
		db_table = 'tblCashFlow'


class tblFinancials(models.Model):
	mineID = models.ForeignKey('tblMine', db_column='mineID')
	projectID = projectID = models.ForeignKey('tblProject', db_column='projectID')
	discountRate = models.IntegerField(null=False)
	NPVPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	NPVPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	IRRPreTax = models.DecimalField(max_digits=20, decimal_places=2)
	IRRPostTax = models.DecimalField(max_digits=20, decimal_places=2)
	date = models.DateField(null=False)
	dateAdded = models.DateTimeField(null=False)

	class Meta:
		db_table = 'tblFinancials'


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
