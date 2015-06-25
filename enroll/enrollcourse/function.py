
from enroll.models import enrolledProgramCourse

def enrollCourse(programInst):
    # TODO: check against re enroll
    enrolledProgramCourseInst = enrolledProgramCourse.objects.create(programDefinitionKey=programInst,
                                                                     amount= programInst.price,
                                                                     publish_date= programInst.publish_date,
                                                                     expiry_date= programInst.expiry_date)
    return enrolledProgramCourseInst