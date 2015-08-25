from rest_framework import serializers


# ----------------------------------------------------
class cell(object):
    def __init__(self, prgid, date, day, begin, end, price, capacity):
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
# ----------------------------------------------------