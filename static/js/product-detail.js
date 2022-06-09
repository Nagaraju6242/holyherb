var fixedTop;
var headerHeight;
var contentbase;

function quantity_inc() {
  x = $("#quantity").text();
  x++;
  if(x > 10){
    x = 10;
  }
  $("#quantity").text(x);
  $(".add-form input[name='quantity']").val(x);
}

function quantity_dec() {
  x = $("#quantity").text();
  x--;
  if (x <= 0) {
    x = 1;
  }
  $("#quantity").text(x);
  $(".add-form input[name='quantity']").val(x);
}

$(document).ready(function () {
  $(".add-form input[type='radio'][name='qp_id']").change(function () {
    $("#price").text($(this).attr("--data-price"));
    var price = $(this).attr("--data-price");
    if (multiple_images) {
      $(".product-image").hide();
      $(`.product-image[--data-price='${price}']`).show();
    }
  });

  window.scrollTo({ top: 0, left: 0, behavior: "auto" });

  change();
  // window.onscroll = change;
});

requestAnimationFrame(change);

function change() {
  requestAnimationFrame(change);

  if($(".product-images")[0].getBoundingClientRect().bottom <= window.innerWidth * 0.4){
     $(".price-box").hide();
  }else{
    $(".price-box").show();
  }

  if ($(window).scrollTop() == 0) {
    fixedTop =
      $(".title-flavour > span.capi")[0].getBoundingClientRect().top +
      $(".title-flavour > span.capi").height();
    headerHeight = $(".header").height();
    contentbase = $(".content").outerHeight() + fixedTop - $(window).height();
    setTimeout(function () {
      $(".content").css("top", fixedTop + "px");
    }, 100);
  }
  if (
    $(".content").outerHeight() + fixedTop - $(window).height() <=
    $(window).scrollTop() - 50
  ) {
    if (
      headerHeight + $(".product-images").height() - $(window).height() <=
      $(window).scrollTop() - 50
    ) {
      var bounding = $("#reviews")[0].getBoundingClientRect();
      if (bounding.top - 100 <= $(window).height()) {
        $(".content")[0].style.top =
          200 - contentbase - $(window).height() + bounding.top + "px"; //Needs to be Adj
      }
    } else {
      $(".content").css(
        "top",
        -($(".content").outerHeight() + fixedTop - $(window).height() - 200) + //Needs to be adjusted large number for large device
          "px"
      );

      $(".price-box").show();
    }
  } else {
    $(".content").css("top", fixedTop - $(window).scrollTop());
  }
}



$(".review-inapp-form").submit(function(e){
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      if (response.success) {
        thisForm.find("button").text("Reported");
      }
    },
  });
})

$(".add-form").submit(function (e) {
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      if (response.added || response.increased) {
        update_logos();
        $("button.add-to-cart").text("Added to Cart");
        setTimeout(function () {
          $("button.add-to-cart").text("Add to Cart");
        }, 1000);
      }
    },
  });
});

function checkoutButton() {
  thisForm = $(".add-form");
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      if (response.added || response.increased) {
        update_logos();
        $(".cart_home_button").click();
      }
    },
  });
}

// Related Products

$(".add-to-wishlist").bind("submit", function (e) {
  e.preventDefault();
  if (js_urls.logged_in == "False") {
    $("#mymodal").modal("toggle");
    return false;
  }
  thisForm = $(this);
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      image = thisForm.find("img");
      if (response.success) {
        if (response.added) {
          image[0].src = js_urls.wishlist_full;
        } else {
          image[0].src = js_urls.wishlist;
        }
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
});

$(".product-form").submit(function (e) {
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      thisForm.find("input[type='submit']").val("ADDED TO CART");
      update_logos();
      setTimeout(function () {
        thisForm.find("input[type='submit']").val("ADD TO CART");
      }, 1000);
    },
  });
});

function openReview() {
  if (js_urls.logged_in === "True") {
    $(".write-review-main").toggle(400);
  } else {
    $("#mymodal").modal("toggle");
  }
}

function starUpdate(x) {
  stars = document.querySelectorAll(".write-review-main .rating-container svg");
  for (i = 0; i < 5; i++) {
    if (i <= x) {
      stars[i].classList.add("filled");
    } else {
      stars[i].classList.remove("filled");
    }
  }
  $("#form-rating").val(x + 1);
}


// alert(window.innerWidth + "," + window.innerHeight)