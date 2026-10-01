from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

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
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Title cannot consist of HTML tags only.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Description cannot consist of HTML tags only.")
        return description

    def clean_tags(self):
        tags = strip_tags(self.cleaned_data["tags"]).strip()
        if not tags:
            raise ValidationError("Tags cannot consist of HTML tags only.")
        return tags

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "ended_at",
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "category": "Category",
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
            "ended_at": DateInput(attrs={"type": "date"}),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Title cannot consist of HTML tags only.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Description cannot consist of HTML tags only.")
        return description