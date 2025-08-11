from django.urls import path,include
from django.conf import settings
from . import views


app_name = 'core'


urlpatterns = [
    path('',views.index, name="index"),
    path('logout/', views.logout, name = "logout"),
    path('settings/',views.settings, name = "settings"),
    
    path('signin_signup/', views.signin_signup, name = "signinSignup"),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('like-post/',views.like_post, name = 'like-post'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('follow/', views.follow, name='follow'),
    path('view_comments/', views.view_comments, name="view_comments"),
    path('follower_list/', views.follower_list, name = "follower_list"),
    path('following_list/', views.following_list, name = "following_list"),
    path('search',views.search, name="search"),
    path('explore/', views.explore, name = "explore"),
    path('plan-trip/', views.planTrip, name="plan-trip"),
    path('packages/', views.packages, name="packages"),
    path('preference/', views.preference, name="preference"),
    path('search_users_for_group/<int:group_id>', views.search_users_for_group, name='search_users_for_group'),
    path('add_participant/<int:group_id>/<int:user_id>/', views.add_participant, name='add_participant'),
    path('remove_participant/<int:group_id>/<int:user_id>/', views.remove_participant, name='remove_participant'),
    path('create_group/', views.create_group, name = "create_group"),
    path('group_detail/<int:group_id>/', views.group_detail, name='group_detail'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('leave_group/<int:group_id>', views.leave_group, name = "leave_group"),
    path('profile/<str:pk>',views.profile, name = 'profile'),
    path('verify_otp/',views.verify_otp, name = "verify_otp"),
    path('verify_otp_for_forgot_password/<str:username>', views.verify_otp_for_forgot_password, name="verify_otp_for_forgot_password"),
    path('change_password/<str:username>',views.change_password, name= "change_password"),
    path('password_rest_success/', views.password_rest_success, name ="password_rest_success"),
    path('update_contact_info', views.update_contact_info, name = "update_contact_info"),
    path('create_post/', views.create_post, name = "create_post"),
    path('delete_post/<uuid:post_id>/', views.delete_post, name='delete_post'),
    path('chat/', views.chat, name = "chat"),
    path('checkRoom/<int:group_id>/<str:username>/', views.check_room, name='checkRoom'),
    path('user_chat_room/<str:follower>/<str:username>/', views.user_chat_room, name="user_chat_room"),
    path('<str:room>/', views.chat_room, name = "chat_room"),
    path('individual_chat_room/<str:room>/<str:follower>/<str:username>/', views.individual_chat_room, name='individual_chat_room'), 
    path('send', views.send, name="send"),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages')
    
    

]
