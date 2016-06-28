from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


# Create your tests here.


class PostTestCase(TestCase):
    def setUp(self):
        usr1 = User.objects.create_user('user1', 'user1@mail.mm', 'p@ssw0rd')
        usr2 = User.objects.create_user('user2', 'user2@mail.mm', 'p@ssw0rd')
        Post.objects.create(title="test 1", body='Test body', author=usr1)
        Post.objects.create(title="test 2", body='Test body 2', author=usr2)

    def test_post_save(self):
        """
        Check, that save method automatically add slug field
        """
        post1 = Post.objects.get(title='test 1')
        post2 = Post.objects.get(title='test 2')
        self.assertEqual(post1.slug, 'test-1')
        self.assertEqual(post2.slug, 'test-2')

    def test_call_denies_anonymous_create_post(self):
        """
        Check that anonymous user cant't add post and vote for post
        """
        response = self.client.get('/add/', follow=True)
        self.assertRedirects(response, '/login/?next=/add/')
        post = Post.objects.get(slug='test-2')
        response = self.client.post('/vote/', {'action': "vote", 'id': post.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(response, '/login/?next=/vote/')

    def test_call_allow_logged(self):
        """
        Check that logged user can view add post page and vote for post
        """
        self.client.login(username='user1', password='p@ssw0rd')
        response = self.client.get('/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(slug='test-2')
        response = self.client.post('/vote/', {'action': "vote", 'id': post.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_add_post(self):
        """
        Check that logged user can add post
        """
        self.client.login(username='user1', password='p@ssw0rd')
        response = self.client.post('/add/', {'title': 'test post', 'body': 'some body'}, follow=True)
        self.assertContains(response, 'test post')

    def test_edit_post(self):
        """
        Check that logged user can edit post
        """
        post = Post.objects.get(slug='test-1')
        self.client.login(username='user1', password='p@ssw0rd')
        response = self.client.post('/edit/' + post.slug + '/', {'title': 'test post', 'body': 'some body 2'}, follow=True)
        self.assertContains(response, 'some body 2')

    def test_add_comment(self):
        """
        Check that logged user can add comment to post
        """
        post = Post.objects.get(slug='test-1')
        response = self.client.post(post.get_absolute_url(), {'name': 'test', 'body': 'test body'})
        self.assertEqual(response.status_code, 200)







