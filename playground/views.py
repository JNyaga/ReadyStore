from turtle import delay
from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Mosh'})

# send email stuff 👇👇👇👇👇
    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Joel'}
    #     )

    #     message.send(['john@readysell.com'])

    #     # Sending email to site admins
    #     # mail_admins('subject', 'message', html_message='message')

    #     """  message = EmailMessage(
    #             'subject', 'message', 'from@joelreadysell.com', ['john@readysell.com'])
    #         message.attach_file('playground/static/images/dog.jpg')
    #         message.send() """

    #     # send_mail('subject', 'message', 'joel@readysell.com',
    #     #           ['bob@readysell.com'])
    # except BadHeaderError:
    #     pass
