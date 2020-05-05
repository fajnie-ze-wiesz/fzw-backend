import random
import uuid

from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fzw.news.models import News


def validate_positive(value):
    value = int(value)
    if value <= 0:
        raise serializers.ValidationError('Value must be positive')


class GenerateQuizSerializer(serializers.Serializer):
    topic_category_name = serializers.CharField(required=False, default=None)
    num_of_questions = serializers.IntegerField(
        required=False,
        default=10,
        validators=[validate_positive],
    )

    def update(self, instance, validated_data):
        # Not supported
        pass

    def create(self, validated_data):
        # No data is being added to the database
        pass


@api_view(['POST'])
def generate_quiz(request):
    serializer = GenerateQuizSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    num_of_questions = serializer.validated_data['num_of_questions']
    topic_category_name = serializer.validated_data['topic_category_name']

    selected_news = News.objects.filter(is_active=True)
    if topic_category_name:
        selected_news = selected_news.filter(
            topic_category__name=topic_category_name)

    unused_news_map = {news.id: news for news in selected_news}
    questions = []

    for _ in range(num_of_questions):
        if not unused_news_map:
            break
        news_id = random.choice(list(unused_news_map.keys()))
        news = unused_news_map.pop(news_id)
        image_url = request.build_absolute_uri(news.image.url)
        questions.append({
            'news_id': news.id,
            'manipulation_category_name': news.manipulation_category.name,
            'image_url': image_url,
            'expected_answer': news.expected_answer,
            'answer_explanation': news.answer_explanation,
        })

    data = {
        'id': uuid.uuid4(),
        'questions': questions,
    }

    return Response(data=data, status=status.HTTP_201_CREATED)
