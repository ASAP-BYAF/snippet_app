from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

# from .models import User
# from .serializers import UserSerializer
from .serializers import SnippetModelSerializer
from .serializers import CustomUserModelSerializer
from snippet_app.models import Snippet
from accounts.models import CustomUser

@csrf_exempt # postman等にはcsrfは無いので無効化
def user_list(request):
    """
    - user の一覧を取得する
    - user を作成する
    """
    if request.method == 'GET':
        user = CustomUser.objects.all()
        serializer = CustomUserModelSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CustomUserModelSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

@csrf_exempt
def user_detail(request, pk):
    """
    単一のスニペットの、取得・更新・削除を行う。
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return HttpResponse(f'id = {pk} の user は存在しません。', status=404)

    if request.method == 'GET':
        serializer = CustomUserModelSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CustomUserModelSerializer(user, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        serializer.save()
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(f'id = {pk} の user が削除されました。', status=204)


class CustomUserList(APIView):
    """
    List all users, or create a new user.
    """
    # authentication_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserModelSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomUserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetList(APIView):
    """
    List all users, or create a new user.
    """
    # authentication_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        users = Snippet.objects.all()
        serializer = SnippetModelSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)