from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, DjangoModelPermissions, BasePermission, IsAuthenticated
from rest_framework import pagination
from datetime import datetime

from .models import Event, EventType
from .serializers import EventsSerializer, EventSerializer, EventCreateSerializer, EventGoingSerializer
from locations.models import Location


class EventUserCreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user in obj.creator.all()


class EventsPagination(pagination.PageNumberPagination):
   page_size = 6


class EventsLocationPagination(pagination.PageNumberPagination):
   page_size = 3


class EventsList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = EventsSerializer   
    pagination_class = EventsPagination
    
    def get_queryset(self):
        sort = self.request.query_params.get('sort', None)        
        if sort == 'past':
            return Event.objects.filter(start__lte=datetime.now())
        elif sort == 'my':
            return Event.objects.filter(creator=self.request.user, start__gt=datetime.now())
        elif sort == 'mypast':
            return Event.objects.filter(creator=self.request.user, start__lte=datetime.now())
        elif sort == 'go':
            return Event.objects.filter(going=self.request.user, start__gt=datetime.now())
        elif sort == 'gopast':
            return Event.objects.filter(going=self.request.user, start__lte=datetime.now())
        elif sort == 'invite':
            return Event.objects.filter(invited=self.request.user, start__gt=datetime.now())
        elif sort == 'recommend':
            user = self.request.user
            locations = Location.objects.filter(followers=user)    
            return Event.objects.filter(location__in=locations, start__gt=datetime.now()).exclude(creator=user).exclude(going=user).exclude(invited=user)
        else:
            return Event.objects.filter(start__gt=datetime.now())


class EventsLocationList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = EventsSerializer   
    pagination_class = EventsLocationPagination 
    
    def get_queryset(self):
        id = self.request.query_params.get('id', None)        
        locations = Location.objects.filter(id=id)
        return Event.objects.filter(location__in=locations, start__gt=datetime.now())
    

class EventsTypeList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = EventsSerializer    
    
    def get_queryset(self):
        type = self.request.query_params.get('name', None)        
        types = EventType.objects.filter(name=type)
        return Event.objects.filter(type__in=types, start__gt=datetime.now())


class EventDetail(generics.RetrieveAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CreateEvent(generics.CreateAPIView, EventUserCreatorPermission):
    permission_classes = [EventUserCreatorPermission]    
    serializer_class = EventCreateSerializer
    def create(self, request, *args, **kwargs):    
        serializer = EventCreateSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):        
            serializer.save(creator=[self.request.user], going=[self.request.user])
            return Response(serializer.data, status=201)


class DeleteEvent(generics.RetrieveDestroyAPIView, EventUserCreatorPermission):
    permission_classes = [EventUserCreatorPermission]   
    queryset = Event.objects.all() 
    serializer_class = EventSerializer


class EditEvent(generics.RetrieveUpdateAPIView, EventUserCreatorPermission):
    permission_classes = [EventUserCreatorPermission]    
    queryset = Event.objects.all() 
    serializer_class = EventCreateSerializer


class EventGoingAction(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]        
    queryset = Event.objects.all()
    serializer_class = EventGoingSerializer
    
    def update(self, request, pk=None):        
        user = self.request.user        
        serializer = EventSerializer(data=self.request.data)
        qs = Event.objects.filter(id=pk)
        if qs.exists():
            obj = qs.first()
            if user in obj.going.all():
                obj.going.remove(user)
                obj.invited.remove(user)
            else:
                obj.going.add(user)
                obj.invited.remove(user)
            serializer = EventSerializer(obj, context={'request': self.request})
            return Response(serializer.data, status=200)    
        else:            
            return Response(status=400)
 