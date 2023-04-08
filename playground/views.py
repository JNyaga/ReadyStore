from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Joel'}
        )

        message.send(['john@readysell.com'])

        # Sending email to site admins
        # mail_admins('subject', 'message', html_message='message')

        """  message = EmailMessage(
                'subject', 'message', 'from@joelreadysell.com', ['john@readysell.com'])
            message.attach_file('playground/static/images/dog.jpg')
            message.send() """

        # send_mail('subject', 'message', 'joel@readysell.com',
        #           ['bob@readysell.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
