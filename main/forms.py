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
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tags": "Tag (pisahkan dengan koma)",
            "thumbnail": "URL Gambar Proyek",
            "link": "URL Proyek",
        }

        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Boneka Bayangan",
                "maxlength": 255,
            }),
            "description": Textarea(attrs={
                "placeholder": "Ceritakan proyekmu",
                "rows": 3,
            }),
            "tags": TextInput(attrs={
                "placeholder": "Film, Directing, Scriptwriting",
            }),
            "thumbnail": URLInput(attrs={
                "placeholder": "https://raw.githubusercontent.com/...",
            }),
            "link": URLInput(attrs={
                "placeholder": "https://drive.google.com/...",
            }),
        }