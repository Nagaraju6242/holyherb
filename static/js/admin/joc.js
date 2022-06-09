li =
  "<li><a style='background-color: var(--link-fg);' href='/admin/accounts/joinourcircle/download' >Download as CSV</a></li>";

window.onload = function () {
    content = document.querySelector("#content-main ul.object-tools");
    content.innerHTML += li;
}