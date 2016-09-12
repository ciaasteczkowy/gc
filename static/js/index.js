$( document ).ready(function() {
    loadData();

    $.notifyDefaults({
        placement: {
            from: "bottom",
            align: "center"
        },
        delay: 2000,
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        }
    });

    $("#add_entry_form").ajaxForm(
        {
            success: function(response, status, xhr, $form) {
                response = JSON.parse(response);
                if (response['status'] == 'success')
                    loadData();
                else
                    var notify = $.notify(response['error']);
            },
            beforeSubmit: function(formData, jqForm, options) {
                var queryString = $.param(formData);
                console.log(formData);
                console.log(queryString);
            }
        }
    );
});

function loadData() {
    $.getJSON( "/data", function( data ) {
        $('#income').text(data['income']);
        if (data['income'] > 0) {
            $('#income').addClass('balance-positive');
        } else {
            $('#income').addClass('balance-negative');
        }

       $('#expense').text(data['expense']);
        if (data['expense'] > 0) {
            $('#expense').addClass('balance-positive');
        } else {
            $('#expense').addClass('balance-negative');
        }

        $('#balance').text(data['balance']);
        if (data['balance'] > 0) {
            $('#balance').addClass('balance-positive');
        } else {
            $('#balance').addClass('balance-negative');
        }

        $.each(data['splits'], function(i, item) {
            var $item = $('.split-item:first').clone();
            $item.find('span.split-amount').text(item['amount']);
            $item.find('span.split-account').text(item['account']);
            $item.appendTo('.split-list');
            console.log(item);
        });

        $('.split-item:first').remove();

        var accounts = data['accounts'];

        var $input = $('.typeahead');
        $input.typeahead({source: accounts,
                autoSelect: true});
        $input.change(function() {
            var current = $input.typeahead("getActive");
            if (current) {
//                $input.val(current.shortname);
                if (current.name == $input.val()) {
                    // This means the exact match is found. Use toLowerCase() if you want case insensitive match.
                } else {
                    // This means it is only a partial match, you can either add a new item
                    // or take the active if you don't want new items
                }
            } else {
                // Nothing is active so it is a new value (or maybe empty value)
            }
        });
    }).fail(function(jqxhr, textStatus, error) {
        var error = jqxhr['responseJSON']['error'];
        console.log(error);
        var notify = $.notify(
            { message: "<strong>Błąd: </strong>" + error },
            { type: 'danger' }
        );
    });
}