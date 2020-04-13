from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Tweet, Hashtag
from django.http import HttpResponseRedirect

# Create your views here.

def splash(request):
  tweets = Tweet.objects.all().order_by("id").reverse()
  if request.method == "POST":
    content = request.POST["content"]
    tweet = Tweet.objects.create(content=content, author=request.user.username)
    tags = {tag.strip("#") for tag in content.replace('#', ' #').split() if tag.startswith("#")}
    print(tags)
#    tag = request.POST["hashtag"]
 #   hasht = tag.strip()
 #   hashtag = hasht.replace(" ", "") """
    for tag in tags:
      tagExists = False
      for hashtag in Hashtag.objects.all():
        if tag == hashtag.name:
          hashtag.tweets.add(tweet)
          tagExists = True

      if tagExists is False:
        newtag = Hashtag.objects.create(name=tag)
        newtag.tweets.add(tweet)
  return render(request, "splash.html", {"tweets": tweets})

def like(request, id):
  tweet = Tweet.objects.get(id=id)
  if request.user in tweet.likes.all():
    tweet.likes.remove(request.user)
  else:
    tweet.likes.add(request.user)
  tweet.save()
  tweet.refresh_from_db()
  tweets = Tweet.objects.all()
  return redirect('splash')

def hashtag(request, id):
  hashtag = Hashtag.objects.get(id=id)
  return render(request, "hashtag.html", {"hashtag": hashtag})

def home(request):
  return render(request, "home.html", {})  
  
def profile(request):
  tweets = Tweet.objects.filter(author=request.user.username)
  return render(request, "profile.html", {"tweets": tweets}) 

def login_(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('splash')
    return render(request, 'signup.html', {})

def logout_(request):
    logout(request)
    return redirect('signup')

def delete(request, id):
  if request.method == "GET":
    tweet = Tweet.objects.get(id=id)
    tweet.delete()
  return redirect('/')

def signup_view(request):
	user = User.objects.create_user(username=request.POST['username'],
					email=request.POST['email'],
					password=request.POST['password'])
	login(request, user)
	return redirect('/')

