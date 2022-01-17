from rest_framework import serializers
from .models import Event, EventType
from users.serializers import UserShortSerializer


class EventsSerializer(serializers.ModelSerializer):
    going = serializers.SerializerMethodField(read_only=True)   
    location = serializers.SerializerMethodField(read_only=True)
    start = serializers.SerializerMethodField(read_only=True)  
    end = serializers.SerializerMethodField(read_only=True)  
    class Meta:
        model = Event
        fields = ['id','name','start','end','going','location','creator','info','address']

    def get_going(self, obj):
        return obj.going.count()

    def get_location(self, obj):
        return [obj.location.id, obj.location.name]

    def get_start(self, obj):
        return obj.start.strftime('%F, %H:%M')

    def get_end(self, obj):
        return obj.end.strftime('%F, %H:%M')
        

class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['name']


class EventSerializer(serializers.ModelSerializer):
    type = TypesSerializer(read_only=True, many=True)
    creator = UserShortSerializer(read_only=True, many=True)
    going_count = serializers.SerializerMethodField(read_only=True)   
    going = UserShortSerializer(read_only=True, many=True)
    location = serializers.SerializerMethodField(read_only=True)
    start = serializers.SerializerMethodField(read_only=True) 
    end = serializers.SerializerMethodField(read_only=True) 
    is_creator = serializers.SerializerMethodField(read_only=True)
    is_going = serializers.SerializerMethodField(read_only=True)    
    start_raw = serializers.SerializerMethodField(read_only=True) 
    end_raw = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = Event
        fields = ['id','name','start','end','going','going_count','location','creator','info','address','type','is_creator','is_going','start_raw','end_raw']

    def get_going_count(self, obj):
        return obj.going.count()

    def get_location(self, obj):
        return [obj.location.id, obj.location.name]

    def get_is_creator(self,obj):
        user =  self.context['request'].user
        if user in obj.creator.all():
            return True
        else:
            return False

    def get_is_going(self,obj):
        user =  self.context['request'].user
        if user in obj.going.all():
            return True
        else:
            return False

    def get_start(self, obj):
        return obj.start.strftime('%F, %H:%M')

    def get_end(self, obj):
        return obj.end.strftime('%F, %H:%M')

    def get_start_raw(self, obj):
        return obj.start

    def get_end_raw(self, obj):
        return obj.end

   
class EventCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Event
        fields = ['name','start','end','location','info','address']


class EventGoingSerializer(serializers.ModelSerializer):        
    followers = UserShortSerializer(read_only=True, many=True)    
    class Meta:
        model = Event
        fields = ['id','followers']
