var pswpElement = document.querySelectorAll('.pswp')[0];
var items = [{}];

function Item(url) {
    // var obj = '<div class="col-12 col-md-4"><div class="event-card-2" onclick=location.href="' + link + '"><span><p>' + name + '</p></span></div></div>';
    var obj = "{src: " + url + ", w: 600, h:400},"
    obj = $.parseHTML(obj);
    return obj[0];
}
$.ajax({
    dataType: "json",
    // url: "https://5a5b96f44611170012fe752c.mockapi.io/api/event",
    url: "/api/upload/image/get",

    method: "GET",
    success: function(data) {
        console.log("printing data:", data.array);

        var item = [{}];
        $.each(data.array, function(k, v) {
            console.log("k is :" + k);
            console.log("v is :" + v);
            items.push({
                'src': v,
                'w': 600,
                'h': 400
            });
            // var obj = {};
            //storing link for a spcific event in link variable
            // obj.id = v.college_id;
            // obj.name = v.college_name;
            // obj.url = v
            // console.log(v.name); // console.log("k.start_name");
            // item.push(obj);

        });
        // console.log("item is" + item);
        // item.forEach(function(k) {
        //     console.log("k is" + k);
        //     items.append(Item(k));
        // });

    }
});
console.log("items are" + items);

// define options (if needed)
var options = {
    // optionName: 'option value'
    // for example:
    index: 0 // start at first slide
};

// Initializes and opens PhotoSwipe
var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
gallery.init();