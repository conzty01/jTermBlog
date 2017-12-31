function isActive(element) {
    return element.name == "active";
}

function showDivs(slideStr,n) {
  var i;
  var x;
  var slides = Array.from(document.getElementsByClassName(slideStr));
  var active = slides[slides.findIndex(isActive)];

  console.log("~~~~")
  console.log(slides.length);
  console.log(parseInt(active.id));
  console.log(n);

  if (parseInt(active.id) + n >= slides.length) {x = 0}
  else if (parseInt(active.id) + n < 0) {x = slides.length - 1}
  else {x = parseInt(active.id) + n}

  for (i = 0; i < slides.length; i++) {
     slides[i].style.display = "none";
     slides[i].name = "inactive";
  }

  slides[x].style.display = "block";
  slides[x].name = "active";
}
