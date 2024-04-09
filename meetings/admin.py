from django.contrib import admin

from .models import User, Visit, Object



admin.site.register(Visit)
admin.site.register(Object)