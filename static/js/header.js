search_form = document.querySelector(".search-form");
search_input = document.querySelector(".search_input");
main_img_2 = document.querySelector(".main_img_2");

var update_logos;
var search_show = false;

function submit_form() {
  if (search_show){
    if (search_input.value != "") {
      search_form.submit();
    }
  }else{
    search_show = true;
    $(".header .search_box").addClass("active");
  }
  
}

function adjust_font() {
  if (window.innerWidth > 800) {
    let x = (window.innerWidth / 1920) * 100;
    $("html").css("font-size", x + "%");
  } else if (window.innerWidth > 500) {
    let x = (window.innerWidth / 800) * 60;
    $("html").css("font-size", x + "%");
  } else {
    let x = (window.innerWidth / 500) * 60;
    $("html").css("font-size", x + "%");
  }
}

adjust_font();

window.onscroll = function () {
  if (window.innerWidth > 800) {
    if ($(window).scrollTop() >= $(window).height() * 0.75) {
      $(".header").addClass("short");
      $(".logo_img").attr("src", js_urls.short_logo);
      if (window.location.pathname == "/") {
        $(".go-to-top").addClass("active");
      }
    } else {
      $(".header").removeClass("short");
      $(".logo_img").attr("src", js_urls.logo);
      if (window.location.pathname == "/") {
        $(".go-to-top").removeClass("active");
      }
    }
  }
};

function toggleNav() {
  if (window.innerWidth <= 800) {
    if ($(".mobile-nav").hasClass("active")) {
      $(".mobile-nav").removeClass("active");
      $(".left_anim").css("opacity", "0");
    } else {
      $(".mobile-nav").addClass("active");
      $(".left_anim").css("opacity", "1");
    }
  }
}

function opendd(x) {
  if (["link-hair", "link-face", "link-body"].includes(x)) {
    $("#" + x).toggleClass("active");
  }
}

// Get cookie with it's name
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

function isElementInViewport(el) {
  var rect = el.getBoundingClientRect();

  return (
    rect.right > 0 &&
    rect.left <
      (window.innerWidth ||
        document.documentElement.clientWidth) /* or $(window).width() */ &&
    rect.top <
      (window.innerHeight ||
        document.documentElement.clientHeight) /* or $(window).height() */
  );
}

$(document).ready(function () {
  // Edit Profile Ajax
  $("#edit-profile-form").submit(function (e) {
    e.preventDefault();
    thisForm = $(this);
    $.ajax({
      type: thisForm.attr("method"),
      url: thisForm.attr("action"),
      data: thisForm.serialize(),
      success: function (response) {
        if(response.success){
          window.location.reload();
        }
        else{
          thisForm.find("small.errors").text(response.errors);
        }
      },
    });
  });

  //Cart and Wishlist Icons

  $(".header_icons .profile-icon .profile-dropdown a").click(function (e) {
    e.stopPropagation();
  });

  $(".header_icons .profile-icon .profile-dropdown").ready(function () {
    let x = $(".header_icons .profile-icon .profile-dropdown");
    x.width(x.height() * 0.866);
  });

  update_logos = function () {
    $.ajax({
      type: "POST",
      url: js_urls.api_length,
      data: "csrfmiddlewaretoken=" + csrftoken,
      success: function (response) {
        if (response.wishlist > 0) {
          src = $(".wishlist-logo img").attr("src");
          src2 = $(".wishlist_slide_page .cart_head_slide img").attr("src");
          if (src.includes("wishlist_full") == false) {
            src = src.replace("wishlist", "wishlist_full");
          }
          $(".wishlist-logo img").attr("src", src);
          if (src2.includes("wishlist_full") == false) {
            src2 = src2.replace("wishlist", "wishlist_full");
          }
          $(".wishlist_slide_page .cart_head_slide img").attr("src", src2);
        } else {
          src = $(".wishlist_slide_page .cart_head_slide img").attr("src");
          src = src.replace("wishlist_full", "wishlist");
          $(".wishlist_slide_page .cart_head_slide img").attr("src", src);

          src = $(".wishlist_slide_page .cart_head_slide img").attr("src");
          src = src.replace("wishlist_full", "wishlist");
          $(".wishlist_slide_page .cart_head_slide img").attr("src", src);
        }
        if (response.cart > 0) {
          src = $(".cart_home_button img").attr("src");
          if (src.includes("cart_full") == false) {
            src = src.replace("cart", "cart_full");
          }
          $(".cart_home_button img").attr("src", src);
          src = $(".cart_slide_page .cart_head_slide img").attr("src");
          if (src.includes("cart_full") == false) {
            src = src.replace("cart", "cart_full");
          }
          $(".cart_slide_page .cart_head_slide img").attr("src", src);
          $(".cart-number").css("display", "flex");
          $(".cart-number").text(response.cart);
        } else {
          src = $(".cart_home_button img").attr("src");
          src = src.replace("cart_full", "cart");
          $(".cart_home_button img").attr("src", src);
          src = $(".cart_slide_page .cart_head_slide img").attr("src");
          src = src.replace("cart_full", "cart");
          $(".cart_slide_page .cart_head_slide img").attr("src", src);
          $(".cart-number").css("display", "none");
        }
      },
    });
  };
  update_logos();

  add_leafs(40);

  function change() {
    return {
      left: Math.random() * 100,
      top: Math.random() * 100,
      rotation: Math.random() * 360,
    };
  }

  function animate_leaves() {
    $(".left_anim img").each(function (index) {
      leaf = $(this);
      data = change();
      leaf.css("top", data.top + "%");
      leaf.css("left", data.left + "%");
      leaf.css("transform", "rotate(" + data.rotation + "deg)");
    });
  }

  function add_leafs(n) {
    for (i = 0; i < n; i++) {
      var ele = document.createElement("img");
      ele.src = js_urls.leaf;
      ele.alt = "Leaf";
      ele.style.position = "absolute";
      ele.style.top = Math.random() * 100 + "%";
      ele.style.left = Math.random() * 100 + "%";
      ele.style.zIndex = -1;
      ele.style.width = 20 + Math.random() * 20 + "px";
      ele.style.transform = "rotate(" + Math.random() * 360 + "deg)";
      // document.querySelector(".wishlist_slide_page .left_slide").appendChild(ele);
      document.querySelector(".left_anim").appendChild(ele);
    }
    setTimeout(animate_leaves, 1000);
    setInterval(animate_leaves, 31000);
  }

  $(".close_slide").click(function () {
    $(".cart_slide_page").css("right", "-100%");
    $(".left_anim").css("opacity", "0");
  });

  $(".continue_button").click(function () {
    $(".cart_slide_page").css("right", "-100%");
    $(".left_anim").css("opacity", "0");
  });

  cart_request = function (e) {
    $(".cart_slide_main").html("");
    if (e) {
      e.preventDefault();
    }
    $.ajax({
      type: "POST",
      url: js_urls.cart_home,
      success: function (response) {
        hiddenEle = $(".cart_slide_item.hidden");
        for (i = 0; i < response.items.length; i++) {
          ele = hiddenEle.clone();
          updateFormDec = $(".update_quantity_form_jquery.hidden").clone();
          updateFormInc = $(".update_quantity_form_jquery.hidden").clone();
          updateFormDec.find(".hidden-item-id").val(response.items[i].id);
          updateFormDec.find(".inc_or_dec").val("dec");
          updateFormDec.find(".submit-hidden").val("-");
          updateFormInc.find(".hidden-item-id").val(response.items[i].id);
          updateFormInc.find(".inc_or_dec").val("inc");
          updateFormInc.find(".submit-hidden").val("+");
          updateFormDec.css("display", "inline-block");
          updateFormInc.css("display", "inline-block");
          updateFormDec.removeClass("hidden");
          updateFormInc.removeClass("hidden");
          ele.removeClass("hidden");
          ele.css("display", "grid");
          ele.find(".item-id-hidden").html(response.items[i].id);
          ele.find("img").attr("src", response.items[i].image);
          ele.find(".slide_item_title").html(response.items[i].name);
          ele.find(".slide_item_quantity").append(updateFormDec);
          ele.find(".slide_item_quantity").append(response.items[i].quantity);
          ele.find(".slide_item_quantity").append(updateFormInc);
          ele.find(".slide_item_price").html("₹" + response.items[i].price);
          $(".cart_slide_main").append(ele);
          $(".cart_slide_main").append("<hr />");
        }
        if (response.items.length > 0) {
          $(".cart_slide_total").html("₹" + response.total);
          $(".slide_main_hr").css("visibility", "visible");
          $(".slide_main_heading").css("visibility", "visible");
          $(".cart_slide_price").css("visibility", "visible");
          $(".empty_cart").css("display", "none");
          $(".checkout_button").css("display", "flex");
        } else {
          $(".empty_cart").css("display", "block");
          $(".slide_main_hr").css("visibility", "hidden");
          $(".slide_main_heading").css("visibility", "hidden");
          $(".cart_slide_price").css("visibility", "hidden");
          $(".cart_slide_total").html("");
          $(".checkout_button").css("display", "none");
        }
        $(".cart_slide_page").css("right", "0");
        $(".left_anim").css("opacity", "0.64");
        $(".cart_slide_page .slide-loader").removeClass("active");
        update_logos();
        $(".update_quantity_form_jquery").submit(function (e) {
          $(".cart_slide_page .slide-loader").addClass("active");
          e.preventDefault();
          thisForm = $(this);
          $.ajax({
            type: thisForm.attr("method"),
            url: thisForm.attr("action"),
            data: thisForm.serialize(),
            success: function (response) {
              cart_request();
            },
          });
        });
      },
      error: function (error) {
        console.log(error);
      },
    });
  };
  $(".cart_home_button").click(cart_request);

  // Dropdown Links
  function setDropdowns() {
    $(".cat-link").each(function () {
      var left = $(this)[0].getBoundingClientRect().left;
      $(this).find(".dropdown").css("left", -left);
    });
  }

  function windowResized(){
    setDropdowns();
    if (window.innerWidth <= 800) {
      $(".header_logo .logo_img").attr("src", js_urls.mixed_logo);
    } else {
      $(".header_logo .logo_img").attr("src", js_urls.logo);
    }
  }

  windowResized();
  $(window).resize(windowResized);
});
// Document Rady Close

$("#register-user-form").submit(function (e) {
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      if (response.location == "/") {
        window.location.reload();
      }else{
        window.location.href = "/";
      }
    },
    error: function (xhr, status, error) {
      $('#register-user-form span[class*="-error"]').text("");
      fields = xhr.responseJSON.form.fields;
      console.log(fields);
      keys = Object.keys(fields);
      keys.forEach((input) => {
        x = fields[input];
        console.log(x);
        if (x.errors.length > 0) {
          $("span." + input + "-error").text(x.errors[0]);
        }
      });
    },
  });
});

$(".login_popup_form").submit(function (e) {
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      if (response.logged_in) {
        window.location.reload();
      } else {
        $(".login_page .errors").text(response.errors);
      }
    },
    error: function (error) {
      $.alert({
        title: "Oops !!",
        content: "An error Occured,Try again later",
        theme: "modern",
      });
    },
  });
});

function showRegister() {
  $(".login_page").fadeOut("fast", function () {
    $(".register_page").fadeIn("fast");
  });
}

function showLogin() {
  $(".register_page").fadeOut("fast", function () {
    $(".login_page").fadeIn("fast");
  });
}

function check_login(e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: js_urls.api_login,
    data: {},
    success: function (response) {
      if (response.logged_in) {
        window.location.href = "/cart/checkout";
      } else {
        jQuery.noConflict();
        $("#mymodal").modal("toggle");
      }
    },
    error: function (error) {
      $.alert({
        title: "Oops !!",
        content: "An error Occured",
        theme: "modern",
      });
    },
  });
}

$("#mymodal").on("click", function (e) {
  if (e.target !== this) return;
  resumeAnimation();
});

function profile(e) {
  // console.log("Sending Request");
  e.preventDefault();
  if (js_urls.logged_in == "True") {
    $(".profile-icon").addClass("active");
  } else {
    $("#mymodal").modal("toggle");
    pauseAnimation();
  }
}

$(".header_icons").mouseleave(() => {
  $(".profile-icon").removeClass("active");
});

$(".close_slide_wishlist").click(function () {
  $(".wishlist_slide_page").css("right", "-100%");
  $(".left_anim").css("opacity", "0");
});

$(".continue_shopping_wishlist").click(function () {
  $(".wishlist_slide_page").css("right", "-100%");
  $(".left_anim").css("opacity", "0");
});

$(".wishlist-logo").click(openWishlist);

function openWishlist() {
  $.ajax({
    type: "POST",
    url: js_urls.api_wishlist,
    success: function (response) {
      $(".wishlist_slide_main").html("");
      if (response.logged_in) {
        var n = response.products.length;
        if (n > 0) {
          $(".wishlist_slide_page .cart_head_slide")
            .find("img")
            .attr("src", js_urls.wishlist_full);
          for (i = 0; i < n; i++) {
            var ele = $(".wishlist_slide_item.hidden").clone();
            ele.removeClass("hidden");
            ele.css("display", "grid");
            ele.find("img").attr("src", response.products[i].image);
            ele.find(".wishlist_item_title").html(response.products[i].title);
            ele
              .find(".wishlist_item_price")
              .html("₹" + response.products[i].price);
            ele
              .find(".wishlist_item_delete")
              .find(".remove_form_id")
              .val(response.products[i].id);
            ele
              .find(".wishlist_item_movecart")
              .find(".move_form_id")
              .val(response.products[i].id);
            $(".wishlist_slide_main").append(ele);
            $(".wishlist_slide_main").append("<hr />");
            $(".empty_wishlist").css("display", "none");
            $(".slide_main_heading_wishlist").css("display", "grid");
            $(".wishlist_main_hr").css("display", "block");
          }
        } else {
          $(".wishlist_slide_page .cart_head_slide")
            .find("img")
            .attr("src", js_urls.wishlist);
          $(".empty_wishlist").css("display", "block");
          $(".slide_main_heading_wishlist").css("display", "none");
          $(".wishlist_main_hr").css("display", "none");
        }
      } else {
        $(".empty_wishlist").css("display", "block");
        $(".empty_wishlist").html("Login to view wishlist");
        $(".slide_main_heading_wishlist").css("display", "none");
        $(".wishlist_main_hr").css("display", "none");
      }

      $(".wishlist_item_delete").submit(function (e) {
        e.preventDefault();
        $(".wishlist_slide_page .slide-loader").addClass("active");
        thisForm = $(this);
        $.ajax({
          type: "POST",
          url: js_urls.api_wishlist + "remove/",
          data: thisForm.serialize(),
          success: function (response) {
            if (response.removed) {
              thisForm.parent().next("hr").remove();
              thisForm.parent().remove();
            }
            if ($(".wishlist_slide_main").html() == "") {
              $(".cart_head_slide").find("img").attr("src", js_urls.wishlist);
              $(".empty_wishlist").css("display", "block");
            }
            $(".wishlist_slide_page .slide-loader").removeClass("active");
          },
        });
      });

      $(".wishlist_item_movecart").submit(function (e) {
        e.preventDefault();
        $(".wishlist_slide_page .slide-loader").addClass("active");
        thisForm = $(this);
        $.ajax({
          type: "POST",
          url: js_urls.api_wishlist + "move/",
          data: thisForm.serialize(),
          success: function (response) {
            if (response.removed) {
              thisForm.parent().next("hr").remove();
              thisForm.parent().remove();
            }
            if ($(".wishlist_slide_main").html() == "") {
              $(".cart_head_slide").find("img").attr("src", js_urls.wishlist);
              $(".wishlist_slide_page .right_slide .empty_wishlist").css(
                "display",
                "block"
              );
            }
            $(".wishlist_slide_page .slide-loader").removeClass("active");
          },
        });
      });
    },
    error: function (error) {
      console.log(error);
      $.alert({
        title: "Oops !!",
        content: "An error Occured",
        theme: "modern",
      });
    },
  });
  $(".wishlist_slide_page").css("right", "0");
  $(".left_anim").css("opacity", "0.64");
}

$(".join-our-circle-form").submit(function(e){
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    type: "POST",
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      if(response.success){
        $.alert({
          title: "Success",
          content: "You are successfully Subscribed",
          theme: "modern",
        });
        $(".join-our-circle-form").find("input[type='email']").val("");
      }else{
        $.alert({
          title: "Error",
          content: response.msg,
          theme: "modern",
        });
      }
    },
    error: function (){
      $.alert({
        title: "Error",
        content: "Something Went Wrong",
        theme: "modern",
      });
    }
  });
})