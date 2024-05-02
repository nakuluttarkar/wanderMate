from django.urls import path,include
from django.conf import settings
from . import views


app_name = 'core'


urlpatterns = [
    path('',views.index, name="index"),
    path('settings/',views.settings, name = "settings"),
    path('signin_signup/', views.signin_signup, name = "signinSignup"),
    path('like-post/',views.like_post, name = 'like-post'),
    path('add_comment', views.add_comment, name = "add_comment"),
    path('view_comments', views.view_comments, name="view_commens"),
    path('follow',views.follow, name="follow"),
    path('follower_list/', views.follower_list, name = "follower_list"),
    path('search',views.search, name="search"),
    # path('search_groups',views.search_groups, name="search_groups"),
    path('search_users_for_group/<int:group_id>', views.search_users_for_group, name='search_users_for_group'),
    path('add_participant/<int:group_id>/<int:user_id>/', views.add_participant, name='add_participant'),
    path('remove_participant/<int:group_id>/<int:user_id>/', views.remove_participant, name='remove_participant'),
    path('create_group/', views.create_group, name = "create_group"),
    path('group_detail/<int:group_id>/', views.group_detail, name='group_detail'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('leave_group/<int:group_id>', views.leave_group, name = "leave_group"),
    path('profile/<str:pk>',views.profile, name = 'profile'),
    path('verify_otp/',views.verify_otp, name = "verify_otp"),
    path('create_post/', views.create_post, name = "create_post"),
    path('chat/', views.chat, name = "chat"),
    # path('chat-room/',views.chat_room, name="chat_room"),
    path('logout/', views.logout, name = "logout"),

]
