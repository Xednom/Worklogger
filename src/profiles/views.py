from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import (login as auth_login, authenticate)
from django.db.models import Sum
from django.db.models import Q
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.views.generic import View


from .forms import RegistrationForm, ProjectForm, TimeForm
from .models import Project, Time


# Create your views here.
def home(request):
    return render(request, 'profiles/home.html')

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['created_date']

class TimeForm(ModelForm):
    class Meta:
        model = Time
        fields = ['date','project','duration','remarks','description']

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
        return render(request, 'profiles/account/register.html', {'form':form})

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
