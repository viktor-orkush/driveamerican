from django.contrib import admin

from driveamericanapp.models import Auction, BuyerFee, InternetBidFee, Contact, TransportationPrice

admin.site.register(Auction)
admin.site.register(BuyerFee)
admin.site.register(InternetBidFee)
admin.site.register(Contact)
admin.site.register(TransportationPrice)
