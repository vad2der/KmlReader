var styleArray = [
	{
		featureType: "all",
		stylers: [
			{ saturation: -80 }
		]
    },{
		featureType: "road.arterial",
		elementType: "geometry",
		stylers: [
			{ hue: "#00ffee" },
			{ saturation: 50 }
		]
    },{
		featureType: "poi.business",
		elementType: "labels",
		stylers: [
			{ visibility: "off" }
		]
    }
];
  
var loc;  
var points;
var bounds = new google.maps.LatLngBounds();
var markers = [];
var initialPosition = {lat: 60.0, lng: 60.0};
var current_marker = new google.maps.Marker();

// Set initial postion first
function getBrowserPosition(){	    
	if (navigator.geolocation) {
	// Try Browser Geolocation
		navigator.geolocation.getCurrentPosition(assignPosition);
	} else {window.alert('Browser does not support geolocation');}
}

function assignPosition(position){
	initialPosition = {
		lat: position.coords.latitude,
		lng: position.coords.longitude
	};
}

getBrowserPosition();
var map;

function initMap(){
	map = new google.maps.Map(document.getElementById('map'), {
		styles: styleArray,
		center: {
			lat: initialPosition.lat,
			lng: initialPosition.lng,
		},
		zoom: 9	
	});
};
initMap();

// set markers, center, zoom
function setMapView(points) {	
	current_marker.setMap(null);
	if ((typeof(points) != 'object') || (points === null) || (points === undefined) || (points.length == 0)){	
		map.setCenter(initialPosition);
		map.setZoom(9);
		google.maps.Map.prototype.clearOverlays = function() {
			for (var i = 0; i < markersArray.length; i++ ) {
				markersArray[i].setMap(null);
			}
		markersArray.length = 0;
		}
	}
	else{		
		setMarkers(map, points);
		map.fitBounds(bounds);
		map.panToBounds(bounds);
	}
};

// zoom on a point
function zoomOnPoint (point) {
	point = eval(point);
	var position = {lat: parseFloat(point.LookAt.latitude), lng: parseFloat(point.LookAt.longitude)};
	map.setCenter(position);
	map.setZoom(20);
};

// helpers...
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}
// Data for the markers consisting of a name, a LatLng and a zIndex for the
// order in which these markers should display on top of each other.

function setMarkers(map, points) {
  // Adds markers to the map.
	bounds = new google.maps.LatLngBounds();
	for (var i = 0; i < points.length; i++) {
		var point = points[i];
		var marker = new google.maps.Marker({
			position: {lng: parseFloat(point.Point.coordinates.split(",")[0]),
			           lat: parseFloat(point.Point.coordinates.split(",")[1])},
			map: map,
			//icon: image,
			//shape: shape,
			label: String(i+1)
			//zIndex: String(point.type)
		});		
		bounds.extend(new google.maps.LatLng(parseFloat(point.Point.coordinates.split(",")[1]),
											parseFloat(point.Point.coordinates.split(",")[0])));
	}		
};


google.maps.event.addListener(map, 'click', function(event) {
    current_marker.setMap(null);
	current_marker = new google.maps.Marker({
        position: event.latLng, 
        map: map,
		color: "blue"
	});
	var p = JSON.parse(JSON.stringify(current_marker.position));
	$('#new_poi').find('#lat').val(p.lat);
	$('#new_poi').find('#lng').val(p.lng);
});

$('body').on('load', '#map', function() {
	setMapView(eval([]));
});