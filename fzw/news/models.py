import uuid

from django.db import models

ANSWER_CHOICES = (
    ('yes', 'tak'),
    ('no', 'nie'),
)


class TopicCategory(models.Model):

    class Meta:
        verbose_name = 'Topic Category'
        verbose_name_plural = 'Topic Categories'

    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name


class ManipulationCategory(models.Model):

    class Meta:
        verbose_name = 'Manipulation Category'
        verbose_name_plural = 'Manipulation Categories'

    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name


class News(models.Model):

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ImageField()
    lead = models.CharField(max_length=255)
    topic_category = models.ForeignKey(
        TopicCategory,
        on_delete=models.PROTECT,
        related_name='news',
    )
    manipulation_category = models.ForeignKey(
        ManipulationCategory,
        on_delete=models.PROTECT,
        related_name='news',
    )
    expected_answer = models.CharField(max_length=32, choices=ANSWER_CHOICES)
    answer_explanation = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.lead
