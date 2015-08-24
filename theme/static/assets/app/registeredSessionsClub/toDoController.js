
app.controller("toDoController",function toDoController($scope, DataService){
	$scope.status = "";
	
	$scope.allAthletes = function() {
		$scope.status = "";
	}

	$scope.notAttendedAthletes = function() {
		$scope.status = false;
	}

	$scope.attendedAthletes = function() {
		$scope.status = true;
	}
	
	$scope.agreement = 1;

	getAllAthletes = function() {
		DataService.getAthletes($scope.agreement).then(
			function (results) {
				$scope.athletes = results.data;
				for(athlete in $scope.athletes)
					$scope.athletes[athlete].isDone = false;
			});
	}
	getAllAthletes();
	

	$scope.addAthlete = function(){
		var newAthlete = {
			firstname : $scope.athlete.firstname,
			lastname : $scope.athlete.lastname,
			isDone : false
		};
		if(newAthlete.firstname.length > 0 && newAthlete.lastname.length > 0){
			// DataService.addAthlete(newAthlete).then(
			// 	function(results){
					//newAthlete.id = results.data;
				 	$scope.athletes.push(newAthlete);
					$scope.athlete.firstname = "";
					$scope.athlete.lastname = "";
				// },
				// function(results){
		 		// 	alert("اینترنت خود را بررسی کنید.");
		 		// });
		}
	}
	
	 $scope.updateStatusAthlete = function(athlete){
	 	// DataService.toggleAttended().then (
	 	// 	function(results) {
	 			athlete.isDone = !athlete.isDone;
	 		// },
			// function(results){
	 		// 	alert("اینترنت خود را بررسی کنید.");
	 		// });
	 }
	 $scope.deleteAthlete = function(athlete){
	 	// DataService.removeAthlete(index).then (
	 	// 	function(results){
	 		$scope.athletes = jQuery.grep($scope.athletes, function(value) {
			  return value != athlete;
			});
	 			//$scope.athletes.splice(index,1);
	 		// },
	 		// function(results){
	 		// 	alert("اینترنت خود را بررسی کنید.");
	 		// });
	 }
});


