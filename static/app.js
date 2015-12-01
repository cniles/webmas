//
// The Angular JS module for the web client
//
(function (){

    var app = angular.module('xmas', []);
    app.controller('XMasController', function($scope, $http){

	// Initialize the light list by getting it from the server
	$http.get("/lights").then(function(response) {
	    $scope.lights = response.data;
	});

	// Simple function that toggles a light on / off and updates
	// the ui from the response
	this.toggle = function(light) {

	    // The server doesn't really even care what the request
	    // body is...
	    var data = {
		action: 'toggle'
	    };

	    // Tell the server to toggle the lights, then update the
	    // ui on success
	    $http.post('/light/' + light.num, data).success(function(data, status) {
		light.status = data.status;
		light.on = data.on;
	    });
	};

    });
})();
