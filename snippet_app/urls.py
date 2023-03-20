from django.urls import path

from . import views

app_name = 'snippet_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/', views.SnippetListView.as_view(), name='list'),
    path('create/', views.SnippetCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.SnippetUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.SnippetDeleteView.as_view(), name='delete'),
]

