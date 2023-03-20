from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

app=Celery()

@app.task()
def send_mails(authorEmail,id,winnerEmail=None,price=0):
    if winnerEmail!=None:
        send_mail(
            'Wygrana Aukcja',
            f'Brawo !!! Wygral pan aukcje szczegoly sa w tym linku: http/127.0.0.1/listing/{id} skontaktuj się z {authorEmail} w celu finalizacji tranzakcji',
            'wobrozek@gmail.com',
            [winnerEmail],
            fail_silently=False,
        )
        send_mail(
            'Aukcja Zakonczona',
            f'Brawo !!! Aukcja zostala sprzedana za {price} szcegóły w linku: http/127.0.0.1/listing/{id} skontaktuj się z {winnerEmail} w celu finalizacji tranzakcji',
            'wobrozek@gmail.com',
            [authorEmail],
            fail_silently=False,
        )
    else:
        send_mail(
            'Aukcja Zakonczona',
            f'Twoja aukcja została zakończona niestety nikt nie zdecydował się jej kupić, powodzenia nastepnym razem!',
            'wobrozek@gmail.com',
            [authorEmail],
            fail_silently=Falses
        )

    return "Done"