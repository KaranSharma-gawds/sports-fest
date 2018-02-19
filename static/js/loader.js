var counter = 0;
var c = 0;
var i = setInterval(function() {
    $(".loading-page .counter h1").html(c + "%");
    $(".loading-page .counter hr").css("width", c + "%");
    //$(".loading-page .counter").css("background", "linear-gradient(to right, #f60d54 "+ c + "%,#0d0d0d "+ c + "%)");

    /*
    $(".loading-page .counter h1.color").css("width", c + "%");
    */
    counter++;
    c++;

    if (counter == 101) {
        clearInterval(i);
    }
}, 50);

$(document).ready(function() {

    /*====================================
  Preloader
======================================*/

    // $("#status").fadeOut("slow");

    // $("#preloader").delay(3000).fadeOut("slow").remove();
    $(".loading-page").fadeOut("slow");

    $(".counter").delay(3000).fadeOut("slow").remove();
});