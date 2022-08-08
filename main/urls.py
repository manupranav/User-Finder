
from django.urls import path, include
from .views import RegisterView, SearchDetail, SearchList, CustomLoginView, LogoutView, home

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',home,name='home'),
    
]
