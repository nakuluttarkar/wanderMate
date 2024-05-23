from django.contrib import admin
from .models import FollowersCount, TravelGroup, Image, LikePost, Membership, Post, Profile, Comment, Room, Message, Preference, PreferenceOption
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(TravelGroup)
admin.site.register(Membership)
admin.site.register(Comment)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(PreferenceOption)
admin.site.register(Preference)