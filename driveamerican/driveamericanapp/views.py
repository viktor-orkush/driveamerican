import datetime
import math

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

RATE_DOLLAR_EURO = 1.15
SHIPPING_PRICE_FOR_CALC_VAT = 400
FUEL_TYPES = {'petrol': 'Бензин',
              'diesel': 'Дизель',
              'electro': 'Электро',
              'hybrid': 'Гибрид'}


def home(request):
    if request.method == 'POST':
        auto_price = request.POST.get('auto_price')
        if auto_price:
            auto_price = float(auto_price)
            auto_engine = float(request.POST.get('auto_engine'))
            fuel_type = request.POST.get('fuel_type')
            auto_age = int(request.POST.get('auto_age'))

            auction_fee = math.ceil(auto_price * 0.1)
            swift_bank_commission = math.ceil(10 + (auto_price + auction_fee) * 0.005)

            excise = get_excise(fuel_type, auto_engine, auto_age)
            duty = math.ceil((auto_price + auction_fee) * 0.1)
            vat = math.ceil((excise + auction_fee + duty + SHIPPING_PRICE_FOR_CALC_VAT) * 0.2)
            customs_clearance = excise + duty + vat

            transportation_in_usa = 500
            shipping_price = 900
            broker_forwarder = 850
            parking_port = 50
            transportation_in_ukraine = 200
            pension_tax = math.ceil((auto_price + auction_fee) * 0.04)
            certification = 300
            registration = 60
            company_services = 600
            total_cost = math.ceil(
                auto_price + auction_fee + swift_bank_commission + customs_clearance + transportation_in_usa + \
                + shipping_price + broker_forwarder + parking_port + transportation_in_ukraine + \
                + pension_tax + certification + registration + company_services)
            return render(request, 'index.html', {'auction_fee': auction_fee,
                                                  'swift_bank_commission': swift_bank_commission,
                                                  'excise': excise,
                                                  'duty': duty,
                                                  'vat': vat,
                                                  'customs_clearance': customs_clearance,
                                                  'transportation_in_usa': transportation_in_usa,
                                                  'shipping_price': shipping_price,
                                                  'broker_forwarder': broker_forwarder,
                                                  'parking_port': parking_port,
                                                  'transportation_in_ukraine': transportation_in_ukraine,
                                                  'pension_tax': pension_tax,
                                                  'certification': certification,
                                                  'registration': registration,
                                                  'company_services': company_services,
                                                  'total_cost': total_cost,
                                                  'fuel_types': FUEL_TYPES,
                                                  'years': range(int(datetime.datetime.now().year), 2009, -1),
                                                  'engine_capacity': [capacity / 10 for capacity in range(7, 40)]})
    return render(request, 'index.html', {'fuel_types': FUEL_TYPES,
                                          'years': range(2010, int(datetime.datetime.now().year)),
                                          'engine_capacity': [capacity / 10 for capacity in range(7, 40)]})


def get_excise(auto_engine_type, auto_engine, auto_age, e_power):
    if auto_engine_type == 'electro':
        excise = math.ceil(e_power * RATE_DOLLAR_EURO)
    if auto_engine_type == 'hybrid':
        excise = math.ceil(100 * RATE_DOLLAR_EURO)
    if auto_engine_type == 'petrol':
        if auto_engine <= 3:
            cof = 50
        else:
            cof = 100
        excise = math.ceil(get_cof_age(auto_age) * auto_engine * cof * RATE_DOLLAR_EURO)
    if auto_engine_type == 'diesel':
        cof = 75
        excise = math.ceil(get_cof_age(auto_age) * auto_engine * cof * RATE_DOLLAR_EURO)
    return excise


def get_cof_age(auto_age):
    cof_age = int(datetime.datetime.now().year) - auto_age - 1
    if cof_age < 1:
        cof_age = 1
    return cof_age


def customs(request):
    # if request.method == 'POST':
    #     auto_price = request.POST.get('auto_price')
    #     if auto_price:
    #         auto_price = float(auto_price)
    #         auto_engine = float(request.POST.get('auto_engine', 0))
    #         fuel_type = request.POST.get('fuel_type', '')
    #         auto_age = int(request.POST.get('auto_age', 0))
    #         print("fuel_type " + fuel_type)
    #         excise = get_excise(fuel_type, auto_engine, auto_age)
    #         duty = math.ceil(auto_price * 0.1)
    #         vat = math.ceil((excise + duty + SHIPPING_PRICE_FOR_CALC_VAT) * 0.2)
    #         customs_clearance = excise + duty + vat
    #         pension_tax = math.ceil(auto_price * 0.04)
    #
    #         return render(request, 'customs.html', {'excise': excise,
    #                                                 'duty': duty,
    #                                                 'vat': vat,
    #                                                 'customs_clearance': customs_clearance,
    #                                                 'pension_tax': pension_tax,
    #                                                 'fuel_types': FUEL_TYPES,
    #                                                 'years': range(int(datetime.datetime.now().year), 2009, -1),
    #                                                 'engine_capacity': [capacity / 10 for capacity in range(7, 40)]})
    return render(request, 'customs.html', {'fuel_types': FUEL_TYPES,
                                            'years': range(2010, int(datetime.datetime.now().year)),
                                            'engine_capacity': [capacity / 10 for capacity in range(7, 40)],
                                            'fuel_type': 'petrol'})


class CalculateCustomsAPI(APIView):
    def post(self, request):
        auto_price = request.POST.get('auto_price')
        if auto_price:
            auto_price = float(auto_price)
            auto_engine = float(request.POST.get('auto_engine', 0))
            fuel_type = request.POST.get('fuel_type', '')
            auto_age = int(request.POST.get('auto_age', 0))
            e_power = int(request.POST.get('e_power', 1))

            excise = get_excise(fuel_type, auto_engine, auto_age, e_power)
            duty = math.ceil(auto_price * 0.1)
            vat = math.ceil((excise + duty + SHIPPING_PRICE_FOR_CALC_VAT) * 0.2)
            customs_clearance = excise + duty + vat
            total_cost = auto_price + customs_clearance
            pension_tax = math.ceil(auto_price * 0.04)

            return JsonResponse({'result': 'success',
                                'excise': excise,
                                 'duty': duty,
                                 'vat': vat,
                                 'customs_clearance': customs_clearance,
                                 'total_cost': total_cost,
                                 'pension_tax': pension_tax})

        return JsonResponse({'result': 'error'})
