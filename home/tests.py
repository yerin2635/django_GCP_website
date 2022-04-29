from django.test import TestCase
from django.test import client
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexWebpageTestCase(TestCase):

    def setUp(self):
        self.c = client.Client()

    def test_index_visiting(self):
        resp = self.c.get('/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login/login.html')


class LoginTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(email="papaya123@gmail.com", password="apple1234")
        self.c = client.Client()

    def test_http_login_and_logout(self):
        resp = self.c.post('/login/', {'email': 'papaya123@gmail.com', 'password': 'apple1234'}, follow=True)
        self.assertEqual(resp.redirect_chain, [('/home', 302)])
        resp = self.c.get('/home')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')
        self.c.get('/logout/')
        resp = self.c.get('/login/')
        self.assertEqual(resp.status_code, 200)


class ArticleTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(email='papaya123@gmail.com', password='apple1234')
        self.c = client.Client()
        resp = self.c.post('/login/', {'email': 'papaya123@gmail.com', 'password': 'apple1234'}, follow=True)
        self.assertEqual(resp.redirect_chain, [('/home', 302)])

    def test_create_article(self):
        resp = self.c.get('/article/')
        self.assertEqual(resp.status_code, 200)
        resp = self.c.post('/article/', {'title': '自動化測試文章', 'content': '測試文章ci/cd', 'photo': 'https://google.com',
                                         'location': '行天宮'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.c.get('/home')
        self.assertContains(resp, ' <a href="user/1">自動化測試文章 </a>')

    def test_delete_article(self):
        resp = self.c.get('/delete-posts/1')
        self.assertEqual(resp.status_code, 200)
