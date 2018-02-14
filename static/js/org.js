$(document).ready(function() {
    function Item2(name, designation, institute, image_url) {
        var obj = '<div class="col-12 col-md-3 profile_card" style="margin-bottom:30px"><div class="card card_style" style=""><img class="card-img-top" src="static/photos/' + image_url + '" alt="Card image cap"><div class="card-body" style="text-align:center"><h4 class="card-text">' + name + '</h4><h6 class="card-text">' + designation + '</h6><p class="card-text">' + institute + '</p></div></div></div>';
        // var obj = '<div class="event-card-2" onclick=location.href="' + link + '"><span>' + name + '</span></div>';
        obj = $.parseHTML(obj);
        return obj[0];
    }

    $.ajax({
        dataType: "json",
        // url: "https://5a5b96f44611170012fe752c.mockapi.io/api/profile",
        url: "http://localhost:8080/api/people/get",
        method: "GET",
        success: function(data) {
            var templateData = [];
            $.each(data.array, function(k, v) {
                var obj = {};
                obj.image_url = v.image_url;
                obj.name = v.name;
                obj.designation = v.designation;
                obj.institute = v.institution;
                templateData.push(obj);
            });
            templateData.forEach(function(k) {
                $('.organiser_container_new').append(Item2(k.name, k.designation, k.institute, k.image_url));

            });
        }
    });
});