import uuid
from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsAnswer(Enum):

    __translations__ = [
        _('True news'),
        _('False news'),
    ]

    TRUE_NEWS = 'yes'
    FALSE_NEWS = 'no'

    @property
    def verbose_name(self):
        name = str(self.name)
        display_name = name.replace('_', ' ').capitalize()
        return _(display_name)

    @classmethod
    def field_choices(cls):
        return tuple((e.value, e.verbose_name) for e in cls)


class TopicCategory(models.Model):

    class Meta:
        verbose_name = _('Topic Category')
        verbose_name_plural = _('Topic Categories')

    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.display_name}'


class ManipulationCategory(models.Model):

    class Meta:
        verbose_name = _('Manipulation Category')
        verbose_name_plural = _('Manipulation Categories')

    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.display_name}'


class News(models.Model):

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ImageField()
    lead = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255, blank=True, default='')
    source_url = models.URLField(blank=True, default='')
    analysis_name = models.CharField(max_length=255, blank=True, default='')
    analysis_url = models.URLField(blank=True, default='')
    topic_category = models.ForeignKey(
        TopicCategory,
        on_delete=models.PROTECT,
        related_name='news',
    )
    manipulation_category = models.ForeignKey(
        ManipulationCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news',
    )
    expected_answer = models.CharField(
        max_length=32,
        choices=NewsAnswer.field_choices(),
    )
    answer_explanation = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.lead}'

    def clean(self):
        super().clean()
        if (self.expected_answer == NewsAnswer.FALSE_NEWS.value
                and self.manipulation_category_id is None):
            raise ValidationError(
                _('False news should have manipulation category set.'))
