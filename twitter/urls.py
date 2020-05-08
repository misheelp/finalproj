"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import splash, signup_view, automatic_reply, reply, logout_, myprofile, home, delete, profile, login_, hashtag, like

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reply/<int:id>', reply, name='reply'),
    path('automatic_reply/<int:id>', automatic_reply, name='automatic_reply'),
    path('', splash, name='splash'),
    path('signup', signup_view, name='signup'),
    path('login', login_, name='signup'),
    path('myprofile', myprofile, name='myprofile'),
    path('profile/<str:id>', profile, name='profile'),
    path('splsh', home, name='home'),
    path('hashtag/<int:id>', hashtag, name='hashtag'),
    path('logout', logout_, name='logout'),
    path('/<int:id>', like, name='like'),
    path('delete/<int:id>', delete, name='delete')
]
