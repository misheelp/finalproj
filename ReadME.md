# Readme
### Collaborator: Shannon Suhendra
### **Installation**

* First install all the necessary packages (namely Keras, Tensorflow, numpy, and Bulma)
* Run the code in the terminal using the command 

```
 python manage.py runserver
```
you may have to add your host to ALLOWED_HOSTS in the settings.py file 

### **Code Structure**
* Our app uses Django with the MVC code structure, with the urls.py file containing the routes and a views.py file
* We have methods in the views.py file to train and predict our machine learning model to generate an automatic reply 
* There are three models: *Tweet*, *Hashtag*, and *Replies*. Tweet and Hashtag were previously created for Assignment 6, and Replies is newly added. The Replies model represents a reply for a Tweet, and there is a One-To-Many relationship between a Tweet and Replies. 