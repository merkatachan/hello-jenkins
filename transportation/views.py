from django.shortcuts import render
from django.utils import timezone

from .forms import *
from setup.models import *

def index(request):
	mineID = request.session["mineID"]
	form_class = transportForm(mineID=mineID)

	if request.method == 'POST':
		projectMatch = tblProject.objects.filter(mineID=int(mineID)).order_by('-projectID')[0]
		LOM = projectMatch.LOM
		form = transportForm(request.POST, mineID=mineID)
		if form.is_valid():
			mineMatch = tblMine.objects.get(mineID=int(mineID))
			dateAdded = timezone.localtime(timezone.now())
			for year in range(1, LOM+1):
				hauling = request.POST.get("year{0}ProductHauling".format(year), '')
				railTransport = request.POST.get("year{0}RailTransportation".format(year), '')
				transportation = request.POST.get("year{0}Transportation".format(year), '')
				shipping = request.POST.get("year{0}ShippingCost".format(year), '')

				tblOPEXObj = tblOPEX(mineID=mineMatch, year=year, hauling=hauling,
					railTransport=railTransport,
					transportation=transportation,
					shipping=shipping, dateAdded=dateAdded)
				tblOPEXObj.save()

			return render(request, 'transportation/success.html', { }) #Redirect

		return render(request, "transportation/transportation.html", {'form': form_class, 'LOM': LOM})
	else:
		# Get the latest project by this user/mine
		latestProject = tblProject.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		LOM = latestProject.LOM

		latestOPEX = tblOPEX.objects.filter(mineID=int(mineID)).order_by('-dateAdded')[0]
		timestamp = latestOPEX.dateAdded

		
		hauling = []
		railTransport = []
		transportation = []
		shipping = []

		for i in range(LOM):
			i += 1
			result = tblOPEX.objects.filter(mineID=int(mineID), year=i, dateAdded=timestamp)
			if result:
				row = result[0]
				hauling.append(row.hauling)
				railTransport.append(row.railTransport)
				transportation.append(row.transportation)
				shipping.append(row.shipping)

		totalHauling = sum(hauling)
		totalRailTransport = sum(railTransport)
		totalTransportation = sum(transportation)
		totalShipping = sum(shipping)

		return render(request, "transportation/transportation.html", {'form': form_class, 'LOM': LOM,
			'hauling': hauling, 'railTransport': railTransport,
			'transportation': transportation, 'shipping': shipping,
			'totalHauling': totalHauling, 'totalRailTransport': totalRailTransport,
			'totalTransportation': totalTransportation, 'totalShipping': totalShipping
			})
	