$(document).ready(function() {



    $('#fullpage').fullpage({
        // scrollOverflow: true,
        scrollingSpeed: 700,
        responsiveWidth: 1100
    });


    function Item(link, name) {
        var obj = '<div class="col-12 col-md-4"><div class="event-card-2" onclick=location.href="' + link + '"><span>' + name + '</span></div></div>';
        obj = $.parseHTML(obj);
        return obj[0];
    }
    $.ajax({
        dataType: "json",
        // url: "https://5a5b96f44611170012fe752c.mockapi.io/api/event",
        url: "http://localhost:8080/api/event/2016/get",

        method: "GET",
        success: function(data) {
            // console.log("printing data:", data.array[0].name);

            var templateData = [];
            $.each(data.array, function(k, v) {
                var obj = {};
                //storing link for a spcific event in link variable
                obj.link = "event#" + v.id;
                obj.name = v.name;
                // console.log(v.name); // console.log("k.start_name");
                templateData.push(obj);

            });
            templateData.forEach(function(k) {
                $('#evento').append(Item(k.link, k.name));
            });

        }
    });

    $(".event-card-2").click(function() {
        window.location = $(this).find("a").attr("href");
        return false;
    });





    $('.responsive').slick({
        arrows: true,
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 4,
        slidesToScroll: 4,
        responsive: [{
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                }

            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
            // You can unslick at a given breakpoint now by adding:
            // settings: "unslick"
            // instead of a settings object
        ]
    });
    $('.slick-frame').on('init', function() {
        $slickFrame.css({ visibility: 'visible' });
    });
    $('.slick-frame').slick()
});