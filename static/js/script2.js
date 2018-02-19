$(document).ready(function() {


    function Item(id, name) {
        // var obj = '<div class="col-12 col-md-4"><div class="event-card-2" onclick=location.href="' + link + '"><span><p>' + name + '</p></span></div></div>';
        var obj = '<div class="col-12 col-md-3 "><div class="card insti-card"><p>' + name + '</p></div></div>'
        obj = $.parseHTML(obj);
        return obj[0];
    }
    $.ajax({
        dataType: "json",
        // url: "https://5a5b96f44611170012fe752c.mockapi.io/api/event",
        url: "/api/institute/get",

        method: "GET",
        success: function(data) {
            console.log("printing data:", data.array[0].college_id);

            var templateData = [];
            $.each(data.array, function(k, v) {
                var obj = {};
                //storing link for a spcific event in link variable
                obj.id = v.college_id;
                obj.name = v.college_short;
                // console.log(v.name); // console.log("k.start_name");
                templateData.push(obj);

            });
            templateData.forEach(function(k) {
                console.log(k);
                $('#participants').append(Item(k.id, k.name));
            });

        }
    });
});