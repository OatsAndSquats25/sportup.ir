from rest_framework import serializers


# ----------------------------------------------------
class cell(object):
    def __init__(self, prgid, date, day, begin, end, price, capacity, ageMin=0, ageMax=0, genderLimit='', needInsurance=False, brief='', description='', title=''):
        self.prgid  = prgid
        self.cellid = -1
        self.date   = date
        self.day    = day
        self.begin  = begin
        self.end    = end
        self.price  = price
        self.capacity= capacity
        self.enroll = 0
        self.status = 1
        self.ageMin = ageMin
        self.ageMax = ageMax
        self.genderLimit = genderLimit
        self.needInsurance = needInsurance
        self.brief = brief
        self.description = description
        self.title = title
# ----------------------------------------------------
class cellSerializer(serializers.Serializer):
        prgid   = serializers.IntegerField()
        cellid  = serializers.IntegerField()
        date    = serializers.DateField()
        day     = serializers.IntegerField()
        begin   = serializers.TimeField()
        end     = serializers.TimeField()
        price   = serializers.IntegerField()
        capacity= serializers.IntegerField()
        enroll  = serializers.IntegerField()
        status  = serializers.IntegerField()
        ageMin  = serializers.IntegerField()
        ageMax  = serializers.IntegerField()
        genderLimit = serializers.CharField()
        needInsurance = serializers.BooleanField()
        brief   = serializers.CharField()
        description = serializers.CharField()
        title = serializers.CharField()
# ----------------------------------------------------