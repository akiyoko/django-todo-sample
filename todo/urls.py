from django.urls import path

from . import views

urlpatterns = [
    # path('todo/', views.index),
    path('', views.TodoListView.as_view()),
    path('create/', views.TodoCreateView.as_view()),
    path('update/<int:pk>/', views.TodoUpdateView.as_view()),
]
