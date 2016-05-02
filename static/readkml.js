// fill collections list
var openKML = function() {    
    $.ajax({    	
        type: 'GET',
	    url: '/api/kml/sample.kml',	    
	    success: function(points) {
	    	//alert(parseFloat(points[0].LookAt.latitude));
			setMapView(eval(points));			
        },
        error: function() {
            alert('error loading points from KML');
        }
    });
  };
$(window).load(openKML);