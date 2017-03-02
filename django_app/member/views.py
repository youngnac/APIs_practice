# Create your views here.
import base64
import json
from email.mime.text import MIMEText

import requests
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.client import flow_from_clientsecrets

from member.forms import MailForm



def login_gmail(request):
    auth_code = request.GET.get('code')
    client_secret = '/Users/yn_c/projects/django/break_week_project/.conf/client_secret.json'
    redirect_uri = "http://localhost:8000/member/login/gmail/"
    SCOPES = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/gmail.send',
    ]
    flow = flow_from_clientsecrets(client_secret, ' '.join(SCOPES), redirect_uri)
    credentials = flow.step2_exchange(auth_code)
    credential_info = json.loads(credentials.to_json())
    # service = build('gmail', 'v1', http=credentials.authorize(Http()))
    USER_ID = credential_info['id_token']['email']
    ACCESS_TOKEN = credential_info['token_response']['access_token']
    fields = ['given_name', 'family_name']
    params = {
        'fields': ','.join(fields),
        'access_token': ACCESS_TOKEN,
    }
    r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json', params)
    extra_user_info = r.json()

    user = authenticate(gmail_address=USER_ID, extra_fields=extra_user_info)
    login(request, user)

    return redirect('index')


def mail_view(request):
    form = MailForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid:
            to = request.POST["to"]
            subject = request.POST["subject"]
            message_text = request.POST["message"]
            sender = request.user.username
            auth_code = request.GET.get('code')
            client_secret = '/Users/yn_c/projects/django/break_week_project/.conf/client_secret.json'
            redirect_uri = "http://localhost:8000/member/mail/"
            SCOPES = [
                'https://mail.google.com/',
                'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/gmail.send',
            ]
            flow = flow_from_clientsecrets(client_secret, ' '.join(SCOPES), redirect_uri)
            credentials = flow.step2_exchange(auth_code)
            service = build('gmail', 'v1', http=credentials.authorize(Http()))
            dict_msg = create_message(to=to, sender=sender, subject=subject, message_text=message_text)
            send_message(service=service, user_id=sender, message=dict_msg)
            messages.success(request, 'Sent Mail!')
            return redirect('member:mail')
    else:
        context = {
            'form': form,
        }
        return render(request, 'member/mail.html', context)


def logout_fbv(request):
    logout(request)
    return redirect('index')


def create_message(to, sender, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


def send_message(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    return message
