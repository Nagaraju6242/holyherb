const speed = 80;

$(".c-index-alphabtical_item").on("click", function () {
  if ($(this).hasClass("is-active")) {
    return;
  }
  $(".c-index-alphabtical_item.is-active").removeClass("is-active");
  var $this = $(this);
  var letter = $(this).find("span").text().toString().toLowerCase()[0];
  var idx = $(this).index();
  if (idx > 13) {
    var toMove = idx - 13;
    for (var x = 0; x < toMove; x++) {
      setTimeout(function () {
        $(".c-index-alphabtical_item:first").appendTo(
          $(".c-index-alphabtical_item").parent()
        );
      }, x * speed);
    }
    setTimeout(function () {
      $this.addClass("is-active");
    }, toMove * speed);
  } else if (idx < 13) {
    var toMove = 13 - idx;
    for (var x = 0; x < toMove; x++) {
      setTimeout(function () {
        $(".c-index-alphabtical_item:last").prependTo(
          $(".c-index-alphabtical_item").parent()
        );
      }, x * speed);
    }
    setTimeout(function () {
      $this.addClass("is-active");
    }, toMove * speed);
  }
  var t = toMove * speed;
  $(".c-index-results .result-box").hide().removeClass("is-active");
  setTimeout(function () {
    $(".c-index-results .result-box[data-letter='" + letter + "']").show();
    $(".c-index-results .result-box[data-letter='" + letter + "']").addClass(
      "is-active"
    );
  }, t);
});

function hashChanged() {
  var hash = location.hash.slice(1, 2).toLowerCase();
  $(".c-index-alphabtical_item[data-letter='" + hash + "']").click();
}

window.onhashchange = hashChanged;

$(document).ready(function () {
  if (location.hash != "") {
    hashChanged();
  }
});
