window.addEventListener('load', function() {
    (function($) {
        var paginator = $(".paginator");
        var list_per_page = $("<select id='list_per_page_selector'><option value=\"1\">1</option><option value=\"2\" selected>2</option><option value=\"150\">150</option><option value=\"200\">200</option><option value=\"250\">250</option></select>")

        var url = new URL(window.location);
        var initial_list_per_page = url.searchParams.get("list_per_page")
        paginator.append(list_per_page)
        if(initial_list_per_page === null) {
            $("#list_per_page_selector").val("10")
        }
        else{
            $("#list_per_page_selector").val(initial_list_per_page)
        }
        $("#list_per_page_selector").on("change", function(event) {
            url.searchParams.set("list_per_page", event.target.value);
            window.location.href = url.href;
        });

    })(django.jQuery);
});