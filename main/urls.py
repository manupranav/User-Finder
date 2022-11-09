
from django.urls import path, include
from .views import RegisterView, SearchDetail, SearchList, CustomLoginView, LogoutView, SearchUpdate, SearchDelete,  home, create_search

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('create-search/', create_search, name='search-create'),
    path('', SearchList.as_view(), name='search-list'),
    path('search/<int:pk>', SearchDetail, name='search-detail'),
    path('search-update/<int:pk>', SearchUpdate.as_view(), name='search-update'),
    path('search-delete/<int:pk>', SearchDelete.as_view(), name='search-delete'),
    path('', home, name='home'),


    path("__reload__/", include("django_browser_reload.urls")),

]
