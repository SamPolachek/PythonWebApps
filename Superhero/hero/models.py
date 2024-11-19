from fileinput import filename
from json import dump, loads
from pathlib import Path
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy

class Superhero(models.Model):
    name = models.CharField(max_length=200)
    identity = models.CharField(max_length=200)
    description = models.TextField(default="None")
    image = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    strengths = models.CharField(max_length=200, default="None")
    weaknesses = models.CharField(max_length=200, default="None")

    def __str__(self):
        return self.identity

    def get_absolute_url(self):
        return reverse_lazy('hero_list')
    
    @staticmethod
    def get_me(user):
        return Superhero.objects.get_or_create(user=user)[0]
    
Superhero.object.all().values()
    
class Article (models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    hero = models.ForeignKey(Superhero, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()

def get_upload(instance, filename):
    return f'images/{filename}'

class Photo (models.Model):

    author = models.ForeignKey(Superhero, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to=get_upload)

    def get_absolute_url(self):
        return reverse_lazy('photo_detail', args=[str(self.id)])
    
class Book(models.Model):
    name = models.CharField(max_length=200)
    hero = models.ForeignKey(Superhero, on_delete=models.CASCADE, editable=False)
    doc_path = models.CharField(max_length=200, default='Documents')
    cover_image = models.CharField(max_length=200, null=True, blank=True)

books = Book.object.all().values()

for book in books:
    print(book)

def read_json(filename):
    path = Path(filename)
    if path.exists():
        return loads(path.read_text())
    return {}

def write_json(filename, data):
    with open(filename, "w") as f:
        dump(data, f, indent=4)

data = [b for b in Book.objects.all().values_list()]
write_json(filename, data)

path = Path(filename)
if path.exists():
    objects = loads(path.read_text())
for o in objects:
    Book.objects.get_or_create(**o)