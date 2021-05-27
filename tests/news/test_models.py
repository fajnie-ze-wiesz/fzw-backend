from fzw.news.models import Language, NewsAnswer


def test_news_answer_enum():
    assert set(NewsAnswer.field_choices()) == {
        ('yes', 'True news'),
        ('no', 'False news'),
    }


def test_language_enum():
    assert set(Language.field_choices()) == {
        ('pl', 'Polish'),
        ('en', 'English'),
    }
