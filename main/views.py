from urllib import request
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
import json
import requests
from requests import Session
from django.http import HttpResponse

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import SearchTerm, SearchResult

from .forms import SearchForm


from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async


import aiohttp
import asyncio
from aiohttp import TCPConnector


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

        return super(RegisterView, self).get(*args, **kwargs)


def home(request):
    return render(request, 'main/home.html')


class SearchList(LoginRequiredMixin, ListView):
    model = SearchTerm
    template_name = 'main/home.html'
    context_object_name = 'searches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searches'] = context['searches'].filter(
            user=self.request.user)
        return context


def SearchDetail(request, pk):
    search = SearchResult.objects.filter(term_id=pk)
    # filter speifically the value and ignore everthing else
    search_test = SearchTerm.objects.filter(
        id=pk).values_list('name', flat=True)[0]
    context = {'searches': search, 'search_test': search_test}

    return render(request, 'main/search_detail.html', context)


class SearchCreate(LoginRequiredMixin, CreateView):
    model = SearchTerm
    fields = ['name']
    success_url = reverse_lazy('search')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SearchCreate, self).form_valid(form)


class SearchUpdate(LoginRequiredMixin, UpdateView):
    model = SearchTerm
    fields = ['name']
    success_url = reverse_lazy('search')


class SearchDelete(LoginRequiredMixin, DeleteView):
    model = SearchTerm
    context_object_name = 'search'
    success_url = reverse_lazy('search-list')


async def get_page(session, url, urlMain, item):  # process request asynchronously
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0',
        'accept-language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }
    async with session.get(url, headers=headers) as response:
        st_code = response.status
        return url, st_code, urlMain, item


@database_sync_to_async
def create_name(user_q, name_q):
    search_term = SearchTerm.objects.create(
        user=user_q,
        name=name_q
    )
    return search_term


@database_sync_to_async
def result_save(host, search_term, urlMain, item, status):
    site_data = SearchResult(
        host=host,
        term=search_term,
        url=urlMain,
        sitename=item,
        search_status=status
    )
    site_data.save()


async def create_search(request):
    form = SearchForm()
    if request.method == 'POST':
        name = request.POST['name']
        # convert space to '_' to compatible with some websites.
        name = name.replace(' ', '_')

        with open('sites-data.json') as f:
            data = json.load(f)
            mod_data = json.loads(json.dumps(data).replace("{}", name))

            term_name = await create_name(request.user, name)

            tasks = []
            async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
                for item in mod_data:
                    if mod_data[item]['errorType'] == "status_code":
                        url = mod_data[item]['url']
                        urlMain = mod_data[item]['urlMain']
                        tasks.append(get_page(session, url, urlMain, item))
                results = await (asyncio.gather(*tasks))

                try:
                    for url, st_code, urlMain, item in results:
                        if st_code == 200:
                            await result_save(request.user, term_name, urlMain, item, 'CLAIMED')
                        else:
                            await result_save(request.user, term_name, urlMain, item, 'AVAILABLE')

                except Exception as e:
                    print(e)
            # store the id and redirect to the search result
            pk = term_name.id
            return redirect("search-detail", pk)

    context = {'form': form}
    return render(request, 'main/search.html', context)
