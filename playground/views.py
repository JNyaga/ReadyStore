from urllib import response
from django.core.cache import cache
from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
import requests
import logging

logger = logging.getLogger(__name__)


class HelloView(APIView):
    # @method_decorator(cache_page(5*60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Recieved response')
            data = response.json()
            return render(request, 'hello.html', {'name': data})
        except requests.ConnectionError:
            logger.critical('httpbin is offline')


@cache_page(5*10)
def say_hello(request):
    # notify_customers.delay('Hello')
    response = requests.get('https://httpbin.org/delay/2')
    data = response.json()

    """ key = 'httpbin_result'
    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data) """
    return render(request, 'hello.html', {'name': data})

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
