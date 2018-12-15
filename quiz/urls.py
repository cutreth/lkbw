from django.urls import path

from quiz import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:category_id>/', views.question, name='question'),
]
