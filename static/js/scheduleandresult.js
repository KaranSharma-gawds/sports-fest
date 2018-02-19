$(document).ready(function() {
    var id = window.location.hash.substr(1);

    function Item1(link1) {
        var obj = '<a href="' + link1 + '" style="padding:20px;margin-bottom:10px; background-color:#1d1d1d;display:block; color:white; "><span> fixture</span></a>';

        obj = $.parseHTML(obj);
        return obj[0];
    }

    function Item2(link2) {
        var obj = '<a href="' + link2 + '"style="padding:20px;margin-bottom:10px;  background-color:#1d1d1d;display:block; color:white; "><span> result</span></a>';
        obj = $.parseHTML(obj);
        return obj[0];
    }
    $.ajax({
        url: "http://localhost:8080/api/day/get/" + id,
        method: "GET",
        success: function(data) {
            // var templateData = [];
            // console.log(templateData);
            $("#event_name").append(data.name);
            var obj = {};
            obj.link1 = data.fixture_pdf;
            obj.link2 = data.result_pdf;
            // templateData.push(obj);
            $('#pdf1').append(Item1(obj.link1));
            $('#pdf2').append(Item2(obj.link2));


        }
    });
});