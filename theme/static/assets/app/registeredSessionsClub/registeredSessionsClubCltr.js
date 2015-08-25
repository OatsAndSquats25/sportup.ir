
app.controller("registeredSessionsClubCltr",function registeredSessionsClubCltr($scope, DataService){
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

	getAllAthletes = function() {
		DataService.getClubs().then(
            function(results) {
                    $scope.clubId = results.data[0].id;
                
            //$scope.data = DataService.getSessionTable(clubId, week);
            //renderTimeTable($scope.data);
            DataService.getAthletes($scope.clubId).then(
			function (results) {
				console.log(results)
				$scope.athletes = results.data;
				for(athlete in $scope.athletes)
					$scope.athletes[athlete].isDone = false;
			});
        });
	}
	getAllAthletes();
	
	 $scope.updateStatusAthlete = function(athlete){
	 	console.log(athlete.id);
	 	DataService.athleteAttended(athlete.id).then (
	 		function(results) {
	 			console.log(results.data+"  "+results.status);
	 			athlete.isDone = !athlete.isDone;
	 		},
			function(results){
	 			alert("مشکل در برقراری ارتباط.");
	 		});
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


