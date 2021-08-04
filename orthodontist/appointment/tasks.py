from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail


@shared_task(bind=True, max_retries=5)
def send_email(self, date, time, name, email):
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
        time = datetime.strptime(time, '%H:%M:%S')
        recipients = ['orthodental@tut.by', email]
        subject = 'Запись на прием к врачу-ортодонту'
        message = 'Уважаемый(-ая) ' + name + \
                  ', \n\nВы успешно записались на прием к врачу-ортодонту Екатерине Бахур, который состоится ' + \
                 date.strftime('%d.%m.%Y') + ' в ' + time.strftime('%H:%M') + \
                  '. C Вами свяжутся заранее, чтобы уточнить делали визита. \n\nБлагодарим за интерес к нашим услугам!'
        sender = 'orthodental@tut.by'
        send_mail(subject, message, sender, recipients)
    except Exception as e:
        self.retry(exc=e, countdown=5)
    return True