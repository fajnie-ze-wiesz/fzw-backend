from django.conf.urls import url

from .views import ping

app_name = 'fzw.main'
urlpatterns = [
    url('ping/$', ping, name='ping'),
]
