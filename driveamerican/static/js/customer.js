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
    setEqualHeight($(".privileges > div> .card"));
});


$('.calc-radio').click(function(){
    if (this.id === "petrol" || this.id === "diesel"){
        $('.calc-tab-panel').parent().find('div.tab-pane').removeClass('active')
        $('#tap_petrol').addClass('active')
    }
    // else if (this.id === 'diesel1'){
    //     $('.calc-tab-panel').parent().find('div.tab-pane').removeClass('active')
    //     $('#tap_diesel').addClass('active')
    // }
    else if (this.id === 'electro'){
        $('.calc-tab-panel').parent().find('div.tab-pane').removeClass('active')
        $('#tap_electro').addClass('active')
    }
    else if (this.id === 'hybrid'){
        $('.calc-tab-panel').parent().find('div.tab-pane').removeClass('active')
        $('#tap_hybrid').addClass('active')
    }
});

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
        error : function(err) {
            console.log('function error result ' + err);
            // show_alert("Вы уже сделали запрос!");
        }
    });
});
