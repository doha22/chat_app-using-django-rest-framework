from django.contrib.auth.models import User
from rest_framework import serializers
from chat.models import Message



# user serialization
class UserProfileInfoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'password']


class MessageSerializer(serializers.ModelSerializer):

    # slug field to view to user the username of sender and reciver
    # one to one relation
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    reciever = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields =['sender' , 'reciver' ,'message','timestamp' ]