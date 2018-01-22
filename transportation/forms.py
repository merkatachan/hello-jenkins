from django import forms
from decimal import Decimal
from setup.models import *

class transportForm(forms.Form):
	def __init__(self, *args, **kwargs):
		mineID = kwargs.pop('mineID')
		super(transportForm, self).__init__(*args, **kwargs)

		# Get the latest project by this user/mine
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		LOM = latestProject.LOM


		for i in range(int(LOM)):
			i += 1
			self.fields["year{0}ProductHauling".format(i)] = forms.DecimalField(required=True,
				label="Year{0} Product Hauling".format(i),
				decimal_places=2, max_digits=20,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			self.fields["year{0}RailTransportation".format(i)] = forms.DecimalField(required=True,
				label="Year{0} Rail Transportation, Port and Shiploading".format(i),
				decimal_places=2, max_digits=20,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			self.fields["year{0}Transportation".format(i)] = forms.DecimalField(required=True,
				label="Year{0} Transportation".format(i),
				decimal_places=2, max_digits=20,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))
			self.fields["year{0}ShippingCost".format(i)] = forms.DecimalField(required=True,
				label="Year{0} Shipping Cost".format(i),
				decimal_places=2, max_digits=20,
				widget=forms.NumberInput(attrs={'placeholder': 'Max 2 Decimal Places'}))


