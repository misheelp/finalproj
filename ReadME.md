# Readme

### **Routes**

* At the bottom, the "profile" link displays the currently logged in user's profile
*   The "logout" or "login" link will display whether a user is logged in or not
*   At the home page, you can click on the tags under each tweet to find the tweets associated with the hashtag
*   The "" or "/" route brings you to the homepage, where you can see every single tweet in vertical order

**Design considerations**: I created a many to many relationship between Tweets and hashtags so that I could access a tweet's hashtags and all the tweets associated with a hashtag. I also created the likes feature as many to many association between tweets and users. This allowed me to determine which users liked a certain tweet.

Also, note that you may have to add your host to ALLOWED_HOSTS in the settings.py file because I had to alter the field when deploying to Heroku

### Extra credit:
Deployed to a cloud service at:
https://twitter-clonecis192.herokuapp.com/