from django.urls import path
from . import views

urlpatterns = [
    # API urls
    path('api/sign_up/', views.UserSignUp.as_view()),
    path('api/sign_in/', views.UserSignIn.as_view()),

    # function based views
    path('signin/', views.sign_in),
    path('signup/', views.sign_up),
    path('signout/', views.sign_out),
]
