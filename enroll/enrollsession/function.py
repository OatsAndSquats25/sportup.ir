
from enroll.models import enrolledProgramCourse

def enrollSession(request, sessionInst):
    # TODO: check against re enroll
    # enrolledProgramCourseInst = enrolledProgramCourse.objects.create(programDefinitionKey=programInst,
    #                                                                  amount= programInst.price,
    #                                                                  publish_date= programInst.publish_date,
    #                                                                  expiry_date= programInst.expiry_date,
    #                                                                  user=request.user)
    # return enrolledProgramCourseInst