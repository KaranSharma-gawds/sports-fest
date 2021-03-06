$(document).ready(function() {


    $('#fullpage').fullpage({
        // scrollOverflow: true,
        // scrollingSpeed: 700,
        responsiveWidth: 1100,
        anchors: ['firstPage', 'secondPage', 'thirdPage', 'fourthPage', 'fifthPage']
    });



    function Item(link, name) {
        var obj = '<div class="col-12 col-md-3"><div class="event-card-2" onclick=location.href="' + link + '"><span><p>' + name + '</p></span></div></div>';
        obj = $.parseHTML(obj);
        return obj[0];
    }
    $.ajax({
        dataType: "json",
        // url: "https://5a5b96f44611170012fe752c.mockapi.io/api/event",
        url: "/api/event/2016/get",

        method: "GET",
        success: function(data) {
            // console.log("printing data:", data.array[0].name);

            var templateData = [];
            $.each(data.array, function(k, v) {
                var obj = {};
                //storing link for a spcific event in link variable
                obj.link = "event#" + v.id;
                obj.name = v.name;
                // console.log(v.name); // console.log("k.start_name");
                templateData.push(obj);

            });
            templateData.forEach(function(k) {
                $('#evento').append(Item(k.link, k.name));
            });

        }
    });

    $(".event-card-2").click(function() {
        window.location = $(this).find("a").attr("href");
        return false;
    });
});