from django.shortcuts import redirect, render
from oauth2client.client import flow_from_clientsecrets


def index_view(request):
    client_secret = '/Users/yn_c/projects/django/break_week_project/.conf/client_secret.json'

    # client_id = settings_local["google_OAuth"]["Client_id"]
    # api_key = settings_local['google_OAuth']["API_key"]
    redirect_uri = "http://localhost:8000/member/login/gmail/"
    redirect_uri_2 = "http://localhost:8000/member/mail/"
    SCOPES = [
        'https://mail.google.com/'
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]
    flow = flow_from_clientsecrets(client_secret, ' '.join(SCOPES), redirect_uri)
    flow2 = flow_from_clientsecrets(client_secret, ' '.join(SCOPES), redirect_uri_2)
    auth_uri = flow.step1_get_authorize_url()
    auth_uri_2 = flow2.step1_get_authorize_url()
    context = {
        'auth_uri': auth_uri,
        'auth_uri_2': auth_uri_2,
        'flow': flow
    }

    return render(request, 'base/index.html',context)