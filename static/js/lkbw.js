var elem = document.querySelector('.grid');

var msnry = new Masonry( elem, {
  itemSelector: 'none',
  columnWidth: '.grid-sizer',
  horizontalOrder: true,
  percentPosition: true,
});

imagesLoaded( elem, function() {
  msnry.options.itemSelector = '.grid_item';
  var items = grid.querySelectorAll('.grid_item');
  msnry.append( items );
});


var infScroll = new InfiniteScroll( elem, {
    path: '?page={{#}}',
    append: 'grid_item',
    outlayer: msnry,
    history: false,
});