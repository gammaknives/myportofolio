from django.shortcuts import render, redirect, get_object_or_404

from main.models import Experience
from main.models import Project
from main.forms import ProjectForm, ExperienceForm
from django.db.models import Q


from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from functools import wraps
from django.core.exceptions import PermissionDenied

import datetime


def show_main(request):
    last_login = request.COOKIES.get("last_login", "No login session yet")
    context = {
        "name": "Nuno",
        "full_name": "Nuno Mikael Nugroho",
        "npm": "2506624865",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS Student at Universitas Indonesia fighting to survive. "
            "I like watching movies, listening to music, and playing video games."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Nuno",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experiences.html", context)

def get_project_json(request):
    query = request.GET.get("q", "").strip()
    projects = Project.objects.all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

def show_project(request):
    query = request.GET.get("q", "").strip()

    json_response = get_project_json(request)
    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    projects = [project.object for project in projects]
    is_editor = request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Nuno",
        "project_list": projects,
        "query": query,
        "is_editor": is_editor,
    }
    return render(request, "projects.html", context)

def owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:login")
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def owner_or_editor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:login")
        is_editor = request.user.groups.filter(name="Editor").exists()
        if not (request.user.is_superuser or is_editor):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

@owner_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New project successfully added!")
        return redirect("main:show_project")

    context = {
        "name": "Nuno",
        "form": form,
    }
    return render(request, "projects_form.html", context)

@owner_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project successfully deleted!")
        return redirect("main:show_project")

    return redirect("main:show_project")

@owner_or_editor_required
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project successfully updated!")
        return redirect("main:show_project")

    context = {
        "name": "Nuno",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)

@owner_required
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")

    context = {
        "name": "Nuno",
        "form": form,
    }
    return render(request, "experiences_form.html", context)

@owner_or_editor_required
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience successfully updated!")
        return redirect("main:show_experience")

    context = {
        "name": "Nuno",
        "form": form,
        "experience": experience,
    }
    return render(request, "experiences_form.html", context)

@owner_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully deleted!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Nuno",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response

    context = {
        "name": "Nuno",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

@login_required(login_url="main:login")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")