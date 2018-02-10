console.log("hey")
$(document).ready(function() {
    var loginpage = "signin";
    var $logout = $("#logout");

    $logout.on("submit", function(e) {
        console.log('somethif');
        $.ajax({
            url: "http://localhost:8080/api/user/logout",
            method: "POST",
            data: data,
            success: function(data) {
                console.log(data);
                if (data.status == 'OK') {
                    // localStorage.setItem("jwtToken",data.jwtToken);
                    // localStorage.setItem("_id",data._id);
                    window.location = loginpage;
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