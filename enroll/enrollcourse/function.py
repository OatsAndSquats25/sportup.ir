from program.models import programDefinition
from enroll.models import enrolledProgramCourse
from django.core.exceptions import ObjectDoesNotExist

def enrollCourseFunction(request):
    # TODO: check against re enroll
    try:
        programInst = programDefinition.objects.get(pk = request.POST.get('courseid'))
        enrolledProgramCourseInst = enrolledProgramCourse.objects.create(programDefinitionKey=programInst,
                                                                         amount= programInst.price,
                                                                         publish_date= programInst.publish_date,
                                                                         expiry_date= programInst.expiry_date,
                                                                         user=request.user)
    except ObjectDoesNotExist:
        return False
    return True

