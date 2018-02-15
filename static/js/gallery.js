$(document).ready(function() {
    //ajax
    $.ajax({
        dataType: "json",
        // url: "http://5a5b96f44611170012fe752c.mockapi.io/api/notification",
        url: "http://localhost:8080/api/upload/photos/get/1",
        method: "GET",
        success: function(data) {
            console.log(data);
            for (var i = 0; i < data.array.length; i++) {
                var url = `/static/photos/${data.array[i]}`
                var x = "<div class='col-12 notification'><span>" + data.array[i] + "<span class='badge badge-secondary'>New</span></span><a style='position:absolute; right:10px' class='btn btn-primary download-btn' href='" + url + "'" + "role='button'>Download</a></div>";
                // var y ="<div class='card card-body noti-card'> " +data[i].file_link +"</div>"
                // $("#notification_div").append(x);

                // var $button = $("a.download-btn");

                // $button.on("click", function(data){
                // 	var link=document.createElement('a');
                //       link.href=window.URL.createObjectURL(data);
                //       link.click();
                // })
                items.append(x);


            }
        }
    });

    var pswpElement = document.querySelectorAll('.pswp')[0];



    console.log("hey");
    // build items array
    var items = [
        //     {src: 'localhost:8080/static/photos/image.jpg',
        //     w: 600,
        //     h: 400
        // },
        // {
        //     src: 'http://fakeimg.pl/350x200/?text=this',
        //     w: 600,
        //     h: 400
        // },
        // {
        //     src: 'http://fakeimg.pl/350x200/?text=is',
        //     w: 600,
        //     h: 400
        // },
        // {
        //     src: 'http://fakeimg.pl/350x200/?text=gallery',
        //     w: 600,
        //     h: 400
        // },
        // {
        //     src: 'http://fakeimg.pl/350x200/?text=thank',
        //     w: 600,
        //     h: 400
        // },
        // {
        //     src: 'http://fakeimg.pl/350x200/?text=you',
        //     w: 600,
        //     h: 400
        // },
    ];

    // define options (if needed)
    var options = {
        // optionName: 'option value'
        // for example:
        index: 0 // start at first slide
    };

    // Initializes and opens PhotoSwipe
    var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
    gallery.init();


});