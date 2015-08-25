app.controller('sessionClubCtlr',
    ["$scope", "$window", "DataService", "$modal", "$modal", "$location", "$rootScope",
    function sessionClubCtlr($scope, $window, DataService, $modal, $location, $rootScope) {
        console.log("session controllerv start");
        $scope.timeTableRenderObject = [];

        $scope.openInfoModal = function () {
            var modalInstance = $modal.open({

              animation: $scope.animationsEnabled,
              templateUrl: 'ClubinfoModal.html',
              controller: 'infoModalCtrl',
              resolve: {
                info: function() {
                  return $scope.info;
                }
              }
            });
        modalInstance.result.then(function () {
              DataService.enrollSession($scope.clubId, $scope.week, $scope.info.cellid).then(
                    function (results) {
                        $location.change('finance/checkout/');
                    },
                    function (results) {
                        console.log("enrollment has error");
                    });
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
          if(event.status) {
            DataService.getInfo(event.prgid).then(
                 function(results) {
                     $scope.info = results.data;
                     $scope.info.cellid = event.cellid;
                     $scope.info.begin = Math.floor((event.begin) / 60) + ':' + ((((event.begin) % 60) < 10) ? '0' + ((event.begin) % 60) : ((event.begin) % 60));
                     $scope.info.end = Math.floor((event.end) / 60) + ':' + ((((event.end) % 60) < 10) ? '0' + ((event.end) % 60) : ((event.end) % 60));
                     $scope.info.date = event.date;
                     $scope.info.format = 'yyyy/MM/dd'
                     $scope.info.beginDate = $scope.beginDate;
                     $scope.openInfoModal();
                 },
                 function (results) {
                     alert(results.status + ': ' + results.statusText);
                 });
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

      var initialTable = function(clubId, week){
            //$scope.data = DataService.getSessionTable(clubId, week);
            //renderTimeTable($scope.data);
       DataService.getSessionTable(clubId, week).then(
                 function(results) {
                     $scope.data = results.data;
                     renderTimeTable($scope.data);
                 },
                 function (results) {
                     console.log(results.status + ': ' + results.statusText);
                     alert(results.status + ': ' + results.statusText);
                 });
        }
        $scope.clubId = $("#club").val();
        $scope.week = 0;
    initialTable($scope.clubId, $scope.week);
}]);

app.controller('infoModalCtrl', function ($scope, $modalInstance, info) {

  $scope.info = info;

  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

app.controller('deleteModalCtrl', function ($scope, $modalInstance) {

  //$scope.info = info;

  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

app.controller('addModalCtrl', function ($scope, $modalInstance) {

  //$scope.info = info;

  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});