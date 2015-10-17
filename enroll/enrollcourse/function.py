from program.models import programDefinition
from enroll.models import enrolledProgramCourse
from django.core.exceptions import ObjectDoesNotExist

def enrollCourseFunction(request):
    # TODO: check against re enroll
    _desc    = request.user.get_full_name()
    try:
        programInst = programDefinition.objects.get(pk = request.POST.get('courseid'))
        enrolledProgramCourseInst = enrolledProgramCourse.objects.create(programDefinitionKey=programInst,
                                                                         amount= programInst.price,
                                                                         publish_date= programInst.publish_date,
                                                                         expiry_date= programInst.expiry_date,
                                                                         user=request.user,
                                                                         title = _desc)
    except ObjectDoesNotExist:
        return False
    return True

