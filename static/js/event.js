console.log("check")

$(document).ready(function(){
	var id = window.location.hash.substr(1);
	console.log(id);

		$.ajax({
			url: "http://localhost:8080/api/event/2016/get/" + id,
			method: "GET",
			success:function(data){
				console.log(data.event);
				$("#event_name").append(data.event.name);
				$("#institute_name").append(data.event.venue);
				$("#time").append(data.date);
				$("#date").append(data.start_time);
				$("#win1_name").append(data.win1);
				$("#win1_inst").append(data.win1_inst);
				$("#win2_name").append(data.win2);
				$("#win2_inst").append(data.win2_inst);
				$("#win3_name").append(data.win3);
				$("#win3_inst").append(data.win3_inst);

			}
		});
		
	});


