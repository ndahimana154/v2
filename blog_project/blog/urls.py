from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

      # Posts
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    path('profile/<str:username>/', views.profile_view, name='profile'),

    # Category Views
path('categories/', views.category_list, name='category_list'),
path('categories/add/', views.category_add, name='category_add'),
path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),


]
