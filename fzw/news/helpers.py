import markdown  # type: ignore

from fzw.news.models import News


def get_answer_explanation_html(news: News) -> str:
    return markdown.markdown(news.answer_explanation)
