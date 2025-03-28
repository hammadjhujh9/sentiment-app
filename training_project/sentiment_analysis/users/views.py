from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from textblob import TextBlob
from .models import Sentence
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Invalid credentials, please try again.")
    
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return HttpResponse("Passwords do not match.")
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    
    return render(request, 'signup.html')

@login_required
def index(request):
    user = request.user
    # Get all sentences ordered by timestamp (newest first)
    sentences = Sentence.objects.all().order_by('-created_at')
    return render(request, 'index.html', {
        'username': user.username, 
        'email': user.email,
        'sentences': sentences
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def upload_sentence(request):
    if request.method == 'POST':
        text = request.POST['text']
        blob = TextBlob(text)
        sentiment = 'positive' if blob.sentiment.polarity > 0 else 'negative' if blob.sentiment.polarity < 0 else 'neutral'
        sentence = Sentence(user=request.user, text=text, sentiment=sentiment)
        sentence.save()
        return redirect('index')
    
    return render(request, 'upload_sentence.html')