import pytest
from django.core.files import File
from rest_framework import status
from rest_framework.test import APIRequestFactory

from fzw.news.models import ManipulationCategory, News, TopicCategory
from fzw.quizes.api.views import generate_quiz
from tests import FILES_DIR_PATH


@pytest.fixture
def topic_category():
    return TopicCategory.objects.create(
        name='politics',
        display_name='Polityka',
    )


@pytest.fixture
def manipulation_category():
    return ManipulationCategory.objects.create(
        name='fake-news',
        display_name='Fake News',
    )


@pytest.fixture
def news_list(topic_category, manipulation_category):
    news_list = []
    for i in range(100):
        news = News(
            lead=f'News #{i + 1}',
            topic_category=topic_category,
            manipulation_category=manipulation_category,
            expected_answer='yes' if i % 2 == 0 else 'no',
        )
        with open(FILES_DIR_PATH / 'tusk-jaruzelski.jpg', 'rb') as f:
            news.image.save(f'news-image={i + 1}.jpg', File(f))
        news_list.append(news)
    return news_list


@pytest.mark.django_db
def test_when_no_news_in_db_then_response_created():
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz')
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == 0


@pytest.mark.django_db
def test_when_100_news_in_db_then_response_created(news_list):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz')
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == 10
