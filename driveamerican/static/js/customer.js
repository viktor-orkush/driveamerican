function setEqualHeight(columns) {
    var tallestcolumn = 0;
    columns.each(
        function () {
            currentHeight = $(this).height();
            if (currentHeight > tallestcolumn) {
                tallestcolumn = currentHeight;
            }
        }
    );
    columns.height(tallestcolumn);
}

$(document).ready(function () {
    setEqualHeight($(".services > div> .card"));
    setEqualHeight($(".privileges > div> div > div > .card"));
});


$('.calc-radio').click(function () {
    if (this.id === "petrol" || this.id === "diesel") {
        $('.calc-tab-panel').parent().find('div.tab-pane').removeClass('active')
        $('#tap_petrol').addClass('active')
    } else if (this.id === 'electro') {
        $('.calc-tab-panel').parent().find('div.tab-pane').removeClass('active')
        $('#tap_electro').addClass('active')
    } else if (this.id === 'hybrid') {
        $('.calc-tab-panel').parent().find('div.tab-pane').removeClass('active')
        $('#tap_hybrid').addClass('active')
    }
});


//calculate customs clearance for all car
$("#calculate_customs_btn").on('click', function () {
    $.ajax({
        url: '/calculate_customs/',
        type: "POST",
        data: $('#calculate_customs_form').serialize(),
        success: function (data) {
            if (data['result'] == 'success') {
                $('#total_cost').text(data['total_cost'])
                $('#excise').text(data['excise'])
                $('#duty').text(data['duty'])
                $('#vat').text(data['vat'])
                $('#customs_clearance').text(data['customs_clearance'])
                $('#pension_tax').text(data['pension_tax'])

                console.log('success ajax');
            } else if (data['result'] == 'error') {
                console.log('data error');
            }
        },
        error: function (err) {
            console.log('function error result ' + err);
        }
    });
});


//calculate all payments for byu cars in usa
$("#calculate_all_payments_btn").on('click', function () {
    $.ajax({
        url: '/calculate_all_payments/',
        type: "POST",
        data: $('#calculate_customs_form').serialize(),
        success: function (data) {
            if (data['result'] == 'success') {
                $('#auto_price').text(data['auto_price'])
                $('#auction_fee').text(data['auction_fee'])
                $('#swift_bank_commission').text(data['swift_bank_commission'])
                $('#insurance_car').text(data['insurance_car'])
                $('#transportation_in_usa').text(data['transportation_in_usa'])
                $('#shipping_price').text(data['shipping_price'])
                $('#shipping_port').text(data['shipping_port'])
                $('#broker_forwarder').text(data['broker_forwarder'])
                $('#parking_port').text(data['parking_port'])
                $('#transportation_in_ukraine').text(data['transportation_in_ukraine'])
                $('#pension_tax').text(data['pension_tax'])
                $('#certification').text(data['certification'])
                $('#registration').text(data['registration'])
                $('#company_services').text(data['company_services'])
                $('#excise').text(data['excise'])
                $('#duty').text(data['duty'])
                $('#vat').text(data['vat'])
                $('#customs_clearance').text(data['customs_clearance'])
                $('#pension_tax').text(data['pension_tax'])
                $('#total_cost').text(data['total_cost'])
            } else if (data['result'] == 'error') {
                console.log('data error');
            }
        },
        error: function (err) {
            console.log('function error result ' + err);
        }
    });
});


//calculate all payments for byu cars in usa
$("#auction_id").change(function () {
    // console.log('change')
    $.ajax({
        url: '/calculate_all_payments/',
        type: "GET",
        data: $('#calculate_customs_form').serialize(),
        success: function (data) {
            // $('#auction_location').append(new Option(data['auction_locations']));
            $('#auction_location').empty();
            $.each(data['auction_locations'], function (val, text) {
                $('#auction_location').append(
                    $('<option></option>').val(text.auction_location).html(text.state + ' - '+ text.auction_location)
                );
            });

            console.log('data success')
            // if (data['result'] == 'success') {
            //     $('#total_cost').text(data['total_cost'])
            // } else if (data['result'] == 'error') {
            //     console.log('data error');
            // }
        },
        error: function (err) {
            console.log('function error result ' + err);
        }
    });
});
