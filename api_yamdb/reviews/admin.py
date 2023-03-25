from django.contrib import admin

from .models import User, Category, Genre, Title, GenreTitle


admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '- пусто -'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '- пусто -'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'year')
    search_fields = ('name', 'category', 'year')
    list_filter = ('category', 'genre', 'year')
    empty_value_display = '- пусто -'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'genre')
    search_fields = ('title', 'genre')
    list_filter = ('title', 'genre')
    empty_value_display = '- пусто -'

