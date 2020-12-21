# pylint: disable=redefined-outer-name,duplicate-code
import random

import pytest
from django.conf import settings
from django.core.files import File
from rest_framework import status
from rest_framework.test import APIRequestFactory

from fzw.news.models import ManipulationCategory, News, TopicCategory
from fzw.quizes.api.views import generate_quiz
from tests import FILES_DIR_PATH

TOPIC_CATEGORIES = [
    ('politics', 'Polityka'),
    ('science', 'Nauka'),
    ('sport', 'Sport'),
    ('entertainment', 'Rozrywka'),
]

MANIPULATION_CATEGORIES = [
    ('fake-news', 'Fake news'),
    ('image-manipulation', 'Manipulacja obrazem'),
    ('clickbait', 'Clickbait'),
    ('emotional-language', 'Emocjonalny język'),
]


@pytest.fixture
def topic_categories(db):
    return [
        TopicCategory.objects.create(name=name, display_name=display_name)
        for name, display_name in TOPIC_CATEGORIES
    ]


@pytest.fixture
def manipulation_categories(db):
    return [
        ManipulationCategory.objects.create(
            name=name, display_name=display_name)
        for name, display_name in MANIPULATION_CATEGORIES
    ]


@pytest.fixture
def news_list(topic_categories, manipulation_categories):
    news_list = []
    for i in range(100):
        topic_category = random.choice(topic_categories)
        manipulation_category = random.choice(manipulation_categories)
        news = News(
            lead=f'News #{i + 1}',
            topic_category=topic_category,
            manipulation_category=manipulation_category,
            expected_answer='yes' if i % 2 == 0 else 'no',
        )
        with open(FILES_DIR_PATH / 'tusk-jaruzelski.jpg', 'rb') as f:
            news.image.save(f'news-image-{i + 1}.jpg', File(f))
        news.save()
        news_list.append(news)
    return news_list


@pytest.fixture
def news(topic_categories, manipulation_categories):
    news_obj = News(
        lead='Tusk jak Jaruzelski... Internet wyśmiał premiera',
        topic_category=TopicCategory.objects.get(name='politics'),
        manipulation_category=ManipulationCategory.objects.get(
            name='image-manipulation'),
        expected_answer='no',
        answer_explanation="""Ten news to manipulacja obrazem.

* Uważaj na nie tylko treść newsa ale także na obrazki
* Wizualny montaż jest niezwykle skuteczny

""",
    )
    with open(FILES_DIR_PATH / 'tusk-jaruzelski.jpg', 'rb') as f:
        news_obj.image.save('news-image-manipulation.jpg', File(f))
    news_obj.save()
    return news_obj


@pytest.fixture
def true_news_without_manipulation(topic_categories):
    news_obj = News(
        lead='Naukowcy doznali odlotu...',
        topic_category=TopicCategory.objects.get(name='politics'),
        expected_answer='yes',
        answer_explanation="Ten news jest prawdziwy",
    )
    with open(FILES_DIR_PATH / 'crazy-nauka-pingwiny.jpg', 'rb') as f:
        news_obj.image.save('news-ok.jpg', File(f))
    news_obj.save()
    return news_obj


def test_when_no_news_in_db_then_response_created(
        topic_categories, manipulation_categories):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz')
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == 0


def test_when_default_then_response_created(news_list):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz')
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == settings.FZW_DEFAULT_NUM_OF_QUIZ_QUESTIONS  # noqa: E501


def test_when_3_questions_requested_then_response_created(news_list):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz', {'num_of_questions': 3})
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == 3


def test_when_too_many_questions_requested_then_response_created(news_list):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz', {
        'num_of_questions': len(news_list) + 1,
    })
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == len(news_list)
    assert {str(q['news_id']) for q in response.data['questions']} == {
        str(news.id) for news in news_list
    }


def test_when_zero_questions_requested_then_bad_response(news_list):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz', {'num_of_questions': 0})
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_when_negative_questions_requested_then_bad_response(news_list):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz', {'num_of_questions': -1})
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_when_topic_category_requested_then_response_created(news_list):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz', {
        'topic_category_name': 'politics',
    })
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert {str(q['news_id']) for q in response.data['questions']}.issubset({
        str(news.id) for news in news_list
        if news.topic_category.name == 'politics'
    })


def test_when_one_fake_news_then_response_created(news):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz')
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == 1
    question_data = response.data['questions'][0]
    assert question_data['answer_explanation_html'] == '\n'.join([
        '<p>Ten news to manipulacja obrazem.</p>',
        '<ul>',
        '<li>Uważaj na nie tylko treść newsa ale także na obrazki</li>',
        '<li>Wizualny montaż jest niezwykle skuteczny</li>',
        '</ul>',
    ])


def test_when_one_true_news_then_response_created(
        true_news_without_manipulation):
    factory = APIRequestFactory()
    request = factory.post('/api/v1/quiz')
    response = generate_quiz(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(str(response.data['id'])) > 0
    assert len(response.data['questions']) == 1
    question_data = response.data['questions'][0]
    assert question_data['answer_explanation_html'] == (
        '<p>Ten news jest prawdziwy</p>'
    )
