from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blogapp.models import Post


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)


admin.site.register(Post, PostAdmin)
