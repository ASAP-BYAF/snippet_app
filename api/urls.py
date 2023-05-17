from django.urls import path
from . import views

urlpatterns = [
    # path('signup', views.user_list),
    path('signup', views.CustomUserList.as_view()),
    path('snippet', views.SnippetList.as_view()),
    path('user/<int:pk>', views.user_detail),
]