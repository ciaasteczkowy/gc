$( document ).ready(function() {
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
    });

    $.getJSON( "/accounts", function( data ) {
        var accounts = data;
        console.log(accounts);

        var $input = $('.typeahead');
        $input.typeahead({source: accounts,
                autoSelect: true});
        $input.change(function() {
            var current = $input.typeahead("getActive");
            if (current) {
                // Some item from your model is active!
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
    });
});