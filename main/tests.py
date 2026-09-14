from django.template import response
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Gonzaga Festival Short Movie Competition Committee",
            description="Helped in planning and managing the competition from start to finish",
            category="volunteer",
            started_at=timezone.now(),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Gonzaga Festival Short Movie Competition Committee")
        self.assertEqual(self.experience.category, "volunteer")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, self.experience.get_category_display())
        self.assertContains(response, "Still going")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, str(self.experience.ended_at.year))
        self.assertNotContains(response, "Still going")

class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Boneka Bayangan",
            description="A short movie about a boy who loves to play with wayang (shadow puppets)",
            tags="Film, Directing, Scriptwriting",
            link="https://drive.google.com/file/d/1viMSeU9cqk5rn-jEcw4O9iR4YvgG2XaI/view?usp=sharing",
        )

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)

    def test_project_model(self):
        self.assertEqual(str(self.project), "Boneka Bayangan")
        self.assertEqual(self.project.get_tags(), ["Film", "Directing", "Scriptwriting"])

    def test_project_page(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Film")
        self.assertContains(response, "Directing")
        self.assertContains(response, "Scriptwriting")
        self.assertContains(response, self.project.link)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_project_without_link_has_no_view_project_button(self):
        Project.objects.all().delete()
        Project.objects.create(
            title="No Link Project",
            description="A project without an external link",
            tags="Test",
        )
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, "No Link Project")
        self.assertNotContains(response, "View Project")

    def test_project_search_matches_title(self):
        response = self.client.get(reverse("main:show_project"), {"q": "Boneka"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)

    def test_project_search_matches_tag(self):
        response = self.client.get(reverse("main:show_project"), {"q": "Directing"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)

    def test_project_search_matches_description(self):
        response = self.client.get(reverse("main:show_project"), {"q": "wayang"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)

    def test_project_search_no_results(self):
        response = self.client.get(reverse("main:show_project"), {"q": "xyz123nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.project.title)
        self.assertContains(response, 'No projects found matching "xyz123nonexistent"')

    def test_project_search_is_case_insensitive(self):
        response = self.client.get(reverse("main:show_project"), {"q": "boneka"})
        self.assertContains(response, self.project.title)