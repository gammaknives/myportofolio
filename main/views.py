from django.shortcuts import render

from main.models import Experience

from main.models import Project


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

def show_project(request):
    context = {
        "name": "Nuno",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)