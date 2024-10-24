from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Article

class BlogAppTest(SimpleTestCase):

    def test_django(self):
        self.assertTrue(True)


class BlogDataTest(TestCase):
    def test_blog(self):
        self.assertEqual(len(Article.objects.all()), 0)
        Article.objects.create(title='Title 1')
        Article.objects.create(title='Title 2')
        self.assertEqual(len(Article.objects.all()), 2)

        a = Article.objects.get(pk=2)
        self.assertEqual(a.title, 'Title 2')

        a.title = "New Title"
        a.save()
        self.assertEqual(a.title, 'New Title')

        a.delete()
        self.assertEqual(len(Article.objects.all()), 1)
    
    def setUp(self):
        self.user, self.user_args = create_test_user()
        self.article1 = Article.objects.create(user=self.user, name='Chuck Dickens')
        self.article2 = Article.objects.create(user=self.user, name='Homer')
        self.hero1 = dict(title='Tale of 2 Cities', article=self.article1, description='None', doc_path='Documents')
        self.hero2 = dict(title='Iliad', article=self.article2, description='None', doc_path='Documents')

    def test_add_hero(self):
        self.assertEqual(len(Article.objects.all()), 0)
        Article.objects.create(**self.hero1)
        Article.objects.create(**self.hero2)
        self.assertEqual(len(Article.objects.all()), 2)

    def test_read_blog(self):
        Article.objects.create(**self.hero1)
        Article.objects.create(**self.hero2)
        x = Article.objects.get(pk=2)
        self.assertEqual(str(x), '2 - Iliad by 2 - Homer')
        self.assertEqual(x.hero.name, 'Homer')
        self.assertEqual(x.title, 'Iliad')

    def test_read_blog(self):
        Article.objects.create(**self.hero1)
        Article.objects.create(**self.hero2)
        x = Article.objects.get(pk=2)
        self.assertEqual(str(x), '2 - Iliad by 2 - Homer')
        self.assertEqual(x.hero.name, 'Homer')
        self.assertEqual(x.title, 'Iliad')

    def test_blog_edit(self):
        Article.objects.create(**self.hero1)
        b = Article.objects.get(pk=1)
        b.hero = self.hero2
        b.title = 'Iliad'
        b.description = 'No description'
        b.save()
        self.assertEqual(b.title, 'Iliad')
        self.assertEqual(b.author.name, 'Homer')
        self.assertEqual(b.description, 'No description')

    def test_book_delete(self):
        Article.objects.create(**self.hero1)
        b = Article.objects.get(pk=1)
        b.delete()
        self.assertEqual(len(Article.objects.all()), 0)


class ArticleViewsTest(TestCase):
    def test_article_list_view(self):
        self.assertEqual(reverse("article_list"), "/article/")

    def test_article_add_view(self):
        a = dict(title='T 1', body='None')
        b = dict(title='T 2', body='None')
        response = self.client.post(reverse("article_add"), a)
        response = self.client.post(reverse("article_add"), b)
        self.assertEqual(len(Article.objects.all()), 2)

def user_args():
    return  dict(username='TESTER', email='test@test.us', password='secret')

def test_user():
    return get_user_model().objects.create_user(**user_args())

class HeroViewsTest(TestCase):

    def login(self):
        username = self.user.username
        password = user_args()['password']
        response = self.client.login(username=username, password=password)
        self.assertEqual(response, True)

    def setUp(self):
        self.user = test_user()
        self.article1 = Article.objects.create(...)
        self.hero1 = dict(...)

    def test_hero_add_view(self):
        # Add without Login
        response = self.client.post(reverse('book_add'), self.hero1)
        self.assertEqual(response.url, '/accounts/login/?next=/book/add')
        self.assertEqual(len(Article.objects.all()), 0)
        # Login to add
        self.login()
        response = self.client.post(reverse('book_add'), self.hero1)
        response = self.client.post(reverse('book_add'), self.hero2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/book/2')
        response = self.client.get('/book/')
        self.assertEqual(len(Article.objects.all()), 2)

    def test_hero_list_view(self):
        self.assertEqual(reverse('hero_list'), '/hero/')
        Article.objects.create(**self.hero1)
        Article.objects.create(**self.hero1)
        response = self.client.get('/hero/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hero_list.html')
        self.assertTemplateUsed(response, 'theme.html')
        self.assertContains(response, '<tr>', count=3)

    def test_hero_detail_view(self):
        Article.objects.create(**self.hero1)
        self.assertEqual(reverse('hero_detail', args='1'), '/hero/1')
        self.assertEqual(reverse('hero_detail', args='2'), '/hero/2')
        response = self.client.get(reverse('hero_detail', args='1'))
        self.assertEqual(response.status_code, 200)

    def test_hero_edit_view(self):
        # Edit without Login
        Article.objects.create(**self.hero1)
        self.assertEqual(reverse('hero_edit', args='1'), '/hero/1/')
        response = self.client.get('/hero/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/hero/1/')
        # Login to edit
        self.login()
        response = self.client.post('/hero/1/', self.hero1)
        self.assertEqual(response.url, '/hero/1')
        response = self.client.get(response.url)
        self.assertContains(response, self.hero1['title'])
        self.assertContains(response, self.article1.name)

    def test_hero_delete_view(self):
        self.login()
        Article.objects.create(**self.hero1)
        self.assertEqual(reverse('book_delete', args='1'), '/book/1/delete')
        response = self.client.get('/book/1/delete')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/book/1/delete')
        self.assertEqual(len(Article.objects.all()), 0)