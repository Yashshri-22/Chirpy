from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

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
