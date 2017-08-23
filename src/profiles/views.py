from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import (login as auth_login, authenticate)
from django.db.models import Sum
from django.db.models import Q
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from .forms import RegistrationForm, ProjectForm, TimeForm
from .models import Project, Time


# Create your views here.
def home(request):
    return render(request, 'profiles/home.html')

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project', 'remarks']

class TimeForm(ModelForm):
    class Meta:
        model = Time
        fields = ['date','duration']

def login_information(request):
    all_project = Project.objects.all()
    all_time = Time.objects.all()
    context = {
    'all_project': all_project,
    'all_time': all_time
    }
    return render(request, 'profiles/projects/login_information.html', context)

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

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'profiles/account/login.html')
        else:
            return render(request, 'profiles/account/register.html', {'form': form})
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'profiles/account/register.html', args)

def add_project(request):
    all_project = Project.objects.all()
    all_time = Time.objects.all()
    total_duration = Time.objects.all().aggregate(Sum('duration'))
    if request.method == 'POST':
        project_form = ProjectForm(request.POST or None)
        time_form = TimeForm(request.POST or None)
        if project_form.is_valid():
            project_form.save()
        if time_form.is_valid():
            time_form.save()
            return redirect('add_project')
        context = {
        'project_form': project_form,
        'time_form': time_form,
        'all_project': all_project,
        'all_time': all_time,
        'total_duration': total_duration
        }
        return render(request, 'profiles/projects/project.html', context)
    else:
        project_form = ProjectForm()
        time_form = TimeForm()

        context = {
        'project_form': project_form,
        'time_form': time_form,
        'all_project': all_project,
        'all_time': all_time,
        'total_duration': total_duration
        }
        return render(request, 'profiles/projects/project.html', context)
