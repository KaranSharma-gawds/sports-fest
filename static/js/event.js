console.log("check")

$(document).ready(function() {
    var id = window.location.hash.substr(1);
    console.log(id);

    $.ajax({
        url: "http://localhost:8080/api/event/2016/get/" + id,
        method: "GET",
        success: function(data) {
            console.log(data.event);
            $("#event_name").append(data.event.name);
            $("#institute_name").append(data.event.venue);



        }
    });
    $.ajax({
        url: "http://localhost:8080/api/result/get/" + id,
        method: "GET",
        success: function(data) {
            console.log(data.result.first_name);
            $("#win1_name").append(data.result.first_name);
            $("#win1_inst").append(data.result.first_institution);
            $("#win2_name").append(data.result.second_name);
            $("#win2_inst").append(data.result.second_institution);
            $("#win3_name").append(data.result.third_name);
            $("#win3_inst").append(data.result.third_institution);

        }
    });

    function Item(link, name) {
        // var obj = '<div class="col-12 col-md-4"><div class="event-card-2" onclick=location.href="' + link + '"><span><p>' + name + '</p></span></div></div>';
        var obj = '<div class="col-12 col-md-4"><a href="' + link + '" style="padding:20px;margin-bottom:10px; background-color:#1d1d1d;display:block; color:white; ">' + name + '</a></div>'
        obj = $.parseHTML(obj);
        return obj[0];
    }
    $.ajax({
        url: "http://localhost:8080/api/day/get/" + id,
        method: "GET",
        success: function(data) {
            console.log("day is:" + data.name);
            var templateData = [];
            $.each(data.array, function(k, v) {
                var obj = {};
                //storing link for a spcific event in link variable
                obj.link = "scheduleandresult#" + v.id;
                obj.name = v.name;
                // console.log(v.name); // console.log("k.start_name");
                templateData.push(obj);

            });
            templateData.forEach(function(k) {
                console.log(k);
                $('#days').append(Item(k.link, k.name));
            });



        }
    });

});