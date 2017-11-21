String.prototype.formatUnicorn = String.prototype.formatUnicorn ||
function () {
    "use strict";
    var str = this.toString();
    if (arguments.length) {
        var t = typeof arguments[0];
        var key;
        var args = ("string" === t || "number" === t) ?
            Array.prototype.slice.call(arguments)
            : arguments[0];

        for (key in args) {
            str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
        }
    }

    return str;
};

$(document).on('show.bs.modal', '#myModal', function (event) {
    var button = $(event.relatedTarget);
    var url = button.data('link');
    var modal = $('#myModal');
    $.get(url, function (data) {
        modal.html(data)
    });
    $()
});

$(function () {
    $('.datepicker').datepicker()
});

function search() {
    $.ajax({
        url: '/books/search/',
        data: $('#search').serialize(),
        type: 'post',
        success: function (response) {
            var d="";
            console.log(response);
            var data = JSON.parse(response);
            for(i=0;i<data.length;i++){
                d+=bookcard(data[i].fields, data[i].pk)
            }
            console.log(d);
            var ob = $('#search_results');
            ob.removeClass('d-none');
            $('#search_results .row').html(d);
        }
    })
}

$(function () {
    $('#search').on("submit", function (event) {
    event.preventDefault();
    search();
});
});


function bookcard(details, pk) {
    var htm = "<div class=\"col-md-3\">\n" +
        "            <div class=\"card\">\n" +
        "                <div class=\"card-header\">\n" +
        "                    <h4 class=\"card-title\">{0}</h4>\n".formatUnicorn(details.title) +
        "                    <p class=\"card-subtitle\">{0}</p>\n".formatUnicorn(details.author) +
        "                </div>\n" +
        "                <div class=\"card-body\">\n" +
        "                    <p>Category: {0}</p>\n".formatUnicorn(details['category']) +
        "                    <p>Publisher: {0}</p>\n".formatUnicorn(details['publisher']) +
        "                </div>\n" +
        "                <div class=\"card-footer\">\n" +
        "                    <a class=\"btn btn-warning\" href='/books/view/"+ pk + "'>View</a>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "        </div>";
    return htm
}


$(document).ajaxStart(function(){
    $("#wait").css("display", "block");
});

$(document).ajaxComplete(function(){
    $("#wait").css("display", "none");
});