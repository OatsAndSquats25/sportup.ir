app.controller('sessionClubCtlr',
    ["$scope", "$window", "DataService", "$modal", "$modal", "$location", "$rootScope",
    function sessionClubCtlr($scope, $window, DataService, $modal, $location, $rootScope) {
        $scope.timeTableRenderObject = [];

        $scope.modalParams = {};

        $scope.openInfoModal = function () {
            var modalInstance = $modal.open({

              animation: $scope.animationsEnabled,
              templateUrl: 'ClubinfoModal.html',
              controller: 'infoModalCtrl',
              resolve: {
                params: function() {
                  return $scope.modalParams;
                }
              }
            });
        }

        $scope.deleteAthlete = function(idx) {
            var modalInstance = $modal.open({

              animation: $scope.animationsEnabled,
              templateUrl: 'deleteModal.html',
              controller: 'deleteModalCtrl',
              
            });
        };

        $scope.addAthlete = function(idx) {
            var modalInstance = $modal.open({

              animation: $scope.animationsEnabled,
              templateUrl: 'addModal.html',
              controller: 'addModalCtrl',
             
            });
        };

        $scope.changeStatus = function (idx) {
            //send status to server
            $scope.data[idx].status = ($scope.data[idx].status + 1) % 2;
            renderTimeTable($scope.data);
        };

        $scope.deleteEvent = function (idx) {
            //if(confirm("are you sure?")){
            /*dataService.delete($scope.data.schedule[day][idx].id)
             .$promise.then(function(data){
             if(data.success){
             $scope.data.schedule[day].splice(idx,1);
             renderTimeTable($scope.data);
             }
             else{
             alert("connection failed");
             }
             });*/
            $scope.data.splice(idx, 1);
            renderTimeTable($scope.data);
        };

        $scope.getInfo = function (event) {
            console.log(event);
            if(event.status) {
                $scope.modalParams.cellid = event.cellid;
                $scope.modalParams.clubId = $scope.clubId;
                $scope.modalParams.week = $scope.week;
                $scope.openInfoModal();
            }
        };

        $scope.Dates = [];
        var getWeekDates = function(todayInfo) {
          $scope.Dates = [];
          var today = new Date(todayInfo.date);
          var tmpDate = new Date(today).setDate(today.getDate() - todayInfo.day);
          for(var i = 0; i < 7; i++) {
            $scope.Dates.push(tmpDate);
            tmpDate = new Date(tmpDate).setDate(new Date(tmpDate).getDate() + 1);
          }
        }

        var renderTimeTable = function(events) {
            getWeekDates(events[0]);
            $scope.timeTableRenderObject = [];
            var lastPlan = [{begin: 0, end: 0}, {begin: 0, end: 0}, {begin: 0, end: 0}, {begin: 0, end: 0}, {begin: 0, end: 0}, {begin: 0, end: 0}, {begin: 0, end: 0}]
            var hasPlan = {0: false, 1: false, 2: false, 3: false, 4: false, 5: false, 6: false};
            $scope.days = ["شنبه", "یک شنبه", "دو شنبه", "سه شنبه", "چهار شنبه", "پنج شنبه", "جمعه"];
            var inInterval = function (myEvent, myTime) {
                if(!myEvent)
                    return false;
                if (myEvent.begin <= myTime && myEvent.end > myTime) {
                    return true;
                }
                return false
            }
            $scope.createLabel = function (data) {
                return Math.floor((data.end) / 60) + ':' + ((((data.end) % 60) < 10) ? '0' + ((data.end) % 60) : ((data.end) % 60))
                    + ' - ' + Math.floor((data.begin) / 60) + ':' + ((((data.begin) % 60) < 10) ? '0' + ((data.begin) % 60) : ((data.begin) % 60))
            }

            var countMinutes = function(str) {
                var splitedStr = str.split(":");
                return parseInt(splitedStr[0]) * 60 + parseInt(splitedStr[1])
            }

            var labelTimeInterval = 60;
            var planTimeInterval = 15;
            $scope.labelTimeSpan = labelTimeInterval / planTimeInterval;
            $scope.timeTableRenderObject = [];
            $scope.label = [];

            var eventIdx = 0;
            var tmp = [];
            //var minutesCount = function (myTime) {
            //    return (myTime.getHours() * 60 + myTime.getMinutes());
            //}
            var begin = countMinutes(events[eventIdx].begin);
            var end = countMinutes(events[eventIdx++].end);
            var event = events[eventIdx];
            //for(var ev in events){
            //    hasPlan[events[ev].day] = true;
            //}

            for (var i = begin; i < end; i += planTimeInterval) {
                if (i % labelTimeInterval == 0)
                    $scope.label.push({begin: i, end: i + labelTimeInterval});
                var tmp = [];

                for (var dayIdx = 0; dayIdx < 7; dayIdx++) {
                    if((event != undefined) && isNaN(event.begin)) {
                        event.begin = countMinutes(event.begin);
                    }
                    if((event != undefined) &&  isNaN(event.end)) {
                        event.end = countMinutes(event.end);
                    }
                    if ((event != undefined) && (event.day == dayIdx) && (inInterval(event, i))) {
                        if (event.begin == i) {
                            lastPlan[event.day].begin = event.begin;
                            lastPlan[event.day].end = event.end;
                            event.type = 1;
                            event.Idx = eventIdx;
                            event.span = (event.end - event.begin) / planTimeInterval;
                            tmp.push(event);
                            event = events[++eventIdx];
                        }
                    }
                    else if (!inInterval(lastPlan[dayIdx], i)){
                        tmp.push({type: 0});
                    }
                }

                $scope.timeTableRenderObject.push(tmp);
            }
        }

        $scope.nextWeek = function(){
          $scope.week++;
           DataService.getSessionTable($scope.clubId, $scope.week).then(
                 function(results) {
                     $scope.data = results.data;
                     renderTimeTable($scope.data);
                 },
                 function (results) {
                     alert("این برنامه ها قابل رویت نیستند.");
                 });
        }
        $scope.previousWeek = function(){
          $scope.week--;
           DataService.getSessionTable($scope.clubId, $scope.week).then(
                 function(results) {
                     $scope.data = results.data;
                     renderTimeTable($scope.data);
                 },
                 function (results) {
                     alert("این برنامه ها قابل رویت نیستند.");
                 });
        }

      var initialTable = function(week){
        DataService.getClubs().then(
            function(results) {
                    $scope.clubId = results.data[0].id;
                
            //$scope.data = DataService.getSessionTable(clubId, week);
            //renderTimeTable($scope.data);
                DataService.getSessionTable($scope.clubId, week).then(
                     function(results) {
                         $scope.data = results.data;
                         renderTimeTable($scope.data);
                     },
                     function (results) {
                         console.log(results.status + ': ' + results.statusText);
                         alert(results.status + ': ' + results.statusText);
                     });
            });
        }
        $scope.week = 0;
    initialTable( $scope.week);
}]);

app.controller('infoModalCtrl', function ($scope, DataService, $modalInstance, params) {

    getCellAthletes = function() {
        DataService.getCellAthletes(params.clubId, params.week, params.cellid).then(
            function (results) {
                console.log(results);
                $scope.athletes = results.data;
                for(athlete in $scope.athletes)
                    $scope.athletes[athlete].isDone = false;
            });
    }
    getCellAthletes();
    $scope.athlete = {};

    $scope.addAthlete = function(){
        var newAthlete = {
            firstname : $scope.athlete.firstname,
            lastname : $scope.athlete.lastname,
            email : $scope.athlete.email,
            phone : $scope.athlete.phone,
            isDone : false
        };
        if(newAthlete.firstname.length > 0 && newAthlete.lastname.length > 0){
          console.log(params.clubId+"week "+ params.week+"cell  "+ params.cellid+"name  "+ newAthlete.firstname+"last  "+ 
                                  newAthlete.lastname+"mail  "+ newAthlete.email+"ph"+ newAthlete.phone)
            DataService.addAthlete(params.clubId, params.week, params.cellid, newAthlete.firstname, 
                                  newAthlete.lastname, newAthlete.email, newAthlete.phone).then(
             function(results){
                    newAthlete.id = results.data;
                    $scope.athletes.push(newAthlete);
                    $scope.athlete.firstname = "";
                    $scope.athlete.lastname = "";
                },
                function(results){
                 alert("اینترنت خود را بررسی کنید.");
                });
        }
    }
    
     $scope.deleteAthlete = function(athlete){
        // DataService.removeAthlete(index).then (
        //  function(results){
            $scope.athletes = jQuery.grep($scope.athletes, function(value) {
              return value != athlete;
            });
                //$scope.athletes.splice(index,1);
            // },
            // function(results){
            //  alert("اینترنت خود را بررسی کنید.");
            // });
     }

  $scope.ok = function () {
    $modalInstance.close();
  };
});
