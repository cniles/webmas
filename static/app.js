(function (){
    var app = angular.module('xmas', []);
    app.controller('XMasController', function($scope, $http){
	$http.get("/lights").then(function(response) {
	    $scope.lights = response.data;
	});

	this.toggle = function(light) {
	    var data = {
		action: 'toggle'
	    };
	    $http.post('/light/' + light.num, data).success(function(data, status) {
		light.status = data.status;
		light.on = data.on;
	    });
	};
    });
})();
