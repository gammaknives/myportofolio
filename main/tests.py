from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from main.models import Project, Experience
from main.forms import ProjectForm, ExperienceForm


class RoleTestMixin:
    """Shared setup for creating the four role types used across this app."""

    def create_users(self):
        self.owner = User.objects.create_superuser(username="test_owner", password="testpass123")

        self.editor = User.objects.create_user(username="test_editor", password="testpass123")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.plain_user = User.objects.create_user(username="test_plain", password="testpass123")

class ProjectAjaxTest(RoleTestMixin, TestCase):
    def setUp(self):
        Project.objects.all().delete()
        self.create_users()

        self.project = Project.objects.create(
            title="Boneka Bayangan",
            description="A short movie about shadow puppets",
            tags="Film, Directing, Scriptwriting",
            link="https://drive.google.com/example",
        )

    def test_get_project_json_status_ok(self):
        response = self.client.get(reverse("main:get_project_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_get_project_json_contains_expected_fields(self):
        response = self.client.get(reverse("main:get_project_json"))
        data = response.json()
        self.assertEqual(len(data), 1)
        fields = data[0]["fields"]
        self.assertEqual(fields["title"], "Boneka Bayangan")
        self.assertIn("star_count", fields)
        self.assertIn("is_starred", fields)
        self.assertIn("starred_by_names", fields)

    def test_get_project_json_search_filters_by_title(self):
        response = self.client.get(reverse("main:get_project_json"), {"q": "Boneka"})
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_get_project_json_search_filters_by_description(self):
        response = self.client.get(reverse("main:get_project_json"), {"q": "shadow puppets"})
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_get_project_json_search_filters_by_tag(self):
        response = self.client.get(reverse("main:get_project_json"), {"q": "Directing"})
        data = response.json()
        self.assertEqual(len(data), 1)

    def test_get_project_json_search_no_match_returns_empty_list(self):
        response = self.client.get(reverse("main:get_project_json"), {"q": "nonexistent123"})
        data = response.json()
        self.assertEqual(data, [])

    def test_get_project_json_is_starred_reflects_logged_in_user(self):
        self.project.starred_by.add(self.plain_user)
        self.client.login(username="test_plain", password="testpass123")
        response = self.client.get(reverse("main:get_project_json"))
        data = response.json()
        self.assertTrue(data[0]["fields"]["is_starred"])
        self.assertEqual(data[0]["fields"]["star_count"], 1)

    def test_get_project_json_is_starred_false_for_anonymous(self):
        self.project.starred_by.add(self.plain_user)
        response = self.client.get(reverse("main:get_project_json"))
        data = response.json()
        self.assertFalse(data[0]["fields"]["is_starred"])
        self.assertEqual(data[0]["fields"]["star_count"], 1)

    def test_create_project_ajax_requires_post(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.get(reverse("main:create_project_ajax"))
        self.assertEqual(response.status_code, 405)

    def test_create_project_ajax_rejects_anonymous(self):
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "New Project", "description": "Desc", "tags": "Tag",
        })
        self.assertEqual(response.status_code, 403)

    def test_create_project_ajax_rejects_plain_user(self):
        self.client.login(username="test_plain", password="testpass123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "New Project", "description": "Desc", "tags": "Tag",
        })
        self.assertEqual(response.status_code, 403)

    def test_create_project_ajax_rejects_editor(self):
        self.client.login(username="test_editor", password="testpass123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "New Project", "description": "Desc", "tags": "Tag",
        })
        self.assertEqual(response.status_code, 403)

    def test_create_project_ajax_succeeds_for_owner(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "New Project", "description": "Desc", "tags": "Tag",
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(title="New Project").exists())

    def test_create_project_ajax_invalid_data_returns_400(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "", "description": "Desc", "tags": "Tag",
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())

    def test_create_project_ajax_rejects_xss_only_title(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "<img src=x onerror=alert(1)>",
            "description": "Desc",
            "tags": "Tag",
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Project.objects.filter(title__icontains="img").exists())

    def test_create_project_ajax_strips_tags_from_mixed_content(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "Hello <b>World</b>",
            "description": "Desc",
            "tags": "Tag",
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(title="Hello World").exists())


class ExperienceAjaxTest(RoleTestMixin, TestCase):
    def setUp(self):
        Experience.objects.all().delete()
        self.create_users()

        self.experience = Experience.objects.create(
            title="Gonzaga Festival Committee",
            description="Helped plan the competition",
            category="volunteer",
        )

    def test_get_experience_json_status_ok(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)

    def test_get_experience_json_contains_expected_fields(self):
        response = self.client.get(reverse("main:get_experience_json"))
        fields = response.json()[0]["fields"]
        self.assertEqual(fields["title"], "Gonzaga Festival Committee")
        self.assertIn("is_ongoing", fields)
        self.assertIn("star_count", fields)

    def test_get_experience_json_search_filters_by_title(self):
        response = self.client.get(reverse("main:get_experience_json"), {"q": "Gonzaga"})
        self.assertEqual(len(response.json()), 1)

    def test_get_experience_json_search_no_match(self):
        response = self.client.get(reverse("main:get_experience_json"), {"q": "zzz_no_match"})
        self.assertEqual(response.json(), [])

    def test_create_experience_ajax_rejects_plain_user(self):
        self.client.login(username="test_plain", password="testpass123")
        response = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "New Experience", "description": "Desc", "category": "volunteer",
        })
        self.assertEqual(response.status_code, 403)

    def test_create_experience_ajax_rejects_editor(self):
        self.client.login(username="test_editor", password="testpass123")
        response = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "New Experience", "description": "Desc", "category": "volunteer",
        })
        self.assertEqual(response.status_code, 403)

    def test_create_experience_ajax_succeeds_for_owner(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "New Experience", "description": "Desc", "category": "volunteer",
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(title="New Experience").exists())

    def test_create_experience_ajax_rejects_xss_only_title(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "<img src=x onerror=alert(1)>",
            "description": "Desc",
            "category": "volunteer",
        })
        self.assertEqual(response.status_code, 400)


class RolePermissionTest(RoleTestMixin, TestCase):
    """Tests the owner_required / owner_or_editor_required decorators directly."""

    def setUp(self):
        Project.objects.all().delete()
        Experience.objects.all().delete()
        self.create_users()

        self.project = Project.objects.create(
            title="Test Project", description="Desc", tags="Tag",
        )
        self.experience = Experience.objects.create(
            title="Test Experience", description="Desc", category="volunteer",
        )

    def test_anonymous_redirected_to_login_on_delete_project(self):
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_plain_user_gets_403_on_delete_project(self):
        self.client.login(username="test_plain", password="testpass123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    def test_editor_gets_403_on_delete_project(self):
        self.client.login(username="test_editor", password="testpass123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_project(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_plain_user_gets_403_on_update_project(self):
        self.client.login(username="test_plain", password="testpass123")
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    def test_editor_can_access_update_project(self):
        self.client.login(username="test_editor", password="testpass123")
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_access_update_project(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_editor_gets_403_on_delete_experience(self):
        self.client.login(username="test_editor", password="testpass123")
        response = self.client.post(reverse("main:delete_experience", args=[self.experience.id]))
        self.assertEqual(response.status_code, 403)

    def test_editor_can_access_update_experience(self):
        self.client.login(username="test_editor", password="testpass123")
        response = self.client.get(reverse("main:update_experience", args=[self.experience.id]))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_delete_experience(self):
        self.client.login(username="test_owner", password="testpass123")
        response = self.client.post(reverse("main:delete_experience", args=[self.experience.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())


class StarTest(RoleTestMixin, TestCase):
    def setUp(self):
        Project.objects.all().delete()
        Experience.objects.all().delete()
        self.create_users()

        self.project = Project.objects.create(title="Test Project", description="Desc", tags="Tag")
        self.experience = Experience.objects.create(title="Test Experience", description="Desc", category="volunteer")

    def test_anonymous_redirected_to_login_on_star(self):
        response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_plain_user_can_star_project(self):
        self.client.login(username="test_plain", password="testpass123")
        self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertIn(self.plain_user, self.project.starred_by.all())

    def test_plain_user_can_unstar_project(self):
        self.project.starred_by.add(self.plain_user)
        self.client.login(username="test_plain", password="testpass123")
        self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertNotIn(self.plain_user, self.project.starred_by.all())

    def test_star_toggle_ajax_returns_json(self):
        self.client.login(username="test_plain", password="testpass123")
        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["starred"])
        self.assertEqual(data["count"], 1)

    def test_plain_user_can_star_experience(self):
        self.client.login(username="test_plain", password="testpass123")
        self.client.post(reverse("main:toggle_star_experience", args=[self.experience.id]))
        self.assertIn(self.plain_user, self.experience.starred_by.all())


class FormValidationTest(TestCase):
    def test_project_form_rejects_xss_only_title(self):
        form = ProjectForm(data={
            "title": "<img src=x onerror=alert(1)>",
            "description": "Desc",
            "tags": "Tag",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_project_form_rejects_xss_only_description(self):
        form = ProjectForm(data={
            "title": "Valid Title",
            "description": "<script></script>",
            "tags": "Tag",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def test_project_form_strips_tags_from_mixed_title(self):
        form = ProjectForm(data={
            "title": "Hello <b>World</b>",
            "description": "Desc",
            "tags": "Tag",
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Hello World")

    def test_experience_form_rejects_xss_only_title(self):
        form = ExperienceForm(data={
            "title": "<script></script>",
            "description": "Desc",
            "category": "volunteer",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_experience_form_strips_tags_from_mixed_description(self):
        form = ExperienceForm(data={
            "title": "Valid Title",
            "description": "Hello <i>World</i>",
            "category": "volunteer",
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["description"], "Hello World")