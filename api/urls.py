from django.urls import path
from . import views

urlpatterns = [
    # path('signup', views.user_list),
    path('user', views.CustomUserList.as_view()),
    path('snippet', views.FromSnippetList.as_view()),
    path('lang', views.LangList.as_view()),
    path('user/<int:pk>', views.user_detail),
]