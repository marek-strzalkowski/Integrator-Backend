from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileSerializer, ProfileUpdateSerializer, UserShortSerializer, ProfilePictureSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, DjangoModelPermissions, BasePermission, SAFE_METHODS

from .models import AppUser


class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj


class UserProfile(generics.RetrieveAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = AppUser.objects.all()
    serializer_class = ProfileSerializer


class EditProfile(generics.RetrieveUpdateAPIView, UserUpdatePermission):
    permission_classes = [UserUpdatePermission]    
    queryset = AppUser.objects.all() 
    serializer_class = ProfileUpdateSerializer


class UserShortProfile(APIView):
    def get(self, request):
        serializer = UserShortSerializer(self.request.user)
        return Response(serializer.data)


class EditProfilePicture(generics.RetrieveUpdateAPIView, UserUpdatePermission):
    permission_classes = [UserUpdatePermission]    
    queryset = AppUser.objects.all() 
    serializer_class = ProfilePictureSerializer