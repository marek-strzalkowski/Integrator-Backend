from rest_framework import serializers
from users.models import AppUser


class UserSerializer(serializers.ModelSerializer):    
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = AppUser
        fields = ('email', 'user_name', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)        
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id','first_name','last_name']


class ProfileSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField(read_only=True)
    is_me = serializers.SerializerMethodField(read_only=True)   
    class Meta:
        model = AppUser
        fields = ['first_name','last_name','about','email','image','friends','location','is_me']

    def get_location(self, obj):
        if obj.location != None:
            return [obj.location.id, obj.location.name]
        else:
            return None

    def get_is_me(self,obj):
        user =  self.context['request'].user
        if user.id == obj.id:
            return True
        else:
            return False


class ProfileUpdateSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField(read_only=True)   
    class Meta:
        model = AppUser
        fields = ['id','about','location','is_me']

    def get_is_me(self,obj):
        user =  self.context['request'].user
        if user.id == obj.id:
            return True
        else:
            return False


class ProfilePictureSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField(read_only=True)   
    class Meta:
        model = AppUser
        fields = ['id','image','is_me']

    def get_is_me(self,obj):
        user =  self.context['request'].user
        if user.id == obj.id:
            return True
        else:
            return False