from django.contrib import admin
from .models import Category, Product, Favorit


admin.site.register([Category, Product, Favorit])
