from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import time

@shared_task
def demo_task():
    try:
        print('start demo_task')
        send_mail(subject='django celery', message='test celery task', from_email=settings.EMAIL_HOST_USER, recipient_list=['premrakh272@gmail.com'])
    except Exception as e:
        print('error')
    return 'demo_task done'

# celery -A mysite worker -l INFO
# celery -A mysite worker --loglevel=info

# above cmd not work On Windows, Celery's default prefork pool doesn't work well 
# ----------------------------------------------------------------------------------------------------------------
# solo pool work with window 
# cmd : celery -A mysite worker --pool=solo --loglevel=debug 
# celery -A mysite worker -l info --pool=solo                                  # Use when result need to save in database