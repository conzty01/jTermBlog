function plusDivs(slideStr,curSlide) {
  showDivs(slideStr, curSlide += n);
}

function showDivs(slideStr,n) {
  var i;
  var x = document.getElementsByClassName(slideStr);
  if (n > x.length) {n = 1}
  if (n < 1) {n = x.length}
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";
  }
  x[n-1].style.display = "block";
}
