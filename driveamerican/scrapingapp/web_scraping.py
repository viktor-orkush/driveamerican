import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(os.path.dirname(BASE_DIR), "driveamerican")
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'driveamerican.settings'
import django

django.setup()


from django.core.management.base import BaseCommand
import logging
import requests

# vin = '1C4BJWDG0EL237674'
from driveamericanapp.models import Auction
from scrapingapp.models import Lot
logger = logging.getLogger(__name__)


class IaaiLot():

    @staticmethod
    def get_and_save_lot_information(vin):
        try:
            url = f'https://www.salvagebid.com/rest-api/v1.0/lots/search?page=1&per_page=26&search_id=&search_query={vin} &sort_field=&sort_order=&odometer_max=*&odometer_min=*&distance=*&destination_zip=&primary_damage=*&loss_type=*&title_name=*&exterior_color=*&year_from=1920&year_to=2021&type=*&make=*&model=*&sales_type=*'
            page_response = requests.get(url)
            if page_response.status_code == 200:
                print(page_response.status_code)
                json_page_response = page_response.json()
                print(len(json_page_response['lots']))
                if len(json_page_response['lots']) > 0:
                    for lot in json_page_response['lots']:
                        if vin == lot['VIN']:
                            print(lot['vehicle_name'])
                            print(lot['vehicle_name'])
                            auction = 'IAAI'
                            vehicle_name = lot['vehicle_name']
                            # todo get real fuel type anf capacity
                            fuel_type = 'Gas'
                            engine_capacity = 2.5
                            start_code = lot['start_code']
                            odometer_value = lot['odometer_value']
                            location_state = lot['location_state']
                            location_city = lot['location_city']
                            retail_value = lot['retail_value']
                            repair_cost = lot['repair_cost']
                            # todo calculate
                            max_bid = int(lot['retail_value'])*0.25
                            cost_in_ukraine = 0
                            sale_date = lot['sale_date']
                            image_url = lot['images'][0]
                            print(image_url)
                            try:
                                IaaiLot.save_lot_db(auction, vehicle_name, vin, fuel_type, engine_capacity, start_code,
                                                    odometer_value, location_state, location_city, retail_value,
                                                    repair_cost, max_bid, cost_in_ukraine, sale_date, image_url)
                            except ValueError as ex:
                                logger.exception(ex)
                        else:
                            raise ValueError('Dont find lot by current VIN.')
                else:
                    raise ValueError('Dont find lot by current VIN.')
        except requests.Timeout as ex:
            logger.exception("request timeout - " + ex)
        except Exception as ex:
            logger.exception(ex)

    @staticmethod
    def save_lot_db(auction, vehicle_name, vin, fuel_type, engine_capacity, start_code, odometer_value,
                    location_state, location_city, retail_value, repair_cost, max_bid, cost_in_ukraine, sale_date,
                    image_url):
        auction_obj = Auction.objects.get(auction=auction)
        if not auction_obj: raise ValueError(f'Auction {auction} dont find and cannot create new lot')
        obj, created = Lot.objects.get_or_create(
            auction=auction_obj,
            vehicle_name=vehicle_name,
            vin=vin,
            fuel_type=fuel_type,
            engine_capacity=engine_capacity,
            start_code=start_code,
            odometer_value=odometer_value,
            location_state=location_state,
            location_city=location_city,
            retail_value=retail_value,
            repair_cost=repair_cost,
            max_bid=max_bid,
            cost_in_ukraine=cost_in_ukraine,
            sale_date=sale_date,
            image_url=image_url)
        if not created: raise ValueError(f'Lot with vin = {vin} already exist')
        return obj


# IaaiLot.get_and_save_lot_information('KMHDH4AEXFU437402')