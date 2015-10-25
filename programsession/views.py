from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

import datetime

from generic.models import Displayable
from program.models import programDefinition
from enroll.models import enrolledProgram, enrolledProgramSession

from models import sessionDefinition, sessionRestriction
from serializers import cell, cellSerializer
# ----------------------------------------------------
def applySessionRestriction(restriction, cellInst):
    """
    apply restriction parameters for each cell
    """
    if restriction.capacityDiff:
        cellInst.capacity += restriction.capacityDiff
    if restriction.blackout:
        cellInst.status = 0
# ----------------------------------------------------
def sessionGenerate(singleSession, dateBegin, dateEnd, weekDay):
    """
    generate table of schedule based on layout, restriction and enrollment
    """
    days = {0:singleSession.daySat,
            1:singleSession.daySun,
            2:singleSession.dayMon,
            3:singleSession.dayTue,
            4:singleSession.dayWed,
            5:singleSession.dayThu,
            6:singleSession.dayFri}

    # Status
    # 0 active
    # 1 blackout
    # 2

    # create table base on layout
    lastDate = (now() + datetime.timedelta(singleSession.daysToShow)).date()
    cells = []
    cellDate = dateBegin
    # count = 0
    for day,status in days.iteritems():
        if status and cellDate <= lastDate and day >= weekDay:# and day >= weekDay and cellDate <= dateEnd:
            bgn = datetime.datetime.combine(datetime.date.today(), singleSession.sessionTimeBegin)
            end = datetime.datetime.combine(datetime.date.today(), singleSession.sessionTimeEnd)
            duration = singleSession.sessionDuration
            while bgn + datetime.timedelta(hours=duration.hour,minutes=duration.minute) < end:
                tempCell = cell(singleSession.id,
                                cellDate,
                                day,
                                bgn.time(),
                                (bgn + datetime.timedelta(hours=duration.hour,minutes=duration.minute)).time(),
                                singleSession.price,
                                singleSession.maxCapacity,
                                singleSession.ageMin,
                                singleSession.ageMax,
                                singleSession.get_genderLimit_display(),
                                singleSession.needInsurance,
                                singleSession.brief,
                                singleSession.description,
                                singleSession.title)
                # count += 1
                cells.append(tempCell)
                bgn += datetime.timedelta(hours=duration.hour,minutes=duration.minute)
        if day >= weekDay:
            cellDate += datetime.timedelta(days=1)

    # apply restriction condition on table
    # coditions for restrictions ---------
    #   date    day     begin   end
    #   +       -       +       +
    #   +       -       -       -
    #   -       +       +       +
    #   -       +       -       -
    #   -       -       +       +

    restrictions = sessionRestriction.objects.filter(sessionDefinitionKey = singleSession)
    for restriction in restrictions:
        if restriction.date is not None:
            if restriction.sessionTimeBegin and restriction.sessionTimeEnd:
                for cellInst in filter(lambda x :(x.date == restriction.date and x.begin>= restriction.sessionTimeBegin and x.end<=restriction.sessionTimeEnd), cells):
                    applySessionRestriction(restriction,cellInst)
            else:
                for cellInst in filter(lambda x :(x.date == restriction.date), cells):
                    applySessionRestriction(restriction,cellInst)
        elif restriction.day is not None:
            if restriction.sessionTimeBegin and restriction.sessionTimeEnd:
                for cellInst in filter(lambda x :(x.day == restriction.day and x.begin>= restriction.sessionTimeBegin and x.end<=restriction.sessionTimeEnd), cells):
                    applySessionRestriction(restriction,cellInst)
            else:
                for cellInst in filter(lambda x :(x.day == restriction.day), cells):
                    applySessionRestriction(restriction,cellInst)
        elif restriction.sessionTimeBegin is not None and restriction.sessionTimeEnd is not None:
            for cellInst in filter(lambda x :(x.begin>= restriction.sessionTimeBegin and x.end<=restriction.sessionTimeEnd), cells):
                    applySessionRestriction(restriction,cellInst)
        else:
            pass

    # apply enrolled information on table
    enrolls = enrolledProgramSession.objects.filter(programDefinitionKey = singleSession).\
        filter(date__gte = dateBegin).filter(date__lte = dateEnd ).exclude(status = Displayable.CONTENT_STATUS_INACTIVE).\
        values('date','sessionTimeBegin','sessionTimeEnd').annotate(count=Count('id'))
    for enroll in enrolls:
        for cellInst in filter(lambda x :(x.date==enroll['date'] and x.begin == enroll['sessionTimeBegin'] and x.end==enroll['sessionTimeEnd']), cells):
            cellInst.enroll     = enroll['count']
            cellInst.capacity  -= enroll['count']

    return cells
# ----------------------------------------------------
def sessionGenerateFull(club , showWeek):
        if showWeek < 0 or club == 0:
            return Response('None')

        #check program isvalid #todo

        #check week number >=0 and is valid with validation and user restriction #todo
        if showWeek< 0:
            return Response('Negative week not allowed!',status=status.HTTP_404_NOT_FOUND)

        # date and day calculation
        today = now()
        weekDay = (today.weekday()+2)%7     # move start of week from Mon to Sat

        if showWeek > 0:
            today += datetime.timedelta(days=((showWeek * 7) - weekDay ))
            weekDay = 0
        dateBegin = today.date()
        dateEnd = today.date() + datetime.timedelta(days=(6-weekDay))

        # retrive layout definition from database and make schedule table
        definitions = programDefinition.objects.instance_of(sessionDefinition).filter(clubKey = club).active()
        scheduleTable = []
        for definition in definitions:
            if definition.expiry_date.date() < dateEnd:             # check for end of the date must be same as program expire date
                dateEnd = definition.expiry_date.date()
            scheduleTable += sessionGenerate(definition, dateBegin, dateEnd, weekDay)

        if not scheduleTable:
            return 0
        # sort schedule table by day and begin time
        scheduleTable.sort(key=lambda x: (x.begin, x.day))

        # add cell to begin for general information
        min = scheduleTable[0].begin
        max = scheduleTable[0].end
        # for sch in scheduleTable:
        for idx, sch in enumerate(scheduleTable):
            sch.cellid = idx
            if sch.begin < min:
                min = sch.begin
            if sch.end > max:
                max = sch.end

        firstCell = cell(-1,
                         dateBegin,
                         weekDay,
                         min,
                         max,
                         -1,
                         2)
        scheduleTable.insert(0,firstCell)

        return scheduleTable
# ----------------------------------------------------
class sessionSchedule(generics.GenericAPIView):
# class sessionSchedule(APIView):
    """
    Full schedule for specific club with all layouts
    """
    serializer_class = cellSerializer
    def get(self, request, *args, **kwargs):
        """
        get generated schedule
        club        -- club id
        week        -- week number >=0 (0 is current week)
        """
        #input parameter club, week and validation #todo
        club = int(request.GET.get('club',0))
        showWeek = int(request.GET.get('week',0))

        if club == 0:
            return Response("Data not found", status=status.HTTP_204_NO_CONTENT)
        sessionTable = sessionGenerateFull(club, showWeek)
        if sessionTable == 0:
            return Response("Data not found", status=status.HTTP_204_NO_CONTENT)
        serializer = cellSerializer(sessionTable, many=True)
        return Response(serializer.data)
# ----------------------------------------------------
