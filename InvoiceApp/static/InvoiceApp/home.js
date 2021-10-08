$(function () {

    $(".form-check-input").on("change", function () {



        var filterObj = {}
        $(".form-check-input").each(function (index, ele) {
            var filterKey = $(this).data('filter');
            filterObj[filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + filterKey + ']:checked')).map(function (el) {
                return el.value;
            });
        });


        $.ajax({
            url: 'invoice/filter-status/',
            data: filterObj,
            dataType: 'json',
            success: function (data) {
                console.log(data)
                $("#table_data").html(data.invoices);

            },
            error: function (response) {
                $("#table_data").html("<p>Sorry! No invoice was found!</p>");

            },
        });

    });
});