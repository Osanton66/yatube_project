from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_username_value = "testuser"
        cls.user = User.objects.create_user(username=cls.user_username_value)
        cls.group_slug_value = "testslug"
        Group.objects.create(
            title="Тестовая группа",
            slug=cls.group_slug_value,
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая запись",
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group-posts', kwargs={'slug': self.group_slug_value}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user_username_value}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}): 'posts/create_post.html',
        }
        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    #def test_index_show_correct_context(self):
    #    response = self.user.get(reverse('posts:index'))
