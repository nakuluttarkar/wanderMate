from django.contrib import admin
from .models import FollowersCount, Image, LikePost, Post, Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(LikePost)
admin.site.register(FollowersCount)


