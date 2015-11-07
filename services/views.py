from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
import math

from services.models import Tracking, Path
from services.serializers import *


class TrackingViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):

    serializer_class = TrackingSerializer
    queryset = Tracking.objects.all()

    def is_valid_request(self, request):
        return 'lat' in request.data and 'long' in request.data

    @list_route(methods=['post'])
    def start(self, request):
        if not self.is_valid_request(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        t = Tracking()
        t.save()
        p = Path(tracking_id=t.id, lat=request.data['lat'], long=request.data['long'])
        p.save()
        return Response(t.id)

    @list_route(methods=['post'])
    def stop(self, request):
        if not self.is_valid_request(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        id = int(request.GET['id'])
        t = Tracking.objects.get(id=id)
        t.stoptime = timezone.now()
        t.save()
        p = Path(tracking_id=t.id, lat=request.data['lat'], long=request.data['long'])
        p.save()
        return Response()

    @list_route(methods=['post'])
    def position(self, request):
        if not self.is_valid_request(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        id = int(request.GET['id'])
        p = Path(tracking_id=id, lat=request.data['lat'], long=request.data['long'])
        p.save()
        return Response()

class PathViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    queryset = Path.objects.all()
    serializer_class = PathSerializer

class HistoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    queryset = Path.objects.all()
    serializer_class = HistorySerializer

    def calc_dist(self, path):
        if len(path) < 2:
            return 0
        def d2(u,v):
            return math.sqrt((u.lat-v.lat)**2 + (u.long-v.long)**2)
        d = 0
        p0 = path[0]
        prev = p0
        for i in range(1, len(path)):
            e = path[i]
            d += d2(prev, e)
            prev = e
        return d

    def convert_timedelta(self, duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return {'hours': hours, 'minutes': minutes, 'seconds':seconds}

    def process_tracking(self, t):
        d = dict()
        d['start'] = t.starttime
        d['stop'] = t.stoptime
        q = self.get_queryset()
        paths = q.filter(tracking_id=t.id)
        d['kms'] = self.calc_dist(paths)
        dur = d['stop'] - d['start']
        d['duration'] = self.convert_timedelta(dur)
        d['speed'] = d['kms']/dur.seconds * 3600
        return d

    def list(self, request, *args, **kwargs):
        trackings = Tracking.objects.all()
        l = list()
        for track in trackings:
            l.append(self.process_tracking(track))
        return Response(l)
