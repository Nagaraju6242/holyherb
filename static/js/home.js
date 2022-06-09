products_scroll = document.querySelector(".products_scroll");
left_button = document.querySelector(".products_scroll .left");
right_button = document.querySelector(".products_scroll .right");

left_button.style.opacity = 0.5;
var Mainsplide = null;

var charcoax_video = true
var charcoax_playing = true
var recipe_video = true
var recipe_playing = true

$(".charcoax .video-holder .button-holder").on("click", function () {
  if(charcoax_playing){
    $(".charcoax video")[0].pause();
    $(".charcoax .button-holder .play-or-pause").removeClass("paused");
    charcoax_playing = false;
  }else{
    $(".charcoax video")[0].play();
    $(".charcoax .button-holder .play-or-pause").addClass("paused");
    charcoax_playing = true;
  }
});

$(".neem .video-holder .button-holder").on("click", function () {
  if (recipe_playing) {
    $(".neem video")[0].pause();
    $(".neem .button-holder .play-or-pause").removeClass("paused");
    recipe_playing = false;
  } else {
    $(".neem video")[0].play();
    $(".neem .button-holder .play-or-pause").addClass("paused");
    recipe_playing = true;
  }
});

$(".charcoax .video-holder video").on("ended",function(){
  charcoax_playing = false;
  $(".charcoax .button-holder .play-or-pause").removeClass("paused");
})

$(".neem .video-holder video").on("ended", function () {
  recipe_playing = false;
  $(".neem .button-holder .play-or-pause").removeClass("paused");
});

$(".products_scroll img").attr("draggable", false);
$(".ii-container img").attr("draggable", false);

var last_scroll_top = 0;
$(window).on("scroll", function () {
  scroll_top = $(this).scrollTop();
  if (window.innerWidth > 500) {
    if (scroll_top < last_scroll_top) {
      $(".go-to-top").removeClass("scrolled-down").addClass("scrolled-up");
    } else {
      $(".go-to-top").removeClass("scrolled-up").addClass("scrolled-down");
    }
  }
  last_scroll_top = scroll_top;
  const vid = $("section.neem video")[0];
  vid_bottom = vid.getBoundingClientRect().bottom;
  if (vid_bottom < window.innerHeight && vid_bottom > 0) {
    if (recipe_video) {
      vid.play();
      recipe_playing = false;
      $(".neem .button-holder .play-or-pause").addClass("paused");
      recipe_video = false;
    } 
  } 
  const about_vid = $(".charcoax-main .video-holder video")[0];
  vid_bottom = about_vid.getBoundingClientRect().bottom;
  if (vid_bottom < window.innerHeight && vid_bottom > 0) {
    if (charcoax_video)
    {
      about_vid.play();
      charcoax_playing = false;
      $(".charcoax .button-holder .play-or-pause").addClass("paused");
      charcoax_video = false;
    } 
  } 
});

function change() {
  return {
    left: Math.random() * 100,
    top: Math.random() * 100,
    rotation: Math.random() * 360,
  };
}

function animate_leaves(selector) {
  $(selector).each(function (index) {
    leaf = $(this);
    data = change();
    leaf.css("top", data.top + "%");
    leaf.css("left", data.left + "%");
    leaf.css("transform", "rotate(" + data.rotation + "deg)");
  });
}

add_leafs(20, document.querySelector(".leaf-container"), -1);
add_leafs(10, document.querySelector(".choose"), 0);
setTimeout(function () {
  animate_leaves(".leaf-container img");
}, 1000);
setInterval(function () {
  animate_leaves(".leaf-container img");
}, 31000);
setTimeout(function () {
  animate_leaves(".choose img");
}, 1000);
setInterval(function () {
  animate_leaves(".choose img");
}, 31000);

function add_leafs(n, parent, zindex) {
  for (i = 0; i < n; i++) {
    var ele = document.createElement("img");
    ele.src = js_urls.leaf;
    ele.alt = "Leaf";
    ele.style.position = "absolute";
    ele.style.top = Math.random() * 100 + "%";
    ele.style.left = Math.random() * 100 + "%";
    ele.style.zIndex = zindex;
    ele.style.width = 20 + Math.random() * 20 + "px";
    ele.style.transform = "rotate(" + Math.random() * 360 + "deg)";
    ele.draggable = false;
    parent.appendChild(ele);
  }
}


$(".join-our-circle-form").submit(function (e) {
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    method: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (data) {
      if (data.success) {
        $.alert({
          title: "Success",
          content: "You are Now Subscribed",
          theme: "modern",
        });
      } else {
        $.alert({
          title: "Oops !!",
          content: data.msg,
          theme: "modern",
        });
      }
      thisForm.find("input[type='email']").val("");
    },
    error: function (errorData) {
      console.log(errorData);
      $.alert({
        title: "Oops !!",
        content: "An error Occured",
        theme: "modern",
      });
    },
  });
});

function changeSlide(pos) {
  pos = parseInt(pos);
  Mainsplide.go(pos - 1);
}

$(document).ready(function () {
  var innerLines = document.querySelectorAll(".line .inner-line");
  Mainsplide = new Splide("#herobannersplide", {
    autoplay: true,
    interval: 4000,
    pauseOnHover: false,
    drag: false,
    rewind: true,
    resetProgress: false,
  }).mount();

  var iisplide = new Splide("#ii-splide", {
    type: "fade",
    speed: 500,
    lazyLoad: "nearby",
    drag: false,
  }).mount();

  var products_splide = new Splide("#products-splide", {
    autoWidth: true,
    lazyLoad: "sequential",
    breakpoints: {
      650: {
        autoWidth: false,
        perPage: 1,
        padding: {
          right: "10rem",
          left: "10rem",
        },
      },
    },
  }).mount();

  $(".ingredient-index .nex").click(function () {
    iisplide.go("+");
  });

  $(".ingredient-index .pre").click(function () {
    iisplide.go("-");
  });

  $(".ii-box p").mouseenter(function () {
    $(".ii-box").addClass("dark");
  });

  $(".ii-box p").mouseleave(function () {
    $(".ii-box").removeClass("dark");
  });

  $(".main-carousel .next").click(function () {
    Mainsplide.go("+");
  });

  $(".main-carousel .prev").click(function () {
    Mainsplide.go("-");
  });

  innerLines[0].classList.add("loading");
  Mainsplide.on("move", refreshCarouselAnim);

  products_splide.on("move", function (e) {
    if (e === 0) {
      left_button.style.opacity = 0.5;
    } else {
      left_button.style.opacity = 1;
    }

    if (e === $(".products_scroll_div").length - 1) {
      right_button.style.opacity = 0.5;
    } else {
      right_button.style.opacity = 1;
    }
  });

  iisplide.on("move", function (e) {
    if (e === 0) {
      $(".ingredient-index .pre").removeClass("active");
    } else {
      $(".ingredient-index .pre").addClass("active");
    }
    if (e === $(".ingredient-index li.splide__slide").length - 1) {
      $(".ingredient-index .nex").removeClass("active");
    } else {
      $(".ingredient-index .nex").addClass("active");
    }
  });

  left_button.onclick = function () {
    products_splide.go("-");
  };

  right_button.onclick = function () {
    products_splide.go("+");
  };

  function refreshCarouselAnim(e) {
    var current_slide_in_loop = e;
    const total_length = $("#herobannersplide ul li.splide__slide").length;
    if (current_slide_in_loop == 0) {
      $(".prev").removeClass("active");
    } else {
      $(".prev").addClass("active");
    }
    if (current_slide_in_loop == total_length - 1) {
      $(".next").removeClass("active");
    } else {
      $(".next").addClass("active");
    }
    if (current_slide_in_loop != 0) {
      for (i = 0; i < total_length; i++) {
        innerLines[i].classList.remove("filled", "loading");
      }
      for (i = 0; i < current_slide_in_loop; i++) {
        innerLines[i].classList.add("filled");
      }
      innerLines[current_slide_in_loop].classList.add("loading");
    } else {
      for (i = 0; i < total_length; i++) {
        innerLines[i].classList.remove("filled", "loading");
      }
      innerLines[0].classList.add("loading");
    }
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

window.onload = function () {
  setTimeout(() => {
    const offerBannerDismissed = getCookie("offerBannerDismissed");
    if (offerBannerDismissed == "false") {
      $("#offerBannerModal").modal("show");
    }
  }, 5000);
};

function pauseAnimation() {
  Mainsplide.Components.Autoplay.pause();
  $(".locate-lines *").css("animation-play-state", "paused");
}

function resumeAnimation() {
  Mainsplide.Components.Autoplay.play();
  $(".locate-lines *").css("animation-play-state", "running");
  el = $(".line .inner-line.loading")[0];
  // el.style.animation = "none";
  // el.offsetHeight; /* trigger reflow */
  // el.style.animation = null;
}

function setCookie(cName, cValue, expDays) {
  let date = new Date();
  date.setTime(date.getTime() + expDays * 24 * 60 * 60 * 1000);
  const expires = "expires=" + date.toUTCString();
  document.cookie = cName + "=" + cValue + "; " + expires + "; path=/";
}

function closeOfferBanner() {
  $("#offerBannerModal").modal("hide");
  setCookie("offerBannerDismissed", "true", 10);
}

$("#offerBannerModal").click(function (e) {
  if (e.target != this) return;
  closeOfferBanner();
});
