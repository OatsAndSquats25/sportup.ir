app.controller("MainController", function($scope){
	
	$scope.today = function() {
    $scope.beginDate = new Date();
    $scope.endDate = new Date();
  };
  $scope.today();



  $scope.clear = function () {
    $scope.beginDate = null;
    $scope.endDate = null;
  };

  // Disable weekend selection
  $scope.disabled = function(date, mode) {
    // return ( mode === 'day' &&date.getDay() === 5  );
  };

  $scope.toggleMin = function() {
    $scope.minDate = $scope.minDate ? null : new Date();
  };
  $scope.toggleMin();

  $scope.openBegin = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.beginIsOpen = true;
    $scope.endIsOpen = false;
  };
  $scope.openEnd = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.endIsOpen = true;
    $scope.beginIsOpen = false;
  };

  $scope.dateOptions = {
    formatYear: 'yy',
    startingDay: 6
  };

  $scope.initDate = new Date('2016-15-20');
  $scope.formats = ['yyyy/MM/dd', 'dd-MMMM-yyyy' , 'dd.MM.yyyy', 'shortDate'];
  $scope.format = $scope.formats[0];
  });
