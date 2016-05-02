// fill collections list
var openKML = function() {    
    $.ajax({    	
        type: 'GET',
	    url: '/api/kml/sample.kml',	    
	    success: function(points) {
	    	//alert(points[0].Point.coordinates.split(',')[0]);
			setMapView(eval(points));			
        },
        error: function() {
            alert('error loading points from KML');
        }
    });
  };
$(window).load(openKML);