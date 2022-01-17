from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, DjangoModelPermissions, BasePermission, IsAuthenticated
from rest_framework import pagination

from .models import Post, Comment
from .serializers import PostsSerializer, PostLikeSerializer, CommentsSerializer, PostCreateSerializer, PostCommentSerializer
from locations.models import Location
from events.models import Event


class PostUserCreatorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.creator


class PostsPagination(pagination.PageNumberPagination):
   page_size = 4


class PostsList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    pagination_class = PostsPagination

     
class PostsLocationList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = PostsSerializer 
    pagination_class = PostsPagination   
    
    def get_queryset(self):
        id = self.request.query_params.get('id', None)        
        locations = Location.objects.filter(id=id)
        return Post.objects.filter(location__in=locations)


class PostsEventList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = PostsSerializer 
    pagination_class = PostsPagination   
    
    def get_queryset(self):
        id = self.request.query_params.get('id', None)        
        events = Event.objects.filter(id=id)
        return Post.objects.filter(event__in=events)


class PostLikeAction(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]        
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer
    
    def update(self, request, pk=None):        
        user = self.request.user        
        serializer = PostsSerializer(data=self.request.data)
        qs = Post.objects.filter(id=pk)
        if qs.exists():
            obj = qs.first()
            if user in obj.likes.all():
                obj.likes.remove(user)                
            else:
                obj.likes.add(user)                
            serializer = PostsSerializer(obj, context={'request': self.request})
            return Response(serializer.data, status=200)    
        else:            
            return Response(status=400)


class PostCommentAction(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]            
    serializer_class = CommentsSerializer
    
    def create(self, request, pk=None):
        user = self.request.user        
        serializer = CommentsSerializer(data=self.request.data)
        qs = Post.objects.filter(id=pk)
        if qs.exists():
            post = qs.first()
            serializer = PostCommentSerializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):        
                obj = serializer.save(creator=self.request.user, post=post)
                serializer = CommentsSerializer(obj, context={'request': self.request})
                return Response(serializer.data, status=201)
            else:            
                return Response(status=400)     
        else:            
            return Response(status=400)

    
class CommentsList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = CommentsSerializer    
    
    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        posts = Post.objects.filter(id=id)
        return Comment.objects.filter(post__in=posts)


class CreateEventPost(generics.CreateAPIView, PostUserCreatorPermission):
    permission_classes = [PostUserCreatorPermission]        
    serializer_class = PostCreateSerializer
    
    def create(self, request, *args, **kwargs):    
        id = self.request.query_params.get('id', None)
        events = Event.objects.filter(id=id)
        if events.exists():
            event = events.first()
            serializer = PostsSerializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):        
                obj = serializer.save(creator=self.request.user, event=event)
                serializer = PostsSerializer(obj, context={'request': self.request})
                return Response(serializer.data, status=201)
            else:            
                return Response(status=400)            
        else:            
            return Response(status=400)


class CreateLocationPost(generics.CreateAPIView, PostUserCreatorPermission):
    permission_classes = [PostUserCreatorPermission]        
    serializer_class = PostCreateSerializer
    
    def create(self, request, *args, **kwargs):    
        id = self.request.query_params.get('id', None)
        locations = Location.objects.filter(id=id)
        if locations.exists():
            locaiton = locations.first()
            serializer = PostsSerializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):        
                obj = serializer.save(creator=self.request.user, location=locaiton)
                serializer = PostsSerializer(obj, context={'request': self.request})
                return Response(serializer.data, status=201)
            else:            
                return Response(status=400)            
        else:            
            return Response(status=400)
