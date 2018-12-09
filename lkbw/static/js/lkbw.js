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