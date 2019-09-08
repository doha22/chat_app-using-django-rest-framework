from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse , HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import *
from chat.serializers import *

from django.urls import reverse_lazy


# function to check for user authentication
def index(request):

    if request.user.is_authenticated:
        return redirect('chats')


    if request.method == 'GET':
        return render(request, 'login.html', {})
                                                                                                                                                                                                                                                                                                                                                                                          # return redirect('index')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')

        return redirect('chats')










#user view
@csrf_exempt


def user_list(request, pk=None):

    if request.method == 'GET':
        if pk:
            # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)
        else:
            # Else get all user list
            users = User.objects.all()

        serializer = UserProfileInfoSerializer(users, many=True, context={'request': request})

        return JsonResponse(serializer.data, safe=False)

## login user
    elif request.method == 'POST':
        data = JSONParser().parse(request)           # On POST, parse the request object to obtain the data in json
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfileInfoSerializer.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)

        # data = JSONParser().parse(request)  # On POST, parse the request object to obtain the data in json
        # serializer = UserProfileInfoSerializer(data=data)  # Seraialize the data
        #
        # if serializer.is_valid():
        #     serializer.save()  # Save it if valid
        #     return JsonResponse(serializer.data, status=201)  # Return back the data on success
        # return JsonResponse(serializer.errors, status=400)  # Return back the errors  if not valid


def signup_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        print('hello')
        return redirect('chats')
    #else
    print('hello')
    return render(request, 'signup.html', {})



# view the messages once you one the chat app if your are already loggined
def message_view(request, sender, receiver):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "messages.html",
                      {'users': User.objects.exclude(username=request.user.username), #List of users
                       'receiver': User.objects.get(id=receiver), # Receiver context user object for using in template
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})
        # Return context with message objects where users are either sender or receiver.


# after login page it redirect to chat
# used in listing users and selecting them
def chat_view(request):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})
        #### note :
        #'users': User.objects.exclude(username=request.user.username)
        #Returning context for all users except the current logged-in user


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)

        serializer = MessageSerializer(messages, many=True, context={'request': request})

        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



