from django.conf.urls import url

from member import views


app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login_fbv, name='login'),
    url(r'^logout/$', views.logout_fbv, name='logout'),
    url(r'^login/gmail/$', views.login_gmail, name='login_gmail'),
]
