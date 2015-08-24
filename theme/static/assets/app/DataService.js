app.factory('DataService',
    function ($http) {

        var getAthletes = function(agreement){
            return $http.get("/api/enroll/session/list/club/"+agreement);
        }
        
        var addAthlete = function(athlete){
            
        }
        
        var removeAthlete = function(index){
            return true;   
        }
        
        var updateItem = function(item){
            items.$save(item);
        }
        var getSessionTable = function (clubId, week) {
            return $http.get("/api/session/schedules/"+clubId+"/"+week );
        };

        var getInfo = function (ProgramId) {
            return $http.get("/api/program/info/"+ProgramId );
        };

        var enrollSession = function (clubId, week, id) {
            return $http.post("/api/enroll/session/"+clubId+"/"+week+"/"+id );
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
            updateItem : updateItem,
            /*delete : function(id){ // ng-resource 
                return request.delete({id : id});
            }*/
            /*save : function(day,start,duration,command,value){//command : single, multiple value : 10

            }*/
        };

    });
