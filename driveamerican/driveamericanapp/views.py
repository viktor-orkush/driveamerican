import datetime
import math

from django.shortcuts import render


RATE_DOLLAR_EURO = 1.15
SHIPPING_PRICE_FOR_CALC_VAT = 400


def home(request):
    fuel_types = {'petrol': 'Бензин',
                 'diesel': 'Дизель',
                 'electro': 'Элктро',
                 'hybrid': 'Гибрид'}

    if request.method == 'POST':
        auto_price = request.POST.get('auto_price')
        if auto_price:
            auto_price = float(auto_price)
            auto_engine = float(request.POST.get('auto_engine'))
            fuel_type = request.POST.get('fuel_type')
            auto_age = int(request.POST.get('auto_age'))

            auction_fee = math.ceil(auto_price * 0.1)
            swift_bank_commission = math.ceil(10 + (auto_price + auction_fee)*0.005)

            excise = get_excise(fuel_type, auto_engine, auto_age)
            duty = math.ceil((auto_price + auction_fee) * 0.1)
            vat = math.ceil((excise + auction_fee + duty + SHIPPING_PRICE_FOR_CALC_VAT) * 0.2)
            customs_clearance = excise + duty + vat

            transportation_in_usa = 500
            shipping_price = 900
            broker_forwarder = 850
            parking_port = 50
            transportation_in_ukraine = 200
            pension_tax = math.ceil((auto_price + auction_fee)*0.04)
            certification = 300
            registration = 60
            company_services = 600
            total_cost = math.ceil(auto_price + auction_fee + swift_bank_commission + customs_clearance + transportation_in_usa +\
                                    + shipping_price + broker_forwarder + parking_port + transportation_in_ukraine +\
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
                                                  'fuel_types': fuel_types,
                                                  'years': range(int(datetime.datetime.now().year), 2009, -1),
                                                  'engine_capacity': [capacity/10 for capacity in range(7, 40)]})
    return render(request, 'index.html', {'fuel_types': fuel_types,
                                          'years': range(2010, int(datetime.datetime.now().year)),
                                          'engine_capacity': [capacity/10 for capacity in range(7, 40)]})


def get_excise(auto_engine_type, auto_engine, auto_age):
    if auto_engine_type == 'Бензин':
        if auto_engine <= 3:
            cof = 50
        else:
            cof = 100
    elif auto_engine_type == 'Дизель':
        cof = 75
    excise = math.ceil(get_conf_age(auto_age) * auto_engine * 50 * RATE_DOLLAR_EURO)
    if auto_engine_type == 'Гибрид':
        excise = math.ceil(100 * RATE_DOLLAR_EURO)
    return excise


def get_conf_age(auto_age):
    cof_age = int(datetime.datetime.now().year) - auto_age - 1
    if cof_age < 1:
        cof_age = 1
    return cof_age
