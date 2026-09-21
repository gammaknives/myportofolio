from django.shortcuts import render, redirect, get_object_or_404

from main.models import Experience

from main.models import Project
from main.forms import ProjectForm, ExperienceForm
from django.db.models import Q


from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse


def show_main(request):
    context = {
        "name": "Nuno",
        "full_name": "Nuno Mikael Nugroho",
        "npm": "2506624865",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS Student at Universitas Indonesia fighting to survive. "
            "I like watching movies, listening to music, and playing video games."
        ),
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

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_project(request):
    query = request.GET.get("q", "").strip()

    json_response = get_project_json(request)
    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    projects = [project.object for project in projects]

    context = {
        "name": "Nuno",
        "project_list": projects,
        "query": query,
    }
    return render(request, "projects.html", context)

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

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project successfully deleted!")
        return redirect("main:show_project")

    return redirect("main:show_project")

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

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully deleted!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")