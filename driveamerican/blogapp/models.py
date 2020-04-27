from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from froala_editor.fields import FroalaField
from froala_editor.widgets import FroalaEditor


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=250, blank=False)
    keywords = models.CharField(max_length=250, blank=False)
    body = FroalaField()
    slug = AutoSlugField(populate_from='title')
    image = models.FileField(upload_to='posts', blank=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def slugify_function(self, content):
        return content.replace(' ', '-').lower()

    def get_absolute_url(self):
        return reverse('blog:post', args={self.slug})

    def __str__(self):
        return '"{title}" '.format(title=self.title)
