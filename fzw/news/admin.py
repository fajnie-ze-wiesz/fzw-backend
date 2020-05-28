from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from fzw.news.helpers import get_answer_explanation_html
from fzw.news.models import ManipulationCategory, News, TopicCategory

ModelT = TypeVar('ModelT')
AdminT = TypeVar('AdminT')


@dataclass(frozen=True)
class AdminReadonlyField(Generic[AdminT, ModelT]):
    getter: Callable[[AdminT, ModelT], Any]
    short_description: str
    html_output: bool = False

    def __get__(
            self, instance: AdminT,
            owner=None) -> 'BoundedAdminReadonlyField[AdminT, ModelT]':
        return BoundedAdminReadonlyField[AdminT, ModelT](self, instance)


@dataclass(frozen=True)
class BoundedAdminReadonlyField(Generic[AdminT, ModelT]):
    field: AdminReadonlyField[AdminT, ModelT]
    admin: AdminT

    def __call__(self, instance: ModelT) -> Any:
        field = self.field
        value = field.getter(self.admin, instance)
        if field.html_output:
            value = mark_safe(value)
        return value

    @property
    def short_description(self) -> str:
        return self.field.short_description


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'lead',
        'image_preview',
        'answer_explanation_preview',
        'expected_answer',
        'topic_category',
        'manipulation_category',
        'is_active',
    )

    readonly_fields = (
        'answer_explanation_preview',
    )

    def _answer_explanation_preview(self, instance: News) -> str:
        return get_answer_explanation_html(instance)

    answer_explanation_preview = AdminReadonlyField['NewsAdmin', News](
        _answer_explanation_preview,
        short_description=_("Answer Explanation Preview"),
        html_output=True,
    )

    def _image_preview(self, instance: News) -> str:
        image_url = instance.image.url
        return f'<a href="{image_url}"><img src="{image_url}" width="200"></a>'

    image_preview = AdminReadonlyField['NewsAdmin', News](
        _image_preview,
        short_description=_("Image Preview"),
        html_output=True,
    )


@admin.register(TopicCategory)
class TopicCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ManipulationCategory)
class ManipulationCategoryAdmin(admin.ModelAdmin):
    pass
