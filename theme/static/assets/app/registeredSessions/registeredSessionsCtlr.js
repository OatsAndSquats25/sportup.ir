app.controller('registeredSessionsCtlr',
    ["$scope", "DataService",
    function registeredSessionsCtlr($scope, DataService) {
        $scope.tableTitles = ["عنوان","تاریخ شروع","تاریخ پایان","قیمت","ساعت شروع","ساعت پایان"];
        $scope.getPrograms = function () {
            DataService.enrollSessionList().then(
                 function(results) {
                     $scope.programs = results.data;
                 },
                 function (results) {
                     alert(results.status + ': ' + results.statusText);
                 });
        };
        $scope.getPrograms();
}]);
