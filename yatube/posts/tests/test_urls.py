from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from http import HTTPStatus

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_username_value = "TestAuthor"
        cls.user = User.objects.create_user(username=cls.user_username_value)
        cls.user_not_author = User.objects.create_user(
            username="TestNotAuthor"
        )
        cls.group_slug_value = "testslug"
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug=cls.group_slug_value,
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая запись",
        )
        cls.url_unexisting_page = "/unexisting_page/"

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_not_author = Client()
        self.authorized_client_not_author.force_login(self.user_not_author)

    def test_guest_urls_access(self):
        """Страницы доступные любому пользователю."""

        url_names = {
            "/",
            f"/group/{self.group_slug_value}/",
            f"/profile/{self.user_username_value}/",
            f"/posts/{self.post.pk}/",
        }

        for address in url_names:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_guest_urls_redirect(self):
        """Переадресация неавторизованного пользователя на страницу с авторизацией."""

        url_names_redirects = {
            f"/posts/{self.post.pk}/edit/": (
                f"/auth/login/?next=/posts/{self.post.pk}/edit/"
            ),
            "/create/": "/auth/login/?next=/create/",
        }
        for address, redirect_address in url_names_redirects.items():
            with self.subTest(address=address):
                response = self.client.get(address, follow=True)
                self.assertRedirects(response, redirect_address)

    def test_auth_user_urls_template(self):
        """URL-адрес использует соответствующий шаблон для авторизованного пользователя."""
        url_names = {
            '/',
            '/create/',
            f'/group/{self.group_slug_value}/',
            f"/profile/{self.user_username_value}/",
            f"/posts/{self.post.pk}/",
            f"/posts/{self.post.pk}/edit/",
        }

        for address in url_names:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_user_notauthor_redirect(self):
        """Переадресация авторизованного пользователя, не являющимся автором поста при изменении чужой записи."""
        response = self.authorized_client_not_author.get(
            f"/posts/{self.post.pk}/edit/", follow=True
        )
        self.assertRedirects(response, f"/posts/{self.post.pk}/")

    def test_task_list_url_corret_templates(self):
        """Страницы доступные авторизованному пользователю."""

        url_names_templates = {
            "/": "posts/index.html",
            f"/group/{self.group_slug_value}/": "posts/group_list.html",
            f"/profile/{self.user_username_value}/": "posts/profile.html",
            f"/posts/{self.post.pk}/": "posts/post_detail.html",
            f"/posts/{self.post.pk}/edit/": "posts/create_post.html",
            "/create/": "posts/create_post.html",
        }
        for address, template in url_names_templates.items():
            with self.subTest(address=address):
                cache.clear()
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_page_not_found(self):
        """Страница не найдена."""
        response = self.client.get(self.url_unexisting_page)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
