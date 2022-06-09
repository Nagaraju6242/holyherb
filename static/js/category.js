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
      update_logos();
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

var x, i, j, l, ll, selElmnt, a, b, c;
/* Look for any elements with the class "custom-select": */
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  /* For each element, create a new DIV that will act as the selected item: */
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /* For each element, create a new DIV that will contain the option list: */
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 0; j < ll; j++) {
    /* For each option in the original select element,
    create a new DIV that will act as an option item: */
    c = document.createElement("a");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.href = selElmnt.options[j].value;
    span = document.createElement("span");
    c.appendChild(span);
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function (e) {
    /* When the select box is clicked, close any other select boxes,
    and open/close the current select box: */
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("select-hide");
    this.classList.toggle("select-arrow-active");
  });
}

function closeAllSelect(elmnt) {
  /* A function that will close all select boxes in the document,
  except the current select box: */
  var x,
    y,
    i,
    xl,
    yl,
    arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i);
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);
