from django.core.mail import send_mail

from crm.celery import app
from crm.settings import EMAIL_HOST_USER


@app.task
def send_code_to_email(code_user, email_user):
    """
    Отправка письма с кодом подтверждения
    """
    mail_sent = send_mail(
        'Код подтверждения',
        f'Ваш код для входа: {code_user}',
        EMAIL_HOST_USER,
        [email_user],
        fail_silently=False,
    )
    return mail_sent
