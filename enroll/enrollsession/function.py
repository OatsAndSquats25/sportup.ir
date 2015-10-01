from program.models import programDefinition
from programsession.views import sessionGenerateFull
from enroll.models import enrolledProgramSession

def enrollSessionFunction(request):
        _club = int(request.POST.get('club','-1'))
        _week = int(request.POST.get('week','-1'))
        _cellid = int(request.POST.get('cellid','-1'))

        if _club == -1 or _week == -1 or _cellid == -1:
            return False

        scheduleTable = sessionGenerateFull(_club, _week)
        cell = filter(lambda x: x.cellid == _cellid, scheduleTable)
        if not cell:
            return False
        if cell[0].capacity <= 0:
            return False

        prginst = programDefinition.objects.get(id = cell[0].prgid)
        enrolledProgramSession.objects.create(programDefinitionKey = prginst,
                                              amount = cell[0].price,
                                              date = cell[0].date,
                                              sessionTimeBegin = cell[0].begin,
                                              sessionTimeEnd = cell[0].end,
                                              user = request.user)

        return True