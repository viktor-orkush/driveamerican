$("#contact_form_btn").on('click', function () {
    $.ajax({
        url: '/contact/',
        type: "POST",
        data: $('#contact_form').serialize(),
        success: function (data) {
            if (data['result'] == 'success') {
                $('#contact_form_id').modal('hide')
                show_alert(data['message']);
                console.log('ok');
                $('#contact_form input').val('');
            } else if (data['result'] == 'error') {
                console.log('error');
            }
        },
        error : function(err) {
            console.log('error result ' + err);
            show_alert("Вы уже сделали запрос!");
        }
    });
});

function show_alert(message) {
    $('#contact_form_alert').html('<div class="alert alert-success">' +
                            '<button type="button" class="close" data-dismiss="alert">&times;</button>' + message +
                            '<div>');
    $(".alert").delay(3000).fadeOut(
      "normal",
      function(){
        $(this).remove();
      });
}

