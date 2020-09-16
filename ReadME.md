# Readme
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

Video link: https://l.messenger.com/l.php?u=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F1KK-eqxsRXdM2ML3iEq7ixcjaN6YBfHMz%2Fview%3Fusp%3Dsharing&h=AT1rv_aHZH5zN9Lx0MmK9CUfzsCYxt3hS58CyBaUj7hr1mc-SpvvADgShaGoUEW9X_6u90DpDJlWDp2GQ3dFu3hDAJaGFiOdPmJ_dY2fIZAwMen7epyp74cA4FkXDpPJEzRqG3HAir_P_4Uy-4HT8w
