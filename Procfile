release: python manage.py check --deploy && python manage.py migrate
web: gunicorn fzw.wsgi --log-file -
