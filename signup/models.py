from django.db import models

# Create your models here.
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
	dateAdded = models.DateTimeField()

	def __str__(self):
		return str(self.userID)

	class Meta:
		db_table = 'tblUsers'


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
