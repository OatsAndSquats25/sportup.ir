app.factory('DataService',
    function ($http) {

        var getAthletes = function(id){
            return $http({
                url: "/api/enroll/session/list/club/", 
                method: "GET",
                params: {clubid: id}
             });
        }

        var getCellAthletes = function(clubId, week, cellId){
            return [{firstname:'علیو', lastname:'رضا', isDone: true}]
            // return $http({
            //     url: "/api/enroll/session/", 
            //     method: "GET",
            //     params: {club : clubId, week : week, cellid : cellId}
            //  });
        }

        getCellAthletes
        
        var addAthlete = function(athlete){
            
        }
        
        var removeAthlete = function(index){
            return true;   
        }
        
        var athleteAttended = function(id){
            return $http({
              url: "/api/access/", 
              method: "POST",
              data: {enrollid : id}
             });
        }
        var getSessionTable = function (clubId, week) {
            return $http({
                url: "/api/session/schedules/", 
                method: "GET",
                params: {club : clubId, week : week}
             });

        };

        var getInfo = function (ProgramId) {
            return $http.get("/api/program/info/"+ ProgramId );
             // return $http({
             //    url: "/api/program/info/", 
             //    method: "GET",
             //    params: {pk : ProgramId}
             // });
        };

        var enrollSession = function (clubId, week, id) {
            //return $http.post("/api/enroll/session/", clubId, week, id );
            return $http({
              url: "/api/enroll/session/", 
              method: "POST",
              data: {club : clubId, week : week, cellid : id}
             });
        };

        var enrollSessionList = function () {
            return $http.get("/api/enroll/session/list/" );
        };

        // var insertEmployee = function (newEmployee) {

        //     return $http.post("api/EmployeeWebApi/Post", newEmployee);
        // };

        // var updateEmployee = function (employee) {
        //     return $http.post("Employee/Update", employee);
        // };

        return {
            getSessionTable : getSessionTable,
            getInfo : getInfo,
            enrollSession : enrollSession,
            enrollSessionList : enrollSessionList,
            getAthletes : getAthletes,
            addAthlete : addAthlete,
            removeAthlete : removeAthlete,
            athleteAttended : athleteAttended,
            getCellAthletes : getCellAthletes,
            /*delete : function(id){ // ng-resource 
                return request.delete({id : id});
            }*/
            /*save : function(day,start,duration,command,value){//command : single, multiple value : 10

            }*/
        };

    });
