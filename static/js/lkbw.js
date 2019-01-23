
//Tracker

var map;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: new google.maps.LatLng(0,0),
    mapTypeId: 'terrain'
  });

  var payload = document.getElementsByClassName('data');

  var bounds = new google.maps.LatLngBounds();
  var infowindow = new google.maps.InfoWindow({
      content: '',
  });

  for (var i = 0; i < payload.length; i++) {
    var lat = payload.item(i).attributes.lat.value;
    var lng = payload.item(i).attributes.lng.value;
    var latLng = new google.maps.LatLng(lat, lng);
    var marker = new google.maps.Marker({
      position: latLng,
      map: map,
      label: '',
      title: payload.item(i).attributes.title.value,
      data: payload.item(i).attributes.caption.value,
      url: payload.item(i).attributes.page.value,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        strokeColor: '#7b2500',
        strokeWeight: 6,
        fillColor: '#7b2500',
        fillOpacity: 1,
      }
    });

    if (i == 0) {
      var path = []
    }

    path.push({lat: parseFloat(lat), lng: parseFloat(lng)})

    var flightPath = new google.maps.Polyline({
      path: path,
      geodesic: true,
      strokeColor: '#a15900',
      strokeWeight: 2,
    });

  var blank_content = ''
  google.maps.event.addListener(marker,'click', (function(marker,blank_content,infowindow){
    return function() {
      var content = marker.data;
      if (marker.url != '') {
        content = '<a href=' + marker.url + ' style="text-decoration:underline;">' + marker.data + '</a>'
      }
      infowindow.setContent(content);
      infowindow.open(map,marker);
    };
  })(marker,blank_content,infowindow));

  flightPath.setMap(map);

  bounds.extend(marker.position);

  }

  map.fitBounds(bounds);

}

// Masonry

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
  scrollThreshold: 800,
});

// Safari fixe
$('.grid').on( 'append.infiniteScroll', function( event, response, path, items ) {
	$('.grid').masonry('layout');
});

// Flickity

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


//
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
