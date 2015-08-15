from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import datetime

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
        cellInst.status = 1
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
    cells = []
    cellDate = dateBegin
    for day,status in days.iteritems():
        if status:# and day >= weekDay and cellDate <= dateEnd:
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
                                singleSession.maxCapacity)
                if day < weekDay or cellDate > dateEnd:
                    tempCell.status = 1
                cells.append(tempCell)
                bgn += datetime.timedelta(hours=duration.hour,minutes=duration.minute)
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
        if restriction.date:
            if restriction.sessionTimeBegin and restriction.sessionTimeEnd:
                for cellInst in filter(lambda x :(x.date == restriction.date and x.begin>= restriction.sessionTimeBegin and x.end<=restriction.sessionTimeEnd), cells):
                    applySessionRestriction(restriction,cellInst)
            else:
                for cellInst in filter(lambda x :(x.date == restriction.date), cells):
                    applySessionRestriction(restriction,cellInst)
        elif restriction.day:
            if restriction.sessionTimeBegin and restriction.sessionTimeEnd:
                for cellInst in filter(lambda x :(x.day == restriction.day and x.begin>= restriction.sessionTimeBegin and x.end<=restriction.sessionTimeEnd), cells):
                    applySessionRestriction(restriction,cellInst)
            else:
                for cellInst in filter(lambda x :(x.day == restriction.day), cells):
                    applySessionRestriction(restriction,cellInst)
        elif restriction.sessionTimeBegin and restriction.sessionTimeEnd:
            for cellInst in filter(lambda x :(x.begin>= restriction.sessionTimeBegin and x.end<=restriction.sessionTimeEnd), cells):
                    applySessionRestriction(restriction,cellInst)
        else:
            pass

    # apply enrolled information on table
    enrolls = enrolledProgramSession.objects.filter(programDefinitionKey = singleSession).filter(date__gte = dateBegin).filter(date__lte = dateEnd ).values('date','sessionTimeBegin','sessionTimeEnd').annotate(count=Count('id'))
    for enroll in enrolls:
        for cellInst in filter(lambda x :(x.date==enroll['date'] and x.begin == enroll['sessionTimeBegin'] and x.end==enroll['sessionTimeEnd']), cells):
            cellInst.enroll     = enroll['count']
            cellInst.capacity  -= enroll['count']

    return cells
# ----------------------------------------------------
class sessionSchedule(APIView):
    # """
    # This view return sessions' schedule for specific club
    # """
    def get(self, request, format=None):
        #input parameter club, week and validation #todo
        showWeek = 0
        club = 1
        if showWeek <0 :
            return Response('None')

        #check program isvalid #todo

        #check week number >=0 and is valid with validation and user restriction #todo

        # date and day calculation
        today = now()
        weekDay = (today.weekday()+2)%7     # move start of week from Mon to Sat
        if showWeek > 0:
            today += datetime.timedelta(days=((showWeek * 7) - weekDay ))
            weekDay = 0
        dateBegin = today.date()
        dateEnd = today.date() + datetime.timedelta(days=(6-weekDay))

        # retrive layout definition from database and make schedule table
        definitions = programDefinition.objects.instance_of(sessionDefinition).filter(clubKey = club)
        scheduleTable = []
        for definition in definitions:
            if definition.expiry_date.date() < dateEnd:             # check for end of the date must be same as program expire date
                dateEnd = definition.expiry_date.date()
            scheduleTable += sessionGenerate(definition, dateBegin, dateEnd, weekDay)

        # sort schedule table by day and begin time
        scheduleTable.sort(key=lambda x: (x.begin, x.day))

        # add cell to begin for general information
        min = scheduleTable[0].begin
        max = scheduleTable[0].end
        for sch in scheduleTable:
            if sch.begin < min:
                min = sch.begin
            if sch.end > max:
                max = sch.end

        firstCell = cell(-1,
                         datetime.date.today(),
                         -1,
                         min,
                         max,
                         -1,
                         -1)
        scheduleTable.insert(0,firstCell)

        serializer = cellSerializer(scheduleTable, many=True)
        return Response(serializer.data)
# ----------------------------------------------------
