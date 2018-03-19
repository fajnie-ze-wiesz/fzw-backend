from django.contrib import admin

from fzw.news.models import ManipulationCategory, News, TopicCategory


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(TopicCategory)
class TopicCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ManipulationCategory)
class ManipulationCategoryAdmin(admin.ModelAdmin):
    pass
