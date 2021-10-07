$(function () {

    $("#id_start_date, #id_end_date").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "2000:2040",
        dateFormat: "yy-mm-dd",
        defaultDate: '',
        showAnim: "slideDown",

    });

    $("#id_start_date").on("change", function () {

        var startdate = $('#id_start_date').datepicker('getDate');
        $('#id_end_date').datepicker("option", "minDate", startdate);

    });
    $("#id_end_date").on("change", function () {

        var enddate = $('#id_end_date').datepicker('getDate');
        $('#id_start_date').datepicker("option", "maxDate", enddate);

    });

});



