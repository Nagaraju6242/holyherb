jQuery(document).ready(function ($) {
  readonly = $(".form-row.field-items").find(".readonly");
  var items = readonly.text().trim().split(",");
  readonly.text("");
  headings = [
    "Product Name",
    "Flavour",
    "Qunaity",
    "Product Quantity",
    "Price",
  ];
  for (i = 0; i < headings.length; i++) {
    div = document.createElement("div");
    div.innerText = headings[i];
    div.classList.add("grid-heading");
    readonly[0].appendChild(div);
  }
  for (i = 0; i < items.length; i++) {
    item = items[i].split("--");
    for (j = 0; j < item.length; j++) {
      div = document.createElement("div");
      div.innerText = item[j];
      readonly[0].appendChild(div);
    }
  }
});
