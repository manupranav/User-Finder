from urllib import request
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Search

# Create your views here.



class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterView(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterView, self).get( *args, **kwargs)


def home(request):
    return render(request,'main/home.html')

 

class SearchList(ListView):
    model = Search
    template_name = 'main/search_list.html'
    context_object_name = 'searches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searches'] = context['searches'].filter(user=self.request.user)

        return context

class SearchDetail(DetailView):
    model = Search
    template_name = 'main/search.html'
    context_object_name = 'search'

class SearchCreate(CreateView):
    model = Search
    fields = ['term']
    success_url = reverse_lazy('')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SearchCreate, self).form_valid(form)
