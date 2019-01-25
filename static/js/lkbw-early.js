
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
        path: 'M 0,-4 4,0 0,4 -4,0  Z',
        fillColor: '#7b2500',
        fillOpacity: 1,
        strokeColor: '#7b2500',
        strokeWeight: 2
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
