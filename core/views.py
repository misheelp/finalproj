from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Tweet, Hashtag, Replies
from django.http import HttpResponseRedirect
import GetOldTweets3 as got
from numpy import array
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.models import model_from_json
import os

# generate a sequence from the model
def generate_seq(model, tokenizer, seed_text, n_words):
	in_text, result = seed_text, seed_text
	# generate a fixed number of words
	for _ in range(n_words):
		# encode the text as integer
		encoded = tokenizer.texts_to_sequences([in_text])[0]
		encoded = array(encoded)
		# predict a word in the vocabulary
		yhat = model.predict_classes(encoded, verbose=0)
		# map predicted word index to word
		out_word = ''
		for word, index in tokenizer.word_index.items():
			if index == yhat:
				out_word = word
				break
		# append to input
		in_text, result = out_word, result + ' ' + out_word
	return result

data = ""
first_word = ""

#gets the list of replies of a user
def allTweets(User):
  global data
  tweet = Tweet.objects.filter(author=User.username)
  list_of_replies = []
  for t in tweet:
    for r in Replies.objects.filter(tweet=t):
      list_of_replies.append(r.content.lower())
  data = " ".join(list_of_replies)

def trainModel(User):
  global data
  allTweets(User)
  if first_word + " " in data:
    # integer encode text
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([data])
    encoded = tokenizer.texts_to_sequences([data])[0]
    # determine the vocabulary size
    vocab_size = len(tokenizer.word_index) + 1
    # create word -> word sequences
    sequences = list()
    for i in range(1, len(encoded)):
      sequence = encoded[i-1:i+1]
      sequences.append(sequence)
    # split into X and y elements
    sequences = array(sequences)
    X, y = sequences[:,0],sequences[:,1]
    # one hot encode outputs
    y = to_categorical(y, num_classes=vocab_size)
    # define model
    model = Sequential()
    model.add(Embedding(vocab_size, 10, input_length=1))
    model.add(LSTM(50))
    model.add(Dense(vocab_size, activation='softmax'))
    print(model.summary())
    # compile network
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit network
    model.fit(X, y, epochs=500, verbose=2)
    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    return predict()
  else: 
    return first_word

#predicts the next word depending on the first word the user types in
def predict():
  global data
  global first_word
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts([data])
  # load json and create model
  json_file = open('model.json', 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  loaded_model = model_from_json(loaded_model_json)
  # load weights into new model
  loaded_model.load_weights("model.h5")
  # evaluate loaded model on test data
  loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
  return generate_seq(loaded_model, tokenizer, first_word, 6)

#allows user to reply to a tweet
def reply(request, id):
  tweet = Tweet.objects.get(id=id)
  if request.method == "POST":
    content = request.POST["content"]
    #create reply
    reply = Replies.objects.create(content=content, tweet=tweet, author=request.user.username)
  #gets the list of replies
  replies = Replies.objects.filter(tweet=tweet).order_by('-time')
  length = len(tweet)
  return render(request, "reply.html", {"tweet": tweet, "replies": replies, "length": length})  

#allows user to submit one word and automatically generates rest of the sentence
def automatic_reply(request, id):
  global first_word
  tweet = Tweet.objects.get(id=id)
  if request.method == "POST":
    #gets the first word so that we can train model and generate sequence of text
    first_word = request.POST["first_word"].lower()
    #train the model
    content = trainModel(User.objects.get(username=tweet.author))
    #create reply
    reply = Replies.objects.create(content=content, tweet=tweet, author=request.user.username)
    #get lists of replies
    replies = Replies.objects.filter(tweet=tweet).order_by('-time')
    return render(request, "reply.html", {"tweet": tweet, "reply": reply, "replies": replies})  
  return render(request, "reply.html", {})

def splash(request):
  if request.method == "POST":
    content = request.POST["content"]
    #create new tweet
    tweet = Tweet.objects.create(content=content, author=request.user.username)
    #gets hashtag
    tags = {tag.strip("#") for tag in content.replace('#', ' #').split() if tag.startswith("#")}
    for tag in tags:
      tagExists = False
      for hashtag in Hashtag.objects.all():
        if tag == hashtag.name:
          hashtag.tweets.add(tweet)
          tagExists = True
      if tagExists is False:
        newtag = Hashtag.objects.create(name=tag)
        newtag.tweets.add(tweet)
  #get list of tweets
  tweets = Tweet.objects.all().order_by("id").reverse()
  return render(request, "splash.html", {"tweets": tweets})

def like(request, id):
  #get the tweet id that is liked
  tweet = Tweet.objects.get(id=id)
  #if user already liked
  if request.user in tweet.likes.all():
    #user unlikes the tweet
    tweet.likes.remove(request.user)
  else:
    #user likes the tweet
    tweet.likes.add(request.user)
  tweet.save()
  tweet.refresh_from_db()
  tweets = Tweet.objects.all()
  return redirect('splash')

def hashtag(request, id):
  hashtag = Hashtag.objects.get(id=id)
  return render(request, "hashtag.html", {"hashtag": hashtag})

def home(request):
  try:
    user = User.objects.get(username='realDonaldTrump')
  except User.DoesNotExist:
    # Create a new user. There's no need to set a password
    # because only the password from settings.py is checked.
    user = User.objects.create_user(username='realDonaldTrump', password='Michelle11')
    user.save()
    
    
    tweetCriteria = got.manager.TweetCriteria().setUsername("realDonaldTrump")\
                                           .setTopTweets(True)\
                                           .setMaxTweets(10)
    twts = got.manager.TweetManager.getTweets(tweetCriteria)
    for tweet in twts:
      Tweet.objects.create(content=tweet.text, author='realDonaldTrump')
  return render(request, "home.html", {})  
  
def myprofile(request):
  #gets the tweet associated to the user that is logged in
  tweets = Tweet.objects.filter(author=request.user.username)
  return render(request, "profile.html", {"tweets": tweets, "user": "me"}) 

def profile(request, id):
  #gets the tweet associated to the user 
  user = User.objects.get(username=id)
  tweets = Tweet.objects.filter(author=user)
  return render(request, "profile.html", {"tweets": tweets, "user": user.username}) 

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

