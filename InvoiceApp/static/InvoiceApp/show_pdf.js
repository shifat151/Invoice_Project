const alertBox = document.getElementById('alert-box');
const handleAlerts = (type, text) => {
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                          ${text}
                        </div>`

}

$(document).ready(function () {


    $('#send_pdf_form').on('submit', function (e) {
        e.preventDefault();
        var data = new FormData($('#contact-form').get(0));
        var formURL = $(this).attr('data-url')

        $.ajax({
            url: formURL,
            method: "POST",
            data: data,
            success: function (response) {

                // console.log(response['ajax_mess']['success'])
                handleAlerts('success', response['ajax_mess']['success']);

            },
            error: function (response) {
                // console.log(response.responseJSON['ajax_mess']['danger'])
                handleAlerts('danger', response.responseJSON['ajax_mess']['danger']);

            },
            processData: false,
            contentType: false,
        });
    });
    $("input[type='text'], input[type='file']").change(function () {
        $('.alert:visible').delay(1000).fadeOut(30)
    });

});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});