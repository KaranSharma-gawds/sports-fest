$(document).ready(function() {

    var items = [{
            src: 'localhost:8080/static/photos/image.jpg',
            w: 600,
            h: 400
        }
    }];
// console.log(items);
//ajax
$.ajax({
    dataType: "json",
    // url: "http://5a5b96f44611170012fe752c.mockapi.io/api/notification",
    url: "http://localhost:8080/api/upload/image/get/1",
    method: "GET",
    success: function(data) {

        for (var i = 0; i < data.array.length; i++) {

            var url = `${data.array[i]}`
                // console.log("url is:" + url);
            var x = "{src: " + url + ", w: 600, h:400},"

            $(items).append(x);


        }
        console.log(data.array[i]);
        console.log("x is :" + x);
    }
});

var pswpElement = document.querySelectorAll('.pswp')[0];




// build items array


// define options (if needed)
var options = {
    // optionName: 'option value'
    // for example:
    index: 0 // start at first slide
};

// Initializes and opens PhotoSwipe
var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options); gallery.init();


});