from django.urls import path
from . import views

app_name = 'api_app'
urlpatterns = [
    path('user_snippet', views.CustomUserList.as_view(), name='user_snippet'),
    path('snippet', views.FromSnippetList.as_view(), name='from_snippet'),
    path('lang', views.LangList.as_view(), name='lang'),
    path('user/<int:pk>', views.user_detail),
]