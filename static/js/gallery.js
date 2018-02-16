$(document).ready(function() {



    function Item(ob) {
        var link = ob.link;
        console.log(link);
        // var obj = '<div class="col-12 col-md-4"><div class="event-card-2" onclick=location.href="' + link + '"><span><p>' + name + '</p></span></div></div>';
        var obj = '<a href=' + link + '><div class="cell"><img class="responsive-image" src=' + link + ' /></div></a>'
        obj = $.parseHTML(obj);
        return obj[0];
    }
    $.ajax({
        dataType: "json",
        // url: "https://5a5b96f44611170012fe752c.mockapi.io/api/event",
        url: "http://localhost:8080/api/upload/image/get",

        method: "GET",
        success: function(data) {

            var templateData = [];
            $.each(data.array, function(k, v) {
                var obj = {};
                //storing link for a spcific event in link variable
                obj.link = v;

                // console.log(v.name); // console.log("k.start_name");
                templateData.push(obj);

            });
            templateData.forEach(function(k) {
                console.log(k);
                $('#lightgallery').append(Item(k));
                console.log("k is :" + k);
            });
            $("#lightgallery").lightGallery({
                thumbnail: true,
                mode: 'lg-fade',
                cssEasing: 'cubic-bezier(0.25, 0, 0.25, 1)'
            });

        }
    });
});