
from django.urls import path, include
from .views import SearchDetail, SearchList, CustomLoginView, LogoutView, home

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',home,name='home'),
    
]
