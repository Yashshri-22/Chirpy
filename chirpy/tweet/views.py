from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    query = request.GET.get('q')
    tweets = Tweet.objects.all().order_by('-created_at')
    
    if query:
        tweets = tweets.filter(
            Q(text__icontains=query) |          # tweet text
            Q(user__username__icontains=query)     # username
        )

    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'query': query,
    })
    
def my_tweets(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_tweets.html', {'tweets': tweets})

@login_required
def create_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES) # to accepts files as well
        if form.is_valid():
            tweet = form.save(commit=False) # just hold it in memory and dont commit directly to db
            tweet.user = request.user # assuming user is logged in
            tweet.save() # now save to db
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'create_tweet.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user) # only the owner can edit the tweet
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet) # as edit is the feature so some data will be there already hence adding instance
    return render(request, 'create_tweet.html', {'form': form})

def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username} 👋")
            return redirect('/tweet/?welcome=1')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})