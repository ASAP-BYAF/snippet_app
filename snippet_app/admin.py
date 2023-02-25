from django.contrib import admin
from .models import Lang, Type, Snippet, User
# Register your models here.

admin.site.register(Lang)
admin.site.register(Type)
admin.site.register(Snippet)
admin.site.register(User)