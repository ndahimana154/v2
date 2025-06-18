from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.models import User


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



from .models import Category

def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)
    if category_id:
        posts = posts.filter(category__id=category_id)

    return render(request, 'blog/home.html', {
        'posts': posts,
        'query': query,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

from django.http import HttpResponseForbidden

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Permission check
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Edit Post'
    })

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Permission check
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'blog/post_delete.html', {'post': post})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_profile).order_by('-created_at')
    
    return render(request, 'blog/profile.html', {
        'profile_user': user_profile,
        'posts': posts
    })

from .models import Category
from .forms import CategoryForm

@login_required
def category_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


@login_required
def category_add(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required
def category_edit(request, category_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/category_form.html', {'form': form, 'title': 'Edit Category'})
