"""BigDataProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path

import landing.views
import dashboard.views
import play.views
import user_settings.views
import authenticate.views
import quiz.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing.views.landing),
    path('home/', landing.views.landing, name='home'),
    path('dashboard/', dashboard.views.dashboard, name="dashboard"),
    path('play/<str:step>', play.views.play, name="play"),
    path('user_settings/<str:menu>', user_settings.views.user_settings, name="user_settings"),
    re_path(r'^get_questions/(?P<themes>[\d,]+)/$', play.views.get_questions, name='get_questions'),
    path('fake_model/', play.views.fake_model, name="fake_model"),
    path('signin/', authenticate.views.SigninPageView.as_view(), name="signin"),
    path('signup/', authenticate.views.SignupPageView.as_view(), name="signup"),
    path('signout/', authenticate.views.signout_user, name="signout"),
    path('quiz/', quiz.views.quiz_list, name="quiz_list"),
    path('quiz/<slug:quiz_hash>/', quiz.views.quiz_attempt, name="quiz_attempt")
]
