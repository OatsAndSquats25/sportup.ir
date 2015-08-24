
app.directive('registeredSessions',
    function () {
        return {
        	scope: {},
            restrict: 'E',
            //
            templateUrl: '/static/assets/app/registeredSessions/registeredSessions.html'
           /*template: '<article class="block" ng-Controller="sessionController"><header><h2>Daily Programs</h2></header><table class="timetable table  table-bordered ">'
            +'<thead><tr><th>SUNDAY</th><th>MONDAY</th><th>TUESDAY</th><th>WEDNESDAY</th><th>THURSDAY</th><th>FRIDAY</th><th>SATURDAY</th><th></th></tr></thead><tbody ><tr ng-repeat="time in timeTableRenderObject"><td ng-class="{\'event\' : day.type == 1}" ng-repeat="day in time " rowspan="{{day.span}}">                    <a href="#"  title="{{day.name}}">{{day.name}}</a>{{day.type == 1 ? createLabel(day) : \'\'}}</td><td ng-if="$index % labelTimeSpan == 0" class="text-center" rowspan="{{4}}">{{createLabel(label[$index / labelTimeSpan])}}</td></tr></tbody></table></article>'*/
        }

    });