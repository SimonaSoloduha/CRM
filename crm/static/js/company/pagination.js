window.addEventListener('load', function() {
    (function($) {
        var changelist_form = $(".admindatefilter");
        var user_list_per_page = $("<div class='paginator-select'><label for='list_per_page_selector'>Count elem: </label><select id='list_per_page_selector'><option value=\"1\">1</option><option value=\"50\" selected>50</option><option value=\"100\">100</option></select></div>");
        var url = new URL(window.location);
        user_list_per_page.insertAfter(changelist_form);

        if (url.searchParams.get('e') != null) {
            $('#list_per_page_selector').val(url.searchParams.get('e'));
        } else {
            $('#list_per_page_selector').val(-1);
        }

        $("#list_per_page_selector").on("change", function(event) {
            url.searchParams.set("e", event.target.value);
            window.location.href = url.href;
        });

    })(django.jQuery);
});