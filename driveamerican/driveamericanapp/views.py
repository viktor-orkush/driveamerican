import datetime
import math

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from driveamericanapp.models import BuyerFee, Auction, InternetBidFee, TransportationPrice
from driveamericanapp.serializers import ContactSerializer
from driveamericanapp.telegram_notification import send_message

RATE_DOLLAR_EURO = 1.1
SHIPPING_PRICE_FOR_CALC_VAT = 400
MY_EXTRA_75 = 75
FUEL_TYPES = {'petrol': 'Бензин',
              'diesel': 'Дизель',
              'electro': 'Электро',
              'hybrid': 'Гибрид'}

port_shipping_price = {
    'port_savannah': 890,
    'port_newark': 890,
    'port_houston': 990,
    'port_los_angeles': 1090,
}

all_shipping_ports = {
    'port_savannah': 'Savannah GA',
    'port_newark': 'Newark NJ',
    'port_houston': 'Houston TX',
    'port_los_angeles': 'Los Angeles CA',
}


def home(request):
    return render(request, 'index.html', )


def faq(request):
    return render(request, 'faq.html', )


def calculation(request):
    return render(request, 'calculation.html', {'fuel_types': FUEL_TYPES,
                                                'auto_engine': 2.0,
                                                'auto_age': '2015',
                                                'fuel_type': 'petrol',
                                                'years': range(2005, int(datetime.datetime.now().year)),
                                                'engine_capacity': [capacity / 10 for capacity in range(7, 40)]})


class CalculateAllPaymentsAPI(APIView):
    def post(self, request):
        auto_price = request.POST.get('auto_price')
        if auto_price:
            auto_price = float(auto_price)
            auto_engine = float(request.POST.get('auto_engine'))
            fuel_type = request.POST.get('fuel_type')
            auto_age = int(request.POST.get('auto_age'))
            e_power = int(request.POST.get('e_power', 1))
            auction = request.POST.get('auction')

            # todo calculate auction fee for iaai and copart
            auction_fee = get_auction_fee(auto_price)

            swift_bank_commission = math.ceil(10 + (auto_price + auction_fee) * 0.005)

            insurance_car = math.ceil((auto_price + auction_fee) * 0.01)
            excise = get_excise(fuel_type, auto_engine, auto_age, e_power)
            duty = get_duty(fuel_type, auto_price, auction_fee)
            vat = get_vat(fuel_type, auto_price, auction_fee, excise, duty)
            customs_clearance = excise + duty + vat

            # calculate transportation for different location
            auction_location = request.POST.get('auction_location')
            try:
                transportation_prices = get_transportation_prices(auction, auction_location)
                shipping_port = min(transportation_prices, key=transportation_prices.get)

                shipping_port_name = all_shipping_ports[shipping_port]
                transportation_in_usa = transportation_prices[shipping_port] + MY_EXTRA_75
                shipping_price = port_shipping_price.get(shipping_port)
            except:
                transportation_in_usa = 399
                shipping_price = 899
                shipping_port_name = 'N/A'

            broker_forwarder = 850
            parking_port = 30
            transportation_in_ukraine = 100
            pension_tax = math.ceil((auto_price + auction_fee) * 0.04)
            certification = 300
            registration = 60
            company_services = 600
            total_cost = math.ceil(
                auto_price + auction_fee + swift_bank_commission + customs_clearance + transportation_in_usa + \
                + shipping_price + broker_forwarder + parking_port + transportation_in_ukraine + \
                + pension_tax + certification + registration + company_services)
            return JsonResponse({'auto_price': auto_price,
                                 'auction_fee': auction_fee,
                                 'insurance_car': insurance_car,
                                 'swift_bank_commission': swift_bank_commission,
                                 'excise': excise,
                                 'duty': duty,
                                 'vat': vat,
                                 'customs_clearance': customs_clearance,
                                 'transportation_in_usa': transportation_in_usa,
                                 'shipping_price': shipping_price,
                                 'shipping_port': shipping_port_name,
                                 'broker_forwarder': broker_forwarder,
                                 'parking_port': parking_port,
                                 'transportation_in_ukraine': transportation_in_ukraine,
                                 'pension_tax': pension_tax,
                                 'certification': certification,
                                 'registration': registration,
                                 'company_services': company_services,
                                 'total_cost': total_cost,
                                 'result': 'success'})
        return JsonResponse({'result': 'error'})

    def get(self, request):
        auction = request.GET.get('auction')
        auction_obj = Auction.objects.get(auction=auction)
        auction_locations = TransportationPrice.objects.filter(auction=auction_obj). \
            values('auction_location', 'state'). \
            order_by('state')
        context = {
            'auction_locations': list(auction_locations)
        }
        return JsonResponse(context)


def customs(request):
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
            vat = math.ceil((auto_price + excise + duty + SHIPPING_PRICE_FOR_CALC_VAT) * 0.2)
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


class UserContactRequest(APIView):
    """
    DRF view API for contact form
    :param request: user, phone, message
    :return: success
    """

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {'result': 'success',
                       'message': '<strong>Ваша заявка принята.</strong> '
                                  'Мы свяжемся с Вами в ближайшее время!'}
            name = request.data.get("user")
            phone = request.data.get("phone")
            message = request.data.get("message")
            message_text = "Новый запрос на сайте " + "\n Имя: " + name + "\n Телефон: " + phone + "\n Сообщение: " + message
            send_message(message_text)
        else:
            context = {'result': 'error'}
        return JsonResponse(context)


def get_transportation_prices(auction, auction_location):
    try:
        auction_obj = Auction.objects.get(auction=auction)
        tp_obj = TransportationPrice.objects.get(auction_location=auction_location, auction=auction_obj)
        transportation_prices = {'port_houston': tp_obj.port_houston,
                                 'port_los_angeles': tp_obj.port_los_angeles,
                                 'port_newark': tp_obj.port_newark,
                                 'port_savannah': tp_obj.port_savannah}
        return {k: v for k, v in transportation_prices.items() if v is not 0}
    except Auction.DoesNotExist:
        raise Auction.DoesNotExist
    except TransportationPrice.DoesNotExist:
        raise TransportationPrice.DoesNotExist


def get_duty(auto_engine_type, auto_price, auction_fee):
    if auto_engine_type == 'electro': return 0
    return math.ceil((auto_price + auction_fee) * 0.1)


def get_vat(auto_engine_type, auto_price, auction_fee, excise, duty):
    if auto_engine_type == 'electro': return 0
    return math.ceil((auto_price + auction_fee + excise + duty + SHIPPING_PRICE_FOR_CALC_VAT) * 0.2)


def get_excise(auto_engine_type, auto_engine, auto_age, e_power):
    excise = 0
    if auto_engine_type == 'electro':
        excise = math.ceil(e_power * RATE_DOLLAR_EURO)
    if auto_engine_type == 'hybrid':
        excise = math.ceil(100 * RATE_DOLLAR_EURO)
    if auto_engine_type == 'petrol' or auto_engine_type == 'Gasoline':
        if auto_engine <= 3:
            cof = 50
        else:
            cof = 100
        excise = math.ceil(get_cof_age(auto_age) * auto_engine * cof * RATE_DOLLAR_EURO)
    if auto_engine_type == 'diesel':
        if auto_engine <= 3.5:
            cof = 75
        else:
            cof = 150
        excise = math.ceil(get_cof_age(auto_age) * auto_engine * cof * RATE_DOLLAR_EURO)
    return excise


def get_cof_age(auto_age):
    cof_age = int(datetime.datetime.now().year) - auto_age - 1
    if cof_age < 1:
        cof_age = 1
    return cof_age


def get_auction_fee(auto_price):
    buyer_fee = 0
    if auto_price < 7500.0:
        buyer_fee = BuyerFee.objects.filter(sale_price_min__lte=auto_price, sale_price_max__gte=auto_price,
                                            ).values('buyer_fee')[0]['buyer_fee']
    elif 7500 <= auto_price <= 19999:
        buyer_fee = 500 + auto_price * 0.01
    elif auto_price >= 20000:
        buyer_fee = auto_price * 0.04

    internet_bid_fee = \
        InternetBidFee.objects.filter(sale_price_min__lte=auto_price, sale_price_max__gte=auto_price).values(
            'internet_bid_fee')[0][
            'internet_bid_fee']
    service_fee = 59
    broker_fee = 35
    return buyer_fee + internet_bid_fee + service_fee + broker_fee
