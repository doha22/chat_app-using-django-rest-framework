from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
import sqlparse

from django.core.cache import cache
# Create your models here.

#here there are 2 databases : 1-user (imported from django )

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



# 2-messages

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)

    # 0 means unread , 1 read
    is_read = models.BinaryField(default=0)


    def __str__(self):
           return self.message

     # order by timestamp
    class Meta:
           ordering = ('timestamp',)