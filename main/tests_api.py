import datetime
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tags="Django",
        )
        self.initial_count = Project.objects.count()
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tags": "Python",
            "link": "https://example.com/", "thumbnail": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = next(p for p in response.data if p["id"] == str(self.project.id))
        self.assertFalse(item["is_starred"])
        self.assertNotIn("fields", item)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        # Search matches title, description, and tags (case-insensitive)
        for term in ("PORT", "website", "django"):
            response = self.client.get(self.list_url, {"q": term})
            self.assertIn(str(self.project.id), [p["id"] for p in response.data], term)
        response = self.client.get(self.list_url, {"q": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), self.initial_count)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"description": "<i></i>"}, "description"),
            ({"tags": "<b></b>"}, "tags"),
            ({"link": "javascript:alert(1)"}, "link"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), self.initial_count)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), self.initial_count)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_by_tag(self):
        other = Project.objects.create(title="Other", description="x", tags="Java, Film")
        third = Project.objects.create(title="Third", description="y", tags="JavaScript")

        def ids(params):
            return [p["id"] for p in self.client.get(self.list_url, params).data]

        self.assertIn(str(self.project.id), ids({"tag": "django"}))
        self.assertNotIn(str(other.id), ids({"tag": "django"}))
        self.assertIn(str(other.id), ids({"tag": "Java"}))
        self.assertNotIn(str(third.id), ids({"tag": "Java"}))
        self.assertNotIn(str(self.project.id), ids({"tag": "Dja"}))
        self.assertEqual(ids({"tag": "zzz-none"}), [])
        self.assertIn(str(other.id), ids({"tag": " film "}))
        self.assertIn(str(other.id), ids({"tag": "java", "q": "Other"}))
        self.assertNotIn(str(other.id), ids({"tag": "java", "q": "Portfolio"}))
        self.assertIn(str(self.project.id), ids({"tag": ""}))


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="exp-owner", password="test-password", email="exp-owner@example.com",
        )
        self.editor = User.objects.create_user(username="exp-editor", password="test-password")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        self.visitor = User.objects.create_user(username="exp-visitor", password="test-password")

        # An ongoing experience (no end date) and one that ended in 2019
        self.experience = Experience.objects.create(
            title="Lab Assistant", description="Helped in the lab", category="research",
        )
        self.ended = Experience.objects.create(
            title="Barista", description="Made coffee", category="part-time",
            ended_at=datetime.datetime(2019, 6, 30, 12, 0, tzinfo=datetime.timezone.utc),
        )
        # The seed migrations already add experiences, so compare against a baseline
        self.initial_count = Experience.objects.count()

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "New role", "description": "Did things", "category": "internship",
        }

    def result_ids(self, response):
        return [item["id"] for item in response.data]

    def assert_experience_unchanged(self):
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Lab Assistant")
        self.assertEqual(self.experience.description, "Helped in the lab")
        self.assertEqual(Experience.objects.count(), self.initial_count)

    # --- Reading ---

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = next(e for e in response.data if e["id"] == str(self.experience.id))
        self.assertFalse(item["is_starred"])
        self.assertTrue(item["is_ongoing"])
        self.assertEqual(item["category_display"], "Research")
        self.assertEqual(item["star_count"], 0)
        self.assertNotIn("fields", item)
        detail = self.client.get(self.detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["title"], "Lab Assistant")

    def test_search_title_category_status_and_year(self):
        ongoing_id = str(self.experience.id)
        ended_id = str(self.ended.id)

        for term in ("lab", "RESEARCH"):
            response = self.client.get(self.list_url, {"q": term})
            self.assertIn(ongoing_id, self.result_ids(response), term)

        response = self.client.get(self.list_url, {"q": "still"})
        self.assertIn(ongoing_id, self.result_ids(response))
        self.assertNotIn(ended_id, self.result_ids(response))

        response = self.client.get(self.list_url, {"q": "2019"})
        self.assertIn(ended_id, self.result_ids(response))
        self.assertNotIn(ongoing_id, self.result_ids(response))

        response = self.client.get(self.list_url, {"q": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        missing = uuid.uuid4()
        self.assertEqual(
            self.client.get(reverse("api:experience-detail", args=[missing])).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(
            self.client.post(reverse("api:experience-star", args=[missing])).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # --- Role permissions (with database checks) ---

    def test_guest_cannot_write_or_star(self):
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assert_experience_unchanged()
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_visitor_can_read_and_star_but_cannot_write(self):
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assert_experience_unchanged()
        self.assertEqual(self.client.post(self.star_url).status_code, 200)
        self.assertEqual(self.experience.starred_by.count(), 1)

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(self.detail_url, {"title": "By editor"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "By editor")
        self.assertEqual(self.experience.description, "Helped in the lab")

        replacement = {"title": "Replaced", "description": "Replaced text", "category": "internship"}
        response = self.client.put(self.detail_url, replacement, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Replaced")
        self.assertEqual(self.experience.category, "internship")

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), self.initial_count)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_staff_without_editor_group_cannot_update(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_experience_unchanged()

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        # The page sends a naive datetime string for the date input
        response = self.client.post(
            self.list_url, {**self.payload, "ended_at": "2024-05-01T00:00:00"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data["is_ongoing"])
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "New role")
        self.assertEqual(Experience.objects.count(), self.initial_count + 1)

        response = self.client.patch(self.detail_url, {"ended_at": None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_ongoing"])

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())
        self.assertEqual(Experience.objects.count(), self.initial_count)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # --- Validation ---

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": "<b></b>"}, "title"),
            ({"description": "<i></i>"}, "description"),
            ({"category": "banana"}, "category"),
            ({"ended_at": "not-a-date"}, "ended_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)

        response = self.client.post(self.list_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertEqual(Experience.objects.count(), self.initial_count)

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_experience_unchanged()

    def test_text_is_sanitized(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url, {**self.payload, "title": "<b>Bold</b> title"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Bold title")

    # --- Star ---

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.data["star_count"], 2)
        self.assertIn("exp-visitor", response.data["starred_by_names"])
        self.assertIn("exp-editor", response.data["starred_by_names"])

        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(self.experience.starred_by.count(), 1)

    def test_star_always_uses_the_logged_in_user(self):
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(
            self.star_url,
            {"user": self.owner.id, "starred_by": [self.owner.id]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = list(self.experience.starred_by.values_list("username", flat=True))
        self.assertEqual(usernames, ["exp-visitor"])

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.starred_by.count(), 0)

    # --- CSRF (real session login, not force_authenticate) ---

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="exp-owner", password="test-password"))
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assert_experience_unchanged()

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="exp-owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), self.initial_count + 1)

    def test_filter_by_category(self):
        def ids(params):
            return self.result_ids(self.client.get(self.list_url, params))

        research_id = str(self.experience.id)
        parttime_id = str(self.ended.id)

        self.assertIn(research_id, ids({"category": "research"}))
        self.assertNotIn(parttime_id, ids({"category": "research"}))
        self.assertIn(parttime_id, ids({"category": "part-time"}))
        self.assertIn(research_id, ids({"category": "RESEARCH"}))
        self.assertNotIn(parttime_id, ids({"category": "part"}))
        self.assertEqual(ids({"category": "banana"}), [])
        self.assertIn(research_id, ids({"category": "research", "q": "lab"}))
        self.assertNotIn(research_id, ids({"category": "research", "q": "barista"}))
        self.assertIn(research_id, ids({"category": ""}))
        self.assertIn(parttime_id, ids({"category": ""}))