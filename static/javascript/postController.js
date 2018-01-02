"use strict"
function nav(direction) {
    let num = window.location.pathname.split("/");
    if (!num.includes("page")) {
        window.location.assign("page/2");
    } else {window.location.assign(parseInt(num.pop())+direction);}
}
