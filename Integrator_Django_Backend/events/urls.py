from .views import EventsList, EventDetail, EventsLocationList, EventsTypeList, CreateEvent, DeleteEvent, EditEvent, EventGoingAction
from django.urls import path

app_name = 'events'

urlpatterns = [
    path('', EventsList.as_view(), name='listevents'),
    path('item/<int:pk>/', EventDetail.as_view(), name='detailevent'),
    path('location/', EventsLocationList.as_view(), name='locationevents'),
    path('type/', EventsTypeList.as_view(), name='typeevents'),
    
    path('going/<int:pk>/', EventGoingAction.as_view(), name='goinglocation'),    
    path('create/', CreateEvent.as_view(), name='createevent'),    
    path('edit/<int:pk>/', EditEvent.as_view(), name='editevent'),
    path('delete/<int:pk>/', DeleteEvent.as_view(), name='deleteevent'),    
]