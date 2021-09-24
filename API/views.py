from django.shortcuts import render, HttpResponse
from .models import Record
from datetime import datetime
from statistics import mean
# Create your views here.
def index(request):
    print(request.GET.get('h')) #request.POST.get
    return HttpResponse('Helooo World')

def swipe_in(request):
    '''
        POST for swipe in, given user_id and station_id and time_stamp
    '''
    user_id = request.POST.get('user_id')
    station_id = request.POST.get('station_id')
    all_records = Record.objects.all()
    action = 'swipe_in'
    timestamp = datetime.strptime(request.POST.get('datetime'), '%d/%m/%Y %H:%M').replace(tzinfo=None) #11 -> 10 + Invalid time + 11 -> 10

    last_record = all_records.filter(user_id=user_id).last()

    if last_record and last_record.action != "swipe_out": return HttpResponse('Please swipe out first')
    if last_record and last_record.datetime.replace(tzinfo=None) >= timestamp: return HttpResponse("Can't swipe_in in past")

    record = Record(user_id=user_id, station_id=station_id, action=action, datetime=timestamp)

    record.save()

    return HttpResponse("Request done !!")

def swipe_out(request):
    '''
        POST for swipe out, given user_id and station_id and time_stamp
    '''
    user_id = request.POST.get('user_id')
    station_id = request.POST.get('station_id')
    action = 'swipe_out'
    timestamp = datetime.strptime(request.POST.get('datetime'), '%d/%m/%Y %H:%M').replace(tzinfo=None)

    all_records = Record.objects.all()
    last_record = all_records.filter(user_id=user_id).last()
    print("Last record", last_record)
    if last_record is None: return HttpResponse('Please swipe in first')
    if last_record.action != "swipe_in": return HttpResponse('Please swipe in first')
    if last_record.datetime.replace(tzinfo=None) >= timestamp: return HttpResponse("Can't swipe_out in past")
    if last_record.station_id == station_id: return HttpResponse('Cannot swipe out at the same station you swiped in')


    record = Record(user_id=user_id, station_id=station_id, action=action, datetime=timestamp)

    record.save()

    return HttpResponse("Request done !!")


def get_avg_time(request):
    station_1 = request.GET.get('station_1')
    station_2 = request.GET.get('station_2')
    # first_swipe_in = Record.objects.filter(action='swipe_in').filter(station_id=station_1).all()
    # get_swipe_out(first_swipe_in)
    travel_times = []
    for swipe_in in Record.objects.filter(station_id=station_1, action='swipe_in'):
        swipe_out = get_swipe_out(swipe_in)
        print(swipe_out.station_id, station_2)
        if swipe_out is not None and swipe_out.station_id == station_2:
            print(swipe_in.datetime, swipe_out.datetime)
            travel_times.append((swipe_out.datetime - swipe_in.datetime).seconds/60)

    if travel_times==[] : return HttpResponse('No journeys has been completed between these stations so far')
    print(travel_times)
    return HttpResponse(str(round(mean(travel_times), 2)))
    




def get_swipe_out(swipe_in):
    print('swipe_out_accessed')
    user_swipe_out = Record.objects.filter(user_id=swipe_in.user_id, action='swipe_out' , datetime__gt = swipe_in.datetime).first()
    return user_swipe_out