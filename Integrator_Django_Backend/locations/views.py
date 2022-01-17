from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from .serializers import LocationsSerializer, LocationSerializer, LocationsShortSerializer, LocationFollowSerializer
from locations.models import Location


class LocationsList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = LocationsSerializer

    def get_queryset(self):
        sort = self.request.query_params.get('sort', None)        
        if sort == 'my':
            return Location.objects.filter(followers=self.request.user)
        elif sort == 'others':
            return Location.objects.exclude(followers=self.request.user)
        else:
            return Location.objects.all()


class LocationsShortList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Location.objects.all()
    serializer_class = LocationsShortSerializer


class LocationDetail(generics.RetrieveAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationFollowAction(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]        
    queryset = Location.objects.all()
    serializer_class = LocationFollowSerializer
    
    def update(self, request, pk=None):        
        user = self.request.user        
        serializer = LocationSerializer(data=self.request.data)
        qs = Location.objects.filter(id=pk)
        if qs.exists():
            obj = qs.first()
            if user in obj.followers.all():
                obj.followers.remove(user)
            else:
                obj.followers.add(user)            
            serializer = LocationSerializer(obj, context={'request': self.request})
            return Response(serializer.data, status=200)    
        else:            
            return Response(status=400)
