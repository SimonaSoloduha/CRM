window.addEventListener('load', function() {
    (function($) {
        var changelist_form = $(".admindatefilter");
        var user_list_per_page = $("<div class='paginator-select'><label for='list_per_page_selector'>Count elem: </label><select id='list_per_page_selector'><option value=\"2\">2</option><option value=\"50\">50</option><option value=\"100\">100</option></select></div>");
        var url = new URL(window.location);
        user_list_per_page.insertAfter(changelist_form);

        if (url.searchParams.get('e') != null && url.searchParams.get('e') != 1) {
            $('#list_per_page_selector').val(url.searchParams.get('e'));
            localStorage['list_per_page_selector'] = url.searchParams.get('e');
        }
        if (localStorage['list_per_page_selector']) {
            $('#list_per_page_selector').val(localStorage['list_per_page_selector']);
        }

        $("#list_per_page_selector").on("change", function(event) {
            url.searchParams.set("e", event.target.value);
            window.location.href = url.href;
        });

        let er = $(".errorlist");
        let er_txt = er.find('li').text();

        if(er_txt) {
            $('.errorlist li').each(function () {
                this.classList.toggle('hide');
            });
        }

    })(django.jQuery);
});