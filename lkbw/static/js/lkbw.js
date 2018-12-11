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
  fullscreen: true,
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


// jQuery
$carousel.on( 'fullscreenChange.flickity', function( event, isFullscreen ) {

    if (isFullscreen) {
        $('#mainNav').css('z-index', 0);
        $('#imageViewer').css('padding-top', '35px');
    } else {
        $('#mainNav').css('z-index', 1030);
    }
});

$carousel.on( 'select.flickity', function() {
  // set image caption using img's alt
  var capt = $(flkty.selectedElement.firstElementChild.id);
  capt.text( flkty.selectedElement.firstElementChild.alt );
});