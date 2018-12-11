// init Masonry

var $grid = $('.grid').masonry({
  itemSelector: '.grid-item', // select none at first
  columnWidth: '.grid-sizer',
  percentPosition: true,
  stagger: 30,
  // nicer reveal transition
  visibleStyle: { transform: 'translateY(0)', opacity: 1 },
  hiddenStyle: { transform: 'translateY(100px)', opacity: 0 },
});

// get Masonry instance
var msnry = $grid.data('masonry');

// layout Masonry after each image loads
$grid.imagesLoaded().progress( function() {
  $grid.masonry('layout');
});

// init Infinte Scroll
$grid.infiniteScroll({
  path: '.pagination_next',
  append: '.grid-item',
  outlayer: msnry,
  prefill: true,
  history: false,
});




// external js: flickity.pkgd.js

var $carousel = $('.carousel').flickity({
  imagesLoaded: true,
  percentPosition: false,
});

var $caption = $('.caption');

var $imgs = $carousel.find('.carousel-cell img');
// get transform property
var docStyle = document.documentElement.style;
var transformProp = typeof docStyle.transform == 'string' ?
  'transform' : 'WebkitTransform';
// get Flickity instance
var flkty = $carousel.data('flickity');

$carousel.on( 'scroll.flickity', function() {
  flkty.slides.forEach( function( slide, i ) {
    var img = $imgs[i];
    var x = ( slide.target + flkty.x ) * -1/3;
    img.style[ transformProp ] = 'translateX(' + x  + 'px)';
  });
});
