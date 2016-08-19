function toAction(action, loading) {
    if (loading != 'N') {
        $('#divPageLoading').show();
    }
    document.forms["navForm"].action = action;
    document.forms["navForm"].submit();
}


function toNav(app, action, params, mode, loading) {
    if (loading != 'N') {
        $('#divPageLoading').show();
    }
    document.forms["navForm"].navForm_pageApp.value = app == undefined ? '' : app;
    document.forms["navForm"].navForm_pageAction.value = action == undefined ? '' : action;
    document.forms["navForm"].navForm_pageParams.value = params == undefined ? '' : params;
    document.forms["navForm"].navForm_pageMode.value = mode == undefined ? '' : mode;
    document.forms["navForm"].submit();
}

function toNavWith(form, app, action, params, mode, loading) {
    if (loading != 'N') {
        $('#divPageLoading').show();
    }
    var cust_form = document.forms[form];
    cust_form.navForm_pageApp.value = app == undefined ? '' : app;
    cust_form.navForm_pageAction.value = action == undefined ? '' : action;
    cust_form.navForm_pageParams.value = params == undefined ? '' : params;
    cust_form.navForm_pageMode.value = mode == undefined ? '' : mode;
    cust_form.submit();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

String.format = function () {
    if (arguments.length == 0)
        return null;
    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
};