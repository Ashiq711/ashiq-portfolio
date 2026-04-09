from django.urls import path,include
from . import views
from .views import payment_success


urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('ideas/', views.ideas),
    path('expertise/', views.expertise),
    path('articles/', views.articles),
    path('contact/', views.contact),
    path('projects/', views.projects),
    path('articles/', views.articles, name='articles'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('payment-success/',payment_success, name='payment_success'),
    path('idea/<int:id>/', views.idea_detail, name='idea_detail'),
]