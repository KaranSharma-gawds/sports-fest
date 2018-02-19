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
            $("#time").append(data.event.start_time);
            $("#date").append(data.event.day);


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

});