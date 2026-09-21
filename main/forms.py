from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput

from main.models import Project, Experience


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tags",
            "thumbnail",
            "link",
        ]

        labels = {
            "title": "Project Name",
            "description": "Project Description",
            "tags": "Tags (comma-separated)",
            "thumbnail": "Project Image URL",
            "link": "Project URL",
        }

        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Boneka Bayangan",
                "maxlength": 255,
            }),
            "description": Textarea(attrs={
                "placeholder": "A short description of your project",
                "rows": 3,
            }),
            "tags": TextInput(attrs={
                "placeholder": "Research, Film, Hardware",
            }),
            "thumbnail": URLInput(attrs={
                "placeholder": "https://raw.githubusercontent.com/...",
            }),
            "link": URLInput(attrs={
                "placeholder": "https://drive.google.com/...",
            }),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Image URL",
            "started_at": "Start Date",
            "ended_at": "End Date (leave blank if ongoing)",
        }

        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Gonzaga Festival Short Movie Competition Committee",
                "maxlength": 255,
            }),
            "description": Textarea(attrs={
                "placeholder": "Describe what you did",
                "rows": 3,
            }),
            "category": Select(),
            "thumbnail": URLInput(attrs={
                "placeholder": "https://raw.githubusercontent.com/...",
            }),
            "started_at": DateInput(attrs={"type": "date"}),
            "ended_at": DateInput(attrs={"type": "date"}),
        }