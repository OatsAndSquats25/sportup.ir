var app = angular.module('app', ["ngRoute", "ui.bootstrap", 'ui.bootstrap.persian.datepicker','ui.bootstrap.datepicker', 'myModule']);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
// app.config(function ($routeProvider) {
//     // $routeProvider
//     //     .when("/home", {
//     //         templateUrl: "app/Home.html",
//     //         controller: "HomeController"
//     //     })
//     //     .when("/showSessionTable2/:id", {
//     //         templateUrl: "app/Session2/sessionTemplate.html",
//     //         controller: "sessionController2"
//     //     })
//     //     .when("/showSessionTable/:id", {
//     //         templateUrl: "app/Session/sessionTemplate.html",
//     //         controller: "sessionController"
//     //     })
//     //     .otherwise({
//     //         redirectTo: "/home"
//     //     });
// });

// app.controller("HomeController",
//      function ($scope, $location, DataService) {
//     //     console.log("start home");
//     //     $scope.showCreateEmployeeForm = function () {
//     //         $location.path('/newEmployeeForm');
//     //     };

//     //     $scope.showUpdateEmployeeForm = function (id) {
//     //         $location.path('/updateEmployeeForm/' + id)
//     //     };

//     //     $scope.showSessionTable = function(id) {
//     //         console.log("home " + id);
//     //         $location.path('/showSessionTable/'+id)
//     //     };
// });
