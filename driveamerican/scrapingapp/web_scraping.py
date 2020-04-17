import math
import numbers
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
from driveamericanapp import views as daapp_views

logger = logging.getLogger(__name__)


class IaaiLot():

    @staticmethod
    def save_lot_information_by_vin(vin):
        try:
            url = f'https://www.salvagebid.com/rest-api/v1.0/lots/search?page=1&per_page=26&search_id=&search_query={vin} &sort_field=&sort_order=&odometer_max=*&odometer_min=*&distance=*&destination_zip=&primary_damage=*&loss_type=*&title_name=*&exterior_color=*&year_from=1920&year_to=2021&type=*&make=*&model=*&sales_type=*'
            json_page_response = IaaiLot.get_json_page_by_url(url)
            if len(json_page_response['lots']) > 0:
                for lot in json_page_response['lots']:
                    if vin == lot['VIN']:
                        engine_inf = IaaiLot.get_engine_information(lot['id'])
                        auction = 'IAAI'
                        vehicle_name = lot['vehicle_name']
                        # todo get real fuel type anf capacity
                        fuel_type = engine_inf['fuel_type']
                        engine_capacity = engine_inf['engine'].split('L')[0]
                        start_code = lot['start_code']
                        odometer_value = lot['odometer_value']
                        location_state = lot['location_state']
                        location_city = lot['location_city']
                        retail_value = lot['retail_value']
                        repair_cost = lot['repair_cost']
                        # todo calculate
                        max_bid = lot['buy_it_now'] if lot['buy_it_now'] != 0 else int(lot['retail_value']) * 0.3
                        cost_in_ukraine = IaaiLot.get_cost_in_ukraine(max_bid, engine_capacity, fuel_type, vehicle_name.split(' ')[0])
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

    def get_engine_information(lot_id):
        url = f'https://www.salvagebid.com/rest-api/v1.0/lots/{lot_id}/'
        json_page_response = IaaiLot.get_json_page_by_url(url)
        print(json_page_response['details'])
        lot_details = json_page_response['details']
        fuel_type = list(filter(lambda detail: detail['label'] == 'Fuel Type', lot_details))
        engine = list(filter(lambda detail: detail['label'] == 'Engine', lot_details))
        if len(fuel_type) == 0: raise ValueError('cannot get fuel_type')
        if len(fuel_type) == 0: raise ValueError('cannot get engine')
        return {'fuel_type': fuel_type[0]['value'], 'engine': engine[0]['value']}

    @staticmethod
    def get_cost_in_ukraine(auto_price, auto_engine, fuel_type, auto_age, e_power=0, auction='IAAI'):
        if not isinstance(auto_price, numbers.Real):
            raise ValueError('auto price must be number')
        if not isinstance(auto_engine, numbers.Real):
            try:
                auto_engine = float(auto_engine)
            except Exception:
                auto_engine = 2.5
        if not isinstance(auto_age, numbers.Real):
            try:
                auto_age = int(auto_age)
            except Exception:
                auto_age = 2015
        auction_fee = daapp_views.get_auction_fee(auto_price)
        swift_bank_commission = math.ceil(10 + (auto_price + auction_fee) * 0.005)
        insurance_car = math.ceil((auto_price + auction_fee) * 0.01)
        excise = daapp_views.get_excise(fuel_type, auto_engine, auto_age, e_power)
        duty = daapp_views.get_duty(fuel_type, auto_price, auction_fee)
        vat = daapp_views.get_vat(fuel_type, auto_price, auction_fee, excise, duty)

        transportation_in_usa = 399
        shipping_price = 899
        document_ship = 100
        broker_forwarder = 850
        parking_port = 30
        pension_tax = math.ceil((auto_price + auction_fee) * 0.03)
        certification = 300
        registration = 60
        company_services = 600
        return auto_price + auction_fee + swift_bank_commission + insurance_car + excise + duty + \
               + vat + transportation_in_usa + shipping_price + broker_forwarder + parking_port + \
               + pension_tax + registration + certification + company_services + document_ship

    @staticmethod
    def get_json_page_by_url(url):
        try:
            page_response = requests.get(url)
            if page_response.status_code != 200:
                raise ValueError('Page response dont return status code 200.')
        except requests.Timeout as ex:
            raise ValueError("request timeout - " + ex)
        return page_response.json()


IaaiLot.save_lot_information_by_vin('5N1AT2MT5HC820396')
# IaaiLot.get_engine_information(257139909)
# IaaiLot.get_cost_in_ukraine()
