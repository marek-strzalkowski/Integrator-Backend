from .views import LocationsList, LocationDetail, LocationsShortList, LocationFollowAction
from django.urls import path

app_name = 'locations'

urlpatterns = [
    path('', LocationsList.as_view(), name='listlocations'),
    path('item/<int:pk>/', LocationDetail.as_view(), name='detaillocation'),
    path('short/', LocationsShortList.as_view(), name='listlocationsshort'),
    
    path('follow/<int:pk>/', LocationFollowAction.as_view(), name='followlocation'),
]