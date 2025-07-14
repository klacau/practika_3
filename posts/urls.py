from django.http import HttpResponseRedirect
from django.urls import path, reverse
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/new/', views.PostCreateView.as_view(), name='create'),  
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('about/', views.AboutPageView.as_view(), name='about'),
]