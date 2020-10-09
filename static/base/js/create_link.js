function create_link(api, link) {
    $.ajax({
        type: "POST",
        url: api,
        data: {
            csrfmiddlewaretoken: csrf,
            'link': link,
        },
        dataType: "json",
        error: function(jqXHR, exception) {
            $('#toast-msg-body').html('')
            let msg = '<div class="mt-2">Short link failed:</div>'
            $('#toast-msg-body').append(msg)
            if (jqXHR.status === 0) {
                msg = 'Not connected.\n Verify Network.'
            } else if (jqXHR.status == 404) {
                msg = 'Requested page not found. [404]'
            } else if (jqXHR.status == 500) {
                msg = 'Internal Server Error [500].'
            } else if (jqXHR.status == 403) {
                msg = 'CSRF Failed: CSRF token missing or incorrect. [403].'
            } else if (exception === 'parsererror') {
                msg = 'Requested JSON parse failed.'
            } else if (exception === 'timeout') {
                msg = 'Time out error.'
            } else if (exception === 'abort') {
                msg = 'Ajax request aborted.'
            } else {
                msg = 'Uncaught Error.\n' + jqXHR.responseText
            }
            $('#toast-strong').html()
            $('#toast-strong').html('Failed creating link')
            msg = '<div class="mt-2">' + msg + '</div>'
            $('#toast-msg-body').append(msg)
            msg = '<div class="mt-2">' + JSON.parse(jqXHR.responseText).msg + '</div>'
            $('#toast-msg-body').append(msg)
            $('.btn-clip').addClass('disabledbutton')
            $('#toast').toast('show');
        },
        success: function(data) {
            $('#toast-strong').html()
            $('#toast-strong').html('Link created successfully')
            $('#toast-msg-body').html('')
            let link = data['link']
            let msg = '<div class="mt-2">You can now copy this link:</div>'
            $('#toast-msg-body').append(msg)
            msg = '<input id=short-link value="' + link + '" class="container-fluid"></input>'
            $('#toast-msg-body').append(msg)
            $('.btn-clip').removeClass('disabledbutton')
            $('#toast').toast('show');
        },
    });
}