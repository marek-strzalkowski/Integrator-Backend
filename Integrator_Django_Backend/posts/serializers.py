from rest_framework import serializers

from .models import Comment, Post
from users.serializers import UserShortSerializer


class PostsSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)   
    location = serializers.SerializerMethodField(read_only=True)
    event = serializers.SerializerMethodField(read_only=True)
    creator = UserShortSerializer(read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True) 
    is_like = serializers.SerializerMethodField(read_only=True)
    class Meta:
        folowers = serializers.SerializerMethodField(read_only=True)   
        model = Post
        fields = ['id','text','url','location','event','likes','timestamp','creator','is_like']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_location(self, obj):
        if obj.location != None:
            return [obj.location.id, obj.location.name]

    def get_event(self, obj):
        if obj.event != None:
            return [obj.event.id, obj.event.name]

    def get_is_like(self,obj):
        user =  self.context['request'].user
        if user in obj.likes.all():
            return True
        else:
            return False

    def get_timestamp(self, obj):
        return obj.timestamp.strftime('%F, %H:%M')


class PostLikeSerializer(serializers.ModelSerializer):        
    likes = UserShortSerializer(read_only=True, many=True)    
    class Meta:
        model = Post
        fields = ['id','likes']


class PostCommentSerializer(serializers.ModelSerializer):            
    class Meta:
        model = Comment
        fields = ['text']


class CommentsSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)   
    timestamp = serializers.SerializerMethodField(read_only=True) 
    creator = UserShortSerializer(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    class Meta:
        folowers = serializers.SerializerMethodField(read_only=True)   
        model = Comment
        fields = ['id','text','url','likes','timestamp','creator','is_like']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_is_like(self,obj):
        user =  self.context['request'].user
        if user in obj.likes.all():
            return True
        else:
            return False

    def get_timestamp(self, obj):
        return obj.timestamp.strftime('%F, %H:%M')


class PostCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Post
        fields = ['text']