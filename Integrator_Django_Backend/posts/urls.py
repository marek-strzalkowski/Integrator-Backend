from .views import PostsList, PostsLocationList, PostsEventList, PostLikeAction, CommentsList, CreateEventPost, CreateLocationPost, PostCommentAction
from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('', PostsList.as_view(), name='listposts'),    
    path('location/', PostsLocationList.as_view(), name='locationposts'),
    path('event/', PostsEventList.as_view(), name='eventposts'),

    path('location/create/', CreateLocationPost.as_view(), name='createlocationpost'),
    path('event/create/', CreateEventPost.as_view(), name='createeventpost'),

    path('comments/', CommentsList.as_view(), name='postcomments'),    
    path('like/<int:pk>/', PostLikeAction.as_view(), name='likepost'),
    path('comment/<int:pk>/', PostCommentAction.as_view(), name='commentpost'),
]