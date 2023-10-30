from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from todolist.forms import *
from todolist.utils import DataMixin

globvar = None

def home_page(request):
    return render(request, "todolist/index.html", context={'title':"Главка"})


class Account(LoginRequiredMixin, DataMixin, ListView):
    model = UserList
    template_name = 'todolist/account.html'
    context_object_name = "lists"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not User.objects.filter(username=self.kwargs['username']):
            raise Http404("Нет такого пользователя!")
        if self.kwargs['username'] != self.request.user.username:
            raise Http404("У вас нет доступа к данной странице!")
        c_def = self.get_user_context(title="Личный кабинет")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return UserList.objects.filter(user__username=self.kwargs['username'])



class CreateList(LoginRequiredMixin, DataMixin, CreateView):
    form_class = CreateListForm
    template_name = 'todolist/createlist.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новый список')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateList, self).form_valid(form)

    def get_success_url(self):
        return '/account/'+self.request.user.username



class ListFormView(LoginRequiredMixin, DataMixin, DetailView):
    model = UserList
    template_name = 'todolist/listform.html'
    slug_url_kwarg = 'list_slug'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global globvar
        globvar = UserList.objects.get(slug=self.kwargs['list_slug'])
        print(globvar)
        tasks = Task.objects.filter(user_list__slug=self.kwargs['list_slug'])
        c_def = self.get_user_context(title='Ваш список', tasks=tasks)
        return dict(list(context.items()) + list(c_def.items()))


class CreateTask(LoginRequiredMixin, DataMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'todolist/createtask.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новая задача')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        global globvar
        form.instance.user_list = globvar
        return super(CreateTask, self).form_valid(form)

    def get_success_url(self):
        global globvar
        return '/account/'+self.request.user.username +'/' + globvar.slug


class UpdateTask(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = CreateTaskForm
    template_name = 'todolist/createtask.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редактировать задачу')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs['pk'])

    def form_valid(self, form):
        global globvar
        form.instance.user_list = globvar
        return super(UpdateTask, self).form_valid(form)

    def get_success_url(self):
        global globvar
        return '/account/'+self.request.user.username +'/' + globvar.slug


class DeleteTask(LoginRequiredMixin, DataMixin, DeleteView):
    model = Task
    context_object_name = 'task'


    def get_success_url(self):
        global globvar
        return '/account/'+self.request.user.username +'/' + globvar.slug


class DeleteList(LoginRequiredMixin, DataMixin, DeleteView):
    model = UserList
    context_object_name = 'list'


    def get_success_url(self):
        return '/account/' + self.request.user.username

class Registration(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'todolist/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class Login(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'todolist/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_from_site(request):
    logout(request)
    return redirect('home')