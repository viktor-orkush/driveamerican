from io import BytesIO

from django.core import files
from django.db import models

import requests


class Lot (models.Model):
    auction = models.ForeignKey('driveamericanapp.Auction', on_delete=models.CASCADE,)
    vehicle_name = models.CharField(max_length=256, blank=False)
    vin = models.CharField(max_length=64, blank=False)
    fuel_type = models.CharField(max_length=64, blank=True)
    engine_capacity = models.FloatField(blank=True)
    start_code = models.CharField(max_length=64, blank=True)
    odometer_value = models.CharField(max_length=64, blank=True)
    location_state = models.CharField(max_length=16, blank=False)
    location_city = models.CharField(max_length=128, blank=False)
    retail_value = models.IntegerField(default=0, blank=True, null=True)
    repair_cost = models.IntegerField(default=0, blank=True, null=True)
    max_bid = models.IntegerField(default=0, blank=True, null=True)
    cost_in_ukraine = models.IntegerField(default=0, blank=True, null=True)
    sale_date = models.DateField()
    image_file = models.FileField(upload_to='lots', blank=False)
    image_url = models.URLField(default=0)

    def save(self, *args, **kwargs):
        super(Lot, self).save(*args, **kwargs)
        if self.image_url and not self.image_file:
            resp = requests.get(self.image_url)
            if resp.status_code != requests.codes.ok:
                raise ValueError("Cannot download image Lot")
            fp = BytesIO()
            fp.write(resp.content)
            file_name = self.image_url.split("/")[-1]
            self.image_file.save(file_name, files.File(fp))


