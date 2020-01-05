

$(document).ready(function(){
  var requesttimes = [];
  var datapoints;
  console.log("ready");
  $.ajax({
    type: "get",
    url: "http://localhost:8080/centers",
    dataType: "json",
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
      requesttimes.push((new Date().getTime() - this.start_time));
      console.log(requesttimes);
    }
  });
});
    

var map, heatmap, info;


function renderMap(data){
  console.log('rendering map');
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 37.783508, lng: -122.439525},
    mapTypeId: 'satellite'
  });

  var heatMapData = [];
  console.log(data.length);
  for(var i = 0; i < data.length; i++){
    var id = data[i].id;
    var latLng = new google.maps.LatLng(data[i].coordinates[0], data[i].coordinates[1]);
    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
      position: latLng,
      map: map,
      id: id,
      infowindow: infowindow
    });


    
    var infoContent;
    (function(marker,content,infowindow) {
      google.maps.event.addListener(marker,'click', function() {
        $.ajax({
          type: "get",
          url: "http://localhost:8080/clusterdata/" + marker.id,
          dataType: "json",
                      
          success: function(result) {
            console.log('success: ', result);
            console.log(marker.id)
            data = result;
            var catList = []
            var countList = []
            var percentList = []
            console.log(data.length)
            for(var i = 0; i < data.length; i++){
              catList.push(data[i].category)
              countList.push(data[i].counts)
              percentList.push(((data[i].percent) * 100).toFixed(2))
            }

            console.log(catList[8]) //this is nothing and the infocontent is not set properly. Should find a whole new way of doing this
            info = 
                '<div id="bodyContent">'+
                '<p><b>Category    Counts    Percent' +
                '<p><b>' + catList[0] + '  |  ' +  countList[0] + '  |  ' + percentList[0] + '%' +
                '<p><b>' + catList[1] + '  |  ' +  countList[1] + '  |  ' + percentList[1] + '%' +
                '<p><b>' + catList[2] + '  |  ' +  countList[2] + '  |  ' + percentList[2] + '%' +
                '<p><b>' + catList[3] + '  |  ' +  countList[3] + '  |  ' + percentList[3] + '%' +
                '<p><b>' + catList[4] + '  |  ' +  countList[4] + '  |  ' + percentList[4] + '%' +
                '<p><b>' + catList[5] + '  |  ' +  countList[5] + '  |  ' + percentList[5] + '%' +
                '<p><b>' + catList[6] + '  |  ' +  countList[6] + '  |  ' + percentList[6] + '%' +
                '<p><b>' + catList[7] + '  |  ' +  countList[7] + '  |  ' + percentList[7] + '%' +
                '<p><b>' + catList[8] + '  |  ' +  countList[8] + '  |  ' + percentList[8] + '%' +
                '</div>'+

              marker.infowindow.setContent(info)
                
          },
          error: function(xhr, status, error) {
            var errorMsg = xhr.status + ': ' + xhr.statusText;
            console.log('error: ', errorMsg);
          }, 
                      
          complete: function(data) {
          
          }
        });
        infowindow.setContent(content);
        infowindow.open(map, marker); 
      });
        
    })(marker,info,infowindow); 
    
  
  }
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}