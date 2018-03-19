from django.conf.urls import url

from .views import generate_quiz

app_name = 'fzw.quizes'
urlpatterns = [
    url('quiz/$', generate_quiz, name='generate_quiz'),
]
