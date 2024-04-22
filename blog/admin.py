from django.contrib import admin
from .models import Post, People, Entries, Payment

admin.site.register(Post)
admin.site.register(People)
admin.site.register(Entries)
admin.site.register(Payment)
