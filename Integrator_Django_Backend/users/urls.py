from django.urls import path
from .views import BlacklistTokenUpdateView, UserCreate, UserProfile, EditProfile, UserShortProfile, EditProfilePicture

app_name = 'users'

urlpatterns = [
    path('register/', UserCreate.as_view(), name='createuser'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),

    path('profile/<int:pk>/', UserProfile.as_view(), name='profiledetail'),
        
    path('edit/<int:pk>/', EditProfile.as_view(), name='editprofile'),
    path('editpicture/<int:pk>/', EditProfilePicture.as_view(), name='editprofilepicture'),
    
    path('authcheck/', UserShortProfile.as_view(), name='shortprofiledetail'),
]