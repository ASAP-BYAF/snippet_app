from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.user_list),
    path('user/<int:pk>', views.user_detail),
]