from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    fname = models.TextField(max_length = 30, blank = True)
    lname = models.TextField(max_length = 30, blank = True)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    profile_img = models.ImageField(upload_to = 'profile_images', default='defaultProfileImg.jpeg')
    location = models.CharField(max_length = 100, blank= True)
    otp_validated = models.BooleanField(default = False)
    is_preference_given = models.BooleanField(default=False)
    # preferences = models.ManyToManyField('Preference', blank=True)
    

    def __str__(self):
        return self.user.username
    
    
class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    user = models.CharField(max_length = 100)
    user_profile = models.ForeignKey(Profile, on_delete = models.CASCADE, default=None, null=False)
    post_location = models.CharField(max_length=100, blank=True)
    images = models.ManyToManyField('Image')
    caption = models.TextField()
    tag = models.CharField(max_length = 20, blank = True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default = datetime.now)
    no_of_likes = models.IntegerField(default = 0)
    

    def __str__(self):
        return self.user
    
class Image(models.Model):
    image = models.ImageField(upload_to='post_images', default='wanderMateLogo.png')

    def __str__(self):
        return self.image.name
    

class LikePost(models.Model):
    post_id = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)

    def __str__(self):
        return self.username 
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length = 100)
    user = models.CharField(max_length = 100)

    def __str__(self):
        return self.user
    
class TravelGroup(models.Model):
    name = models.CharField(max_length=100)
    group_image = models.ImageField(upload_to='group_images', blank = True)
    travel_location = models.CharField(max_length = 100, blank=True)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    category = models.CharField(max_length=20, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='joined_groups')
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_group = models.ForeignKey(TravelGroup, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username
    
class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    value = models.CharField(max_length=100000)
    date = models.DateTimeField(default=datetime.now, blank = True)
    user = models.CharField(max_length=100000)
    room = models.CharField(max_length=10000)

class Preference(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete = models.CASCADE, blank = True, default = None)
    is_preference_given = models.BooleanField(default = False)
    preferences = models.ManyToManyField('PreferenceOption')

    def __str__(self):
        return f"{self.user_profile.user.username} Preferences"

class PreferenceOption(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


    


    