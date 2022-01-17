from rest_framework import serializers

from .models import Location
from users.models import AppUser


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        folowers = serializers.SerializerMethodField(read_only=True)   
        model = Location
        fields = ['id','name','followers']

    def get_followers(self, obj):
        return obj.followers.count()


class LocationsShortSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Location
        fields = ['id','name']


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id','first_name','last_name']


class LocationSerializer(serializers.ModelSerializer):        
    followers = UsersSerializer(read_only=True, many=True)
    followers_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Location
        fields = ['id','name','followers','followers_count','parent','is_following']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_is_following(self,obj):
        user =  self.context['request'].user
        if user in obj.followers.all():
            return True
        else:
            return False


class LocationFollowSerializer(serializers.ModelSerializer):        
    followers = UsersSerializer(read_only=True, many=True)    
    class Meta:
        model = Location
        fields = ['id','followers']
        