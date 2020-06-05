from django.db import models


class Auction(models.Model):
    auction = models.CharField(max_length=256)


class BuyerFee(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, )
    sale_price_min = models.IntegerField()
    sale_price_max = models.IntegerField()
    buyer_fee = models.IntegerField()

    def __str__(self):
        return '"{buyer_fee}"'.format(buyer_fee=self.buyer_fee)


class InternetBidFee(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, )
    sale_price_min = models.IntegerField()
    sale_price_max = models.IntegerField()
    internet_bid_fee = models.IntegerField()

    def __str__(self):
        return '"{internet_bid_fee}"'.format(internet_bid_fee=self.internet_bid_fee)


class Contact(models.Model):
    user = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=100, blank=False)
    message = models.CharField(max_length=256, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '"{user}"'.format(user=self.user)


class TransportationPrice(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, )
    auction_location = models.CharField(max_length=512, blank=True)
    state = models.CharField(max_length=32, blank=True)
    port_savannah = models.IntegerField(default=0, blank=True, null=True)
    port_newark = models.IntegerField(default=0, blank=True, null=True)
    port_houston = models.IntegerField(default=0, blank=True, null=True)


def __str__(self):
    return '"{auction_location}"'.format(auction_location=self.auction_location)
