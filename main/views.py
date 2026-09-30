from django.shortcuts import render, redirect, get_object_or_404
from main.models import Experience, Project
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
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
    is_editor = request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Nuno",
        "experience_list": Experience.objects.all(),
        "is_editor": is_editor,
    }
    return render(request, "experiences.html", context)

def get_project_json(request):
    query = request.GET.get("q", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tags": project.tags,
                "thumbnail": project.thumbnail or "",
                "link": project.link or "",
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)

def show_project(request):
    query = request.GET.get("q", "").strip()
    is_editor = request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Nuno",
        "query": query,
        "is_editor": is_editor,
        "form": ProjectForm(),
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

@login_required(login_url="main:login")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@login_required(login_url="main:login")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
            starred = False
        else:
            project.starred_by.add(request.user)
            starred = True

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "starred": starred,
                "count": project.starred_by.count(),
            })

    return redirect("main:show_project")


@login_required(login_url="main:login")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
            starred = False
        else:
            experience.starred_by.add(request.user)
            starred = True

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "starred": starred,
                "count": experience.starred_by.count(),
            })

    return redirect("main:show_experience")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add projects."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Project successfully added.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)