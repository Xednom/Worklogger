from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import (login as auth_login, authenticate)
from django.db.models import Sum
from django.db.models import Q
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import View, generic


from .forms import RegistrationForm, TimeForm
from .models import Project, Time


# Create your views here.
class HomeView(View):
    template_name = 'profiles/home.html'


class TimeForm(ModelForm):
    class Meta:
        model = Time
        fields = ['project', 'duration', 'remarks', 'date']


class RegistrationFormView(View):
    form_class = RegistrationForm
    template_name = 'profiles/account/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            _username = form.cleaned_data['username']
            _password = form.cleaned_data['password1']
            user.set_password(_password)
            user.save()
        return render(request, 'profiles/account/register.html', {'form': form})


def login(request):
    _message = "Please login"
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('add_project'))
            else:
                _message = 'Your account is not activated'
        else:
            _message = "Username or password is incorrect."
    context = {'message': _message,}
    return render(request, 'profiles/account/login.html', context)


def load_logs(request):
    queryset_list = Time.objects.all()
    query = request.GET.get("date")
    if query:
        queryset_list = queryset_list.filter(date__icontains=query)
    context = {
        "queryset_list": queryset_list
    }
    return render(request, 'profiles/projects/load_logs.html', context)


def add_project(request):

    all_project = Project.objects.all()
    all_time = Time.objects.all()
    total_duration = Time.objects.all().aggregate(Sum('duration'))
    if request.method == 'POST':
        time_form = TimeForm(request.POST or None)
        if time_form.is_valid():
            time_form.save()
            return redirect('add_project')
        return render(request, 'profiles/projects/project.html')
    else:
        time_form = TimeForm()

        context = {
            'time_form': time_form,
            'all_project': all_project,
            'all_time': all_time,
            'total_duration': total_duration
        }
        return render(request, 'profiles/projects/project.html', context)
