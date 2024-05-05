from django.shortcuts import render, redirect
from blog.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def blog(request):
    if request.method == "POST":
        data = request.POST
        title = data.get('blog_title')
        description = data.get('blog_description')
        image = request.FILES.get('blog_image')
        print(title)
        
        BlogApp.objects.create(
            title = title,
            description = description,
            image = image
        )

        return redirect('/blog/')
    queryset = BlogApp.objects.all()

    if request.GET.get('Search'):
        queryset = queryset.filter(title__icontains = request.GET.get('Search'))
    context = {'blogs': queryset}
    return render(request, 'index.html', context)

def view_blog(request, id):
    queryset = BlogApp.objects.get(id = id)
    if request.method == "POST":
        data = request.POST

    context = {'view_blog': queryset}
    return render(request, 'view_blog.html', context)

def update_blog(request, id):
    queryset = BlogApp.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        title = data.get('blog_title')
        description = data.get('blog_description')
        image = request.FILES.get('blog_image')

        queryset.title = title
        queryset.description = description

        if image:
            queryset.image = image
        queryset.save()
        return redirect('/blog/')

    context = {'blog': queryset}
    return render(request, 'update_blog.html',context)

def delete_blog(request, id):
    queryset = BlogApp.objects.get(id = id)
    queryset.delete()
    return redirect('/blog/')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username already exists.")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully.")

    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username.")
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, "Invalid Password.")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/blog/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def about_us(request):
    return render(request, 'about-us.html')