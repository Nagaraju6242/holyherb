function showModalLogin(e) {
  e.preventDefault();
  if (js_urls.logged_in == "True") {
    window.location.href = "/cart/checkout";
  } else {
    $("#mymodal").modal("toggle");
  }
}

// $(".number-only").keyup(function () {
//   this.value = this.value.replace(/[^0-9\.]/g, "");
// });

$(".number-only").keypress(function (e) {
  var verified =
    e.which == 8 || e.which == undefined || e.which == 0
      ? null
      : String.fromCharCode(e.which).match(/[^0-9]/);
  if (verified) {
    e.preventDefault();
  }
});

$(".text-only").keypress(function (e) {
  var verified =
    e.which == 8 || e.which == undefined || e.which == 0
      ? null
      : String.fromCharCode(e.which).match(/[^A-Z a-z]/);
  if (verified) {
    e.preventDefault();
  }
});


$(document).ready(function () {
  $(".coupon-box form").submit(function (e) {
    e.preventDefault();
    thisForm = $(this);
    $.ajax({
      type: thisForm.attr("method"),
      url: thisForm.attr("action"),
      data: thisForm.serialize(),
      success: function (response) {
        if (response.added) {
          window.location.reload();
        } else {
          $(".coupon-errors").html(response.error);
        }
      },
    });
  });

  $(".coupon-remove-box  .coupon-remove-form").submit(function (e) {
    e.preventDefault();
    thisForm = $(this);
    $.ajax({
      type: thisForm.attr("method"),
      url: thisForm.attr("action"),
      data: thisForm.serialize(),
      success: function (response) {
        if (response.removed) {
          window.location.reload();
        } else {
          $(".coupon-errors").html(response.error);
        }
      },
    });
  });
});

$(".checkout-main .signin-button").click(showModalLogin);
$(".checkout-main .login-button").click(showModalLogin);

$("form.shipping-form").submit(function (e) {
  e.preventDefault();
  thisForm = $(this);
  $.ajax({
    type: thisForm.attr("method"),
    url: thisForm.attr("action"),
    data: thisForm.serialize(),
    success: function (response) {
      if (response.added) {
        window.location.reload();
        thisForm.find("small.errors").text("");
      } else {
        thisForm.find("small.errors").text(response.error);
      }
    },
  });
});
