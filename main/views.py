from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
 
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from .models import Search

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def home(request):
    return render(request,'main/home.html')

 

class SearchList(ListView):
    model = Search
    template_name = 'main/search_list.html'
    context_object_name = 'searches'

class SearchDetail(DetailView):
    model = Search
    template_name = 'main/search.html'
    context_object_name = 'search'