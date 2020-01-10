$(document).ready(function() {
  var requesttimes = [];
  var datapoints;
  console.log('ready');
  $.ajax({
    type: 'get',
    url: 'http://localhost:8080/centers',
    dataType: 'json',
    start_time: new Date().getTime(),

    success: function(result) {
      console.log('success: ', result);
      datapoints = result;
      renderMap(result);
    },
    error: function(xhr, status, error) {
      var errorMsg = xhr.status + ': ' + xhr.statusText;
      console.log('error: ', errorMsg);
    },

    complete: function(data) {
      requesttimes.push(new Date().getTime() - this.start_time);
      console.log(requesttimes);
    }
  });
});

var map, heatmap, info;

function renderMap(data) {
  console.log('rendering map');
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: { lat: 37.783508, lng: -122.439525 },
    mapTypeId: 'satellite'
  });

  var heatMapData = [];
  console.log(data.length);
  for (var i = 0; i < data.length; i++) {
    var id = data[i].id;
    var latLng = new google.maps.LatLng(
      data[i].coordinates[0],
      data[i].coordinates[1]
    );
    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
      position: latLng,
      map: map,
      id: id,
      infowindow: infowindow
    });

    var infoContent;
    (function(marker, content, infowindow) {
      google.maps.event.addListener(marker, 'click', function() {
        $.ajax({
          type: 'get',
          url: 'http://localhost:8080/clusterdata/' + marker.id,
          dataType: 'json',

          success: function(result) {
            console.log('success: ', result);
            console.log(marker.id);
            var data = result;

            var infostring =
              '<div id="bodyContent"><p><b>Category    Counts    Percent</p>';
            console.log(data.length);
            for (var i = 0; i < data.length; i++) {
              infostring +=
                '<p><b>' +
                data[i].category +
                '  |  ' +
                data[i].counts +
                '  |  ' +
                (data[i].percent * 100).toFixed(2) +
                '%</p>';
              console.log(infostring);
            }
            infostring.concat('</div>');

            marker.infowindow.setContent(infostring);
          },
          error: function(xhr, status, error) {
            var errorMsg = xhr.status + ': ' + xhr.statusText;
            console.log('error: ', errorMsg);
          },

          complete: function(data) {}
        });
        infowindow.setContent(content);
        infowindow.open(map, marker);
      });
    })(marker, info, infowindow);
  }
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}
