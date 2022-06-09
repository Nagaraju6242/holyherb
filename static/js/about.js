let root = document.documentElement;

window.scrollTo(0, 0);
max_scroll = $(document).height() - $(window).height();
about_text_height = $(".text-about").height() + 10;
$(".text-about").css("bottom", "-" + about_text_height + "px");
const n = 9;

mobile = true ? window.innerWidth <= 450 : false

function scrolled() {
  scroll_per = $(window).scrollTop() / max_scroll;
  if (scroll_per < 1 / n) {
    $(".dark-film").css("opacity", scroll_per * (n - 2));
    $(".logo-about").css("opacity", 0);
    $(".text-about").css("bottom", "-1600px");
  } else if (scroll_per < 2 / n) {
    $(".logo-about").css("opacity", (scroll_per - 1 / n) * n);
    if(mobile){
      $(".logo-about").css("width", "50vw");
      $(".logo-about").css("height", "50vw");
    }else{
      $(".logo-about").css("width", "50vh");
      $(".logo-about").css("height", "50vh");
    }
    $(".logo-about").css("top", "50%");
    $(".text-about").css("bottom", "-40%");
  } else if (scroll_per < 3 / n) {
    $(".logo-about").css("opacity", "100%");
    x = (scroll_per - 2 / n) * (n * 100);

    if(mobile){
      $(".logo-about").css("width", 50 - x / 4 + "vw");
      $(".logo-about").css("height", 50 - x / 4 + "vw");
    }
    else{
      $(".logo-about").css("width", 50 - x / 4 + "vh");
      $(".logo-about").css("height", 50 - x / 4 + "vh");
    }
    $(".logo-about").css("top", 50 - x / 3.33 + "%");
    $(".text-about").css("bottom", -40 + x / 1.81818 + "%");
  } else if (scroll_per < 4 / n) {
  } else if (scroll_per < 5 / n) {
    x = (scroll_per - 4 / n) * n;
    $(".logo-about").css("opacity", 1 - x);
    $(".text-about").css("opacity", 1 - x);
  } else if (scroll_per < 6 / n) {
    root.style.setProperty("--sample-png", "url(" + js_urls.sample + ")");
    $(".logo-about").css("opacity", 0);
    $(".text-about").css("opacity", 0);
    x = (scroll_per - 5 / n) * n;
    x /= n / 2;
    $(".dark-film").css("opacity", 5 / n + x);
  } else if (scroll_per < 7 / n) {
    $(".dark-film").css("opacity", 1);
  } else if (scroll_per < 8 / n) {
    console.log("Should Change");
    root.style.setProperty("--sample-png", "url(" + js_urls.sample_2 + ")");
    x = (scroll_per - 7 / n) * n;
    $(".dark-film").css("opacity", 1 - x);
    $(".values-about").css("bottom", 0);
    $(".values-about").css("transform", "translateY(100%)");
  } else {
    x = (scroll_per - 8 / n) * n;
    $(".values-about").css("bottom", x * 50 + "%");
    k = 100 - x * 50;
    $(".values-about").css("transform", "translateY(" + k + "%)");
  }
}

$(window).scroll(scrolled);

if ($(".header").length > 0) {
  var last_scroll_top = 0;
  $(window).on("scroll", function () {
    scroll_top = $(this).scrollTop();
    if (window.innerWidth > 500) {
      if (scroll_top < last_scroll_top) {
        $(".header").css("top", "0");
      } else {
        $(".header").css("top", "-100%");
      }
    }
    last_scroll_top = scroll_top;
  });
}
