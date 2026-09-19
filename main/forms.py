from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project


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