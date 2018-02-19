console.log("hey")
$(document).ready(function() {
    var dashboard = "dashboard";
    var $form = $("#loginForm");

    $form.on("submit", function(e) {
        var data = $form.serialize();
        console.log(data);
        $.ajax({
            url: "/api/user/login",
            method: "POST",
            data: data,
            success: function(data) {
                console.log(data);
                if (data.status == 'OK') {
                    // localStorage.setItem("jwtToken",data.jwtToken);
                    // localStorage.setItem("_id",data._id);
                    window.location = dashboard;
                }
            },
            //   error:function(data){
            // console.log(data);
            //   }
        });
        e.preventDefault();
    });

    function successFunction() {
        window.location = dashboard;
    }
});